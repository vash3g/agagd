from agagd_core.models import Game, Tournament
from django.core.urlresolvers import reverse
from django.db.models.query import Q
from datetime import datetime, timedelta
from agagd_core.utils import json_table, create_table

@json_table
def games(request):
    return games_table(request)

@json_table
def member_games(request, member_id):
    game_list = Game.objects.filter(
        Q(pin_player_1__exact=member_id) | Q(pin_player_2__exact=member_id)
    ).order_by('-game_date','round')
    return games_table(request, game_list)

@json_table
def tournaments(request):
    return tournaments_table(request)

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

def tournaments_table(request, queryset=None):
    queryset = queryset or {
    }.get(request.GET.get('queryset', None), Tournament.objects.order_by('-tournament_date'))
    table = create_table(
        request,
        queryset,
        (
            ('tournament_code', 'Tournament Code'),
            ('description', 'Description'),
            ('tournament_date', 'Tournament Date'),
            ('city', 'City'),
            ('state', 'State'),
            ('total_players', 'Total Players'),
            ('rounds', 'Rounds'),
            ('elab_date', 'Rated On'),
        )
    )
    return table

def opponents_table(request, queryset=None):
    queryset = queryset or {
    }.get(request.GET.get('queryset', None), Tournament.objects.order_by('-tournament_date'))
    table = create_table(
        request,
        queryset,
        (
            ('tournament_code', 'Tournament Code'),
            ('description', 'Description'),
            ('tournament_date', 'Tournament Date'),
            ('city', 'City'),
            ('state', 'State'),
            ('total_players', 'Total Players'),
            ('rounds', 'Rounds'),
            ('elab_date', 'Rated On'),
        )
    )
    return table
