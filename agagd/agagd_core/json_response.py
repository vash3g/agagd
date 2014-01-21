# taken from http://djangosnippets.org/snippets/154/
# used with permission (http://djangosnippets.org/about/tos/)

from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.query import QuerySet
from django.http import HttpResponse
import json

class JsonResponse(HttpResponse):
    def __init__(self, object):
        if isinstance(object, QuerySet):
            content = serialize('json', object)
        else:
            content = json.dumps(
                object, indent=2, cls=DjangoJSONEncoder,
                ensure_ascii=False)
        super(JsonResponse, self).__init__(
            content, content_type='application/json')

def json_view(fn):
    def wrapped(request, *args, **kwargs):
        return JsonResponse(fn(request, *args, **kwargs))
    return wrapped
