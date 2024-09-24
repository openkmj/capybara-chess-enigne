import chess
import random

PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0,
}
BOARD_VALUES = {
    chess.PAWN: [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5, 5, 10, 25, 25, 10, 5, 5],
        [0, 0, 0, 20, 20, 0, 0, 0],
        [5, -5, -10, 0, 0, -10, -5, 5],
        [5, 10, 10, -20, -20, 10, 10, 5],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ],
    chess.KNIGHT: [
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20, 0, 0, 0, 0, -20, -40],
        [-30, 0, 10, 15, 15, 10, 0, -30],
        [-30, 5, 15, 20, 20, 15, 5, -30],
        [-30, 0, 15, 20, 20, 15, 0, -30],
        [-30, 5, 10, 15, 15, 10, 5, -30],
        [-40, -20, 0, 5, 5, 0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50],
    ],
    chess.BISHOP: [
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 10, 10, 5, 0, -10],
        [-10, 5, 5, 10, 10, 5, 5, -10],
        [-10, 0, 10, 10, 10, 10, 0, -10],
        [-10, 10, 10, 10, 10, 10, 10, -10],
        [-10, 5, 0, 0, 0, 0, 5, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20],
    ],
    chess.ROOK: [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [5, 10, 10, 10, 10, 10, 10, 5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [0, 0, 0, 5, 5, 0, 0, 0],
    ],
    chess.QUEEN: [
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 5, 5, 5, 0, -10],
        [-5, 0, 5, 5, 5, 5, 0, -5],
        [0, 0, 5, 5, 5, 5, 0, -5],
        [-10, 5, 5, 5, 5, 5, 0, -10],
        [-10, 0, 5, 0, 0, 0, 0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20],
    ],
    chess.KING: [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ],
}


def evaluate_board(board: chess.Board, depth=0):
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            # black win
            return -10000 - depth
        else:
            # white win
            return 10000 + depth
    if board.is_game_over():
        # draw
        return 0

    board_value = 0
    for square, piece in board.piece_map().items():
        x, y = chess.square_file(square), chess.square_rank(square)
        piece_value = PIECE_VALUES[piece.piece_type]
        if piece.color:
            y = 7 - y
        board_weight = BOARD_VALUES[piece.piece_type][y][x]

        value = piece_value + board_weight / 100
        # value = piece_value
        if piece.color == chess.BLACK:
            value = -value

        board_value += value

    return board_value


def alpha_beta(board: chess.Board, depth, alpha, beta):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board, depth)

    legal_moves = list(board.legal_moves)

    if board.turn:
        for move in legal_moves:
            board.push(move)
            alpha = max(alpha, alpha_beta(board, depth - 1, alpha, beta))
            board.pop()
            if beta <= alpha:
                break
        return alpha
    else:
        for move in legal_moves:
            board.push(move)
            beta = min(beta, alpha_beta(board, depth - 1, alpha, beta))
            board.pop()
            if beta <= alpha:
                break
        return beta


def minimax(board, depth):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    legal_moves = list(board.legal_moves)

    if board.turn:
        best_value = -float("inf")
        for move in legal_moves:
            board.push(move)
            board_value = minimax(board, depth - 1)
            board.pop()
            best_value = max(best_value, board_value)
        return best_value
    else:
        best_value = float("inf")
        for move in legal_moves:
            board.push(move)
            board_value = minimax(board, depth - 1)
            board.pop()
            best_value = min(best_value, board_value)
        return best_value


def select_best_move(board, depth):
    best_moves = []
    best_value = -float("inf") if board.turn else float("inf")

    for move in board.legal_moves:
        board.push(move)
        # board_value = minimax(board, depth)
        board_value = alpha_beta(board, depth, -float("inf"), float("inf"))
        print("Move:", move, "Value:", board_value)
        board.pop()

        if board.turn:
            if board_value > best_value:
                best_value = board_value
                best_moves = [move]
            elif board_value == best_value:
                best_moves.append(move)
        else:
            if board_value < best_value:
                best_value = board_value
                best_moves = [move]
            elif board_value == best_value:
                best_moves.append(move)

    # print("Best value:", best_value)
    if not best_moves:
        return None
    return random.choice(best_moves)


def main():
    game = chess.Board()

    while True:
        args = input().split()
        command = args[0]

        if command == "exit":
            break
        elif command == "uci":
            print("id name CapybaraEngine")
            print("uciok")
        elif command == "isready":
            print("readyok")
        elif command == "position":
            if args[1] == "startpos":
                game = chess.Board()
            elif args[1] == "fen":
                game = chess.Board(fen=" ".join(args[2:]))
                # game = chess.Board(fen=args[2])

        elif command == "go":
            # print(game.legal_moves)
            legal_moves = list(game.legal_moves)
            if not legal_moves:
                print("bestmove (none)")
            else:
                # move = random.choice(legal_moves)
                move = select_best_move(game, 3)
                print("bestmove", move.uci())


if __name__ == "__main__":
    main()
