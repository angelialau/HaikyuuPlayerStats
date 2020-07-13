import pandas as pd

DATA_PATH = 'raw_stats.txt'

players = []
with open(DATA_PATH, 'r') as f:
    position = None
    player = {}
    for line in f.readlines():
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

# check output
players = pd.DataFrame(players)
print(players.shape) # TODO check if we captured all the player
print(players.head())
print(players.tail())