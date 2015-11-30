#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Parses a FreeChess .pgn file object (Portable Game Notation) into a list.
Currently, this parser understands files written by Jin and eBoard clients.
Only completed games are included in the gamelist.

Returns a list of all the played games. Each game is represented as a dictionary.

example call:
    from pgnparser import parsePGNfile
    allgames = parsePGNfile('path_to_my_pgn_file')
"""
import time
import datetime
import argparse
from collections import Counter

# DJANGO_GAMEFIELDS = ChessGame._meta.get_all_field_names()
DJANGO_GAMEFIELDS = ['comment', 'date', 'game_nr', 'opponent_elo', 'opponent_name', 'result', 'self_elo', 'self_white',
              'timecontrol']


def segment_pgns(pgn_buffer):
    current_game = []
    for line in pgn_buffer.splitlines():
        if line.startswith('[Event'):
            if current_game:
                yield current_game
                current_game = []
        current_game.append(line.strip())

    if current_game:
        yield current_game


def parse_pgn(pgn_buffer):
    for game in segment_pgns(pgn_buffer):
        tuples = [l.strip('[]').split(' ', 1) for l in game if l and l.startswith('[')]
        nontuples = [l for l in game if l and not l.startswith('[')]
        parsed_game = dict([(k.lower().strip(), v.strip('"')) for (k, v) in tuples])
        parsed_game['moves'] = " ".join([l for l in nontuples if not l.startswith('{')])
        yield parsed_game


def determineMostCommonPlayer(games):
    """
    takes a list of pgn games as dictionaries and returns the name of the most common player
    """
    allplayers = []
    for g in games:
        allplayers.append(g['white'])
        allplayers.append(g['black'])
    cnt = Counter(allplayers)
    most_common_player = cnt.most_common(1)[0][0]
    return most_common_player


def parsePGNfile(pgnfile):
    """
    takes a pgn file object and returns a generator of parsed dictionaries for each completed game
    """
    # create game generator
    allgames = parse_pgn(open(pgnfile).read())
    # player is not yet determined
    # get the first two games from the generator
    g1 = allgames.next()
    g2 = allgames.next()
    # determine the player that appears in both games
    player = determineMostCommonPlayer((g1, g2))
    # yield the parsed first two games
    if g1['result'] != "*":  # skip adjourned games
        yield parsePGNgame(g1, player)
    if g2['result'] != "*":  # skip adjourned games
        yield parsePGNgame(g2, player)
        # go through rest of the generator
    for g in allgames:
        if g['result'] != "*":  # skip adjourned games
            yield parsePGNgame(g, player)


def parsePGNgame(game, player):
    """
    takes a pgn game dictionary and player name and remodels the dictionary
    returns a dictionary ready to be mapped to ChessGame django model
    """
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
    if not ((game['white'] == player) or (game['black'] == player)):
        raise ValueError("player '%s' is not in the game" % player)
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
        if key not in DJANGO_GAMEFIELDS:
            del game[key]
    return game


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='parse JIN or eBoard PGN files')
    parser.add_argument("pgnfile", nargs="?", default='/Users/hoffsummer/.jin/captnswing.pgn',
                        help='the pgn file to parse (default: %(default)s)')
    args = parser.parse_args()

    t0 = time.time()
    i = 0
    print "parsing %s..." % args.pgnfile
    allgames = parsePGNfile(args.pgnfile)
    for i, game in enumerate(allgames):
        game['game_nr'] = i + 1
        print game
    print "parsed %s games in %.2f seconds" % (i, time.time() - t0)
