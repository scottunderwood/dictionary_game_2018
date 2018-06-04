#new imports from other sub-files
from random import *
from collections import deque


#-------------------------------------
#attempt at defining separate search function to use in the score vote tranlation function
def search_tool(dict_value, dict_key, dict_list):
	return [element for element in dict_list if element[dict_key] == dict_value]

  
#-------------------------------------
#Player Setup Game Logic

#Creates Player List, players identified by ascending numbers
def player_list_creator(player_count):
    player_list = []
    for p in range(0,player_count):
        player_list.append(p+1)
    return player_list

# Change the concept of "Players Roles List" into a list index that loops

#Creates Player Roles List
def player_roles_list_creator(players, player_roles):
	player_role_count_int = len(players)
	initial_host = randint(0,(player_role_count_int - 1))
	player_role_assignment_num = -1

	while player_role_count_int > 0:
		player_role_assignment_num = player_role_assignment_num + 1
		if player_role_assignment_num == initial_host:
			player_roles.append("round_host")
		else:
			player_roles.append("round_participant")
		player_role_count_int = player_role_count_int - 1

	return player_roles


#-------------------------------------
#Score Tools Game Logic

#Sets initial scores at start of game
def score_set(player_list, score_dict_list):
	for x in player_list:
		score_dict = {'player': x, 'score': 0}
		score_dict_list.append(score_dict)
	return score_dict_list

#Updates scores after each round
def score_update(score_d,r_scores):
	for x in score_d:
		p_holder = search_tool(x['player'], 'player', r_scores)[0]
		x['score'] = x['score'] + p_holder['p_r_score']
	return score_d

#Returns the contents of the score dictionary 
def score_report(score_d):
	for x in score_d:
		print "%s Current Score: %s" % (x['player'], x['score'])


#-------------------------------------
#Game Round Game Logic   

#identifies which player is the host in the current round
def round_pos_determination(player_list, player_role_list):
	r_host_num_start = 0
	for x in player_role_list:
		if x == "round_host":
			r_host_num = r_host_num_start
		else:
			r_host_num_start = r_host_num_start + 1
	return player_list[r_host_num]

#prompts the current round host to provide a word for the round
def round_word_share(r_host):
	r_word = raw_input("%s please provide a word: " % (r_host))
	return r_word

#prompts all players (including the host) to submit their definition for the word in question this round
def round_answer_sub(player_list):
	r_answer_list = []
	for x in player_list:
		p_answer = raw_input("%s please provide your answer: " % (x))
		p_answer_dict = {'player': x, 'answer': p_answer}
		r_answer_list.append(p_answer_dict)
	return r_answer_list

#updating reound answer return to randomize the order of the return
#def round_answer_shuffle(r_answer_list):
#  r_answer_list_shuffled = []
#  size = len(r_answer_list)
#  while size:
#    index = randint(0, (size - 1))
#    if not r_answer_list[index] in r_answer_list_shuffled:
#      r_answer_list_shuffled.append(r_answer_list[index])
#      size = size - 1
#    else:
#      pass
#  r_answer_list = r_answer_list_shuffled
#  return r_answer_list

#prints out the player-supplied definitions for the round in question to facilitate voting
def round_answer_return(r_answer_list):
	n = 1
	for x in r_answer_list:
		print "%s) %s" % (n, x['answer'])
		n = n + 1

#all non host users are asked to vote on the potential definitions, and their vote is stored in the round votes dictionary    
def round_vote(player_list, r_answer_list, r_votes, r_host):
	for x in player_list:
		if x != r_host:
			p_r_vote = raw_input("%s please provide your vote: " % (x))
			#need to validate for 1 - x based on length of answers
			#need to make validation to ensure vote is a number
			p_r_vote_dict = {'player': x, 'vote': p_r_vote}
			r_votes.append(p_r_vote_dict)
	for z in r_votes:
		z_num = int(z['vote']) - 1
		z['vote_text'] = r_answer_list[z_num]['answer']
		z['vote_origin'] = r_answer_list[z_num]['player']
	return r_votes

