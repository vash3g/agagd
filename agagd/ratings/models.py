from agagd_core.models import Member
from django.db import models

class GoServer(models.Model):
    """Stores information about servers eligible to post game results to us."""
    name = models.CharField(primary_key=True, max_length=60)
    homepage = models.CharField(max_length=256)
    api_key = models.CharField(max_length=1024)
    game_url_root = models.CharField(max_length=256) 
    class Meta:
        db_table = u'go_server'
        verbose_name = u'go_server'
        verbose_name_plural = u'go_servers'

    def __str__(self):
        return self.name


class OnlineRating(models.Model): 
    pin_player = models.ForeignKey(Member, db_column=u'Pin_Player', related_name='online_ratings_set', primary_key=True)
    rating = models.FloatField(db_column=u'Rating')
    sigma = models.FloatField(db_column=u'Sigma')
    timestamp = models.DateField(db_column=u'Timestamp') # When the rating was calculated.
    class Meta:
        db_table = u'online_rating'


class OnlinePlayer(models.Model):
    """ Potentially many OP's per AGA member. """
    pin_player = models.ForeignKey(Member, db_column=u'Pin_Player', primary_key=True)
    go_server = models.ForeignKey(GoServer, db_column=u'Server', related_name='server_set')
    go_server_secret_key = models.CharField(max_length=1024, unique=True)
    nickname = models.CharField(max_length=50)
    class Meta:
        db_table = u'online_player'


class OnlineGame(models.Model): 
    game_id = models.AutoField(primary_key=True, db_column=u'Game_ID') 
    go_server = models.ForeignKey(GoServer, db_column=u'Server', related_name='online_games_on')
    game_date = models.DateTimeField(db_column=u'Game_Date') 
    handicap = models.IntegerField(db_column=u'Handicap') 
    komi = models.FloatField(db_column=u'Komi') 
    pin_player_1 = models.ForeignKey(Member, db_column=u'Pin_Player_1', related_name='online_games_as_p1')
    pin_player_2 = models.ForeignKey(Member, db_column=u'Pin_Player_2', related_name='online_games_as_p2') 
    result = models.CharField(max_length=1, db_column=u'Result') 
    sgf_url = models.CharField(max_length=256, db_column=u'Sgf_Url', blank=True) 
    is_rated = models.BooleanField(db_column=u'Is_Rated', default=False)
    exclude = models.BooleanField(db_column=u'Exclude', default=False)
    submitted_at = models.DateTimeField(db_column=u'Submitted_At', auto_now_add=True)
    class Meta:
        db_table = u'online_game'

    def __str__(self):
        return 'Game on %s @ %s between%s and %s' % (self.go_server, self.game_date, self.pin_player_1, self.pin_player_2)
    
