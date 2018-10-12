from rest_framework import status,serializers,exceptions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView


from .renderers import ArticleJSONRenderer
from .serializers import ArticlesSerializer
from .models import Article
from authors.apps.authentication.backends import JWTAuthentication

class ArticleCreationAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = ArticlesSerializer

    def get(self,request):
        article = Article.objects.all()
        serializer = self.serializer_class(article,many=True)
        res_data = Article.format_data_for_display(serializer.data)
        return Response({"articles":res_data},status.HTTP_200_OK)

    def post(self, request):
        article = request.data.get('article')
        user = get_user_from_auth(request)
        article['author'] = user.id

        if Article.title_exists(user.id, article['title']):
            raise serializers.ValidationError('You already have an article with the same title',409)
        
        article = ArticlesSerializer.convert_tagList_to_str(article)
        serializer = self.serializer_class(data=article)
        serializer.is_valid(raise_exception=True)
        save_status = serializer.save()

        res_data = Article.format_data_for_display(serializer.data)
    
        return Response(res_data, status=status.HTTP_201_CREATED)



class GetSingleArticleAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ArticlesSerializer
    def get(self,request,slug):
        article = Article.get_article(slug)
      
        if not article:
            raise exceptions.NotFound('The selected article was not found.')

        serializer = self.serializer_class(article)
        res_data = Article.format_data_for_display(serializer.data)
        return Response({"article":res_data}, status.HTTP_200_OK)

    def put(self,request,slug):
        user = get_user_from_auth(request)
        new_article = request.data.get('article')
        status = Article.update_article(user.id,slug,new_article)

        if status[1] == 202:
            serializer = self.serializer_class(status[0])
            res_data = Article.format_data_for_display(serializer.data)
            return Response(res_data, 202)

        return Response({'message':status[0]},status[1])
        
    def delete(self,request,slug):
        user = get_user_from_auth(request)
        # returns (statusMessage, httpCode)
        status = Article.delete_article(user.id,slug)
        return Response({'message':status[0]},status[1])
    

class RateArticleAPIView(APIView):
    """
    This class contains the views regarding the article
    rating feature
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ArticlesSerializer

    def get_values(self, queryset):
        """
        This method takes in the article queryset and 
        returns a dictionary of the article's data
        """
        return queryset.values()[0]

    def validate_rating(self, rating):
        if rating not in list(range(1, 6)):
            raise exceptions.ParseError(
                "Sorry, only a rating in the 1-5 range can be given."
            )

    def put(self, request, slug):
        """
        This method rates an article and saves the updated
        rating and ratingsCount in the database
        """
        queryset = Article.objects.filter(slug=slug)
        article = self.get_values(queryset)

        if not queryset:
            raise exceptions.NotFound(
                'The selected article was not found.')
        elif article.get("author_id") == get_user_from_auth(request).id:
            raise exceptions.ParseError(
                "Sorry, you cannot rate your own article."
            )

        serializer_instance = queryset.first()
        serializer_data = request.data.get('article', {})
        self.validate_rating(serializer_data.get("rating"))

        current_rating = article['rating']
        current_rating_count = article['ratingsCount']
        user_rating = serializer_data.get('rating')
        new_rating = Article.calculate_rating(
                            current_rating, 
                            current_rating_count, 
                            user_rating)

        serializer_data["rating"] = new_rating["rating"]
        serializer_data["ratingsCount"] = new_rating["ratingsCount"]
        serializer = self.serializer_class(
            serializer_instance,
            data=serializer_data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"article": serializer.data}, status=status.HTTP_202_ACCEPTED)

def get_user_from_auth(request):
    """
    This helper function returns an instance of the authenticated user and their token
    from the authentication class
    """
    auth = JWTAuthentication()
    user = auth.authenticate(request)[0]
    return user
