
import copy
from itertools import cycle
import os
import random
import sys
import time

DEBUG = False
PRUNING = True
INFINITY = 999999999

DEPTH = 6

# Kind of IA
IA_JOSEGALARZE = -1
RANDOM = 0
MINMAX = 1
# Q-Learning = 2

WHITE = " ⚫️ "
BLACK = " ⚪️ "
EMPTY = "    "
BACK_GREEN = "\x1b[0m" # "\x1b[0;30;42m"  # style=0=normal, front=30=black, back=42=green
RESET_COLOR = "\x1b[0m"
DANGEROUS_POSITIONS = [
    (0, 1), (0, 6),
    (1, 0), (1, 1), (1, 6), (1, 7),
    (6, 0), (6, 1), (6, 6), (6, 7),
    (7, 1), (7, 6)
]
CORNER_POSITIONS = [(0, 0), (7, 0), (7, 7), (0, 7)]


class Board():
    def __init__(self):
        self.board = [[EMPTY for i in range(8)] for i in range(8)]
        self.board[3][4] = WHITE
        self.board[3][3] = BLACK
        self.board[4][3] = WHITE
        self.board[4][4] = BLACK


    def __str__(self):
        b = self.board
        return f"""     1    2    3    4    5    6    7    8
   {BACK_GREEN}┼────┼────┼────┼────┼────┼────┼────┼────┼{RESET_COLOR}
 A {BACK_GREEN}│{b[0][0]}│{b[0][1]}│{b[0][2]}│{b[0][3]}│{b[0][4]}│{b[0][5]}│{b[0][6]}│{b[0][7]}│{RESET_COLOR} A
   {BACK_GREEN}┼────┼────┼────┼────┼────┼────┼────┼────┼{RESET_COLOR}
 B {BACK_GREEN}│{b[1][0]}│{b[1][1]}│{b[1][2]}│{b[1][3]}│{b[1][4]}│{b[1][5]}│{b[1][6]}│{b[1][7]}│{RESET_COLOR} B
   {BACK_GREEN}┼────┼────┼────┼────┼────┼────┼────┼────┼{RESET_COLOR}
 C {BACK_GREEN}│{b[2][0]}│{b[2][1]}│{b[2][2]}│{b[2][3]}│{b[2][4]}│{b[2][5]}│{b[2][6]}│{b[2][7]}│{RESET_COLOR} C
   {BACK_GREEN}┼────┼────┼────┼────┼────┼────┼────┼────┼{RESET_COLOR}
 D {BACK_GREEN}│{b[3][0]}│{b[3][1]}│{b[3][2]}│{b[3][3]}│{b[3][4]}│{b[3][5]}│{b[3][6]}│{b[3][7]}│{RESET_COLOR} D
   {BACK_GREEN}┼────┼────┼────┼────┼────┼────┼────┼────┼{RESET_COLOR}
 E {BACK_GREEN}│{b[4][0]}│{b[4][1]}│{b[4][2]}│{b[4][3]}│{b[4][4]}│{b[4][5]}│{b[4][6]}│{b[4][7]}│{RESET_COLOR} E
   {BACK_GREEN}┼────┼────┼────┼────┼────┼────┼────┼────┼{RESET_COLOR}
 F {BACK_GREEN}│{b[5][0]}│{b[5][1]}│{b[5][2]}│{b[5][3]}│{b[5][4]}│{b[5][5]}│{b[5][6]}│{b[5][7]}│{RESET_COLOR} F
   {BACK_GREEN}┼────┼────┼────┼────┼────┼────┼────┼────┼{RESET_COLOR}
 G {BACK_GREEN}│{b[6][0]}│{b[6][1]}│{b[6][2]}│{b[6][3]}│{b[6][4]}│{b[6][5]}│{b[6][6]}│{b[6][7]}│{RESET_COLOR} G
   {BACK_GREEN}┼────┼────┼────┼────┼────┼────┼────┼────┼{RESET_COLOR}
 H {BACK_GREEN}│{b[7][0]}│{b[7][1]}│{b[7][2]}│{b[7][3]}│{b[7][4]}│{b[7][5]}│{b[7][6]}│{b[7][7]}│{RESET_COLOR} H
   {BACK_GREEN}┼────┼────┼────┼────┼────┼────┼────┼────┼{RESET_COLOR}
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

    def get_player_score(self, player):
        score = 0
        for y in range(8):
            for x in range(8):
                if self.board[x][y] == player.color:
                    score += 1
        return score


    def alpha_beta_search(self, player, adversary):
        boardAlgo = Board()
        boardAlgo.board = copy.deepcopy(self.board)
        moves = [(0,0) for _ in range(DEPTH)]
        boardAlgo.max_value(player, adversary, -INFINITY, INFINITY, moves, 0)
        return moves[0]

    def max_value(self, player, adversary, alpha, beta, moves, cmpt):
        if DEBUG: print(cmpt, cmpt*"    ", "Max", player.color, "alpha=", alpha, "beta=", beta)

        # If end of recursion/tree return evaluation function
        if cmpt >= DEPTH or self.is_full() or not self.has_valid_moves(player):
            return self.get_player_score(player)

        # Loops over possibles moves
        for move in self._get_valid_moves(player):
            if DEBUG: print(cmpt, cmpt*"    ", "move:", player.color, move)
            # Play the next turn on a copy of the board
            nextBoard = Board()
            nextBoard.board = copy.deepcopy(self.board)
            nextBoard.put_stone(player, move)
            # Compute recusively the evaluation function (minMax)
            utility = nextBoard.min_value(adversary, player, alpha, beta, moves, cmpt+1)
            if DEBUG: print(cmpt, cmpt * "    ", utility >= beta, ":: utility >= beta ::", utility, ">=", beta)
            if DEBUG: print(cmpt, cmpt * "    ", utility > alpha, ":: utility > alpha ::", utility, ">", alpha)
            # Pruning if utility out of optimal range
            if PRUNING and utility >= beta:
                if DEBUG: print("PRUNING")
                return utility
            # Update range limit if best (affine range)
            elif utility > alpha:
                alpha = utility
                moves[cmpt] = move
        return alpha

    def min_value(self, player, adversary, alpha, beta, moves, cmpt):
        if DEBUG: print(cmpt, cmpt*"    ", "min", player.color, "moves=", moves, "alpha=", alpha, "beta=", beta)

        # If end of recursion/tree return evaluation function
        if cmpt >= DEPTH or self.is_full() or not self.has_valid_moves(player):
            return self.get_player_score(player)

        # Loops over possibles moves
        for move in self._get_valid_moves(player):
            if DEBUG: print(cmpt, cmpt*"    ", "move:", player.color, move)
            # Play the next turn on a copy of the board
            nextBoard = Board()
            nextBoard.board = copy.deepcopy(self.board)
            nextBoard.put_stone(player, move)
            # Compute recusively the evaluation function (minMax)
            utility = nextBoard.max_value(adversary, player, alpha, beta, moves, cmpt+1)
            if DEBUG: print(cmpt, cmpt*"    ", utility <= alpha, ":: utility =< alpha ::", utility, "<=", alpha)
            if DEBUG: print(cmpt, cmpt*"    ", utility < beta, ":: utility < beta ::", utility, "<", beta)
            # Pruning if utility out of optimal range
            if PRUNING and utility <= alpha:
                if DEBUG: print("PRUNING")
                return utility
            # Update range limit if best (affine range)
            elif utility < beta:
                beta = utility
                moves[cmpt] = move
        return beta




    def get_best_next_move_from_josegalarza(self, player):
        """
        Returns best next move for the `player` based on max score.
        TODO: Predicts moves up to `look_head` times.
        TODO: Should care more for strategic positions than just score.
        """
        valid_moves = self._get_valid_moves(player)
        time.sleep(0.25 * (len(valid_moves) + 1))
        random.shuffle(valid_moves)
        best_next_move = None
        max_score = 0
        # Avoid dangerous positions
        safe_moves = list(filter(lambda move: move not in DANGEROUS_POSITIONS, valid_moves))
        if safe_moves:
            valid_moves = safe_moves
        for move in valid_moves:
            # Get the corners
            if move in CORNER_POSITIONS:
                return move
            # Get to the walls
            elif 0 in move:
                return move
            # Get max flip
            else:
                tmp_board = Board()
                tmp_board.board = copy.deepcopy(self.board)  # copy this board
                tmp_board.put_stone(player, move)
                score = tmp_board.get_player_score(player)
                if score > max_score:
                    max_score = score
                    best_next_move = move
        return best_next_move

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
    def __init__(self, color, is_bot=0, level=0):
        self.color = color
        self.is_bot = is_bot
        self.level = level

    def inversePlayer(self, players):
        if self == players[0]:
            return players[1]
        else :
            return players[0]


    def bot_move(self, board, players):
        if self.level == IA_JOSEGALARZE:
            print("josegalarze")
            return board.get_best_next_move_from_josegalarza(self)
        elif self.level == RANDOM:
            print("random")
            return board.get_random_move(self)
        elif self.level == MINMAX:
            print("minmax")
            return board.alpha_beta_search(self, self.inversePlayer(players))
        else:
            raise("Error: Invalid IA level !")

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
    def __init__(self):
        self.board = Board()
        self.players = [Player(BLACK), Player(WHITE)]

    def _print(self):
        """
        Prints the game: the header, notification(s) (if any) and the board
        """
        os.system("cls") # todo operating system dependent
        header = "Reversi • By @josegalarza (2020)"
        p0 = self.players[0]
        p1 = self.players[1]
        p0_score = f"{p0.color}{'%2d' % self.board.get_player_score(p0)}"
        p1_score = f"{p1.color}{'%2d' % self.board.get_player_score(p1)}"
        render = f"""{header}
