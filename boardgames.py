'''Convenience functions to calculate on refactored BGStatsExport.json
and Google Sheets data.'''

from utils import refactor_json_data
import dateparser
import json
import random


def least_recent_play(game):
	'''Return a value for a game based on it's overall least recent play.'''
	if game['plays']:
		return dateparser.parse(sorted(game['plays'], key=lambda play: dateparser.parse(play['playDate']))[0]['playDate'])
	else:
		return dateparser.parse('jan 1 1980')


def viable_game_list(games, n_players, an_owner, sort_option='least_recent'):
	'''Return a list of games that you can play!

	`games` is the bg_data['games'] from 'master_bg_data.json'
	`n_players` is how many players want to play
	`an_owner` is a single name that indicates where you are.

	As of 6/25/2018 that means:
	Tricia = SamR = Ryan = Travis
	SamD = Andrew = pixels

	with all other names being unique.'''

	owner_decode = {'samd'		: lambda game: 'andrew' in game['Owner'].lower(),
					'andrew'	: lambda game: 'andrew' in game['Owner'].lower(),
					'pixels'	: lambda game: 'andrew' in game['Owner'].lower(),
					'tricia'	: lambda game: 'ryan' in game['Owner'].lower() or 'tricia' in game['Owner'].lower(),
					'samr'		: lambda game: 'ryan' in game['Owner'].lower() or 'tricia' in game['Owner'].lower(),
					'travis'	: lambda game: 'ryan' in game['Owner'].lower() or 'tricia' in game['Owner'].lower(),
					'ryan'		: lambda game: 'ryan' in game['Owner'].lower() or 'tricia' in game['Owner'].lower(),
					'alex'		: lambda game: 'alex' in game['Owner'].lower(),
					'tim'		: lambda game: 'tim' in game['Owner'].lower(),
					'evan'		: lambda game: 'evan' in game['Owner'].lower(),
					}

	viable_games = []
	available_games = {bgg_id: game for bgg_id, game in games.items() if owner_decode[an_owner](game)}
	for bgg_id, game in available_games.items():
		if int(game['Max Players']) >= n_players >= int(game['Min Players']):
			viable_games.append(game)

	sort_func = {'least_recent': least_recent_play,
				 'random'	   : random.random}

	viable_games.sort(key=sort_func[sort_option])

	return viable_games


def show_me_games(viable_game_list):
	for game in viable_game_list:
		if game['plays']:
			print(game['Name'], least_recent_play(game))
		else:
			print(game['Name'], 'No recorded play.')


def load_data(json_file='master_bg_data.json'):
	'''Return games from the json file.'''

	with open(json_file, 'r') as inf:
		bg_data = json.load(inf)

	games = bg_data['games']
	return games


if __name__ == '__main__':
	#with open('master_bg_data.json', 'r') as inf:
	#	bg_data = json.load(inf)

	#games = bg_data['games']
	
	#players = refactor_json_data(bg_data['players'], 'id')
	#locations = refactor_json_data(bg_data['locations'], 'id')
	games = load_data()
	show_me_games(viable_game_list(games, 3, 'tricia'))