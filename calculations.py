# This file contains all of the compairson methods

import random

def is_one_pair(player_cards, community_cards):
    combined_cards = player_cards + community_cards
    for i in range(len(combined_cards) - 1):
        for j in range(i + 1, len(combined_cards)):
            if combined_cards[i][0] == combined_cards[j][0]:
                return True
    return False


def is_two_pair(player_cards, community_cards):
    combined_cards = player_cards + community_cards
    rank_counts = {}

    for card in combined_cards:
        rank = card[0]
        rank_counts[rank] = rank_counts.get(rank, 0) + 1

    pairs = [rank for rank, count in rank_counts.items() if count == 2]

    return len(pairs) >= 2


def is_three_of_a_kind(player_cards, community_cards):
    combined_cards = player_cards + community_cards
    rank_counts = {}
    for card in combined_cards:
        rank = card[0]
        rank_counts[rank] = rank_counts.get(rank, 0) + 1
    return any(count >= 3 for count in rank_counts.values())
    

def is_straight(player_cards, community_cards):
    all_cards = player_cards + community_cards
    rank_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    number_ranks = []

    for card in all_cards:
        rank = card[:-1]  # Get all characters except the last one (which is assumed to be the suit)
        try:
            number_ranks.append(rank_values[rank])
        except KeyError:
            print("KeyError for card:", card, "Dictionary:", rank_values, rank)

    # Sort and remove duplicates
    number_ranks = sorted(list(set(number_ranks)))

    # Add Ace as rank 1 if there's an Ace with rank 14
    if 14 in number_ranks:
        number_ranks.insert(0, 1)

    for i in range(len(number_ranks) - 4):
        # Check for 5 consecutive ranks
        if number_ranks[i + 4] - number_ranks[i] == 4 and len(set(number_ranks[i:i+5])) == 5:
            return True

    return False


def is_flush(player_cards, community_cards):
    combined_cards = player_cards + community_cards
    suit_counter = {'s': 0, 'd': 0, 'c': 0, 'h': 0}
    
    for card in combined_cards:
        if len(card) == 2 and card[0] in '23456789TJQKA' and card[1] in 'sdch':
            suit_counter[card[1]] += 1
    
    return any(count >= 5 for count in suit_counter.values())

    
def is_full_house(player_cards, community_cards):
    combined_cards = player_cards + community_cards
    rank_counts = {}
    
    for card in combined_cards:
        rank = card[0]
        rank_counts[rank] = rank_counts.get(rank, 0) + 1
    
    three_of_a_kind_ranks = [rank for rank, count in rank_counts.items() if count >= 3]
    
    if len(three_of_a_kind_ranks) >= 2:
        # If there are two or more three-of-a-kind ranks, it's a full house
        return True
    
    if len(three_of_a_kind_ranks) == 1:
        three_of_a_kind_rank = three_of_a_kind_ranks[0]
        two_of_a_kind_ranks = [rank for rank, count in rank_counts.items() if count == 2]
        
        return len(two_of_a_kind_ranks) >= 1 and three_of_a_kind_rank != two_of_a_kind_ranks[0]
    
    return False


def is_four_of_a_kind(player_cards, community_cards):
    combined_cards = player_cards + community_cards
    rank_counts = {}
    for card in combined_cards:
        rank = card[0]
        rank_counts[rank] = rank_counts.get(rank, 0) + 1
    return any(count >= 4 for count in rank_counts.values())


def is_straight_flush(player_cards, community_cards):
    combined_cards = player_cards + community_cards
    sorted_suits = {}
    for card in combined_cards:
        suit = card[1]
        sorted_suits.setdefault(suit, []).append(card)
    for suit, cards_in_suit in sorted_suits.items():
        if is_straight(cards_in_suit, []):
            return True
    return False


def is_royal_flush(player_cards, community_cards):
    all_cards = player_cards + community_cards
    suits = set(card[-1] for card in all_cards)

    for suit in suits:
        royal_flush = {'10', 'J', 'Q', 'K', 'A'}
        suit_cards = {card[:-1] for card in all_cards if card[-1] == suit}
        #print(f"Suits: {suits}, Suit: {suit}, Suit Cards: {suit_cards}")

        if royal_flush.issubset(suit_cards):
            return True

    return False

def high_card_tiebreaker(my_cards, opponents_hand, community_cards):
    my_highest = sorted(my_cards + community_cards, reverse=True)
    opponents_highest = sorted(opponents_hand + community_cards, reverse=True)

    for i in range(len(my_highest)):
        if my_highest[i] > opponents_highest[i]:
            return True
        elif my_highest[i] < opponents_highest[i]:
            return False

    print("random")
    return random.choice([True, False])

RANKS = '23456789TJQKA'  # T for 10, followed by face cards and ace

