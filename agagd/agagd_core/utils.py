from django.db.models.query import QuerySet, ValuesQuerySet
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET
from agagd_core.json_response import JsonResponse

DEFAULT_PER_PAGE = 10

def json_table(fn):
    def wrapped(request, *args, **kwargs):
        return JsonResponse(cleanup_table(fn(request, *args, **kwargs)))
    return wrapped

def cleanup_table(table):
    ''' Make sure only the headers show up in each field list '''
    headers = set(map(lambda h: h['key'], table['headers']))
    for row in table['results']:
        keys_to_delete = set(row.keys()) - headers
        for key in keys_to_delete:
            del row[key]
    return table

@require_GET
def create_table_from_queryset(request, queryset, headers):
    pages = Paginator(
        queryset,
        per_page=request.GET.get('per_page', DEFAULT_PER_PAGE)
    )
    requested_page = request.GET.get('page', 1)
    current_page = pages.page(requested_page).object_list

    if isinstance(current_page, ValuesQuerySet):
        current_page = list(current_page)
    elif isinstance(current_page, QuerySet):
        current_page = map(
            model_to_dict,
            pages.page(requested_page).object_list
        )

    return {
        'results': current_page,
        'total_pages': pages.num_pages,
        'page': requested_page,
        'headers': map(lambda h: {'key': h[0], 'label': h[1]}, headers),
    }

@require_GET
def create_table_from_iterable(request, iterable, headers):
    pages = Paginator(
        iterable,
        per_page=request.GET.get('per_page', DEFAULT_PER_PAGE)
    )
    requested_page = request.GET.get('page', 1)
    current_page = pages.page(requested_page).object_list

    return {
        'results': current_page,
        'total_pages': pages.num_pages,
        'page': requested_page,
        'headers': map(lambda h: {'key': h[0], 'label': h[1]}, headers),
    }
