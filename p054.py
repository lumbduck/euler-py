"""
Poker Hands

In the card game poker, a hand consists of five cards and are ranked, from lowest to highest, in the following way:

High Card: Highest value card.
One Pair: Two cards of the same value.
Two Pairs: Two different pairs.
Three of a Kind: Three cards of the same value.
Straight: All cards are consecutive values.
Flush: All cards of the same suit.
Full House: Three of a kind and a pair.
Four of a Kind: Four cards of the same value.
Straight Flush: All cards are consecutive values of same suit.
Royal Flush: Ten, Jack, Queen, King, Ace, in same suit.
The cards are valued in the order:
2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King, Ace.

If two players have the same ranked hands then the rank made up of the highest value wins; for example, a pair of eights beats a pair of fives (see example 1 below). But if two ranks tie, for example, both players have a pair of queens, then highest cards in each hand are compared (see example 4 below); if the highest cards tie then the next highest cards are compared, and so on.

Consider the following five hands dealt to two players:

Hand	 	Player 1	 	Player 2	 	Winner
1       5H 5C 6S 7S KD  2C 3S 8S 8D TD  Player 2
        Pair of Fives   Pair of Eights

2	 	5D 8C 9S JS AC  2C 5C 7D 8S QH  Player 1
    Highest card Ace    Highest card Queen

3	 	2D 9C AS AH AC  3D 6D 7D TD QD  Player 2
        Three Aces      Flush with Diamonds

4	 	4D 6S 9H QH QC  3D 6D 7H QD QS  Player 1
        Pair of Queens  Pair of Queens
    Highest card Nine   Highest card Seven

5	 	2H 2D 4C 4D 4S  3C 3D 3S 9S 9D  Player 1
        Full House      Full House
    With Three Fours    with Three Threes

The file, p54_data/poker.txt, contains one-thousand random hands dealt to two players. Each line of the file contains ten cards (separated by a single space): the first five are Player 1's cards and the last five are Player 2's cards. You can assume that all hands are valid (no invalid characters or repeated cards), each player's hand is in no specific order, and in each hand there is a clear winner.

How many hands does Player 1 win?
"""
from common import elapsed

f_path = 'data/p54_poker.txt'

# Pre-generate ranks and straights
rank_map = {r: i for i, r in enumerate('23456789TJQKA', 2)}

# Each straight is a key value, representing the lowest rank in the hand, mapped to a set of the 4 other ranks.
# NOTE: All rank keys are integers, retrievable via :func get_rank: below.
straight_map = {
    r: set(range(r + 1, r + 5))
    for r in range(2, 11)
}
# Include ace-first straight and empty entries for other cards
straight_map.update({14: set((2, 3, 4, 5))})
straight_map.update({
    r: set()
    for r in range(11, 14)
})


def get_rank(card, rank_map=rank_map):
    """Return card rank as a value 2 - 14 (where 14 represents an Ace) to simplify comparisons."""
    return rank_map[card[0]]


def sort_hand(hand):
    """Return hand sorted with high card first."""
    return tuple(sorted(hand, key=get_rank, reverse=True))


def remove_rank(target, ranks):
    """Return sorted tuple of given ranks with the target rank removed."""
    return tuple(filter(lambda x: x != target, ranks))


def players(pokers_txt_line):
    """
    Return two poker player tuples.

    tuples are composed as follows:
    (
        5-tuple of player cards as given in data file, sorted with highest rank first,
        5-tuple of card ranks as integers, sorted with highest rank first
    )
    """
    cards = pokers_txt_line.split()

    hand1 = sort_hand(cards[:5])
    player1 = (hand1, tuple(get_rank(card) for card in hand1))

    hand2 = sort_hand(cards[5:])
    player2 = (hand2, tuple(get_rank(card) for card in hand2))

    return player1, player2


def flush(player):
    """Return highest rank if hand is a flush."""
    hand = player[0]
    if all(hand[0][1] == card[1] for card in hand[1:]):
        return player[1][0]


def straight(player, straight_map=straight_map):
    """Return high card if hand is a straight."""
    ranks = player[1]

    # Special handling if hand has both an Ace and a 2 (since these ranks are not consecutive)
    if ranks[0] == 14 and ranks[1] == 5:
        if set(ranks[1:]).issuperset(straight_map[14]):
            # The high card is always rank 5 for straights starting with an Ace
            return 5

    # Otherwise, straight must start with a Ten or lower
    elif set(ranks[:-1]).issuperset(straight_map[ranks[-1]]):
        return ranks[0]


