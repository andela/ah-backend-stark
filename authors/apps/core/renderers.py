import json

from rest_framework.renderers import JSONRenderer

class BaseJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    object_label = 'object'

    def render(self,data, media_type=None, render_context=None):

        errors = data.get('errors',None)

        if errors:
            return super(BaseJSONRenderer, self).render(data)

        return json.dumps({self.object_label:data})