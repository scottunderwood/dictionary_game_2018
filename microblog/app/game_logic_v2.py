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

#def player_list_creator(player_count):
#    player_list = {}
#    for p in range(0,player_count):
#        player_list[p]['player_name'] = 
        
#def push_word(word):
    
#def collect_responses(responses, response_type):
#    if response_type == 'vote':
             
def push_definitions(definitions, round_host):
    definition_list = []
    for d in definitions:
        definition_list.append(definitions[d])
    print(type(definition_list))
    random.shuffle(definition_list)
    def_counter = 1
    for shuffled_d in definition_list:
        print(str(def_counter) +': ' + shuffled_d)
        def_counter +=1
        
        
        
responses = {1: 'cat', 2: 'dog', 3: 'horse', 4: 'cow'}
response_type = 'vote'

#collect_responses(responses, response_type)
push_definitions(responses,1)