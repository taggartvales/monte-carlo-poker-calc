# This file contains the driver code for the program

import game

# Driver code
game.get_valid_hole_card('What is your first hole card? (ex. Jc for Jack of clubs)\n')
game.get_valid_hole_card('What is your second hole card? (ex. Jc for Jack of clubs)\n')
game.monte_carlo_pre_flop()
game.get_valid_community_card('What is the first community card? (ex. Jc for Jack of clubs)\n')
game.get_valid_community_card('What is the second community card? (ex. Jc for Jack of clubs)\n')
game.get_valid_community_card('What is the third community card? (ex. Jc for Jack of clubs)\n')
game.monte_carlo_pre_turn()
game.get_valid_community_card('What is the fourth community card? (ex. Jc for Jack of clubs)\n')
game.monte_carlo_pre_river()
game.get_valid_community_card('What is the fifth community card? (ex. Jc for Jack of clubs)\n')
game.monte_carlo_post_river()
