#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Parses a FreeChess .pgn file object (Portable Game Notation) into a list.
Currently, this parser understands files written by Jin and eBoard clients.
Only completed games are included in the gamelist.

Returns a list of all the played games. Each game is represented as a dictionary.

example call:
    from pgnparser import parsePGNfile
    allgames = parsePGNfile(open('path_to_my_pgn_file'))
    allgames = parsePGNfile(urllib2.urlopen('http://url/to/my_pgn_file'))
"""
import sys
import time
import datetime
from freechess.stats.models import ChessGame
from collections import Counter

GAMEFIELDS = ChessGame._meta.get_all_field_names()


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
    allgames = getGames(pgnfile)
    # player is not yet determined
    # get the first two games from the generator
    g1 = allgames.next()
    g2 = allgames.next()
    # determine the player that appears in both games
    player = determineMostCommonPlayer((g1, g2))
    # yield the parsed first two games
    if g1['result'] != "*": # skip adjourned games
        yield parsePGNgame(g1, player)
    if g2['result'] != "*": # skip adjourned games
        yield parsePGNgame(g2, player)
        # go through rest of the generator
    for g in allgames:
        if g['result'] != "*": # skip adjourned games
            yield parsePGNgame(g, player)


def gamelist2dict(game):
    """
    takes a list of lines representing a pgn game and parses the list into a dict
    """
    # ahem. it's either this, or regexp
    data = [tuple(elem.strip('[').strip(']').split(' ', 1)) for elem in game if "]" in elem]
    data += [('comment', elem.split('}')[0].strip('{')) for elem in game if '{' in elem]
    dictgame = dict([(k.lower(), v.strip('"')) for k, v in data])
    return dictgame


def getGames(pgnfile):
    """
    takes a pgn file object and iterates through all lines
    returns a generator of pgn games as dictionaries
    """
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
            # produce dict of so far accumulated lines in game list
            yield gamelist2dict(game)
            # reset game list
            game = []
        else:
            # just accumulate lines into the game list
            game.append(line)
            # if the line had been empty, we'd never gotten here (yield/continue above)
        previous_line_empty = False
        # don't forget to yield the very last game
    yield gamelist2dict(game)


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
        if key not in GAMEFIELDS:
            del game[key]
    return game


if __name__ == "__main__":
    pgnfile = 'fixtures/eboard.pgn'
    args = sys.argv[1:]
    if len(args) == 1:
        pgnfile = args[0]

    t0 = time.time()
    print "importing %s..." % pgnfile
    allgames = parsePGNfile(open(pgnfile))
    ChessGame.objects.all().delete()
    for i, game in enumerate(allgames):
        game['game_nr'] = i+1
        _result = ChessGame.objects.create(**game)
    print "imported %s games in %.2f seconds" % (i, time.time() - t0)
