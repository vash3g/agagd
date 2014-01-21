from django.core.paginator import Paginator
from django.views.decorators.http import require_GET
from agagd_core.json_response import JsonResponse
from agagd_core.models import Game, Tournament
from django.forms.models import model_to_dict
from django.core.urlresolvers import reverse
from django.db.models.query import QuerySet, ValuesQuerySet

DEFAULT_PER_PAGE = 10

def json_table(fn):
    def wrapped(request, *args, **kwargs):
        return JsonResponse(cleanup_table(fn(request, *args, **kwargs)))
    return wrapped

@json_table
def games(request):
    table = create_table(
        request,
        Game.objects.values('pin_player_1', 'pin_player_2', 'pin_player_1__full_name', 'pin_player_2__full_name'),
        ['player_1', 'player_2'],
    )

    for game in table['results']:
        game['player_1'] = {
            'type': 'link',
            'display': game['pin_player_1__full_name'],
            'link': reverse('member_detail', kwargs={'member_id': game['pin_player_1']})
        }
        game['player_2'] = {
            'type': 'link',
            'display': game['pin_player_2__full_name'],
            'link': reverse('member_detail', kwargs={'member_id': game['pin_player_2']})
        }

    return table

@json_table
def tournaments(request):
    return create_table(request, Tournament.objects.all(), [])

@require_GET
def create_table(request, queryset, headers):
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
        'headers': headers
    }

def cleanup_table(table):
    ''' Make sure only the headers show up in each field list '''
    headers = set(table['headers'])
    for row in table['results']:
        keys_to_delete = set(row.keys()) - headers
        for key in keys_to_delete:
            del row[key]
    return table
