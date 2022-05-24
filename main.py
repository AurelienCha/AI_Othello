import copy
from itertools import cycle
import os
import random
import sys
import time

DEBUG = False
INFINITY = 999999999

# Kind of IA


WHITE = " ⚫️ "
BLACK = " ⚪️ "
EMPTY = "    "

DANGEROUS_POSITIONS = [
    (0, 1), (0, 6),
    (1, 0), (1, 1), (1, 6), (1, 7),
    (6, 0), (6, 1), (6, 6), (6, 7),
    (7, 1), (7, 6)
]
CORNER_POSITIONS = [(0, 0), (7, 0), (7, 7), (0, 7)]


class Board():
    def __init__(self):
        self.remaining_round = 60
        self.board = [[EMPTY for i in range(8)] for i in range(8)]
        self.board[3][4] = WHITE
        self.board[3][3] = BLACK
        self.board[4][3] = WHITE
        self.board[4][4] = BLACK


    def __str__(self):
        b = self.board
        return f"""Remaining round {self.remaining_round}\n     1    2    3    4    5    6    7    8
   ┼────┼────┼────┼────┼────┼────┼────┼────┼
 A │{b[0][0]}│{b[0][1]}│{b[0][2]}│{b[0][3]}│{b[0][4]}│{b[0][5]}│{b[0][6]}│{b[0][7]}│ A
   ┼────┼────┼────┼────┼────┼────┼────┼────┼
 B │{b[1][0]}│{b[1][1]}│{b[1][2]}│{b[1][3]}│{b[1][4]}│{b[1][5]}│{b[1][6]}│{b[1][7]}│ B
   ┼────┼────┼────┼────┼────┼────┼────┼────┼
 C │{b[2][0]}│{b[2][1]}│{b[2][2]}│{b[2][3]}│{b[2][4]}│{b[2][5]}│{b[2][6]}│{b[2][7]}│ C
   ┼────┼────┼────┼────┼────┼────┼────┼────┼
 D │{b[3][0]}│{b[3][1]}│{b[3][2]}│{b[3][3]}│{b[3][4]}│{b[3][5]}│{b[3][6]}│{b[3][7]}│ D
   ┼────┼────┼────┼────┼────┼────┼────┼────┼
 E │{b[4][0]}│{b[4][1]}│{b[4][2]}│{b[4][3]}│{b[4][4]}│{b[4][5]}│{b[4][6]}│{b[4][7]}│ E
   ┼────┼────┼────┼────┼────┼────┼────┼────┼
 F │{b[5][0]}│{b[5][1]}│{b[5][2]}│{b[5][3]}│{b[5][4]}│{b[5][5]}│{b[5][6]}│{b[5][7]}│ F
   ┼────┼────┼────┼────┼────┼────┼────┼────┼
 G │{b[6][0]}│{b[6][1]}│{b[6][2]}│{b[6][3]}│{b[6][4]}│{b[6][5]}│{b[6][6]}│{b[6][7]}│ G
   ┼────┼────┼────┼────┼────┼────┼────┼────┼
 H │{b[7][0]}│{b[7][1]}│{b[7][2]}│{b[7][3]}│{b[7][4]}│{b[7][5]}│{b[7][6]}│{b[7][7]}│ H
   ┼────┼────┼────┼────┼────┼────┼────┼────┼
     1    2    3    4    5    6    7    8"""

    def has_dominated(self, player):
        """
        Returns False if the other player is still on the board
        """
        for y in range(8):
            for x in range(8):
                if self.board[x][y] != EMPTY and self.board[x][y] != player.color:
                    return False
        return True

    def is_full(self):
        """
        Returns True/False if the board is/isn't full.
        """
        for y in range(8):
            for x in range(8):
                if self.board[x][y] == EMPTY:
                    return False
        return True

    def has_valid_moves(self, player):
        try:
            return True if self._get_valid_moves(player) else False
        except Exception as e:
            return False

    def _get_valid_moves(self, player):
        valid_moves = []
        for y in range(8):
            for x in range(8):
                move = x, y
                if self.is_valid_move(player, move):
                    valid_moves.append(move)
        return valid_moves

    def is_valid_move(self, player, move):
        """
        Returns True/False if the player can/cannot play the move.
        """

        x, y = move
        if x not in range(8) or y not in range(8):
            return False  # Off the board
        elif self.board[x][y] != EMPTY:
            return False  # Position to move is not empty
        else:
            return True if self._get_flips(player, move) else False

    def _get_flips(self, player, move):
        """
        Return a list of tuples that represents stones (x,y positions) to flip.
        """

        flips = []
        flips += self._get_flips_in_direction(player, move, direction=(0, 1))  # right
        flips += self._get_flips_in_direction(player, move, direction=(0, -1))  # left
        flips += self._get_flips_in_direction(player, move, direction=(1, 0))  # down
        flips += self._get_flips_in_direction(player, move, direction=(-1, 0))  # up
        flips += self._get_flips_in_direction(player, move, direction=(1, 1))  #
        flips += self._get_flips_in_direction(player, move, direction=(-1, 1))  #
        flips += self._get_flips_in_direction(player, move, direction=(1, -1))  #
        flips += self._get_flips_in_direction(player, move, direction=(-1, -1))  #
        return flips

    def _get_flips_in_direction(self, player, move, direction):
        line = self._get_line_in_direction(player, move, direction)
        if not line:
            return []
        elif line[-1] == player.color:
            return line[:-1]
        else:
            return []

    def _get_line_in_direction(self, player, position, direction):
        """
        Returns a list (line) of stones in a direction.
        """
        next_position = position[0]+direction[0], position[1]+direction[1]
        x, y = next_position

        if x not in range(8) or y not in range(8):
            return []
        cell = self.board[x][y]
        if cell==EMPTY:
            return [EMPTY]
        elif cell==player.color:
            return [player.color]
        else:
            return [(x,y)] + self._get_line_in_direction(player, next_position, direction)  # todo stop if wrong capture

    def put_stone(self, player, move):
        """
        Checks if the move is valid, and if so, puts the stone and flip others.
        """
        if not self.is_valid_move(player, move):
            raise RuntimeError("Invalid move")
        x, y = move
        self.board[x][y] = player.color
        for xi, yi in self._get_flips(player, move):
            self.board[xi][yi] = player.color
        self.remaining_round -= 1

    def get_player_score(self, player):
        score = 0
        for y in range(8):
            for x in range(8):
                if self.board[x][y] == player.color:
                    score += 1
        return score

    def _start_with_max(self, player):
        rep = False
        if player.cost_function == "max" or (player.cost_function=="hybrid" and self.remaining_round <= 2*player.depth):
            rep = True
        if player.depth % 2:
            return not rep
        else:
            return rep


    def alpha_beta_search(self, player, adversary):
        boardAlgo = Board()
        boardAlgo.board = copy.deepcopy(self.board)
        depth = player.depth
        if player.cst_depth and self.remaining_round <= 15:
            depth += 2
        moves = [(0,0) for _ in range(depth)]
        if self._start_with_max(player):
            boardAlgo.max_value(player, adversary, -INFINITY, INFINITY, moves, 0, depth)
        else:
            boardAlgo.min_value(player, adversary, -INFINITY, INFINITY, moves, 0, depth)
        return moves[0]

    def max_value(self, player, adversary, alpha, beta, moves, cmpt, depth):
        if DEBUG: print(cmpt, cmpt*"    ", "Max", player.color, "alpha=", alpha, "beta=", beta)

        # If end of recursion/tree return evaluation function
        if cmpt >= depth or self.is_full() or not self.has_valid_moves(player):
            return self.get_player_score(player)

        # Loops over possibles moves
        for move in self._get_valid_moves(player):
            if DEBUG: print(cmpt, cmpt*"    ", "move:", player.color, move)
            # Play the next turn on a copy of the board
            nextBoard = Board()
            nextBoard.board = copy.deepcopy(self.board)
            nextBoard.put_stone(player, move)
            # Compute recusively the evaluation function (minMax)
            utility = nextBoard.min_value(adversary, player, alpha, beta, moves, cmpt+1, depth)
            if DEBUG: print(cmpt, cmpt * "    ", utility >= beta, ":: utility >= beta ::", utility, ">=", beta)
            if DEBUG: print(cmpt, cmpt * "    ", utility > alpha, ":: utility > alpha ::", utility, ">", alpha)
            # Pruning if utility out of optimal range
            if player.pruning and utility >= beta:
                if DEBUG: print("PRUNING")
                return utility
            # Update range limit if best (affine range)
            elif utility > alpha:
                alpha = utility
                moves[cmpt] = move
        return alpha

    def min_value(self, player, adversary, alpha, beta, moves, cmpt, depth):
        if DEBUG: print(cmpt, cmpt*"    ", "min", player.color, "moves=", moves, "alpha=", alpha, "beta=", beta)

        # If end of recursion/tree return evaluation function
        if cmpt >= depth or self.is_full() or not self.has_valid_moves(player):
            return self.get_player_score(player)

        # Loops over possibles moves
        for move in self._get_valid_moves(player):
            if DEBUG: print(cmpt, cmpt*"    ", "move:", player.color, move)
            # Play the next turn on a copy of the board
            nextBoard = Board()
            nextBoard.board = copy.deepcopy(self.board)
            nextBoard.put_stone(player, move)
            # Compute recusively the evaluation function (minMax)
            utility = nextBoard.max_value(adversary, player, alpha, beta, moves, cmpt+1, depth)
            if DEBUG: print(cmpt, cmpt*"    ", utility <= alpha, ":: utility =< alpha ::", utility, "<=", alpha)
            if DEBUG: print(cmpt, cmpt*"    ", utility < beta, ":: utility < beta ::", utility, "<", beta)
            # Pruning if utility out of optimal range
            if player.pruning and utility <= alpha:
                if DEBUG: print("PRUNING")
                return utility
            # Update range limit if best (affine range)
            elif utility < beta:
                beta = utility
                moves[cmpt] = move
        return beta

    def get_random_move(self, player):
        return random.choice(self._get_valid_moves(player))

    def print_valid_moves(self, player):
        moves = self._get_valid_moves(player)
        for move in moves:
            x, y = move
            x = chr(x+65)
            y += 1
            print(f"({x}, {y})", end=" ")
        print()


