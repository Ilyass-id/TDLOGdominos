"""TDLOG TP3 - Pauline MOLITOR, Ilyass RAMDANI - ? brain hours"""
import itertools
import random


class InvalidIndexError(Exception):
    """Represent an error on the indexes from the input of the user"""
    def __init__(self, n):
        super().__init__()
        self._value = n

    @property
    def value(self):
        """Value of the error"""
        return self._value

    def __str__(self):
        return f"Invalid index: '{self._value}'"


class Domino:
    """Represent a domino with left and right integer values in [0, 6]"""
    # the pip used to render a domino on screen
    _PIPS = [
        ["     ", "     ", "     "],
        ["     ", "  *  ", "     "],
        ["*    ", "     ", "    *"],
        ["*    ", "  *  ", "    *"],
        ["*   *", "     ", "*   *"],
        ["*   *", "  *  ", "*   *"],
        ["* * *", "     ", "* * *"]]

    # boundaries of a displayed domino
    _HORIZONTAL_BAR = "+-----|-----+"

    def __init__(self, left, right):
        assert (0 <= left < 7), "Value of the domino's left-side must be in [0,6]"
        assert (0 <= right < 7), "Value of the domino's right-side must be in [0,6]"
        self._left = left
        self._right = right

    @property
    def left(self):
        """Value of the domino's left-side"""
        return self._left

    @property
    def right(self):
        """Value of the domino's right side"""
        return self._right

    @property
    def score(self):
        """Number of points on the domino (sum of left and right sides)"""
        return self.left + self.right

    def __repr__(self):
        return f'Domino({self.left}, {self.right})'

    def __str__(self):
        domino = [self._HORIZONTAL_BAR]
        for i in range(3):
            domino.append(
                '|' + self._PIPS[self.left][i] +
                '|' + self._PIPS[self.right][i] + '|')
        domino.append(self._HORIZONTAL_BAR)
        return '\n'.join(domino)

    def __eq__(self, other):
        return (
            (self.left == other.left and self.right == other.right)
            or
            (self.left == other.right and self.right == other.left))

    def __ne__(self, other):
        return not self == other


class Solitaire:
    """Manage a domino's solitaire game

    Parameters
    ----------
    target : int
        The target sum player must reach in order to discard dominos from it's
        hand at each turn.

    """

    def __init__(self, target=12):
        self._target = target

        # generate the set of 28 dominos for the game (in random order)
        dominos = [
            Domino(left, right)
            for left in range(7) for right in range(left + 1)]
        random.shuffle(dominos)

        # hand is made of the first 7 dominos, the pile of the 21 others
        self._hand = dominos[:7]
        self._pile = dominos[7:]

    def _exists_legal_move(self):
        """Returns True if some combination in the hand sums to the target"""
        # get an iterator over all the dominos combinations in the hand
        combinations = itertools.chain.from_iterable(
            itertools.combinations(self.hand, r)
            for r in range(len(self.hand) + 1))

        # a legal move exists if one combination sum to the target score
        for combination in combinations:
            if sum(d.score for d in combination) == self.target:
                return True
        return False

    @staticmethod
    def _display_domino(index, domino):
        """Prints a single domino to stdout"""
        # display a domino line per line, add it's index as prefix (and its
        # score as suffix, this is out of the TP subject but make the game
        # easier)
        prefix_empty = ' ' * (len(str(index)) + 4)
        for idx, line in enumerate(str(domino).strip().split('\n')):
            prefix = f' ({index}) ' if idx == 2 else prefix_empty
            suffix = f' -> {domino.score}' if idx == 2 else ''
            print(prefix + line + suffix)

    def _display_hand(self):
        """Prints the dominos hand to stdout"""
        # display all the dominos in the hand, indexed starting at 1
        for index, domino in enumerate(self.hand):
            self._display_domino(index + 1, domino)
            print()

    @property
    def hand(self):
        """The hand of 7 (maximum) dominos to play with"""
        return self._hand

    @property
    def pile(self):
        """The pile of remaining dominos"""
        return self._pile

    @property
    def target(self):
        """The target score to get in order to discard dominos"""
        return self._target

    def is_game_won(self):
        """Return True if and only if the game is won"""
        return not self.hand

    def is_game_lost(self):
        """Returns True if and only of the game is lost"""
        return not self._exists_legal_move()


class InteractiveSolitaire(Solitaire):
    """Solitaire's daughter class

    Launch a new interactive game with the play() method.

    """

    def __init__(self, target=12):
        super().__init__()

    def _check_indexes(self, indexes):
        """Raise InvalidIndexError if the indexes are not valid"""
        total = 0
        for i in indexes:
            if 0 <= i < len(self.hand):
                total += self.hand[i].score
            else:
                raise InvalidIndexError(
                    "Index must be between 1 and the size of the hand")

        if total != self.target:
            raise InvalidIndexError(
                f"invalid total ({total} but expected {self.target})")

    def _get_player_input(self):
        """Returns the indexes of dominos to discard entered by the player"""
        indexes = input(f"(pile size: {len(self.pile)}), indexes to pull out?")

        # substract 1 because indexes are displayed as starting at 1
        try:
            indexes = [int(i) - 1 for i in indexes]
            self._check_indexes(indexes)
        except ValueError:
            raise InvalidIndexError("Index must be integer") from ValueError
        else:
            return indexes

    def turn(self):
        """Manage a single turn of the game

        The following steps are managed:
        1. display the player's hand to stdout
        2. ask the player to choose the dominos to discard
        3. ensures the chosen dominos sum to `target`
        4. if true discard them and refill the hand from the pile, if not do
        nothing

        """
        # print the dominos in the hand to screen
        self._display_hand()

        # ask the player to choose the dominos to discard
        try:
            indexes = self._get_player_input()
        except InvalidIndexError as error :
            print(error)
        else:
            # discard the played dominos
            for i in sorted(indexes, reverse=True):
                self.hand.pop(i)

            # fill the hand with dominos in the pile
            while len(self.hand) != 7 and self.pile:
                self.hand.append(self.pile.pop())

    def play(self):
        """Play the game turn by turn until victory or defeat

        Returns True on victory, False on defeat.

        """
        while True:
            if self.is_game_won():
                print('You win ')
                return True

            if self.is_game_lost():
                self._display_hand()
                print('No more legal move, you loose ')
                return False

            self.turn()

class AutoPlaySolitaire(Solitaire):
    """Solitaire's daughter class

    Launch a new game and search a solution with the play() method.

    """

    def __init__(self, target=12):
        super().__init__()

    def play(self):
        """Play the game automatically

        Returns True on victory, False on defeat.

        """
        #TODO
        return False

if __name__ == '__main__':
    InteractiveSolitaire().play()
