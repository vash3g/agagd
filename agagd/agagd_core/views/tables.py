from django.core.paginator import Paginator
from django.views.decorators.http import require_GET
from agagd_core.json_response import JsonResponse
from agagd_core.models import Game, Tournament
from django.forms.models import model_to_dict
from django.core.urlresolvers import reverse
from django.db.models.query import QuerySet, ValuesQuerySet, Q
from datetime import datetime, timedelta
#from django.db.models import Q

DEFAULT_PER_PAGE = 10

def json_table(fn):
    def wrapped(request, *args, **kwargs):
        return JsonResponse(cleanup_table(fn(request, *args, **kwargs)))
    return wrapped

@json_table
def games(request):
    return games_table(request)

@json_table
def member_games(request, member_id):
    game_list= Game.objects.filter(
        Q(pin_player_1__exact=member_id) | Q(pin_player_2__exact=member_id)
    ).order_by('-game_date','round')
    return games_table(request, game_list)

def games_table(request, queryset=None):
    queryset = queryset or {
        'last_180_days': Game.objects.filter(game_date__gte=datetime.now() - timedelta(days=180)).order_by('-game_date')
    }.get(request.GET.get('queryset', None), Game.objects.all())
    table = create_table(
        request,
        queryset.values(
            'tournament_code', 'komi', 'handicap', 'game_date', 'round',
            'pin_player_1', 'pin_player_2', 'pin_player_1__full_name', 'pin_player_2__full_name'
        ),
        (
            ('game_date', 'Game Date'),
            ('round', 'Round'),
            ('player_1', 'White Player'),
            ('player_2', 'Black Player'),
            ('handicap', 'Handicap'),
            ('komi', 'Komi'),
            ('tournament', 'Tournament'),
        ),
    )

    for game in table['results']:
        game['player_1'] = {
            'type': 'link',
            'label': '%s (%s)' % (game['pin_player_1__full_name'], game['pin_player_1']),
            'link': reverse('member_detail', kwargs={'member_id': game['pin_player_1']})
        }
        game['player_2'] = {
            'type': 'link',
            'label': '%s (%s)' % (game['pin_player_2__full_name'], game['pin_player_2']),
            'link': reverse('member_detail', kwargs={'member_id': game['pin_player_2']})
        }
        game['tournament'] = {
            'type': 'link',
            'label': game['tournament_code'],
            'link': reverse('tourney_detail', kwargs={'tourn_code': game['tournament_code']})
        }
        game['round'] = game['round'] or '--'

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
        'headers': map(lambda h: {'key': h[0], 'label': h[1]}, headers),
    }

def cleanup_table(table):
    ''' Make sure only the headers show up in each field list '''
    headers = set(map(lambda h: h['key'], table['headers']))
    for row in table['results']:
        keys_to_delete = set(row.keys()) - headers
        for key in keys_to_delete:
            del row[key]
    return table
