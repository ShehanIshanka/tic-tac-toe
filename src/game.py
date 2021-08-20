import random
import logging

from src.enum import GameState, GameMode
from src.strategy.minimax_algo import Minimax


class Game:
    """
    Class for game functions
    """

    def __init__(self, game_mode, clicked):
        """
        Initial constructor
        :param game_mode: Game mode : EASY, MEDIUM, HARD
        :param clicked: Clicked slot array
        """
        self.game_mode = game_mode
        self.clicked = clicked
        self.minimax = Minimax()
        logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')

    def check_game_state(self):
        """
        Check game state
        :return: game state
        """
        x_winner_string = "111"
        o_winner_string = "000"
        cur_strings = []

        # Checking columns
        for i in range(0, 7, 3):
            cur_strings.append(f"{self.clicked[i]}{self.clicked[i + 1]}{self.clicked[i + 2]}")

        # Checking rows
        for i in range(0, 3):
            cur_strings.append(f"{self.clicked[i]}{self.clicked[i + 3]}{self.clicked[i + 6]}")

        # Checking diagonals
        cur_strings.append(f"{self.clicked[0]}{self.clicked[4]}{self.clicked[8]}")
        cur_strings.append(f"{self.clicked[2]}{self.clicked[4]}{self.clicked[6]}")

        if x_winner_string in cur_strings:
            logging.info("Player X wins")
            return GameState.WIN
        elif o_winner_string in cur_strings:
            logging.info("Player O wins")
            return GameState.LOOSE

        if -1 not in self.clicked:
            logging.info("Game is drawn")
            return GameState.DRAW

        logging.info("Game is still playing")
        return GameState.PLAYING

    def play_opponent(self):
        """
        Decide opponent's move based on the game mode
        :return: opponent's move
        """
        # Decide opponent's move randomly
        if self.game_mode == GameMode.EASY:
            indices = [i for i, x in enumerate(self.clicked) if x == -1]
            if len(indices) != 0:
                return indices[random.randint(0, len(indices)) - 1]
        # Decide opponent's move by attempting to avoid winning or trying to winning yourself
        # Otherwise generate random move
        elif self.game_mode == GameMode.MEDIUM:
            player_x_strings = ["-111", "1-11", "11-1"]
            player_o_strings = ["-100", "0-10", "00-1"]

            # Checking columns
            for i in range(0, 7, 3):
                cur_string = f"{self.clicked[i]}{self.clicked[i + 1]}{self.clicked[i + 2]}"
                if cur_string in player_o_strings:
                    return i + player_o_strings.index(cur_string)
                elif cur_string in player_x_strings:
                    return i + player_x_strings.index(cur_string)

            # Checking rows
            for i in range(0, 3):
                cur_string = f"{self.clicked[i]}{self.clicked[i + 3]}{self.clicked[i + 6]}"
                if cur_string in player_o_strings:
                    return i + player_o_strings.index(cur_string) * 3
                elif cur_string in player_x_strings:
                    return i + player_x_strings.index(cur_string) * 3

            # Checking diagonals
            cur_string = f"{self.clicked[0]}{self.clicked[4]}{self.clicked[8]}"
            if cur_string in player_o_strings:
                return player_o_strings.index(cur_string) * 3 + player_o_strings.index(cur_string)
            elif cur_string in player_x_strings:
                return player_x_strings.index(cur_string) * 3 + player_x_strings.index(cur_string)
            cur_string = f"{self.clicked[2]}{self.clicked[4]}{self.clicked[6]}"
            if cur_string in player_o_strings:
                return (player_o_strings.index(cur_string) + 1) * 2
            elif cur_string in player_x_strings:
                return (player_x_strings.index(cur_string) + 1) * 2

            # Otherwise generate random move
            indices = [i for i, x in enumerate(self.clicked) if x == -1]
            if len(indices) != 0:
                return indices[random.randint(0, len(indices)) - 1]
        # Decide opponent's move from Minimax algorithm
        elif self.game_mode == GameMode.HARD:
            board = []
            for i in range(0, 7, 3):
                board.append(self.clicked[i:i + 3])
            best_move = self.minimax.findBestMove(board=board)
            return best_move[0] * 3 + best_move[1]