def one_pair_tiebreaker(my_cards, opponents_hand, community_cards):
    # Convert 10s to Ts
    all_cards = [card.replace('10', 'T') for card in my_cards + community_cards]
    opponents_all_cards = [card.replace('10', 'T') for card in opponents_hand + community_cards]

    # Initialize rank count dictionaries
    my_rank_counts = {rank: 0 for rank in RANKS}
    opponents_rank_counts = {rank: 0 for rank in RANKS}

    # Count the ranks for both sets of cards
    for card in all_cards:
        rank = card[0]
        my_rank_counts[rank] += 1

    for card in opponents_all_cards:
        rank = card[0]
        opponents_rank_counts[rank] += 1

    # Extract pair rank and other ranks for each hand
    my_pair_rank = [rank for rank, count in my_rank_counts.items() if count == 2]
    my_remaining_ranks = [rank for rank, count in my_rank_counts.items() if count == 1]

    opponents_pair_rank = [rank for rank, count in opponents_rank_counts.items() if count == 2]
    opponents_remaining_ranks = [rank for rank, count in opponents_rank_counts.items() if count == 1]

    # Compare pairs
    if my_pair_rank and opponents_pair_rank:
        if RANKS.index(my_pair_rank[0]) > RANKS.index(opponents_pair_rank[0]):
            return True
        elif RANKS.index(my_pair_rank[0]) < RANKS.index(opponents_pair_rank[0]):
            return False

    # If pairs are equal, compare remaining cards
    my_remaining_ranks.sort(key=lambda x: RANKS.index(x), reverse=True)
    opponents_remaining_ranks.sort(key=lambda x: RANKS.index(x), reverse=True)

    min_length = min(len(my_remaining_ranks), len(opponents_remaining_ranks))

    for i in range(min_length):
        if RANKS.index(my_remaining_ranks[i]) > RANKS.index(opponents_remaining_ranks[i]):
            return True
        elif RANKS.index(my_remaining_ranks[i]) < RANKS.index(opponents_remaining_ranks[i]):
            return False

    return random.choice([True, False])


def two_pair_tiebreaker(my_cards, opponents_hand, community_cards):
    # Group cards by rank for both the player and opponents
    my_rank_counts = {}
    for card in my_cards + community_cards:
        rank = card[0]
        my_rank_counts[rank] = my_rank_counts.get(rank, 0) + 1

    opponents_rank_counts = {}
    for card in opponents_hand + community_cards:
        rank = card[0]
        opponents_rank_counts[rank] = opponents_rank_counts.get(rank, 0) + 1

    # Extract pairs
    my_pairs = sorted([rank for rank, count in my_rank_counts.items() if count == 2], reverse=True)
    opponents_pairs = sorted([rank for rank, count in opponents_rank_counts.items() if count == 2], reverse=True)

    # If one of the hands doesn't have two pairs, return false
    if len(my_pairs) != 2 or len(opponents_pairs) != 2:
        return False 

    # Compare the higher pair first
    if my_pairs[0] > opponents_pairs[0]:
        return True
    elif my_pairs[0] < opponents_pairs[0]:
        return False
    # If the higher pairs are equal, compare the lower pairs
    elif my_pairs[1] > opponents_pairs[1]:
        return True
    elif my_pairs[1] < opponents_pairs[1]:
        return False
    else:
        # If both pairs are equal, handle the tie with the high-card tiebreaker
        return high_card_tiebreaker(my_cards, opponents_hand, community_cards)


def three_of_a_kind_tiebreaker(my_cards, opponents_hand, community_cards):
    # Group cards by rank for both the player and opponents
    my_rank_counts = {}
    for card in my_cards + community_cards:
        rank = card[0]
        my_rank_counts[rank] = my_rank_counts.get(rank, 0) + 1

    opponents_rank_counts = {}
    for card in opponents_hand + community_cards:
        rank = card[0]
        opponents_rank_counts[rank] = opponents_rank_counts.get(rank, 0) + 1

    # Find the rank of the three-of-a-kind for both the player and opponents
    my_three_of_a_kind = [rank for rank, count in my_rank_counts.items() if count == 3]
    opponents_three_of_a_kind = [rank for rank, count in opponents_rank_counts.items() if count == 3]

    # Check if there is a three-of-a-kind rank in both hands
    if my_three_of_a_kind and opponents_three_of_a_kind:
        # Compare the ranks of the three-of-a-kind
        if my_three_of_a_kind[0] > opponents_three_of_a_kind[0]:
            return True

    return False


