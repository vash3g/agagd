from django.core.paginator import Paginator
from django.views.decorators.http import require_GET
from agagd_core.json_response import json_view
from agagd_core.models import Game, Tournament
from django.forms.models import model_to_dict
from django.core.urlresolvers import reverse

DEFAULT_PER_PAGE = 10

@json_view
def games(request):
    table = create_table(request, Game.objects.all())
    for game in table['results']:
        game['player_1_details'] = reverse('member_detail', kwargs={'member_id': game['pin_player_1']})
        game['player_2_details'] = reverse('member_detail', kwargs={'member_id': game['pin_player_2']})
    return table

@json_view
def tournaments(request):
    return create_table(request, Tournament.objects.all())

@require_GET
def create_table(request, queryset):
    pages = Paginator(
        queryset,
        per_page=request.GET.get('per_page', DEFAULT_PER_PAGE)
    )
    requested_page = request.GET.get('page', 1)
    current_page = map(
        model_to_dict,
        pages.page(requested_page).object_list
    )

    return {
        'results': current_page,
        'total_pages': pages.num_pages,
        'page': requested_page,
    }
