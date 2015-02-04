#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyelasticsearch import ElasticSearch
from pyelasticsearch.exceptions import IndexAlreadyExistsError
from pgnparser import parsePGNfile

es = ElasticSearch("http://192.168.33.121:9200/")

game_mapping = {
    'game': {
        'properties': {
             'self_elo': {'type': 'integer'},
             'opponent_name': {'type': 'string'},
             'opponent_elo': {'type': 'integer'},
             'self_white': {'type': 'boolean'},
             'result': {'type': 'string'},
             'date': {'type': 'date'},
             'timecontrol': {'type': 'string'},
             'game_nr': {'type': 'integer'}
        }
    }
}

try:
    es.create_index('games', settings={'mappings': game_mapping})
except IndexAlreadyExistsError:
    pass

pgnfile = '/Users/hoffsummer/.jin/captnswing.pgn'
allgames = parsePGNfile(open(pgnfile))
data = []
for i, game in enumerate(allgames):
    game['game_nr'] = i+1
    data.append(game)

es.bulk_index('games', 'game', data, id_field='game_nr')
print data[10]


# print "importing %s..." % pgnfile
# allgames = parsePGNfile(open(pgnfile))
# ChessGame.objects.all().delete()
# for i, game in enumerate(allgames):
#     game['game_nr'] = i+1
#     _result = ChessGame.objects.create(**game)
# print "imported %s games in %.2f seconds" % (i, time.time() - t0)
