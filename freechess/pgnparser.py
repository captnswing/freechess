#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Parses a FreeChess .pgn file (Portable Game Notation) into a list.
Currently, this parser understands files written by Jin and eBoard clients.
Only completed games are included in the gamelist.

Returns a list of all the played games. Each game is represented as a dictionary.

example call:
    from pgnparser import parsePGNfile
    allgames = parsePGNfile('path_to_my_pgn_file')
"""
import sys
import time
import datetime
from freechess.stats.models import ChessGame
from collections import Counter

GAMEFIELDS = ChessGame._meta.get_all_field_names()

def determinePlayer(games):
    allplayers = []
    for g in games:
        allplayers.append(g['white'])
        allplayers.append(g['black'])
    cnt = Counter(allplayers)
    likelyplayer = cnt.most_common(1)[0][0]
    return likelyplayer

def parsePGNfile(pgnfile):
    player = None
    allgames = getGames(pgnfile)
    for g in allgames:
        if not player:
            # player not yet determined. get one more game
            g2 = allgames.next()
            # determine player that appears in both games
            player = determinePlayer((g, g2))
            if not g['result'] == "*": # skip adjourned games
                yield parsePGNgame(g, player)
            if not g2['result'] == "*": # skip adjourned games
                yield parsePGNgame(g2, player)
            # next please
            continue
        # we have a player already
        if not g['result'] == "*": # skip adjourned games
            yield parsePGNgame(g, player)

def game2dict(game):
    # ahem. never mind.
    data = [ tuple(elem.strip('[').strip(']').split(' ', 1)) for elem in game if "]" in elem ]
    data += [ ('comment', elem.split('}')[0].strip('{')) for elem in game if '{' in elem ]
    dictgame = dict([(k.lower(), v.strip('"')) for k, v in data])
    return dictgame

def getGames(pgnfile):
    game = []
    previous_line_empty = False
    for line in pgnfile.readlines():
        line = line.replace('\r', '').strip() # dos2unix, and strip
        # check if we have an empty line
        if not line:
            # set previous_line_empty
            previous_line_empty = True
            # move on, next line please
            continue
        # ok, we have a non-empty line
        # check if previous line was empty and is now followed by line beginning with '['
        if previous_line_empty and line[0] == '[':
            # produce dict of so far accumulated lines
            yield game2dict(game)
            # reset game
            game = []
        else:
            game.append(line)
        # if the line had been empty, we'd never gotten here (yield/continue above)
        previous_line_empty = False
    # don't forget to yield last game
    dictgame = game2dict(game)
    yield game2dict(game)

def parsePGNgame(game, player):
    try:
        game['whiteelo'] = int(game['whiteelo'])
    except (ValueError, KeyError):
        # default elo for guest opponents
        game['whiteelo'] = 1100
    try:
        game['blackelo'] = int(game['blackelo'])
    except (ValueError, KeyError):
        # default elo for guest opponents
        game['blackelo'] = 1100
    # sort out white and black
    if game['white'] == player:
        game['self_white'] = True
        game['self_elo'] = game['whiteelo']
        game['opponent_elo'] = game['blackelo']
        game['opponent_name'] = game['black']
    else:
        game['self_white'] = False
        game['self_elo'] = game['blackelo']
        game['opponent_elo'] = game['whiteelo']
        game['opponent_name'] = game['white']
    # set date
    y, m, d = game['date'].split('.')
    game['date'] = datetime.date(int(y), int(m), int(d))
    # delete unused keys
    for key in game.keys():
        if key not in GAMEFIELDS:
            del game[key]
    return game

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 2:
        pgnfile = args[0]
        player = args[1]
    else:
        pgnfile = 'fixtures/eboard.pgn'

    t0 = time.time()
    print "parsing %s..." % pgnfile
    allgames = parsePGNfile(open(pgnfile))
    print "parsed %s in %.2f seconds" % (pgnfile, time.time() - t0)
