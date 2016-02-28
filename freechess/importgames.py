#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "freechess.settings.docker")
import django

django.setup()

from pgnparser import parse_pgn
from freechess.models import ChessGame

pgnfile = './captnswing.pgn'
t0 = time.time()
i = 0
print "importing %s..." % pgnfile
for line in open(pgnfile):
    print line
print "importing %s..." % pgnfile

ChessGame.objects.all().delete()
for i, game in enumerate(parse_pgn(open(pgnfile).read())):
    game['game_nr'] = i + 1
    _result = ChessGame.objects.create(**game)
print "imported %s games in %.2f seconds" % (i, time.time() - t0)
