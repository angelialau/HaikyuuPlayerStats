import pandas as pd
import sys

DATA_PATH = 'raw_stats.txt'
OUTPUT_PATH = 'haikyuu_players.csv'

def raw_to_dict(lines):
    '''Return dictionary of player data from haikyuu raw data'''
    players = []
    position = None
    player = {}
    for line in lines:
        if line.strip(): # not an empty line
            if ('(' in line) and (')' in line):             # is a name
                # save previous player
                if len(player)==9: 
                    players.append(player)
                # init new player
                name, school = line.split(' - ')[-1].split(' (')
                name = name.strip()
                school = school.strip().replace(')', '')
                player = {
                    'Position': position, 
                    'Name': name,
                    'School': school
                }
            else:
                if len(line.split()) == 1:                  # is a player position
                    if position: 
                        players.append(player)
                    position = line.strip()
                    player = {'Position': position}
                else:                                       # is a stat
                    line = line.strip().split(' - ')
                    player[line[0]] = line[1]
    return players



with open(DATA_PATH, 'r') as f:
    parsed_data =  raw_to_dict(f.readlines())

# generate csv
players = pd.DataFrame(parsed_data)
players = players[['Name', 'School', 'Position', 'Game Sense', 
                   'Jumping', 'Power', 'Speed', 'Stamina', 
                   'Technique']].set_index('Name').sort_index()

players.to_csv(OUTPUT_PATH)