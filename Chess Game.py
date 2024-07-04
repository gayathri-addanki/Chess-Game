import chess
import random

def evaluate_board(board):
    """
    Evaluate the given chess board by summing up the piece values.
    Positive values represent white pieces, and negative values represent black pieces.
    """
    evaluation = 0
    piece_map = board.piece_map()
    for square, piece in piece_map.items():
        if piece.color == chess.WHITE:
            evaluation += piece.piece_type
        else:
            evaluation -= piece.piece_type
    return evaluation

def generate_moves(board):
    """
    Generate all legal moves for the current board position.
    """
    return [move for move in board.legal_moves]

def minimax(board, depth, alpha, beta, maximizing_player):
    """
    Minimax algorithm with alpha-beta pruning to determine the best move for the computer.
    """
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing_player:
        max_eval = float('-inf')
        for move in generate_moves(board):
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in generate_moves(board):
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def play_computer_move(board, difficulty):
    """
    Choose the computer's move based on the selected difficulty level.
    Difficulty 1: Random move
    Difficulty 2: Minimax with depth 2
    Difficulty 3: Minimax with depth 3
    """
    if difficulty == 1:
        return random.choice(list(board.legal_moves))
    elif difficulty in [2, 3]:
        best_move = None
        max_eval = float('-inf')
        depth = 2 if difficulty == 2 else 3
        for move in generate_moves(board):
            board.push(move)
            eval = minimax(board, depth, float('-inf'), float('inf'), False)
            board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return best_move

def print_board(board):
    """
    Print the chess board with coordinates and pieces.
    """
    print('   a b c d e f g h')
    print('  +----------------')
    for i in range(8, 0, -1):
        row = f'{i} |'
        for j in range(1, 9):
            piece = board.piece_at(chess.square(j - 1, i - 1))
            if piece is None:
                row += ' '
            else:
                row += piece.symbol()
            row += '|'
        print(row)
        print('  +----------------')

def play_game():
    """
    Main function to play the chess game.
    """
    board = chess.Board()
    difficulty = int(input("Choose difficulty level (1-3): "))
    
    while not board.is_game_over():
        print_board(board)
        
        # Player's move input
        valid_move = False
        while not valid_move:
            player_move = input("Enter your move (e.g., 'e2e4'): ")
            if chess.Move.from_uci(player_move) in board.legal_moves:
                valid_move = True
            else:
                print("Invalid move. Please try again.")
        board.push(chess.Move.from_uci(player_move))
        
        print_board(board)
        
        # Computer's move
        computer_move = play_computer_move(board, difficulty)
        print(f"Computer's next move: {chess.Move.uci(computer_move)}")
        board.push(computer_move)

    print("Game Over. Result:", board.result())

# Start the game
play_game()