class Player():
    def __init__(self, color, type, depth, cst_depth, pruning, cost):
        self.color = color
        self.type = type
        self.depth = depth
        self.cst_depth = cst_depth
        self.pruning = pruning
        self.cost_function = cost
        self.describe()

    def describe(self):
        print(f"\nPlayer {self.color} is {self.type}")
        if self.type == 'IA':
            print(f" Depth : {self.depth} (cst={self.cst_depth}) \n Pruning : {self.pruning} \n Cost function : {self.cost_function}")

    def inversePlayer(self, players):
        if self == players[0]:
            return players[1]
        else:
            return players[0]

    def get_move(self):
        # Input move
        move = input( \
            f"Where will you play next, {self.color}? "
        ).strip().replace(" ", "").replace(",", "").replace("|", "")
        if len(move) != 2:
            raise RuntimeError  # Invalid move
        # Parse move
        x, y = move[0].upper(), move[1].upper()
        # fix move
        if x in "12345678" and y.upper() in "ABCDEFGH":
            x, y = y, x
            x, y = ord(x.upper()) - 65, int(y) - 1
        elif x in "ABCDEFGH" and y in "12345678":
            x, y = ord(x.upper()) - 65, int(y) - 1
        elif x in "?" and y in "?":
            return "?"
        else:
            raise RuntimeError  # Invalid move - can't parse
        return x, y


