import pygame, sys

# Constants
WINDOW_SIZE = 800
SQUARE_SIZE = WINDOW_SIZE // 8
BLACK, WHITE = (0, 0, 0), (255, 255, 255)
SQUARE_COLOUR_1, SQUARE_COLOUR_2 = (169, 160, 153), (96, 76, 59)
HIGHLIGHT_COLOR = (0, 255, 0)  
FONT_COLOR = (255, 255, 255)
BG_COLOR = (50, 50, 50)  

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Chess")
font = pygame.font.SysFont(None, 72)
button_font = pygame.font.SysFont(None, 48)

# Load piece images
def load_images():
    pieces = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
    images = {}
    for piece in pieces:
        images[piece] = {
            'white': pygame.transform.scale(pygame.image.load(f'assets/w_{piece}.png'), (SQUARE_SIZE, SQUARE_SIZE)),
            'black': pygame.transform.scale(pygame.image.load(f'assets/b_{piece}.png'), (SQUARE_SIZE, SQUARE_SIZE))
        }
    return images

IMAGES = load_images()

# Piece class
class Piece:
    def __init__(self, name, colour, pos):
        self.name = name
        self.colour = colour
        self.pos = pos
        self.img = IMAGES[name][colour]

    def move(self, new_pos):
        self.pos = new_pos

