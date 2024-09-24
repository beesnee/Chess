import unittest
import pygame
from main import Piece, Board, Game

class TestChessGame(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.game = Game()  # Initialize the Game class
        self.board = self.game.board  # Access the Board instance

    def tearDown(self):
        pygame.quit()

    def test_piece_initialization(self):
        # Test that pieces are initialized correctly
        black_pawn = self.board.board[1][0]  # Get black pawn at position (1,0)
        white_pawn = self.board.board[6][0]  # Get white pawn at position (6,0)

        self.assertIsInstance(black_pawn, Piece)
        self.assertEqual(black_pawn.name, 'pawn')
        self.assertEqual(black_pawn.colour, 'black')
        self.assertEqual(black_pawn.pos, (1, 0))

        self.assertIsInstance(white_pawn, Piece)
        self.assertEqual(white_pawn.name, 'pawn')
        self.assertEqual(white_pawn.colour, 'white')
        self.assertEqual(white_pawn.pos, (6, 0))

    def test_initial_board_setup(self):
        # Test the initial setup of the chess board
        self.assertIsNotNone(self.board.board[0][0])  # Rook at (0,0)
        self.assertIsNotNone(self.board.board[0][7])  # Rook at (0,7)
        self.assertIsNotNone(self.board.board[7][0])  # Rook at (7,0)
        self.assertIsNotNone(self.board.board[7][7])  # Rook at (7,7)
        self.assertIsNone(self.board.board[3][3])     # Empty square at (3,3)

    def test_move_piece(self):
        # Test moving a piece
        self.board.move_piece((1, 0), (3, 0))  # Move black pawn from (1, 0) to (3, 0)
        moved_piece = self.board.board[3][0]
        self.assertIsNotNone(moved_piece)
        self.assertEqual(moved_piece.pos, (3, 0))
        self.assertIsNone(self.board.board[1][0])  # Ensure the original position is now empty

    def test_invalid_move(self):
        # Placeholder for testing invalid moves
        # Implement your own logic to prevent invalid moves
        original_position = self.board.board[1][0].pos
        self.board.move_piece(original_position, (4, 0))  # Attempting to move two squares
        self.assertEqual(self.board.board[1][0].pos, original_position)  # The position should remain unchanged

    def test_valid_moves_highlighted(self):
        # Test that valid moves are highlighted (this requires integration with the game loop)
        self.game.handle_click((0, 0))  # Simulate clicking on a piece
        valid_moves = self.game.valid_moves
        self.assertIn((2, 0), valid_moves)  # Check if moving the pawn forward is valid

    def test_restart_game(self):
        # Test the restart functionality
        self.game.reset()
        self.assertIsNone(self.board.board[1][0])  # Black pawn should be back in its original position
        self.assertIsNotNone(self.board.board[0][0])  # Rook should be in its original position

if __name__ == '__main__':
    unittest.main()
