# Shared methods and variables that need to be accessed by more than one file
# This helps to avoid circular imports

# Takes input for number of players, detects invalid inputs and repeats until valid
def get_valid_number_of_players(prompt):
    while True:
        try: 
            player_count = int(input(prompt))
            if 2<= player_count <= 10:
                return player_count
            else:
                print("Invalid input. Please enter a new number.")
        except ValueError:
            print("Invalid input. Please enter a new number.")

player_count = get_valid_number_of_players('How many players? (2-10)\n') 
