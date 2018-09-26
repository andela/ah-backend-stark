from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .renderers import ArticleJSONRenderer
from .serializers import ArticleSerializer

class ArticleCreationAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ArticleSerializer
    def post(self, request):
        article = request.data.get('article')
        serializer = self.serializer_class(data=article)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
