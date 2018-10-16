import json

from rest_framework.renderers import JSONRenderer


class ArticleJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(
            self, data, media_type=None, render_context=None):

        errors = data.get('errors', None)

        if errors:
            return super(ArticleJSONRenderer, self).render(data)

        return json.dumps({'article': data})


class LikesJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, render_context=None):

        errors = data.get('errors', None)

        if errors:
            return super(LikesJSONRenderer, self).render(data)

        return json.dumps({'status': data})
