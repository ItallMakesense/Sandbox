"""
Usage:
	$: python task_1.py [path to files]
"""

from heapq import heappush, heappop, heapify
from statistics import mean
import csv
import sys
import os


players_rates = {}
team_rates = []

def collect_rates(path):
    with open(path) as file:
        reader = csv.reader(file, delimiter=' ')
        for line in reader:
            players_rates[line[0]] = line[1]

def collect_teams(path):
    with open(path) as file:
        reader = csv.reader(file, delimiter=' ')
        for line in reader:
            heappush(team_rates, (calc_rate(line[1:]), line[0]))

def calc_rate(players_ids):
    team_rate = 0
    for pid in players_ids:
        team_rate += int(players_rates[pid])
        del players_rates[pid]
    return team_rate

def calc_avr_diff(seq):
    return mean(abs(element[0]-seq[index+1][0]) for index, element
                in enumerate(seq) if not index % 2)

def pop_spare_team():
    with_weakest = calc_avr_diff(team_rates[:-1]) # First in the heap
    with_strongest = calc_avr_diff(team_rates[1:]) # Last in the heap
    if with_weakest < with_strongest:
        spare_team = team_rates.pop() # Dropping last team, because getting better distrubution
    else:
        spare_team = heappop(team_rates) # Dropping first team
    return spare_team

def gather_teams(path):
    spare_team = None
    if len(team_rates) % 2:
        spare_team = pop_spare_team()
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=' ')
        while team_rates:
            writer.writerow([heappop(team_rates)[1], heappop(team_rates)[1]])
        if spare_team:
            writer.writerow([spare_team[1]])

def get_test_files(folder, files={}):
    for entry in os.scandir(folder):
        current_dir = folder if isinstance(folder, str) else folder.path
        if entry.is_file():
            if entry.name in [P_FILE, T_FILE]:
                files.setdefault(current_dir, []).append(entry)
        elif entry.is_dir():
            files = get_test_files(entry, files)
    return files


if __name__ == "__main__":

    P_FILE = "players.txt"
    T_FILE = "teams.txt"
    R_FILE = "pairs.txt"

    files = get_test_files(sys.argv[1])
    if not files:
        print("No data files found")
        exit()
    for folder, pair in files.items():
        for file in pair:
            if file.name == P_FILE:
                collect_rates(file.path)
            elif file.name == T_FILE:
                collect_teams(file.path)
        result_dir = os.path.dirname(folder)
        test_name = os.path.basename(folder)
        gather_teams(os.path.join(result_dir, f"{test_name}_{R_FILE}"))
