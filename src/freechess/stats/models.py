#-*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q
from django.conf import settings

class GameManager(models.Manager):
    def won_games(self):
        return super(GameManager, self).get_query_set().filter((Q(self_white=True) & Q(result="1-0")) | (Q(self_white=False) & Q(result="0-1")))
    def lost_games(self):
        return super(GameManager, self).get_query_set().filter((Q(self_white=True) & Q(result="0-1")) | (Q(self_white=False) & Q(result="1-0")))
    def drawn_games(self):
        return super(GameManager, self).get_query_set().filter(result__contains="1/2")
    def elo_trend(self):
        return super(GameManager, self).get_query_set().values_list('game_nr', 'date', 'self_elo')
    def elo_trend_flat(self):
        return super(GameManager, self).get_query_set().values_list('self_elo', flat=True)


class ChessGame(models.Model):
    game_nr = models.IntegerField(primary_key=True)
    date = models.DateField()
    self_white = models.BooleanField()
    self_elo = models.IntegerField()
    opponent_name = models.CharField(max_length=20)
    opponent_elo = models.IntegerField()
    timecontrol = models.CharField(max_length=10)
    result = models.CharField(max_length=7)
    comment = models.CharField(max_length=255)
    objects = GameManager()
    def __repr__(self):
        return "#%s  %s (%s) - %s (%s): %s" % (self.game_nr, self.self_white, self.self_elo, self.opponent_name, self.opponent_elo, self.result)
    class Meta:
        verbose_name = "Chess Game"
        ordering = ['game_nr']
        get_latest_by = 'game_nr'
    class Admin:
        list_display = ('game_nr', 'date', 'self_white', 'opponent_name', 'self_elo', 'opponent_elo', 'timecontrol', 'result', 'comment')
        ordering = ['game_nr']


class PGNfile(models.Model):
    pgnfile = models.FileField(upload_to=settings.MEDIA_ROOT)
    slug = models.SlugField(max_length=50, blank=True)
    def __unicode__(self):
        return self.pgnfile
    @models.permalink
    def get_absolute_url(self):
        return 'upload-new',
    def save(self, *args, **kwargs):
        self.slug = self.pgnfile.name
        super(PGNfile, self).save(*args, **kwargs)
