import json

from rest_framework.renderers import JSONRenderer


class CustomUserJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        errors = data.get('errors', None)
        access_token = data.get('access_token', None)

        if errors is not None:
            return super(CustomUserJSONRenderer, self).render(data)

        if access_token is not None and isinstance(access_token, bytes):
            data['access_token'] = access_token.decode('utf-8')

        return json.dumps(
            data
        )