class Game:
    def __init__(self, type_1, depth_1, cst_depth_1, pruning_1, cost_1, type_2, depth_2, cst_depth_2, pruning_2, cost_2):
        self.board = Board()
        self.players = [Player(BLACK, type_1, depth_1, cst_depth_1, pruning_1, cost_1),
                        Player(WHITE, type_2, depth_2, cst_depth_2, pruning_2, cost_2)]

    def _print(self):
        """
        Prints the game: the header, notification(s) (if any) and the board
        """
        header = "Reversi"
        p0 = self.players[0]
        p1 = self.players[1]
        p0_score = f"{p0.color}{'%2d' % self.board.get_player_score(p0)}"
        p1_score = f"{p1.color}{'%2d' % self.board.get_player_score(p1)}"
        render = f"""{header}
Score: {p0_score} vs. {p1_score}
{self.board}
"""
        print(render)

    def _no_possible_move(self):
        if not (self.board.has_valid_moves(self.players[0])) and not (self.board.has_valid_moves(self.players[1])):
            return True
        else:
            return False

    def play(self):
        for player in cycle(self.players):
            self._print()
            if self.board.is_full() or self.board.has_dominated(player) or self._no_possible_move():
                print("BREAK", self.board.is_full(), " ", self.board.has_dominated(player), " ", self._no_possible_move)
                break
            if self.board.has_valid_moves(player):
                start = time.time()
                while True:
                    try:
                        if player.type == 'H':  # Human Player
                            move = player.get_move()
                        elif player.type == 'R': # Random IA
                            move = self.board.get_random_move(player)
                        else: # IA
                            print(f"Player {player.color} is thinking..")
                            move = self.board.alpha_beta_search(player, player.inversePlayer(self.players))
                            print(move)
                        if type(move) is tuple:
                            end = time.time()
                            self.board.put_stone(player, move)
                            break
                        else:
                            self.board.print_valid_moves(player)
                    except KeyboardInterrupt:
                        sys.exit(1)
                    except RuntimeError as e:
                        pass
                    except Exception as e:
                        pass
                print(f"time for last play {end - start}")
                print(f"Score Player 1 : {self.board.get_player_score(self.players[0])}")
                print(f"Score Player 2 : {self.board.get_player_score(self.players[1])}")
                print(f"Last move : Player {player.color} in ({chr(65+move[0])}, {move[1]+1})\n")
                # todo put in datframe for CSV (+ save corner pos)
        self._print()