def longest_kind(player):
    """
    Return a 2-tuple with the length and rank of longest run of identically ranked cards in hand.

    If there are two pairs, returns the higher ranked pair.
    If there is no pair or longer in the player's hand, returns None instead.
    """
    ranks = player[1]

    best_length = 0
    best_rank = None

    curr_rank = None
    curr_length = 0

    for rank in ranks:
        if rank == curr_rank:
            curr_length += 1
            if curr_length > best_length:
                best_length = curr_length
                best_rank = curr_rank
        else:
            curr_rank = rank
            curr_length = 1

    if best_rank:
        return best_length, best_rank


def full_house(longest_kind_tuple, player):
    """
    Return 2-tuple with ranks of both the three of a kind and pair, respectively, if the player has a full house.

    NOTE: longest_kind_tuple must be output of :func longest_kind:.
    """
    if not longest_kind_tuple or longest_kind_tuple[0] != 3:
        return

    triple_rank = longest_kind_tuple[1]

    # Get the 2 cards not in the given three of a kind
    test_pair = remove_rank(triple_rank, player[1])

    if test_pair[0] == test_pair[1]:
        return triple_rank, test_pair[0]


def two_pair(longest_kind_tuple, player):
    """
    If player has two pairs, return 3-tuple of pair ranks (highest first) followed by the other card rank.

    NOTE: longest_kind_tuple must be output of :func longest_kind:.
    """
    if not longest_kind_tuple or longest_kind_tuple[0] != 2:
        return

    first_pair_rank = longest_kind_tuple[1]

    # Get the 3 cards not in the given pair
    unpaired = remove_rank(first_pair_rank, player[1])

    if unpaired[0] == unpaired[1]:
        return first_pair_rank, unpaired[0], unpaired[2]

    if unpaired[0] == unpaired[2]:
        return first_pair_rank, unpaired[0], unpaired[1]

    elif unpaired[1] == unpaired[2]:
        return first_pair_rank, unpaired[1], unpaired[0]


def compare_players(player1, player2):
    """Return True if player1 has a better hand than player2."""
    # Test for straight flush (including royal flush)
    flush1 = flush(player1)
    flush2 = flush(player2)
    if flush1 and straight(player1):
        if not flush2 or not straight(player2):
            return True
        else:
            # Compare high card
            return flush1 > flush2

    elif flush2 and straight(player2):
        return False

    # Get longest kind from each hand
    longest1 = longest_kind(player1)
    if longest1:
        kind_length1, kind_rank1 = longest1
    else:
        kind_length1 = 0
    longest2 = longest_kind(player2)
    if longest2:
        kind_length2, kind_rank2 = longest2
    else:
        kind_length2 = 0

    # Test four of a kind
    if kind_length1 == 4:
        if kind_length2 < 4:
            return True
        else:
            # Compare high card (one four of a kind must be higher than the other)
            return kind_rank1 > kind_rank2

    elif kind_length2 == 4:
        return False

    # Test full house
    full_house1 = full_house(longest1, player1)
    full_house2 = full_house(longest2, player2)
    if full_house1:
        if not full_house2:
            return True
        else:
            # Compare high cards (three of a kind first)
            return full_house1 > full_house2

    elif full_house2:
        return False

    # Test flush
    if flush1:
        if not flush2:
            return True
        else:
            # Compare high cards
            return player1[1] > player2[1]

    elif flush2:
        return False

    # Test straight
    straight1 = straight(player1)
    straight2 = straight(player2)
    if straight1:
        if not straight2:
            return True
        else:
            # Compare high card
            return straight1 > straight2

    elif straight2:
        return False

    # Test three of a kind
    if kind_length1 == 3:
        if kind_length2 < 3:
            return True
        else:
            # Compare high card (one three of a kind must be higher than the other)
            return kind_rank1 > kind_rank2

    elif kind_length2 == 3:
        return False

    # Test two-pair
    two_pair1 = two_pair(longest1, player1)
    two_pair2 = two_pair(longest2, player2)
    if two_pair1:
        if not two_pair2:
            return True
        else:
            # Compare high cards (pairs first)
            return two_pair1 > two_pair2

    elif two_pair2:
        return False

    # Test pair
    if kind_length1 == 2:
        if kind_length2 < 2:
            return True
        else:
            # Compare high cards
            if kind_rank1 > kind_rank2:
                return True
            elif kind_rank1 < kind_rank2:
                return False
            else:
                return remove_rank(kind_rank1, player1[1]) > remove_rank(kind_rank2, player2[1])

    elif kind_length2 == 2:
        return False

    # High cards only
    return player1[1] > player2[1]


def run(file_path):
    wins = 0
    total = 0
    with open(file_path) as data:
        for line in data:
            total += 1
            player1, player2 = players(line)
            wins += compare_players(player1, player2)
    print(f"Player one wins {wins} out of {total} hands")


run(f_path)
elapsed()
