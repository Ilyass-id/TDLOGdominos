import random

_LIMIT = '+-----|-----+'
"""The top and bottom lines of a domino representation"""


_DOTS = [
    ['     ', '     ', '     '],
    ['     ', '  *  ', '     '],
    ['*    ', '     ', '    *'],
    ['*    ', '  *  ', '    *'],
    ['*   *', '     ', '*   *'],
    ['*   *', '  *  ', '*   *'],
    ['* * *', '     ', '* * *']]
"""The dots lines of a domino representation"""

class Domino :
    def __init__ (self, left0, right0):
        self._left = left0
        self._right = right0

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    def __repr__(self):
        result = "Domino("+str(self.left)+", "+str(self.right)+")"
        return result

    def __str__(self):

        # build the domino representation line by line
        result = '\n'.join([
            _LIMIT,
            '|' + _DOTS[self.left][0] + '|' + _DOTS[self.right][0] + '|',
            '|' + _DOTS[self.left][1] + '|' + _DOTS[self.right][1] + '|',
            '|' + _DOTS[self.left][2] + '|' + _DOTS[self.right][2] + '|',
            _LIMIT]) + '\n'
        return result

    def __eq__(self, other):
        return ((self.left == other.left and self.right == other.right) or (self.left == other.right and self.right == other.left))

    def __ne__(self, other):
        return (not ((self.left == other.left and self.right == other.right) or (self.left == other.right and self.right == other.left)))


DOMINOS_SET = [Domino(left, right) for left in range(7) for right in range(left + 1)]
"""The 28 dominos in the game"""


HAND_SIZE = 7
"""Number of dominos in the hand"""


TARGET = 12
"""Number of points on dominos to discard them"""

class Solitaire:
    def __init__(self):
        self.pile = random.sample(DOMINOS_SET, len(DOMINOS_SET))
        self.hand = []
        self.is_won = False
    
    def turn(self):
        # fill the hand with HAND_SIZE dominos until the pile is empty
        while len(self.hand) != HAND_SIZE and self.pile:
            self.hand.append(self.pile.pop())

        # check if the game is won (the hand and the pile are empty)
        if not self.hand:
            self.is_won = True
            return 0

        # print the dominos hand and ask the player to play
        for (i, d) in enumerate(self.hand):
            print (i+1)
            print(d)
        indexes = input(f'pile size = {len(self.pile)}, dominos to discard?')

        # count the sum of the selected dominos
        try:
            indexes = set(sorted(
                [int(idx) - 1 for idx in indexes], reverse=True))
            total = sum(self.hand[idx].left + self.hand[idx].right for idx in indexes)
        except (ValueError, IndexError):
            print('invalid indexes')
            return 1

        # If the total is correct, discard the selected dominos
        if  total != TARGET:
            print(f'invalid total ({total} but expected {TARGET})')
        else:
            for idx in indexes:
                self.hand.pop(idx)

    def play(self):
        while not self.is_won:
            self.turn()

def main():
    d1 = Domino(3, 5)
    print (repr(d1))
    print(d1)
    d2 = Domino(3, 5)
    d3 = Domino(2, 4)
    print(d1 == d2)
    print(d1 == d3)
    print(d1 != d2)
    print(d1 != d3)
    s = Solitaire()
    s.play()


if __name__ == '__main__':
    main()