def straight_tiebreaker(my_cards, opponents_hand, community_cards):
    # Extract the ranks from the player's and opponents' cards
    my_ranks = sorted([card[0] for card in my_cards + community_cards], reverse=True)
    opponents_ranks = sorted([card[0] for card in opponents_hand + community_cards], reverse=True)

    # Convert the ranks to their numeric values
    rank_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    
    # Handle the case where '1' represents '10'
    my_rank_values = [rank_values[rank] if rank != '1' else rank_values['10'] for rank in my_ranks]
    opponents_rank_values = [rank_values[rank] if rank != '1' else rank_values['10'] for rank in opponents_ranks]

    # Compare the highest cards in the straight
    if my_rank_values[0] > opponents_rank_values[0]:
        return True
    elif my_rank_values[0] == opponents_rank_values[0]:
        return random.choice([True, False])
    
    return False


def flush_tiebreaker(my_cards, opponents_hand, community_cards):
    # Extract and sort the suits of the player's and opponents' flushes
    my_suits = sorted([card[1] for card in my_cards + community_cards], reverse=True)
    opponents_suits = sorted([card[1] for card in opponents_hand + community_cards], reverse=True)

    # Compare the highest suits in the flush
    if my_suits[0] > opponents_suits[0]:
        return True
    elif my_suits[0] == opponents_suits[0]:
        return random.choice([True, False])
    
    return False


def full_house_tiebreaker(my_cards, opponents_hand, community_cards):
    # Group cards by rank for both the player and opponents
    my_rank_counts = {}
    for card in my_cards + community_cards:
        rank = card[0]
        my_rank_counts[rank] = my_rank_counts.get(rank, 0) + 1

    opponents_rank_counts = {}
    for card in opponents_hand + community_cards:
        rank = card[0]
        opponents_rank_counts[rank] = opponents_rank_counts.get(rank, 0) + 1

    # Extract the trio and pair for each player
    my_trio_rank = next((rank for rank, count in my_rank_counts.items() if count == 3), None)
    my_pair_rank = next((rank for rank, count in my_rank_counts.items() if count == 2), None)

    opponents_trio_rank = next((rank for rank, count in opponents_rank_counts.items() if count == 3), None)
    opponents_pair_rank = next((rank for rank, count in opponents_rank_counts.items() if count == 2), None)

    # If either hand does not have a full house, return false
    if not my_trio_rank or not my_pair_rank or not opponents_trio_rank or not opponents_pair_rank:
        return False 
    
    # Compare the trio rank first
    if my_trio_rank > opponents_trio_rank:
        return True
    elif my_trio_rank < opponents_trio_rank:
        return False
    else:
        # If the trios are equal, compare the pair rank
        return my_pair_rank > opponents_pair_rank


def four_of_a_kind_tiebreaker(my_cards, opponents_hand, community_cards):
    # Count the occurrences of each rank in the player's and opponents' hands
    my_rank_counts = {card[0]: my_cards.count(card) + community_cards.count(card) for card in my_cards + community_cards}
    opponents_rank_counts = {card[0]: opponents_hand.count(card) + community_cards.count(card) for card in opponents_hand + community_cards}

    # Find the rank(s) with four of a kind in both hands
    my_four_of_a_kind_rank = [rank for rank, count in my_rank_counts.items() if count == 4]
    opponents_four_of_a_kind_rank = [rank for rank, count in opponents_rank_counts.items() if count == 4]

    # Check if there are four-of-a-kind ranks in both hands
    if my_four_of_a_kind_rank and opponents_four_of_a_kind_rank:
        # Compare the ranks of four of a kind
        if my_four_of_a_kind_rank[0] > opponents_four_of_a_kind_rank[0]:
            return True

    return False


def straight_flush_tiebreaker(my_cards, opponents_hand, community_cards):
    my_highest_straight_flush = find_highest_straight_flush(my_cards + community_cards)
    opponents_highest_straight_flush = find_highest_straight_flush(opponents_hand + community_cards)

    if my_highest_straight_flush > opponents_highest_straight_flush:
        return True
    elif my_highest_straight_flush < opponents_highest_straight_flush:
        return False
    else:
        return random.choice([True, False])


def find_highest_straight_flush(cards):
    rank_values = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
    }

    # Find cards of the same suit (at least 5 required for a straight flush)
    suits = ['H', 'D', 'C', 'S']
    for suit in suits:
        suit_cards = sorted([card for card in cards if card[1] == suit], key=lambda x: rank_values[x[0]], reverse=True)
        
        if len(suit_cards) < 5:
            continue

        # Check for straight in suit_cards
        for i in range(len(suit_cards) - 4):
            high_rank_value = rank_values[suit_cards[i][0]]
            if all(rank_values[suit_cards[i + j][0]] == high_rank_value - j for j in range(5)):
                return high_rank_value

            # Special case: Check for A-2-3-4-5 straight flush
            if suit_cards[i][0] == 'A' and all(card[0] in ['2', '3', '4', '5'] for card in suit_cards[i+1:i+5]):
                return rank_values['5']  # Return 5 as the highest card in the A-2-3-4-5 straight flush

    return 0
