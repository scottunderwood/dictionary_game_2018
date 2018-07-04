from datetime import datetime, timedelta
import unittest
from app.game_logic_v3 import DGPlayer, DGGame, TurnState, GameState

player_one = DGPlayer(name='Scott')
print()


class TestNewPlayer(unittest.TestCase):
    def setUp(self):
        player_one = DGPlayer(name='Scott')

    def test(self):
        assert player_one.score == 0
        assert player_one.is_picker == False
        player_name = player_one.get_name()
        assert player_name == 'Scott'


test_game = DGGame()
test_game.add_player(player_name='Scott')
test_game.add_player(player_name='George')
test_game.add_player(player_name='Jenny')
print()


class TestNewGame(unittest.TestCase):
    def setUp(self):
        test_game = DGGame()
        test_game.add_player(player_name='Scott')

    def test(self):
        assert test_game.round == 0
        assert test_game.round_word == None
        assert test_game.picker == None
        assert test_game.get_player_by_name(
            player_name='Scott').get_name() == 'Scott'
        assert test_game.get_player_by_name(player_name='Kevin') == None
        assert len(test_game.players) == 3
        test_game.run_round()
        assert test_game.round_word == 'car'
        assert len(test_game.round_definitions) == 3
        assert len(test_game.round_votes) == 3
        assert test_game.get_player_by_name(
            player_name='Scott').round_def == 'fast'
        assert test_game.find_definer(
            test_game.round_definitions[1]) == 'George'
        assert test_game.get_player_by_name(player_name='Jenny').score == 3
        assert test_game.get_player_by_name(player_name='Scott').score == 1


if __name__ == '__main__':
    unittest.main(verbosity=2)
