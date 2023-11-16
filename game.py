# This file contains all of the game logic

import random
import calculations
from shared import player_count

# Variable definitions
deck = ["As", "Ks", "Qs", "Js", "10s", "9s", "8s", "7s", "6s", "5s", "4s", "3s", "2s", 
        "Ad", "Kd", "Qd", "Jd", "10d", "9d", "8d", "7d", "6d", "5d", "4d", "3d", "2d",
        "Ac", "Kc", "Qc", "Jc", "10c", "9c", "8c", "7c", "6c", "5c", "4c", "3c", "2c",
        "Ah", "Kh", "Qh", "Jh", "10h", "9h", "8h", "7h", "6h", "5h", "4h", "3h", "2h"]

hole_cards = []

community_cards = []   


# Higher number will give more accurate results at the expense of runtime
num_simulations = 10000


# Takes input for players hole cards, only accepts input if it's in the list 'deck', then removes from deck
def get_valid_hole_card(prompt):
    while True:
        try:
            hole_card = str(input(prompt))
            if hole_card in deck:
                deck.remove(hole_card)
                hole_cards.append(hole_card)
                break 
            else:
                print("Invalid input. Please enter a new card.")
        except ValueError:
            print("Invalid input. Please enter a new card.")

# Takes input for community cards, only accepts input if it's in the list 'deck', then removes from deck
def get_valid_community_card(prompt):
    while True:
        try:
            community_card = str(input(prompt))
            if community_card in deck:
                deck.remove(community_card)
                community_cards.append(community_card)
                break
            else:
                print("Invalid input. Please enter a new card.")
        except ValueError:
            print("Invalid input. Please enter a new card.")

            
# Determines the strength of a hand and assigns it a numeric value
def evaluate_hand(player_cards, community_cards):
    if calculations.is_royal_flush(player_cards, community_cards):
        return 10
    elif calculations.is_straight_flush(player_cards, community_cards):
        return 9
    elif calculations.is_four_of_a_kind(player_cards, community_cards):
        return 8
    elif calculations.is_full_house(player_cards, community_cards):
        return 7
    elif calculations.is_flush(player_cards, community_cards):
        return 6
    elif calculations.is_straight(player_cards, community_cards):
        return 5
    elif calculations.is_three_of_a_kind(player_cards, community_cards):
        return 4
    elif calculations.is_two_pair(player_cards, community_cards):
        return 3
    elif calculations.is_one_pair(player_cards, community_cards):
        return 2
    else: # Defaults to high card
        return 1

# Runs tiebreaker methods to determine the winner in the case of equal hand strength and returns true or false
def strength_tiebreaker(my_strength, hole_cards, opponents_hands, community_cards):
    if (my_strength == 1):
        return calculations.high_card_tiebreaker(hole_cards, opponents_hands, community_cards)
    elif (my_strength == 2):
        return calculations.one_pair_tiebreaker(hole_cards, opponents_hands, community_cards)
    elif (my_strength == 3):
        return calculations.two_pair_tiebreaker(hole_cards, opponents_hands, community_cards)
    elif (my_strength == 4):
        return calculations.three_of_a_kind_tiebreaker(hole_cards, opponents_hands, community_cards)
    elif (my_strength == 5):
        return calculations.straight_tiebreaker(hole_cards, opponents_hands, community_cards)
    elif (my_strength == 6):
        return calculations.flush_tiebreaker(hole_cards, opponents_hands, community_cards)
    elif (my_strength == 7):
        return calculations.full_house_tiebreaker(hole_cards, opponents_hands, community_cards)
    elif (my_strength == 8):
        return calculations.four_of_a_kind_tiebreaker(hole_cards, opponents_hands, community_cards)
    elif (my_strength == 9):
        return calculations.straight_flush_tiebreaker(hole_cards, opponents_hands, community_cards)
    elif (my_strength == 10):
        return random.choice([True, False])


