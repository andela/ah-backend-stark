import json
from rest_framework import status,serializers,exceptions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

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
    serializer_class = ArticlesSerializer

    def get(self,request,slug):
        article = Article.get_single_article(slug)
      
        if not article:
            raise exceptions.NotFound('The selected article was not found.')

        serializer = self.serializer_class(article, many=True)
        res_data = Article.format_data_for_display(serializer.data)
        return Response({"article":res_data}, status.HTTP_200_OK)
    

class RateArticleAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ArticlesSerializer

    def get_queryset_values(self, queryset):
        return queryset.values()[0]
    
    def put(self,request,slug):
        article_queryset = Article.get_single_article(slug)
        # article = get_query_set(article_queryset)
        rated_article = request.data.get('article')

        if not article:
            raise exceptions.NotFound(
                'The selected article was not found.')

        current_rating = article['rating']
        current_rating_count = article['ratingsCount']
        user_rating = rated_article.get('rating')
        new_rating = Article.calculate_rating(
                            current_rating, 
                            current_rating_count, 
                            user_rating)

        rating = new_rating[0]
        ratingsCount = new_rating[1]

        article_queryset.update(
                       rating = rating,
                       ratingsCount = ratingsCount)

        # serializer = self.serializer_class(data=article, many=True)
        # Article.get_single_article(slug)
        # serializer = self.serializer_class(data=article, partial=True)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        # res_data = Article.format_data_for_display(serializer.data)

        return Response({"article":article_queryset.values()[0]}, status=status.HTTP_202_ACCEPTED)
        #return Response({"data":res_data}, status=status.HTTP_200_OK)

def get_user_from_auth(request):
    """
    This helper function returns an instance of the authenticated user and their token
    from the authentication class
    """
    auth = JWTAuthentication()
    user = auth.authenticate(request)[0]
    return user
