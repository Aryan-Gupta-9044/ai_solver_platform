from typing import List, Tuple, Optional
import numpy as np

class TicTacToeGame:
    def __init__(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.current_player = 1  # 1 for X, -1 for O
        self.game_over = False
        self.winner = None
        
    def make_move(self, position: Tuple[int, int]) -> Dict:
        """Make a move at the specified position"""
        row, col = position
        
        if self.game_over:
            return {
                'status': 'error',
                'message': 'Game is already over'
            }
            
        if not (0 <= row < 3 and 0 <= col < 3):
            return {
                'status': 'error',
                'message': 'Invalid position'
            }
            
        if self.board[row, col] != 0:
            return {
                'status': 'error',
                'message': 'Position already taken'
            }
            
        # Make the move
        self.board[row, col] = self.current_player
        
        # Check for win
        if self._check_win():
            self.game_over = True
            self.winner = self.current_player
            return {
                'status': 'success',
                'board': self.board.tolist(),
                'game_over': True,
                'winner': 'X' if self.current_player == 1 else 'O'
            }
            
        # Check for draw
        if np.all(self.board != 0):
            self.game_over = True
            return {
                'status': 'success',
                'board': self.board.tolist(),
                'game_over': True,
                'winner': 'Draw'
            }
            
        # Switch players
        self.current_player *= -1
        
        return {
            'status': 'success',
            'board': self.board.tolist(),
            'game_over': False,
            'current_player': 'X' if self.current_player == 1 else 'O'
        }
        
    def _check_win(self) -> bool:
        """Check if the current player has won"""
        # Check rows
        for row in range(3):
            if np.all(self.board[row] == self.current_player):
                return True
                
        # Check columns
        for col in range(3):
            if np.all(self.board[:, col] == self.current_player):
                return True
                
        # Check diagonals
        if np.all(np.diag(self.board) == self.current_player):
            return True
        if np.all(np.diag(np.fliplr(self.board)) == self.current_player):
            return True
            
        return False

class MinimaxSolver:
    def __init__(self, game: TicTacToeGame):
        self.game = game
        
    def get_best_move(self) -> Tuple[int, int]:
        """Get the best move using minimax algorithm"""
        best_score = float('-inf')
        best_move = None
        
        for row in range(3):
            for col in range(3):
                if self.game.board[row, col] == 0:
                    # Try the move
                    self.game.board[row, col] = self.game.current_player
                    score = self._minimax(False)
                    self.game.board[row, col] = 0  # Undo the move
                    
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
                        
        return best_move
        
    def _minimax(self, is_maximizing: bool) -> int:
        """Minimax algorithm implementation"""
        # Check for terminal states
        if self._check_win(1):  # X wins
            return 1
        if self._check_win(-1):  # O wins
            return -1
        if np.all(self.game.board != 0):  # Draw
            return 0
            
        if is_maximizing:
            best_score = float('-inf')
            for row in range(3):
                for col in range(3):
                    if self.game.board[row, col] == 0:
                        self.game.board[row, col] = 1
                        score = self._minimax(False)
                        self.game.board[row, col] = 0
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for row in range(3):
                for col in range(3):
                    if self.game.board[row, col] == 0:
                        self.game.board[row, col] = -1
                        score = self._minimax(True)
                        self.game.board[row, col] = 0
                        best_score = min(score, best_score)
            return best_score
            
    def _check_win(self, player: int) -> bool:
        """Check if the specified player has won"""
        # Check rows
        for row in range(3):
            if np.all(self.game.board[row] == player):
                return True
                
        # Check columns
        for col in range(3):
            if np.all(self.game.board[:, col] == player):
                return True
                
        # Check diagonals
        if np.all(np.diag(self.game.board) == player):
            return True
        if np.all(np.diag(np.fliplr(self.game.board)) == player):
            return True
            
        return False 