import logging


class Minimax:
    """
    Program to find the next optimal move for a player based on Minimax algorithm
    Adapted from https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-3-tic-tac-toe-ai-finding-optimal-move
    """

    def __init__(self):
        """
        Initial constructor
        """
        self.player, self.opponent, self.empty = 0, 1, -1
        logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')

    def _is_moves_left(self, board):
        """
        Check if there moves remaining on the board
        :param board: game arena
        :return: true if there are moves remaining on the board. false if there are no moves left to play.
        """
        for i in range(3):
            for j in range(3):
                if board[i][j] == self.empty:
                    return True
        return False

    def _evaluate(self, b):
        """
        Minimax algorithm evaluation function
        https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-2-evaluation-function
        :param b: game arena
        :return: Evaluation value
        """
        # Checking for Rows for X or O victory.
        for row in range(3):
            if b[row][0] == b[row][1] and b[row][1] == b[row][2]:
                if b[row][0] == self.player:
                    return 10
                elif b[row][0] == self.opponent:
                    return -10

        # Checking for Columns for X or O victory.
        for col in range(3):

            if b[0][col] == b[1][col] and b[1][col] == b[2][col]:

                if b[0][col] == self.player:
                    return 10
                elif b[0][col] == self.opponent:
                    return -10

        # Checking for Diagonals for X or O victory.
        if b[0][0] == b[1][1] and b[1][1] == b[2][2]:

            if b[0][0] == self.player:
                return 10
            elif b[0][0] == self.opponent:
                return -10

        if b[0][2] == b[1][1] and b[1][1] == b[2][0]:

            if b[0][2] == self.player:
                return 10
            elif b[0][2] == self.opponent:
                return -10

        # Else if none of them have won then return 0
        return 0

    def _minimax(self, board, depth, isMax):
        """
        Minimax function considers all the possible ways the game can go
        :param board: game arena
        :param depth: tree depth
        :param isMax: Maximizer move or Minimizer move
        :return: the value of the board
        """
        score = self._evaluate(board)

        # If Maximizer has won the game return his/her
        # evaluated score
        if score == 10:
            return score

        # If Minimizer has won the game return his/her
        # evaluated score
        if score == -10:
            return score

        # If there are no more moves and no winner then
        # it is a tie
        if not self._is_moves_left(board):
            return 0

        # If this maximizer's move
        if isMax:
            best = -1000

            # Traverse all cells
            for i in range(3):
                for j in range(3):

                    # Check if cell is empty
                    if board[i][j] == self.empty:
                        # Make the move
                        board[i][j] = self.player

                        # Call minimax recursively and choose
                        # the maximum value
                        best = max(best, self._minimax(board, depth + 1, not isMax))

                        # Undo the move
                        board[i][j] = self.empty
            return best

        # If this minimizer's move
        else:
            best = 1000

            # Traverse all cells
            for i in range(3):
                for j in range(3):

                    # Check if cell is empty
                    if board[i][j] == self.empty:
                        # Make the move
                        board[i][j] = self.opponent

                        # Call minimax recursively and choose
                        # the minimum value
                        best = min(best, self._minimax(board, depth + 1, not isMax))

                        # Undo the move
                        board[i][j] = self.empty
            return best

    def findBestMove(self, board):
        """
        Find the best possible move for the player
        :param board: game arena
        :return: the best possible move for the player
        """
        bestVal = -1000
        bestMove = (-1, -1)

        # Traverse all cells, evaluate minimax function for
        # all empty cells. And return the cell with optimal
        # value.
        for i in range(3):
            for j in range(3):

                # Check if cell is empty
                if board[i][j] == self.empty:

                    # Make the move
                    board[i][j] = self.player

                    # compute evaluation function for this move.
                    moveVal = self._minimax(board, 0, False)

                    # Undo the move
                    board[i][j] = self.empty

                    # If the value of the current move is
                    # more than the best value, then update
                    # best
                    if moveVal > bestVal:
                        bestMove = (i, j)
                        bestVal = moveVal

        logging.info("The value of the best Move is :", bestVal)
        logging.info("The value of the best Move is :", bestMove)
        return bestMove


def main():
    board = [
        [1, 0, 1],
        [0, 0, 1],
        [-1, -1, -1]
    ]

    bestMove = Minimax().findBestMove(board)

    print(f"The Optimal Move is - ROW: {bestMove[0]} COL: {bestMove[1]}")


if __name__ == "__main__":
    main()
