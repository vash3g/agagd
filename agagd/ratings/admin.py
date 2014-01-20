from django.contrib import admin
from ratings.models import GoServer, OnlinePlayer, OnlineGame


class GoServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'homepage', 'game_url_root')

class OnlinePlayerAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'pin_player', 'go_server')


admin.site.register(GoServer, GoServerAdmin)
admin.site.register(OnlineGame)
admin.site.register(OnlinePlayer, OnlinePlayerAdmin)
