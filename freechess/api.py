# -*- coding: utf-8 -*-
import datetime
import time
import json
from django.http import HttpResponse
from freechess.models import ChessGame
from dateutil.relativedelta import relativedelta
from dateutil import rrule

# http://stackoverflow.com/q/1077414/41404
# multiply by 1000 as Flot expects milliseconds
from freechess.util import createhist

dthandler = lambda obj: 1000 * time.mktime(obj.timetuple()) if (
    isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date)) else None


def elohist(request):
    if not ChessGame.objects.count():
        raise Exception, 'no data in database. try running importgames first.'
    startdate = ChessGame.objects.latest().date + relativedelta(months=-15)
    allgames = ChessGame.objects.all().filter(date__gte=startdate)
    last_date = None
    elosum_per_day = 0
    games_per_day = None
    averaged_elotrend = {}
    for g in allgames:
        if g.date != last_date:
            # new day, set counter end elo
            games_per_day = 1
            elosum_per_day = g.self_elo
        else:
            # same day, add to counter and elo
            games_per_day += 1
            elosum_per_day += g.self_elo
            # calculate average elo for the day
        average_elo = elosum_per_day / float(games_per_day)
        averaged_elotrend[g.date] = average_elo
        last_date = g.date
    x = sorted(averaged_elotrend.keys())
    y = [averaged_elotrend[d] for d in x]
    response_data = {
        'label': 'test',
        'data': zip(x, y)
    }
    return HttpResponse(json.dumps(response_data, default=dthandler), content_type="application/json")


def monthlyresult(request):
    if not ChessGame.objects.count():
        raise Exception, 'no data in database. try running importgames first.'
        # compile dict of won games per month
    won_games_permonth = {}
    for game in ChessGame.objects.won_games():
        month = game.date.replace(day=1)
        won_games_permonth[month] = won_games_permonth.get(month, 0) + 1
        # compile dict of lost games per month
    lost_games_permonth = {}
    for game in ChessGame.objects.lost_games():
        month = game.date.replace(day=1)
        lost_games_permonth[month] = lost_games_permonth.get(month, 0) + 1
        # compile dict of drawn games per month
    drawn_games_permonth = {}
    for game in ChessGame.objects.drawn_games():
        month = game.date.replace(day=1)
        drawn_games_permonth[month] = drawn_games_permonth.get(month, 0) + 1
        # compile the data
    latestmonth = ChessGame.objects.latest().date.replace(day=1)
    sixteenMonthsEarlier = latestmonth + relativedelta(months=-14)
    months = [m.date() for m in rrule.rrule(rrule.MONTHLY, dtstart=sixteenMonthsEarlier, until=latestmonth)]
    lost = [lost_games_permonth.get(month, 0) for month in months]
    drawn = [drawn_games_permonth.get(month, 0) for month in months]
    won = [won_games_permonth.get(month, 0) for month in months]
    xticks = zip(range(len(lost)), [m.strftime("%b '%y") for m in months])
    response_data = [
        {
            'label': 'won',
            'color': '#00aa00',
            'data': zip(range(len(won)), won)
        },
        {
            'label': 'drawn',
            'color': '#ff9933',
            'data': zip(range(len(drawn)), drawn)
        },
        {
            'label': 'lost',
            'color': '#cc0000',
            'data': zip(range(len(lost)), lost)
        },
        xticks[::2]
    ]
    return HttpResponse(json.dumps(response_data, default=dthandler), content_type="application/json")


def opponentselo(request):
    if not ChessGame.objects.count():
        raise Exception, 'no data in database. try running importgames first.'
    last_won_games = ChessGame.objects.won_games()[:100]
    hist = createhist([g.opponent_elo for g in last_won_games], 50)
    response_data = {
        'data': sorted(hist.items())
    }
    return HttpResponse(json.dumps(response_data, default=dthandler), content_type="application/json")
