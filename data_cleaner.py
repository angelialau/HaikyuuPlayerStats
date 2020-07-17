import pandas as pd
import sys


def clean_raw(input_path='raw_stats.txt',
              output_path='haikyuu_players.csv'):
    '''Parses raw player data from input_path and 
    outputs csv of cleaned player data to specified output_dath'''
    with open(input_path, 'r') as f:
        df =  raw_lines_to_df(f.readlines())

    col_order = ['Name', 'School', 'Position', 'Game Sense',
                 'Jumping', 'Power', 'Speed', 'Stamina', 'Technique']
    df = df[col_order].set_index('Name').sort_index() # clean df
    df.to_csv(output_path)
    print(f'Cleaned output to {output_path}...')



def raw_lines_to_df(lines):
    '''Return pandas dataframe of player data from lines of raw haikyuu data'''
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
    # generate df
    players = pd.DataFrame(players)

    return players


if __name__ == "__main__":
    clean_raw()
