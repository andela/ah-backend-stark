import json
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .renderers import ArticleJSONRenderer
from .serializers import ArticleSerializer
from authors.apps.authentication.backends import JWTAuthentication

class ArticleCreationAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ArticleSerializer

    def post(self, request):
        article = request.data.get('article')
        user = get_user_from_auth(request)
        article['author'] = user.id
        article = ArticleSerializer.convert_tagList_to_str(article)
        serializer = self.serializer_class(data=article)
        serializer.is_valid(raise_exception=True)
        save_status = serializer.save()

        # Convert the taglist back to list format
        res_data = ArticleSerializer.convert_tagList_str_to_list(serializer.data)
    
        return Response(res_data, status=status.HTTP_201_CREATED)

def get_user_from_auth(request):
    """
    This helper function returns an instance of the authenticated user and their token
    from the authentication class
    """
    auth = JWTAuthentication()
    user = auth.authenticate(request)[0]
    return user