def extract_player_option(str):
    if str[0] == 'H' or str[0] == 'h':
        return 'H', None, None, None, None
    elif str[0] == 'R' or str[0] == 'r':
        return 'R', None, None, None, None
    else:
        print(str)
        depth = ''
        for c in str:
            if c.isdigit():
                depth += c
            else:
                break
        if depth.isdigit():
            depth = int(depth)
        else:
            sys.exit(11)

        cst_depth = True if ('+' in str) else False
        pruning = False if ('P' in str or 'p' in str) else True

        if 'min' in str or 'Min' in str or 'MIN' in str: cost = 'min'
        elif 'max' in str or 'Max' in str or 'MAX' in str: cost = 'max'
        else: cost = 'hybrid'

        return 'IA', depth, cst_depth, pruning, cost


def help():
    print("The program needs 2 arguments: py main.py [player_1] [player_2]")
    print("Where argument [player] is the parameters for player")
    print(" - 'H' : Human")
    print(" - 'R' : Random")
    print(" - '<depth>' : AI where depth is a digit representing the depth of the tree (may have optionnal parameters)")
    print("             - '+' for increasing depth at the end")
    print("             - 'p' for removing pruning")
    print("             - 'min' or 'max' to specify the capture strategy (by default : 'hybrid' -> min at the beginning, max at the end)")
    print("\n\ne.g. To run a Random algo against an AI with a depth of 4, increasing towards the end, without pruning and minimizing the number of pawns captured\npy main.py R 4+Pmin")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        help()
        sys.exit()
    if len(sys.argv) > 3:
        print("Please refers you to the documentation...", file=sys.stderr)
        sys.exit(1)

    type_1, depth_1, cst_depth_1, pruning_1, cost_1 = extract_player_option(sys.argv[1])
    type_2, depth_2, cst_depth_2, pruning_2, cost_2 = extract_player_option(sys.argv[2])

    game = Game(type_1, depth_1,  cst_depth_1, pruning_1, cost_1, type_2, depth_2, cst_depth_2, pruning_2, cost_2)
    game.play()