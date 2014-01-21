from django.contrib import admin
from ratings.models import GoServer, OnlinePlayer, OnlineGame


class GoServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'homepage', 'game_url_root')

class OnlinePlayerAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'pin_player', 'go_server')

class OnlineGameAdmin(admin.ModelAdmin):
    list_display = ('go_server', 'pin_player_1', 'pin_player_2',)

admin.site.register(GoServer, GoServerAdmin)
admin.site.register(OnlineGame, OnlineGameAdmin)
admin.site.register(OnlinePlayer, OnlinePlayerAdmin)
