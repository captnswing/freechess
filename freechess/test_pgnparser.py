# -*- coding: utf-8 -*-
import datetime
import time
import unittest
from freechess.pgnparser import process_pgngame, determineMostCommonPlayer, parse_pgn

WHITE_GAME = """[Event "ICS Rated Chess Match"]
[Site "?"]
[Date "2004.11.19"]
[Round "?"]
[White "captnswing"]
[Black "Kleeblatt"]
[WhiteElo "945"]
[BlackElo "1133"]
[TimeControl "120+10"]
[Result "0-1"]

1. e4 Nc6 2. Nf3 b6 3. Bc4 Bb7 4. Ng5 Ne5 5. Qh5 g6 6. Qe2 Bh6 7. d3 Bxg5
8. Bxg5 Nxc4 9. dxc4 f6 10. Bh4 g5 11. Bg3 e5 12. f3 Qe7 13. O - O O - O - O
14. b4 c5 15. bxc5 Qxc5 + 16. Bf2 Qd6 17. Nc3 a6 18. Na4 Kb8 19. Bxb6 Rc8
20. Rad1 Qa3 21. Rxd7 Qxa4 22. Qe3 Qxd7 23. Ba7 + Ka8 24. Qb6 Qc6 25. c5
Qxb6 26. cxb6 Rxc2 27. a4 Ra2 28. Rc1 Rxa4 29. Rd1 Ne7 30. Rd6 f5 31. Re6
Ra1 + 32. Kf2 Ra2 + 33. Kg3 f4 + 34. Kg4 Rxg2 + 35. Kh5 Rxh2 + 36. Kxg5 Rg8 +
37. Kf6 Nc6 38. Kf7 Nd8 + 39. Kxg8 Nxe6 40. Kf7 Ng5 + 41. Kf6 Nxf3 42. Kf5
h5
{captnswing resigns} 0 - 1\n
"""

BLACK_GAME = """[Event "ICS Rated Chess Match"]
[Site "?"]
[Date "2004.11.19"]
[Round "?"]
[White "aidant"]
[Black "captnswing"]
[WhiteElo "1015"]
[BlackElo "952"]
[TimeControl "120+10"]
[Result "1-0"]

1. e4 e5 2. Nf3 d6 3. d4 Nf6 4. dxe5 Nxe4 5. Qd5 f5 6. Bc4 Qe7 7. O - O c6
8. Qd3 Be6 9. Bxe6 Qxe6 10. Re1 Be7 11. Nc3 d5 12. Bg5 Bc5 13. Be3 Bxe3
14. Qxe3 O - O 15. Nxe4 fxe4 16. Ng5 Qxe5 17. b3 Nd7 18. c4 Nf6 19. cxd5
cxd5 20. Rac1 Qb2 21. Qh3 Qxa2 22. Rc7 b6 23. Qe6 + Kh8 24. Nf7 + Rxf7 25. Qxf7
Qxb3 26. Qxg7#
{captnswing checkmated} 1 - 0\n
"""

ADJOURNED_GAME = """[Event "ICS Rated Chess Match"]
[Site "?"]
[Date "2004.11.27"]
[Round "?"]
[White "captnswing"]
[Black "alexcardoso"]
[WhiteElo "965"]
[BlackElo "887"]
[TimeControl "120+12"]
[Result "*"]

1. e4 e5 2. Nf3 d6 3. Bc4 Nf6 4. Ng5 Be6 5. Bxe6 fxe6 6. Nxe6 Qd7 7. Ng5
d5 8. d3 Qc6 9. exd5 Qxd5 10. c4 Qxg2 11. Rf1 Ng4 12. Qa4+ c6 13. d4 Nxh2
14. Nd2 Nxf1 15. Nxf1 Qxg5 16. Bxg5 exd4 17. Qa5 b6 18. Qe5+ Kf7 19. Qc7+
Kg6 20. Bd2
{alexcardoso lost connection; game adjourned} *\n
"""

BAD_GAME = """[Event "ICS Rated Chess Match"]
[Site "?"]
[Date "2004.11.19"]
[Round "?"]
[White "aidant"]
[Black "captnswing"]
[WhiteElo "1015"]
[BlackElo "952"]
[TimeControl "120+10"]
[Result "1-0"]
[RandomShit "blablabla"]

1. e4 e5 2. Nf3 d6 3. d4 Nf6 4. dxe5 Nxe4 5. Qd5 f5 6. Bc4 Qe7 7. O - O c6
8. Qd3 Be6 9. Bxe6 Qxe6 10. Re1 Be7 11. Nc3 d5 12. Bg5 Bc5 13. Be3 Bxe3
14. Qxe3 O - O 15. Nxe4 fxe4 16. Ng5 Qxe5 17. b3 Nd7 18. c4 Nf6 19. cxd5
cxd5 20. Rac1 Qb2 21. Qh3 Qxa2 22. Rc7 b6 23. Qe6 + Kh8 24. Nf7 + Rxf7 25. Qxf7
Qxb3 26. Qxg7#
{captnswing checkmated} 1 - 0\n
"""

