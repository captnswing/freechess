#-*- coding: utf-8 -*-
from piston.handler import BaseHandler
from piston.emitters import JSONEmitter, Emitter
from freechess.stats.models import ChessGame


class ChessGameHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = ChessGame

    def read(self, request, chessgame_id=None):
        """Returns a single game if `chessgame_id` is given,
        otherwise a subset."""
        if chessgame_id:
            return ChessGame.objects.get(pk=chessgame_id)
        else:
            return ChessGame.objects.elo_trend_flat()

Emitter.register('json', JSONEmitter, 'application/json; charset=utf-8')
