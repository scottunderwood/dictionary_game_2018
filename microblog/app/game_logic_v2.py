# new imports from other sub-files
import random


def find_key(dic, val):
    """return the key of dictionary dic given the value"""
    return [k for k, v in dic.iteritems() if v == val][0]


# -------------------------------------
# Player Setup Game Logic

# Creates a dictionary of players including the players name, number for the game, and starting score of zero
# Takes a count of players, and a list of the players names as arguiments
def player_dict_creator(player_count, name_list):
    player_dict = {}
    for p in range(1, player_count + 1):
        player_dict[p] = {}
        player_dict[p]['player_name'] = name_list[p - 1]
        player_dict[p]['player_score'] = 0
        player_dict[p]['player_number'] = p
    return player_dict


def push_word(round_word):
    return round_word


def collect_responses(responses, response_type, player_dict):
    if response_type == 'vote':
        pass
        # score updates
        # advance round
    elif response_type == 'define':
        return responses


def shuffle_definitions(definitions, round_host):
    definition_list = []
    shuffled_definition_list = []
    for d in definitions:
        definition_list.append(definitions[d])
    random.shuffle(definition_list)
    def_counter = 1
    for shuffled_d in definition_list:
        shuffled_definition_list.append(str(def_counter) + ': ' + shuffled_d)
        def_counter += 1
    return shuffled_definition_list


# collect_responses(responses, response_type)

def vote_unshuffle(votes, shuffled_definitions, definitions):
    unshuffled_votes = {}
    for k, v in votes.items():
        unshuffled_votes[k] = find_key(definitions, shuffled_definitions[v - 1][3:])
    return unshuffled_votes


def score_update(host_num, player_dict, unshuffled_votes):
    correct_answers = 0
    for k, v in unshuffled_votes.items():
        if k == host_num or k == v:
            pass
        elif v == host_num:
            player_dict[k]['player_score'] += 1
            correct_answers += 1
        elif v != host_num:
            player_dict[v]['player_score'] += 1
    if correct_answers == 0:
        player_dict[host_num]['player_score'] += 3
    return player_dict


def host_rotation(host_num, player_count, round_number):
    if round_number == 0:
        host_num = random.randint(1, player_count)
        print('first round')
    else:
        if host_num == player_count - 1:
            host_num = 1
        else:
            host_num += 1
    return host_num


def game_round(host_num, player_dict):
    # test word will be replaced with a prompted input from the round host
    r_word = 'test_word'
    # needs to cause the round word to be visually pushed onto each of the players screens
    push_word(r_word)

    responses = {1: 'test response one', 2: 'test response two', 3: 'test response three', 4: 'test response four', 5: 'test response five'}
    response_type = 'define'
    definitions = collect_responses(responses, response_type, player_dict)

    shuffled_definitions = shuffle_definitions(definitions, host_num)
    for d in shuffled_definitions:
        print(d)

    votes = {1: 2, 2: 3, 3: 2, 4: 4, 5: 2}
    # round_scores = collect_responses(votes, response_type, player_dict)

    unshuffled_votes = vote_unshuffle(votes, shuffled_definitions, definitions)

    player_dict = score_update(host_num, player_dict, unshuffled_votes)

    print(player_dict)
    return player_dict


player_count = 5
player_names = ['scott', 'nicole', 'jane', 'don', 'meg']


def game(player_count, name_list):
    player_dict = player_dict_creator(player_count, name_list)

    round_number = 0
    host_num = 0

    while round_number < 3:  # player_count * 2:
        host_num = host_rotation(host_num, player_count, round_number)
        print(host_num)
        game_round(host_num, player_dict)
        round_number += 1
        print(round_number)


game(player_count, player_names)