JIN_GAME = """[Event "rated blitz game"]
[Site "Free Internet Chess Server"]
[Date "2005.09.14"]
[Round "-"]
[White "pastablues"]
[Black "KingMarc"]
[WhiteElo "904"]
[BlackElo "1064"]
[Result "0-1"]
[Time "22:19:57"]
[TimeControl "120+12000"]
[Mode "ICS"]

1. e3 e6 2. b3 d6 3. Bb2 d5 4. d3 Bb4+ 5. c3 Ba5 6. b4 Bb6 7. a4 c5 8. b5 Ba5
9. Nd2 c4 10. d4 Nd7 11. Ne2 Nb6 12. Nb1 Nf6 13. Ba3 Ne4 14. Bb4 Bxb4 15. cxb4
O-O 16. a5 Nd7 17. Nbc3 b6 18. a6 Qf6 19. Nxe4 dxe4 20. Nc3 Qf5 21. Bxc4 Nf6
22. d5 Ng4 23. O-O Qe5 24. Qb3 Qxh2# 0-1\n
"""


class TestPGNParser(unittest.TestCase):
    def setUp(self):
        self.eboardfile = 'fixtures/eboard.pgn'
        self.jinfile = 'fixtures/jin.pgn'

    def test_white_game(self):
        white_game = list(parse_pgn(WHITE_GAME))[0]
        result = process_pgngame(white_game, 'captnswing')
        self.assertEqual(result,
                         {'self_elo': 945, 'opponent_name': 'Kleeblatt', 'opponent_elo': 1133, 'self_white': True,
                          'result': '0-1', 'date': datetime.date(2004, 11, 19), 'timecontrol': '120+10'})

    def test_black_game(self):
        black_game = list(parse_pgn(BLACK_GAME))[0]
        result = process_pgngame(black_game, 'captnswing')
        self.assertEqual(result, {'self_elo': 952, 'opponent_name': 'aidant', 'opponent_elo': 1015, 'self_white': False,
                                  'result': '1-0', 'date': datetime.date(2004, 11, 19), 'timecontrol': '120+10'})

    def test_adjourned_game(self):
        adjourned_game = list(parse_pgn(ADJOURNED_GAME))[0]
        result = process_pgngame(adjourned_game, 'captnswing')
        self.assertIsNotNone(result)
        self.assertEqual(adjourned_game['result'], '*')

    def test_bad_game(self):
        bad_game = list(parse_pgn(BAD_GAME))[0]
        result = process_pgngame(bad_game, 'captnswing')
        self.assertEqual(result, {'opponent_name': 'aidant', 'opponent_elo': 1015, 'self_elo': 952, 'self_white': False,
                                  'result': '1-0', 'date': datetime.date(2004, 11, 19), 'timecontrol': '120+10'})

    def test_jin_game(self):
        jin_game = list(parse_pgn(JIN_GAME))[0]
        result = process_pgngame(jin_game, 'KingMarc')
        self.assertEqual(result,
                         {'self_elo': 1064, 'opponent_name': 'pastablues', 'opponent_elo': 904, 'self_white': False,
                          'result': '0-1', 'date': datetime.date(2005, 9, 14), 'timecontrol': '120+12000'})

    def test_segment_pgns(self):
        t0 = time.time()
        print "parsing %s..." % self.eboardfile
        allgames = list(parse_pgn(open(self.eboardfile).read()))
        print "parsed %s games in %.2f seconds" % (len(allgames), time.time() - t0)
        print
        t0 = time.time()
        print "parsing %s..." % self.jinfile
        allgames = list(parse_pgn(open(self.jinfile).read()))
        print "parsed %s games in %.2f seconds" % (len(allgames), time.time() - t0)

    def test_most_common_player(self):
        allgames = list(parse_pgn(open(self.eboardfile).read()))
        self.assertEqual(determineMostCommonPlayer(allgames), 'captnswing')
        allgames = list(parse_pgn(open(self.jinfile).read()))
        self.assertEqual(determineMostCommonPlayer(allgames), 'KingMarc')


if __name__ == "__main__":
    unittest.main()
