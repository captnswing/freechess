#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Parses a FreeChess .pgn file (Portable Game Notation) into a list.
Currently, this parser understands files written by Jin and eBoard clients.
Only completed games are included in the gamelist.

Returns a list of all the played games. Each game is represented as a dictionary.

example call:
    from pgnparser import parsePGNfile
    allgames = parsePGNfile('path_to_my_pgn_file', 'player_name')
"""
import sys
import time
import datetime
from freechess.stats.models import ChessGame
from collections import Counter

GAMEFIELDS = ChessGame._meta.get_all_field_names()

def getGames(pgndata):
    if '\r' in pgndata: pgndata = pgndata.replace('\r', '') # dos2unix
    games = pgndata.split('\n\n[') # one empty line followed by line beginning with '['
    for game in games:
        data = [ tuple(elem.strip('[').strip(']').split(' ', 1)) for elem in game.splitlines() if "]" in elem ]
        data += [ ('comment', elem.split('}')[0].strip('{')) for elem in game.splitlines() if '{' in elem ]
        parsedgame = dict([ (k.lower(), v.strip('"')) for k, v in data ])
        if parsedgame['result'] == "*":
            # skip adjourned games
            continue
        yield parsedgame
        
def determinePlayer(pgndata):
    allplayers = []
    for game in getGames(pgndata):
        allplayers.append(game['white'])
        allplayers.append(game['black'])
    cnt = Counter(allplayers)
    return cnt.most_common(1)[0][0].lower()

def parsePGNfile(pgnfilename):
    pgndata = open(pgnfilename).read()
    return parsePGNdata(pgndata)

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

def parsePGNdata(pgndata, player=None):
    if not player:
        player = determinePlayer(pgndata)
    i = 1
    allgames = []
    for game in getGames(pgndata):
        parsedgame = parsePGNgame(game, player)
        parsedgame['game_nr'] = i
        allgames.append(parsedgame)
        i += 1
    return allgames


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 2:
        pgnfile = args[0]
        player = args[1]
    else:
        pgnfile = 'fixtures/eboard.pgn'

    t0 = time.time()
    pgndata = open(pgnfile).read()
    print "parsing %s..." % pgnfile
    allgames = parsePGNdata(pgndata)
    print "parsed %s games in %.2f seconds" % (len(allgames), time.time()-t0)
