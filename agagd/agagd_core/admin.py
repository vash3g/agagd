from agagd_core.models import Chapters, CommentsAuthors, Country, Game, Member, MembersRegions, Membership
from django.contrib import admin

class MemberAdmin(admin.ModelAdmin): 
    list_display = ('member_id', 'full_name', 'join_date', 'chapter', 'chapter_id')

admin.site.register(Chapters)
admin.site.register(MembersRegions)
