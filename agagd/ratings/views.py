from ratings.models import OnlinePlayer, GoServer, OnlineRating, OnlineGame

from django.views.decorators.http import require_POST, require_GET
from agagd_core.json_response import JsonResponse
from datetime import datetime, timedelta

@require_POST
def submit_game(request):
    """The endpoint servers will post game results to.  Should unpack, validate
    server keys and player keys, add the game to the database."""

    pass

@require_GET
def server_detail(request, server_name):
    """show an overview of the most recent games on the server."""
    server = GoServer.objects.get(pk=server_name)
    game_list = OnlineGame.objects.filter(game_date__gte=datetime.now() - timedelta(days=180)).order_by('-game_date')
    return JsonResponse({
        'server': str(server),
        'game_list': map(str, game_list)
        })

def rating_distributions():
    """Show an overview of the distribution of ratings by server."""
    pass

def _add_game(game):
    pass

def _unpack_posted_game(data):
    pass

def view_games(request):
    return JsonResponse({'data':'woot'})