# Board class
class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.init_board()

    def init_board(self):
        for i in range(8):
            self.board[1][i] = Piece('pawn', 'black', (1, i))
            self.board[6][i] = Piece('pawn', 'white', (6, i))
        pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
        for i, piece in enumerate(pieces):
            self.board[0][i] = Piece(piece, 'black', (0, i))
            self.board[7][i] = Piece(piece, 'white', (7, i))

    def draw(self, window):
        for row in range(8):
            for col in range(8):
                color = SQUARE_COLOUR_1 if (row + col) % 2 == 0 else SQUARE_COLOUR_2
                pygame.draw.rect(window, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

                piece = self.board[row][col]
                if piece:
                    window.blit(piece.img, (col * SQUARE_SIZE, row * SQUARE_SIZE))

    def move_piece(self, start_pos, end_pos):
        piece = self.board[start_pos[0]][start_pos[1]]
        if piece:
            piece.move(end_pos)
            self.board[end_pos[0]][end_pos[1]] = piece
            self.board[start_pos[0]][start_pos[1]] = None

    def is_empty(self, pos):
        return self.board[pos[0]][pos[1]] is None

    def is_enemy(self, pos, colour):
        piece = self.board[pos[0]][pos[1]]
        return piece and piece.colour != colour

    def get_king(self, colour):
        for row in self.board:
            for piece in row:
                if piece and piece.name == 'king' and piece.colour == colour:
                    return piece
        return None

# Game class
class Game:
    def __init__(self):
        self.board = Board()
        self.selected_piece = None
        self.turn = 'white'
        self.valid_moves = []
        self.menu_active = False  # Track whether the menu is active
        self.king_captured = False  # Track if the king is captured

    def reset(self):
        self.board = Board()
        self.selected_piece = None
        self.turn = 'white'
        self.valid_moves = []
        self.king_captured = False  # Reset king captured status

    def get_valid_moves(self, piece):
        # Returns a list of valid moves for the selected piece
        if not piece:
            return []
        moves = []
        row, col = piece.pos

        if piece.name == 'pawn':
            direction = -1 if piece.colour == 'white' else 1
            start_row = 6 if piece.colour == 'white' else 1
            # Move forward one square
            if self.board.is_empty((row + direction, col)):
                moves.append((row + direction, col))
            # Capture diagonally
            if col > 0 and self.board.is_enemy((row + direction, col - 1), piece.colour):
                moves.append((row + direction, col - 1))
            if col < 7 and self.board.is_enemy((row + direction, col + 1), piece.colour):
                moves.append((row + direction, col + 1))
        
        elif piece.name == 'rook':
            moves = self.get_straight_line_moves(piece.pos)
        elif piece.name == 'bishop':
            moves = self.get_diagonal_moves(piece.pos)
        elif piece.name == 'queen':
            moves = self.get_straight_line_moves(piece.pos) + self.get_diagonal_moves(piece.pos)
        elif piece.name == 'knight':
            moves = self.get_knight_moves(piece.pos)
        elif piece.name == 'king':
            moves = self.get_king_moves(piece.pos)

        return moves

    def get_straight_line_moves(self, pos):
        # Returns valid moves in straight lines (for rook and queen)
        row, col = pos
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8 and self.board.is_empty((r, c)):
                moves.append((r, c))
                r += dr
                c += dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board.is_enemy((r, c), self.turn):
                moves.append((r, c))
        return moves

    def get_diagonal_moves(self, pos):
        #Returns valid moves in diagonals (for bishop and queen)
        row, col = pos
        moves = []
        directions = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8 and self.board.is_empty((r, c)):
                moves.append((r, c))
                r += dr
                c += dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board.is_enemy((r, c), self.turn):
                moves.append((r, c))
        return moves

    def get_knight_moves(self, pos):
        # Returns valid moves for a knight
        row, col = pos
        moves = []
        potential_moves = [(row + 2, col + 1), (row + 2, col - 1), (row - 2, col + 1), (row - 2, col - 1),
                           (row + 1, col + 2), (row + 1, col - 2), (row - 1, col + 2), (row - 1, col - 2)]
        for r, c in potential_moves:
            if 0 <= r < 8 and 0 <= c < 8 and (self.board.is_empty((r, c)) or self.board.is_enemy((r, c), self.turn)):
                moves.append((r, c))
        return moves

    def get_king_moves(self, pos):
        # Returns valid moves for a king
        row, col = pos
        moves = []
        potential_moves = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1),
                           (row + 1, col + 1), (row - 1, col - 1), (row + 1, col - 1), (row - 1, col + 1)]
        for r, c in potential_moves:
            if 0 <= r < 8 and 0 <= c < 8 and (self.board.is_empty((r, c)) or self.board.is_enemy((r, c), self.turn)):
                moves.append((r, c))
        return moves

    def is_valid_move(self, start_pos, end_pos):
        """Check if the move is valid"""
        piece = self.board.board[start_pos[0]][start_pos[1]]
        return end_pos in self.get_valid_moves(piece)

    def handle_click(self, pos):
        row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE
        piece = self.board.board[row][col]

        if self.selected_piece:
            if self.is_valid_move(self.selected_piece.pos, (row, col)):
                self.board.move_piece(self.selected_piece.pos, (row, col))
                # Check if king is captured
                if piece and piece.name == 'king':
                    self.king_captured = True
                self.selected_piece = None
                self.turn = 'black' if self.turn == 'white' else 'white'
                self.valid_moves = []
            else:
                self.selected_piece = None
                self.valid_moves = []
        elif piece and piece.colour == self.turn:
            self.selected_piece = piece
            self.valid_moves = self.get_valid_moves(piece)

    def draw(self, window):
        self.board.draw(window)
        # Highlight valid moves
        for move in self.valid_moves:
            pygame.draw.rect(window, HIGHLIGHT_COLOR, (move[1] * SQUARE_SIZE, move[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)
        if self.selected_piece:
            row, col = self.selected_piece.pos
            pygame.draw.rect(window, (0, 255, 0), (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)
        if self.king_captured:
            self.show_restart_button(window)

    def show_restart_button(self, window):
        restart_button = button_font.render('Restart', True, FONT_COLOR)
        restart_rect = restart_button.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
        window.blit(restart_button, restart_rect)

        return restart_rect

# Menu 
def menu():
    """Display the menu."""
    window.fill(BG_COLOR)  # Sets the background color

    # Creates the game title
    title = font.render('CHESS', True, FONT_COLOR)
    title_rect = title.get_rect(midtop=(WINDOW_SIZE // 2, 100))
    window.blit(title, title_rect)

    # Create buttons
    rstart_button = button_font.render('Restart', True, FONT_COLOR)
    rstart_button_rect = rstart_button.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 - 20))
    window.blit(rstart_button, rstart_button_rect)

    quit_button = button_font.render('Quit', True, FONT_COLOR)
    quit_button_rect = quit_button.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 + 20))
    window.blit(quit_button, quit_button_rect)

    return rstart_button_rect, quit_button_rect

# Main loop
game = Game()
running = True
while running:
    if game.menu_active:
        rstart_button_rect, quit_button_rect = menu()
    else:
        game.draw(window)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game.menu_active = not game.menu_active  # Toggle menu visibility

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            if game.menu_active:
                # Check if the play button is clicked
                if rstart_button_rect.collidepoint(mouse_position):
                    game.reset()
                    game.menu_active = False  # Exit menu and start game
                # Check if the quit button is clicked
                elif quit_button_rect.collidepoint(mouse_position):
                    running = False
            else:
                if game.king_captured:
                    restart_rect = game.show_restart_button(window)
                    if restart_rect.collidepoint(mouse_position):
                        game.reset()  # Restart the game
                else:
                    game.handle_click(mouse_position)

    pygame.display.update()

pygame.quit()
sys.exit()
