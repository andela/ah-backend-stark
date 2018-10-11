import json

from authors.apps.core.renderers import BaseJSONRenderer

from rest_framework.renderers import JSONRenderer

class ArticleJSONRenderer(BaseJSONRenderer):
    object_label = "article"


class LikesJSONRenderer(BaseJSONRenderer):
    object_label = "status"