Score: {p0_score} vs. {p1_score}
{self.board}
"""
        print(render)

    def play(self):
        for player in cycle(self.players):
            self._print()
            if self.board.is_full() or self.board.has_dominated(player):
                break
            if self.board.has_valid_moves(player):
                while True:
                    try:
                        if not player.is_bot:
                            move = player.get_move()
                        else:
                            print(f"Player {player.color} is thinking...")
                            move = player.bot_move(self.board, self.players)
                        if type(move) is tuple:
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
        self._print()

    def start(self):
        while True:
            try:
                self._print()
                players = input("Number of players (0-2)? ").strip()
                if players in ["0", "1", "2"]:
                    break
            except KeyboardInterrupt:
                sys.exit(1)
            except Exception:
                pass
        if players != "2":
            print(f"Levels of IA\n "
                  f"{IA_JOSEGALARZE} : IA_from_josegalarza\n"
                  f"{RANDOM} : Random\n"
                  f"{MINMAX} : MinMax\n")
            for i in range(2-int(players)):
                while True:
                    try:
                        lvl = input(f"Level of IA_{i+1} : ").strip()
                        if lvl in [str(IA_JOSEGALARZE), str(RANDOM), str(MINMAX)]:
                            break
                    except KeyboardInterrupt:
                        sys.exit(1)
                    except Exception:
                        pass
                self.players[i-1].is_bot = True
                self.players[i-1].level = int(lvl)
        self.play()


if __name__ == '__main__':
    game = Game()
    game.start()