#-*- coding: utf-8 -*-
import datetime
from GChartWrapper import VerticalBarStack, LineXY
from django.template.context import RequestContext
from freechess.stats.models import ChessGame
from django.http import HttpResponse
from dateutil.relativedelta import relativedelta
from django.shortcuts import render_to_response
from util import createhist
from dateutil import rrule

def eloHistImgHighCharts(request):
    return render_to_response('elohist.html', context_instance=RequestContext(request))


def create_eloHistImg():
    global games_per_day
    if not ChessGame.objects.count():
        raise Exception, 'no data in database. try running importgames first.'
    startdate = ChessGame.objects.latest().date + relativedelta(months=-9)
    allgames = ChessGame.objects.all().filter(date__gte=startdate)
    last_date = None
    elosum_per_day = 0
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
    x = sorted([ d.toordinal() for d in averaged_elotrend.keys() ])
    tickspace = 30 # days per month
    xaxislabels = [ datetime.date.fromordinal(d).strftime("%b %y") for d in range(min(x), max(x)+tickspace, tickspace) ]
    y = [ averaged_elotrend[d] for d in sorted(averaged_elotrend.keys()) ]
    maxvalue = max(averaged_elotrend.values())
    bin = 50
    maxv = divmod(maxvalue + bin, bin)[0] * bin
    yaxislabels = range(1000, int(maxv), bin)
    # create graph
    G = LineXY([x, y])
    G.size(930, 300)
    G.scale(min(x), max(x), 1000, int(maxv))
    G.grid(0., 100./divmod(yaxislabels[-1]-yaxislabels[0], bin)[0], 0, 0)
    G.axes.type('xyr')
    G.axes.label(0, *xaxislabels)
    G.axes.tick(0, 3)
    yaxislabels[0] = None
    G.axes.label(1, *yaxislabels)
    G.axes.label(2, *yaxislabels)
    G.fill('bg','s','FFFFFF00')
    G.marker('s', 'red', 0, -1, 3.5)
    return G.image()

def create_monthlyResultImg():
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
    months = [ m.date(  ) for m in rrule.rrule(rrule.MONTHLY, dtstart=sixteenMonthsEarlier, until=latestmonth) ]
    xaxislabels = [ m.strftime("%b %y") for m in months ]
    for i in range(len(xaxislabels))[1::2]:
        xaxislabels[i] = None
    lost = [ lost_games_permonth.get(month, 0) for month in months ]
    drawn = [ drawn_games_permonth.get(month, 0) for month in months ]
    won = [ won_games_permonth.get(month, 0) for month in months ]
    # figure out bins
    maxvalue = max([ lost[i] + drawn[i] + won[i] for i in range(len(won)) ])
    if maxvalue > 50:
        bin = 50
    else:
        bin = 10
    maxv = divmod(maxvalue + bin, bin)[0] * bin
    yaxislabels = range(0, int(maxv + bin), bin)
    # create graph
    G = VerticalBarStack([lost, drawn, won])
    G.size(500, 350)
    G.color('cc0000' , 'ff9933', '00aa00')
    G.scale(0, maxv)
    G.axes.type('xyr')
    G.axes.label(0, *xaxislabels)
    G.axes.label(1, *yaxislabels)
    G.axes.label(2, *yaxislabels)
    G.fill('bg','s','FFFFFF00')
    G.grid(0., 100. / (maxv / bin), 1, 0)
    return G.image()

#noinspection PyArgumentList
def create_opponentsEloImg():
    if not ChessGame.objects.count():
        raise Exception, 'no data in database. try running importgames first.'
    bin = 40
    last_won_games = ChessGame.objects.won_games()[:100]
    opponent_elos = [ g.opponent_elo for g in last_won_games ]
    hist = createhist(opponent_elos, bin)
    hist = sorted(hist.items())
    xaxislabels = list(zip(*hist)[0])
    for i in range(len(xaxislabels))[::2]:
        xaxislabels[i] = None
    maxv = max(zip(*hist)[1])
    yaxislabels = range(0, maxv + 10, 10)
    G = VerticalBarStack(zip(*hist)[1])
    G.size(600, 150)
    G.color('00aa00')
    G.scale(0, maxv)
    G.axes.type('xyr')
    G.axes.label(0, *xaxislabels)
    G.axes.label(1, *yaxislabels)
    G.axes.label(2, *yaxislabels)
    G.grid(0., 8, 1, 0)
    return G.image()

def monthlyResultImg(request):
    image = create_monthlyResultImg()
    # create response, return
    response = HttpResponse(mimetype="image/png")
    image.save(response, "PNG")
    return response

def opponentsEloImg(request):
    image = create_opponentsEloImg()
    # create response, return
    response = HttpResponse(mimetype="image/png")
    image.save(response, "PNG")
    return response

def eloHistImg(request):
    image = create_eloHistImg()
    # create response, return
    response = HttpResponse(mimetype="image/png")
    image.save(response, "PNG")
    return response

if __name__ == "__main__":
#    image = create_monthlyResultImg()
#    image = create_opponentsEloImg()
    image = create_eloHistImg()
    image.save(open("test.png", "wb"), "PNG")
