from django.core.paginator import Paginator
from django.views.decorators.http import require_GET
from agagd_core.json_response import json_view
from agagd_core.models import Game
from django.forms.models import model_to_dict

DEFAULT_PER_PAGE = 10

@json_view
def games(request):
    return create_table(request, Game.objects.all())

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