# Runs the monte carlo simulation on the pre flop cards
def monte_carlo_pre_flop():
    global community_cards
    favorable_outcomes = 0
    for _ in range(num_simulations):
        future_community_cards = community_cards + random.sample(deck, 5)
        temp_deck = [i for i in deck if i not in future_community_cards]

        opponents_hands = [random.sample(temp_deck, 2) for _ in range(player_count - 1)]
        opponents_hands = [card for sublist in opponents_hands for card in sublist]
        
        my_strength = evaluate_hand(hole_cards, future_community_cards)
        opponents_strengths = [evaluate_hand(opponents_hands[i:i+2], future_community_cards) for i in range(0, len(opponents_hands), 2)]

        print(temp_deck)
        print(future_community_cards)
        print(opponents_hands)
        print("My strength", my_strength)
        print("Opponents' Hand Strengths:", opponents_strengths)

        # Check if my hand beats all opponent hands
        wins_all = True
        for idx, opponent_strength in enumerate(opponents_strengths):
            if my_strength < opponent_strength:
                wins_all = False
                break
            elif my_strength == opponent_strength:
                opponent_hand = opponents_hands[2*idx:2*(idx+1)]
                if not strength_tiebreaker(my_strength, hole_cards, opponent_hand, future_community_cards):
                    wins_all = False
                    break

        if wins_all:
            favorable_outcomes += 1
            print (favorable_outcomes)

    win_percentage = float(favorable_outcomes / num_simulations) * 100
    print("You have a {:.2f}% chance of winning.".format(win_percentage))


# Runs the monte carlo simulation on the pre turn cards
def monte_carlo_pre_turn():
    global community_cards
    favorable_outcomes = 0
    for _ in range(num_simulations):
        future_community_cards = community_cards + random.sample(deck, 2)
        temp_deck = [i for i in deck if i not in future_community_cards]

        opponents_hands = [random.sample(temp_deck, 2) for _ in range(player_count - 1)]
        opponents_hands = [card for sublist in opponents_hands for card in sublist]
        
        my_strength = evaluate_hand(hole_cards, future_community_cards)
        opponents_strengths = [evaluate_hand(opponents_hands[i:i+2], future_community_cards) for i in range(0, len(opponents_hands), 2)]

        # Check if my hand beats all opponent hands
        wins_all = True
        for idx, opponent_strength in enumerate(opponents_strengths):
            if my_strength < opponent_strength:
                wins_all = False
                break
            elif my_strength == opponent_strength:
                opponent_hand = opponents_hands[2*idx:2*(idx+1)]
                if not strength_tiebreaker(my_strength, hole_cards, opponent_hand, future_community_cards):
                    wins_all = False
                    break

        if wins_all:
            favorable_outcomes += 1

    win_percentage = float(favorable_outcomes / num_simulations) * 100
    print("You have a {:.2f}% chance of winning.".format(win_percentage))


# Runs the monte carlo simulation on the pre river cards
def monte_carlo_pre_river():
    global community_cards
    favorable_outcomes = 0
    for _ in range(num_simulations):
        future_community_cards = community_cards + random.sample(deck, 1)
        temp_deck = [i for i in deck if i not in future_community_cards]

        opponents_hands = [random.sample(temp_deck, 2) for _ in range(player_count - 1)]
        opponents_hands = [card for sublist in opponents_hands for card in sublist]
        
        my_strength = evaluate_hand(hole_cards, future_community_cards)
        opponents_strengths = [evaluate_hand(opponents_hands[i:i+2], future_community_cards) for i in range(0, len(opponents_hands), 2)]

        # Check if my hand beats all opponent hands
        wins_all = True
        for idx, opponent_strength in enumerate(opponents_strengths):
            if my_strength < opponent_strength:
                wins_all = False
                break
            elif my_strength == opponent_strength:
                opponent_hand = opponents_hands[2*idx:2*(idx+1)]
                if not strength_tiebreaker(my_strength, hole_cards, opponent_hand, future_community_cards):
                    wins_all = False
                    break

        if wins_all:
            favorable_outcomes += 1

    win_percentage = float(favorable_outcomes / num_simulations) * 100
    print("You have a {:.2f}% chance of winning.".format(win_percentage))


# Runs the monte carlo simulation on the post river cards
def monte_carlo_post_river():
    global community_cards
    favorable_outcomes = 0
    for _ in range(num_simulations):
        temp_deck = [i for i in deck if i not in community_cards]
        
        opponents_hands = [random.sample(temp_deck, 2) for _ in range(player_count - 1)]
        opponents_hands = [card for sublist in opponents_hands for card in sublist]
        
        my_strength = evaluate_hand(hole_cards, community_cards)
        opponents_strengths = [evaluate_hand(opponents_hands[i:i+2], community_cards) for i in range(0, len(opponents_hands), 2)]

        # Compare with each opponent
        for opponent_strength in opponents_strengths:
            if my_strength > opponent_strength:
                favorable_outcomes += 1
            elif my_strength == opponent_strength:
                if (strength_tiebreaker(my_strength, hole_cards, opponents_hands, community_cards) == True):
                    favorable_outcomes += 1

    win_percentage = float(favorable_outcomes / num_simulations) * 100
    print("You have a {:.2f}% chance of winning.".format(win_percentage))

