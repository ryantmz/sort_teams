from collections import defaultdict

def input_teams():
    teams = []
    print("Please enter 32 teams in the format 'Team Name,Pot,Country':")
    for _ in range(32):  # Expecting 32 teams
        while True:
            try:
                team_input = input().strip()
                name, pot, country = team_input.split(',')
                pot = int(pot)  # Ensure pot is an integer
                teams.append([name, pot, country])
                break  # Break the loop if the input format is correct
            except ValueError:
                print("Invalid format. Please use 'Team Name,Pot,Country'.")
    return teams

def add_team_to_group(team, groups):
    for i in range(1, 9):  # 8 groups
        if not any(t[1] == team[1] or t[2] == team[2] for t in groups[i]):
            groups[i].append(team)
            return True
    return False

def sort_teams_into_groups(teams):
    teams.sort(key=lambda x: x[1])
    groups = defaultdict(list)

    for team in teams:
        if not add_team_to_group(team, groups):
            print(f"Failed to add {team[0]} to any group.")
            break

    for i in range(1, 9):
        print(f"Group {i}: {[team[0] for team in groups[i]]}")

def main():
    teams = input_teams()
    sort_teams_into_groups(teams)

if __name__ == "__main__":
    main()
