import json


class TicTacToe:
    def __init__(self) -> None:
        # Players
        # Player 1 : X
        # Player 2 : O
        self.winningConditions = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6],
        ]
        self.board = ["" for _ in range(9)]
        self.currentPlayer = "O"
        self.done = False
        self.winner = None

    def __repr__(self) -> dict:
        return {
            "currentPlayer": self.currentPlayer,
            "done": self.done,
            "board": self.board,
            "winner": self.winner,
        }

    def isWinner(self, player) -> bool:
        for condition in self.winningConditions:
            if (
                self.board[condition[0]] == player
                and self.board[condition[1]] == player
                and self.board[condition[2]] == player
            ):
                return True
        else:
            return False

    def makeMove(self, position: int):
        # Check if Position is free
        if not "" in self.board:
            self.done = True
        if position >= 0 and position <= 8 and not self.done:
            if self.board[position] == "":
                self.board[position] = self.currentPlayer
                # Check if someone won with this move
                if self.isWinner(self.currentPlayer):
                    self.done = True
                    self.winner = self.currentPlayer
                else:
                    # Switch Player for next move
                    self.currentPlayer = "O" if self.currentPlayer == "X" else "X"
                return True
        return False