#Translates round votes into round scores for non round host players
#https://docs.google.com/spreadsheets/d/1H5v99y8FTe2-qGrfrQJH0kFtQ-IxeXbEjGYtN64Zt5U/edit#gid=0
#need to fix lingering count issues
def p_r_score_determination(r_vote_item, p_r_scores, p_r_host):
	non_responder_score_holder = search_tool(r_vote_item['vote_origin'], 'player', p_r_scores)[0]
	responder_score_holder = search_tool(r_vote_item['player'], 'player', p_r_scores)[0]
	#added filter for if people vote for their own answer
	if r_vote_item['vote_origin'] == r_vote_item['player']:
		responder_score_holder['p_r_score'] = responder_score_holder['p_r_score']
	elif r_vote_item['vote_origin'] == p_r_host:
		responder_score_holder['p_r_score'] = responder_score_holder['p_r_score'] + 1 
	elif r_vote_item['vote_origin'] != p_r_host:
		non_responder_score_holder['p_r_score'] = non_responder_score_holder['p_r_score'] + 2
	for k in p_r_scores:
		if k['player'] == non_responder_score_holder['player']:
			k['p_r_score'] = k['p_r_score'] + non_responder_score_holder['p_r_score']
			#(1.17.17)added to test where score breakdown is occuring
			print(p_r_scores)
		elif k['player'] == responder_score_holder['player']:
			k['p_r_score'] = k['p_r_score'] + responder_score_holder['p_r_score']
			#(1.17.17)added to test where score breakdown is occuring
			print(p_r_scores)
		else:
			k['p_r_score'] = k['p_r_score']
			#(1.17.17)added to test where score breakdown is occuring
			print(p_r_scores)
		return p_r_scores

#Translates round votes into round scores for round host player
def r_host_score_determination(r_vote, rnd_scores, rnd_host):
	r_host_vote_count = 0
	for z in r_vote:
		if z['vote_origin'] == rnd_host:
			r_host_vote_count = r_host_vote_count + 1
		else:
			r_host_vote_count = r_host_vote_count
	r_host_score_holder = search_tool(rnd_host, 'player', rnd_scores)[0]
	if r_host_vote_count == 0:
		r_host_score_holder['p_r_score'] = 3
	for m in rnd_scores:
 		if m['player'] == rnd_host:
			#changed from m['p_r_score'] = m['p_r_score'] + r_host_score_holder['p_r_score'] and appears to have solved the problem?
			m['p_r_score'] = r_host_score_holder['p_r_score']
		else:
			m['p_r_score'] = m['p_r_score']
	return rnd_scores
  
#adds round scores for all players in the game score disctionary   
def round_vote_score_translation(player_list, r_host, r_votes, r_scores):
	for y in player_list:
		r_scores.append({'player': y, 'p_r_score': 0})
	for x in r_votes:
		p_r_score_determination(x, r_scores, r_host)  
	r_host_score_determination(r_votes, r_scores, r_host)
	return (r_scores)

#advances the game forward one round to designate a new round host
def round_advancement(r_list):
	last_index = len(r_list) - 1
	last_index_item = r_list[last_index]
	r_list.pop(last_index)
	r_list.insert(0,last_index_item)
	return r_list


#-------------------------------------
#DictGame Class

#Creates DictGame Class for later replication 
class DictGame():
	#add other inputs later like room and platers list?
	def __init__(self):
		pass

	def run_game(q):
		players_list = []
		player_roles_list = []

		player_list_creator(players_list)
		player_roles_list_creator(players_list, player_roles_list)

		score_dictionary_list =[]

		score_set(players_list, score_dictionary_list)

		current_round_count = 1
		#testing full game loop with assumption that round limit is 2x the player count, ultimately want this managed as a user setting
		#round_limit = (len(players_list) * 2) + 1
		round_limit = 3

 		#start of round loop
		while current_round_count < round_limit:
			round_host = ""
			round_host = round_pos_determination(players_list, player_roles_list)

			round_word = ""
			round_word = round_word_share(round_host)

			round_answers = []
			round_answers = round_answer_sub(players_list)

 			# shelving round answer shuffle function for now
			#round_answer_shuffle(round_answers)

			round_answer_return(round_answers)

			round_votes = []
			round_vote(players_list,round_answers,round_votes, round_host)

			round_scores = []
			round_vote_score_translation(players_list,round_host,round_votes,round_scores)

			score_update(score_dictionary_list, round_scores)
			#(1.17.17)next line in as test
			score_report(score_dictionary_list)

			round_advancement(player_roles_list)

			current_round_count = current_round_count + 1

		#end of round loop

		score_report(score_dictionary_list)
		