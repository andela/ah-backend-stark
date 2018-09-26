from rest_framework import status,serializers,exceptions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
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

def get_user_from_auth(request):
    """
    This helper function returns an instance of the authenticated user and their token
    from the authentication class
    """
    auth = JWTAuthentication()
    user = auth.authenticate(request)[0]
    return user
