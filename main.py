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

def add_team_to_group(team_index, teams, groups, group_constraints):
    if team_index >= len(teams):
        return True  # All teams have been successfully added

    team = teams[team_index]
    for group in range(len(groups)):
        if can_place_team_in_group(team, group, groups, group_constraints):
            groups[group].append(team)
            if add_team_to_group(team_index + 1, teams, groups, group_constraints):
                return True
            groups[group].remove(team)  # Backtrack

    return False

def can_place_team_in_group(team, group, groups, group_constraints):
    # Check if the group already has a team from the same pot or country
    for existing_team in groups[group]:
        if existing_team[1] == team[1] or existing_team[2] == team[2]:
            return False
    # Additional constraints can be checked here
    return True

def sort_teams_into_groups(teams, total_teams):
    num_groups = total_teams // 4  # Assuming 4 teams per group for simplicity
    groups = [[] for _ in range(num_groups)]
    group_constraints = defaultdict(lambda: {'pots': set(), 'countries': set()})

    # Prepare group constraints (not used in this simple example, but can be for more complex rules)
    for group in range(num_groups):
        group_constraints[group] = {'pots': set(), 'countries': set()}

    teams.sort(key=lambda x: x[1])  # Sort teams by pot for backtracking efficiency
    if not add_team_to_group(0, teams, groups, group_constraints):
        print("Failed to organize all teams into groups under the given constraints.")
        return

    # Display the sorted groups
    for i, group in enumerate(groups, 1):
        print(f"Group {i}: {[team[0] for team in group]}")

def main():
    competition_name = get_competition_name()
    num_pots, pot_sizes, total_teams = input_pot_configuration(competition_name)
    teams = input_teams_by_pot(num_pots, pot_sizes)
    sort_teams_into_groups(teams, total_teams)

if __name__ == "__main__":
    main()
