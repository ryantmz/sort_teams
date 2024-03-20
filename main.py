from collections import defaultdict
import re  # Import regular expression module for parsing input

def get_competition_name():
    competition_name = input("Enter the name of the competition: ").strip()
    return competition_name

def input_pot_configuration(competition_name):

    while True:
        try:
            total_teams = int(input("Enter the total number of teams: "))
            if total_teams <= 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a valid positive integer for the total number of teams.")
    
    print(f"There will be {total_teams} teams participating in {competition_name}.")
    print()  # This adds a blank line for ease of reading
    print("Teams are allocated into pre-determined pots.")
    print("This is done based on teams' past performance and ranking.")


    while True:
        try:
            num_pots = int(input("Enter the number of pots: "))
            if num_pots <= 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a valid positive integer for the number of pots.")

    pot_sizes = {}
    teams_entered = 0
    for pot in range(1, num_pots):
        while True:
            try:
                size = int(input(f"Enter the number of teams in pot {pot}: "))
                if size <= 0 or teams_entered + size > total_teams:
                    raise ValueError
                pot_sizes[pot] = size
                teams_entered += size
                break
            except ValueError:
                print(f"Please enter a valid positive integer for the number of teams in pot {pot}, ensuring the total does not exceed {total_teams - teams_entered} remaining teams.")
    
    # Automatically determine the size of the last pot
    pot_sizes[num_pots] = total_teams - teams_entered
    print(f"Pot {num_pots} consists of {pot_sizes[num_pots]} teams.")  # Notify the user about the size of the last pot

    return num_pots, pot_sizes, total_teams

def input_teams_by_pot(num_pots, pot_sizes):
    teams = []
    for pot in range(1, num_pots + 1):
        print(f"Please enter teams in pot {pot} in the format: 'Team Name (Country)' ({pot_sizes[pot]} teams):")
        for _ in range(pot_sizes[pot]):
            while True:
                team_input = input().strip()
                # Use regular expressions to parse the input
                match = re.match(r"(.*) \((.*)\)", team_input)
                if match:
                    name, country = match.groups()
                    teams.append([name, pot, country])
                    break
                else:
                    print("Invalid format. Please use 'Team Name (Country)'.")
    return teams

def add_team_to_group(team, groups):
    for i in range(1, len(groups) + 1):
        if not any(t[1] == team[1] or t[2] == team[2] for t in groups[i]):
            groups[i].append(team)
            return True
    return False

def sort_teams_into_groups(teams, total_teams):
    teams.sort(key=lambda x: x[1])
    groups = defaultdict(list)
    group_count = total_teams // len(set([team[1] for team in teams]))  # Calculate number of groups

    for team in teams:
        if not add_team_to_group(team, groups):
            print(f"Failed to add {team[0]} to any group.")
            break

    for i in range(1, group_count + 1):
        print(f"Group {i}: {[team[0] for team in groups[i]]}")

def main():
    competition_name = get_competition_name()
    num_pots, pot_sizes, total_teams = input_pot_configuration(competition_name)
    teams = input_teams_by_pot(num_pots, pot_sizes)
    sort_teams_into_groups(teams, total_teams)

if __name__ == "__main__":
    main()
