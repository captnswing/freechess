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

GAMEFIELDS = ChessGame._meta.get_all_field_names()

def parsePGNgame(game, player):
    """
    takes a multi-line string representing a stats game in PGN notation (Portable Game Notation) and parses it into a dict.
    the keywords of this dict correspond to the table columns defined in stats.models.ChessGame
    """
    data = [ tuple(elem.strip('[').strip(']').split(' ', 1)) for elem in game.splitlines() if "]" in elem ]
    data += [ ('comment', elem.split('}')[0].strip('{')) for elem in game.splitlines() if '{' in elem ]
    parsedgame = dict([ (k.lower(), v.strip('"')) for k, v in data ])
    if parsedgame['result'] == "*":
        # skip adjourned games
        return None
    try:
        parsedgame['whiteelo'] = int(parsedgame['whiteelo'])
    except (ValueError, KeyError):
        # default elo for guest opponents
        parsedgame['whiteelo'] = 1100
    try:
        parsedgame['blackelo'] = int(parsedgame['blackelo'])
    except (ValueError, KeyError):
        # default elo for guest opponents
        parsedgame['blackelo'] = 1100
    # sort out white and black
    if player.lower() == parsedgame['white'].lower():
        parsedgame['self_white'] = True
        parsedgame['self_elo'] = parsedgame['whiteelo']
        parsedgame['opponent_elo'] = parsedgame['blackelo']
        parsedgame['opponent_name'] = parsedgame['black']
    else:
        parsedgame['self_white'] = False
        parsedgame['self_elo'] = parsedgame['blackelo']
        parsedgame['opponent_elo'] = parsedgame['whiteelo']
        parsedgame['opponent_name'] = parsedgame['white']
    # set date
    y, m, d = parsedgame['date'].split('.')
    parsedgame['date'] = datetime.date(int(y), int(m), int(d))
    # delete unused keys
    for key in parsedgame.keys():
        if key not in GAMEFIELDS:
            del parsedgame[key]
    return parsedgame

def parsePGNfile(pgnfilename, player):
    data = open(pgnfilename).read()
    return parsePGNdata(data, player)

def parsePGNdata(pgndata, player):
    i = 1
    allgames = []
    if '\r' in pgndata: pgndata = pgndata.replace('\r', '') # dos2unix
    games = pgndata.split('\n\n[') # one empty line followed by line beginning with '['
    for gamedata in games:
        game = parsePGNgame(gamedata, player)
        if not game: continue
        game['game_nr'] = i
        allgames.append(game)
        i += 1
    return allgames


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 2:
        pgnfile = args[0]
        player = args[1]
    else:
        pgnfile = 'fixtures/eboard.pgn'
        player = 'captnswing'

    t0 = time.time()
    print "parsing %s..." % pgnfile
    allgames = parsePGNfile(pgnfile, player)
    print "parsed %s games in %.2f seconds" % (len(allgames), time.time()-t0)
