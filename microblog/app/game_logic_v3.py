import random
from enum import Enum
import uuid


# Below mirrors the "init.py" section of the cards against online game

class DGPlayer(object):
    """
    Represents a player for the game
    """

    def __init__(self, name=None):
        self.score = 0
        self.is_picker = False
        self.name = name
        self.id = uuid.uuid4()
        self.round_def = None
        self.round_vote = None
        self.submitted = None

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def submit_definition(self, definition):
        assert type(definition) == str
        self.round_def = definition
        return (self.id, definition)

    def submit_vote(self, vote):
        assert type(vote) == int
        self.round_vote = vote
        return (self.id, vote)


# Below mirrors the "game_handler.py" section of the cards against online game


# May be able to delete this once I finishe creating the
def find_key(dic, val):
    """return the key of dictionary dic given the value"""
    return [k for k, v in dic.iteritems() if v == val][0]


class TurnState(Enum):
    PickWord = 1  # Picker selects a word for the round
    PushWord = 2  # Picker pushes the word to other players
    Submission = 3  # All players submit a definition for the word
    Sharing = 4  # Submissions shuffled and shared with all players
    Voting = 5  # Each player votes on their selection
    Scoring = 6  # Scores calculated and correct word revealed to other players


class GameState(Enum):
    WaitingForEnoughPlayers = 1
    Playing = 2
    End = 3


class DGGame:
    def __init__(self):
        self.host_connected = False
        self.players = []
        self.round = 0
        self.picker = None
        self.submission_count = 0
        self.time_to_pick_word = 120
        self.time_to_type_definition = 180
        self.time_to_vote = 120
        self.quitting = False
        self.round_word = None
        self.round_definitions = []
        self.round_votes = []

        self.game_state = GameState.WaitingForEnoughPlayers

        self.turn_state = TurnState.PickWord
        print("Game Created")

    def add_player(self, player_name=None):
        player = DGPlayer(name=player_name)
        print('%s, has entered the game' % player.name)
        self.players.append(player)
        return

    def remove_players(self, player=None):
        quitter = self.get_player_by_name(player.name)
        self.score = 0
        self.players.remove(quitter)
        return

    def get_player_by_name(self, player_name=None) -> DGPlayer:
        """
        Return player from game's player list via player's name.
        """
        player = [player for player in self.players if player.name in player_name]
        if not player:
            return None
        return player[0]

    def get_player_by_id(self, player_id=None):
        return [player for player in self.players if player_id in player.get_id()][0]

    # Unclear if this is still needed

    def get_player_names(self):
        names = []
        for player in self.players:
            name = player.names
            names.append(name)
        return names

    def get_player_count(self):
        return len(self.players)

    def clean_up_round(self):
        for player in self.players:
            player.round_def = None
            player.submitted = None
            self.is_picker = False
        # round word, round votes and round definitions all need to reset
        return

    def clean_up_game(self):
        for player in self.players:
            player.score = 0
            self.is_picker = False
        return

    def get_picker(self):
        """
        Choose and return the picker. Picker is chosen randomly from the players in round 1 but then
        rotates through self.players until the end of the game
        """
        # blocked all below out to lock in the picker for score testing
        #player_count = self.get_player_count()
        # if self.round == 0:
        #    picker_num = random.randint(0, player_count - 1)
        #    self.picker = self.players[picker_num]
        #    self.picker.is_picker == True
        # else:
        #    prev_host_num = self.players.index(self.picker)
        #    if prev_host_num == player_count - 1:
        #        picker_num = 0
        #    else:
        #        picker_num += 1
        #    self.picker = self.players[picker_num]
        #    self.players[player_num].is_picker == True
        # return self.picker
        self.picker = self.players[2]
        self.picker.is_picker = True
        return self.picker

    # below are all functions called as part of the round function

    def pick_word(self):
        while self.round_word == None:
            self.round_word = 'car'  # this will turn in to an active input prompt
        return self.round_word

    def collect_definitions(self):
        # TODO Add time countdown for submission in future feature
        while len(self.round_definitions) != len(self.players):
            # will turn in to an active input prompts
            self.round_definitions.append(self.get_player_by_name(
                player_name='Scott').submit_definition('fast')[1])
            self.round_definitions.append(self.get_player_by_name(
                player_name='George').submit_definition('slow')[1])
            # self.submission_count = 0
            # for player in self.players:
            # if player.submitted:
            # self.submission_count += 1
            # need a sepparate dedicated prompt for the round host
            self.round_definitions.append(self.get_player_by_name(
                player_name='Jenny').submit_definition('auto')[1])
        self.turn_state = TurnState.Sharing
        return self.round_definitions

    def shuffle_definitions(self):
        random.shuffle(self.round_definitions)
        return self.round_definitions

    def present_definitions(self):
        option_num = 1
        for d in self.round_definitions:
            print('Option %d: %s' % (option_num, d))
            option_num += 1
        self.turn_state = TurnState.Voting

    def vote_on_definitions(self):
        # TODO Add time countdown for submission in future feature
        while len(self.round_votes) != len(self.players):
            player_num = 0
            # will turn in to an active input prompt
            # turning off random voting for testing purposes
            # random_vote = random.randint(1, len(self.players))
            self.round_votes.append(self.get_player_by_name(
                player_name='Scott').submit_vote(1)[1])
            self.round_votes.append(self.get_player_by_name(
                player_name='George').submit_vote(1)[1])
            # need to remove this final vote event for the round picker
            self.round_votes.append(self.get_player_by_name(
                player_name='Jenny').submit_vote(1)[1])
            # self.submission_count = 0
            # for player in self.players:
            # if player.submitted:
            # self.submission_count += 1
        self.turn_state = TurnState.Scoring
        return self.round_votes

    def find_definer(self, lookup_deff):
        for p in self.players:
            if p.round_def == lookup_deff:
                return p.name

    def find_voted_definition(self, vote):
        return self.round_definitions[vote - 1]

    def round_scoring(self):
        true_definition = None
        for p in self.players:
            if p.is_picker == True:
                true_definition = p.round_def
        correct_votes = 0
        for pl in self.players:
            if pl.is_picker == False and self.find_voted_definition(pl.round_vote) == true_definition:
                pl.score += 1
                correct_votes += 1
            elif pl.is_picker == False and self.find_voted_definition(pl.round_vote) != pl.round_def:
                for other_player in self.players:
                    if self.find_voted_definition(pl.round_vote) == other_player.round_def:
                        other_player.score += 1
            elif pl.is_picker == False and self.find_voted_definition(pl.round_vote) == pl.round_def:
                pass
        if correct_votes == 0:
            for p in self.players:
                if p.is_picker == True:
                    p.score += 3

    def run_round(self):
        self.picker = self.get_picker()
        print(self.picker.get_name())
        print(self.picker.get_id())
        self.round_word = self.pick_word()
        self.round_definitions = self.collect_definitions()
        # turned off shuffle so that the find definer test continues to work
        # self.shuffle_definitions()
        self.present_definitions()
        self.vote_on_definitions()
        self.round_scoring()
