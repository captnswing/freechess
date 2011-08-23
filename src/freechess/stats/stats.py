#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseServerError
from django.template import RequestContext
from freechess.stats.models import ChessGame
from dateutil.relativedelta import relativedelta
import datetime

def chessStats(request):
    # some general variables
    player = 'captnswing'
    allgames = ChessGame.objects.all()
    if not allgames:
        return HttpResponseServerError("No data")
    firstgame = allgames[0]
    lastgame = allgames.latest()
    number_of_games = ChessGame.objects.count()
    daterange = (lastgame.date - firstgame.date)
    today = datetime.date.today()
    y, m = today.timetuple()[:2]

    # some basic stats
    elotrend =  ChessGame.objects.elo_trend()
    all_elos = list(allgames.values_list('self_elo'))
    stats = {
        "startdate": datetime.date(y, m, 1) + relativedelta(months=-9),
        "enddate": lastgame.date,
        "firstdate": firstgame.date,
        "perday": number_of_games / float(daterange.days),
        "total": number_of_games,
        "currentelo": lastgame.self_elo,
        "alltime_maxelo": max(all_elos)[0],
        "alltime_maxelo_date": elotrend[all_elos.index(max(all_elos))][1],
        "alltime_minelo": min(all_elos)[0],
        "alltime_minelo_date": elotrend[all_elos.index(min(all_elos))][1],
    }

    comments = ChessGame.objects.values_list('comment')
    flattenedcomments = ''.join([item for sublist in comments for item in sublist])
    if flattenedcomments:
        # result tallies
        # retrieve a list of all results interactively using
        # sorted(list(set([ ' '.join(elem.values()[0].split()[1:]) for elem in ChessGame.objects.all().values('comment') ])))
        win_comments = [ ('resigns', 'opponent resigns'),
                         ('forfeits on time', 'opponent forfeits on time'),
                         ('checkmated', 'opponent checkmated'),
                         ('forfeits by disconnection', 'opponent forfeits by disconnection'), ]

        lost_comments = [ (player + ' resigns', player + ' resigns'),
                          (player + ' forfeits on time', player + ' forfeits on time'),
                          (player + ' checkmated', player + ' checkmated'),
                          (player + ' forfeits by disconnection', player + ' forfeits by disconnection'), ]

        draw_comments = [ ('player has mating material', 'neither player has mating material'),
                          ('drawn by repetition', 'game drawn by repetition'),
                          ('ran out of time and %s has no material to mate' % player, 'opponent ran out of time and %s can\'t mate' % player),
                          ('%s ran out of time and' % player, '%s ran out of time and opponent can\'t mate' % player),
                          ('drawn because both players ran out of time', 'game drawn because both players ran out of time'),
                          ('drawn by stalemate', 'game drawn by stalemate'),
                          ('drawn by mutual agreement', 'game drawn by mutual agreement'), ]

        won_tally = []
        for filterstring, cleartext in win_comments:
            won_tally.append((cleartext, ChessGame.objects.won_games().filter(comment__contains=filterstring).count()))

        drawn_tally = []
        for filterstring, cleartext in draw_comments:
            drawn_tally.append((cleartext, ChessGame.objects.drawn_games().filter(comment__contains=filterstring).count()))

        lost_tally = []
        for filterstring, cleartext in lost_comments:
            lost_tally.append((cleartext, ChessGame.objects.lost_games().filter(comment__contains=filterstring).count()))
    else:
        won_tally = lost_tally = drawn_tally = []

    # stats over last three months
    three_months_ago = today + relativedelta(months=-3)
    three_months_games = allgames.filter(date__range=(three_months_ago, today))
    # three_months_games.aggregate(Max('self_elo'), Min('self_elo'))
    three_months_elotrend = three_months_games.values_list('game_nr', 'date', 'self_elo')
    three_months_elos = list(three_months_games.values_list('self_elo'))
    stats["three_months_maxelo"] = max(three_months_elos)[0]
    stats["three_months_maxelo_date"] = three_months_elotrend[three_months_elos.index(max(three_months_elos))][1]
    stats["three_months_minelo"] = min(three_months_elos)[0]
    stats["three_months_minelo_date"] = three_months_elotrend[three_months_elos.index(min(three_months_elos))][1]

    # stats over color
    allgames_played_as_white = allgames.filter(self_white=True)
    allgames_played_as_black = allgames.filter(self_white=False)
    stats["won_as_white"] = allgames_played_as_white.filter(result="1-0").count()
    stats["drawn_as_white"] = allgames_played_as_white.filter(result__contains="1/2").count()
    stats["lost_as_white"] = allgames_played_as_white.filter(result="0-1").count()
    stats["won_as_black"] = allgames_played_as_black.filter(result="0-1").count()
    stats["drawn_as_black"] = allgames_played_as_black.filter(result__contains="1/2").count()
    stats["lost_as_black"] = allgames_played_as_black.filter(result="1-0").count()

    # stats over opponents
    opponent_elosum = 0
    stronger = 0
    weaker = 0
    last3months = allgames.filter(date__gt=three_months_ago)
    numberofgames_last3months = last3months.count()
    for game in last3months:
        opponent_elosum += game.opponent_elo
        if game.self_elo < game.opponent_elo:
            stronger += 1
        else:
            weaker += 1
    stats["opponentaverage"] = float(opponent_elosum) / numberofgames_last3months
    stats["stronger"] = float(stronger) / numberofgames_last3months * 100
    stats["weaker"] = float(weaker) / numberofgames_last3months * 100

    most_frequent_opponents = {}
    for game in allgames:
        score = most_frequent_opponents.get(game.opponent_name, [0, 0, 0, 0])
        if game.self_white:
            myresult = game.result.split("-")[0]
        else:
            myresult = game.result.split("-")[1]
        score[0] += 1
        if myresult == '1': score[1] += 1
        if myresult == '1/2': score[2] += 1
        if myresult == '0': score[3] += 1
        most_frequent_opponents[game.opponent_name] = score

    most_frequent_opponents = [ (v, k) for k, v in most_frequent_opponents.items() ]
    most_frequent_opponents = sorted(most_frequent_opponents, reverse=True)

    strongest_opponents_won = ChessGame.objects.won_games().values_list('opponent_elo', 'opponent_name', 'date')
    strongest_opponents_won = sorted(strongest_opponents_won, reverse=True)

    # return the response
    return render_to_response('stats.html', {
            'player': player,
            'stats': stats,
            'won_tally': won_tally,
            'drawn_tally': drawn_tally,
            'lost_tally': lost_tally,
            'most_frequent_opponents': most_frequent_opponents[:15],
            'strongest_opponents_won': strongest_opponents_won[:15],
            'last100games': allgames.reverse().filter(game_nr__range=(number_of_games-100,number_of_games))
        }, context_instance=RequestContext(request))
