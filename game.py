from piece import Color, PieceType, Piece
from board import Board
from tree import *
import os
import copy


def clear() -> int: return os.system('cls') if os.name == "nt" else os.system('clear')


def min_max_tree(color: Color, game: 'Game', tree: MoveTree, depth: int = 2) -> MoveTree:
    max_value: int = 0
    pieces: list[Piece] = game.board.get_pieces(color)
    for piece in pieces:
        moves: Move = piece.get_move_list()
        for move in moves:
            value: int = moves.get(move)
            max_value = max(max_value, abs(value))
            sub_game: Game = copy.deepcopy(game)
            sub_game.move_spaces(piece.get_pos(), move, False)
            if depth == 0:
                if color == Color.WHITE:
                    tree.add(MoveNode({tuple([piece.get_pos(), move]): value * -1}))
                else:
                    tree.add(MoveNode({tuple([piece.get_pos(), move]): value}))
            else:
                if color == Color.WHITE:
                    tree.add(Node(Tree, min_max_tree(Color.BLACK, sub_game,
                                                     MoveTree(str(tuple([piece.get_pos(), move])), sub_game),
                                                     depth - 1)))
                else:
                    tree.add(Node(Tree, min_max_tree(Color.WHITE, sub_game,
                                                     MoveTree(str(tuple([piece.get_pos(), move])), sub_game),
                                                     depth - 1)))
            # print(move)

    return tree


class Game:
    def __init__(self) -> None:
        self.board: Board = Board()
        print(self)

    def __str__(self) -> str:
        return str(self.board)

    def move(self, init_row: int, init_col: int, mov_row: int, mov_col: int, print_en: bool = True) -> bool:
        if print_en:
            clear()
        piece: Piece = self.board.get(init_row, init_col)
        piece.get_move_list()
        if (mov_row, mov_col) in piece.move_list.keys():
            if piece.type == PieceType.KING:
                rook: Piece
                if mov_col == 2:
                    rook = self.board.get(mov_row, mov_col - 2)
                    self.board.board[mov_row][mov_col] = piece
                    self.board.board[mov_row][mov_col + 1] = rook
                    self.board.board[mov_row][mov_col - 2] = Piece(self.board)
                    self.board.board[init_row][init_col] = Piece(self.board)
                else:
                    rook = self.board.get(mov_row, mov_col + 1)
                    self.board.board[mov_row][mov_col] = piece
                    self.board.board[mov_row][mov_col - 1] = rook
                    self.board.board[mov_row][mov_col + 1] = Piece(self.board)
                    self.board.board[init_row][init_col] = Piece(self.board)
            else:
                self.board.board[mov_row][mov_col] = piece
                self.board.board[init_row][init_col] = Piece(self.board)
            piece.move_list.clear()
            piece.has_moved = True
        else:
            return False
        if print_en:
            print(self)
            print("\33[2K\r", end='')
        return True

    def move_spaces(self, start_pos: tuple[int, int], end_pos: tuple[int, int], print_en: bool = True) -> bool:
        if print_en:
            clear()
        piece: Piece = self.board.get(start_pos[0], start_pos[1])
        piece.get_move_list()
        if (end_pos[0], end_pos[1]) in piece.move_list.keys():
            self.board.board[end_pos[0]][end_pos[1]] = piece
            self.board.board[start_pos[0]][start_pos[1]] = Piece(self.board)
            piece.move_list.clear()
            piece.has_moved = True
        else:
            return False
        if print_en:
            print(self)
            print("\33[2K\r", end='')
        return True

    def get_move_list(self, init_row: int, init_col: int) -> Move:
        piece: Piece = self.board.get(init_row, init_col)
        piece.get_move_list()
        return piece.move_list

    """
    def min_max(self, color: Color, game: 'Game', depth: int = 1, max_depth: int = 2):
        max_score: int = -10000
        best_move: tuple[int, int] = (-1, -1)
        best_piece: list[int] = []

        # print(game)

        pieces: list[Piece] = game.board.get_pieces(color)
        for piece in pieces:
            # print(piece)
            piece_moves: Move = piece.get_move_list()
            pos: list[int] = piece.get_pos()
            for move in piece_moves:
                score: int = game.board.get(move[0], move[1]).value
                if depth > 0:
                    temp_game: 'Game' = copy.deepcopy(game)
                    temp_game.move(pos[0], pos[1], move[0], move[1], False)
                    if color == Color.WHITE:
                        score += self.min_max(Color.BLACK, temp_game, depth, max_depth)
                    else:
                        score -= self.min_max(Color.WHITE, temp_game, depth - 1, max_depth)
                if (depth == max_depth) and (score > max_score):
                    max_score = score
                    best_move = move
                    best_piece = pos
        # print(max_score)
        if depth == max_depth:
            return [best_piece, best_move]
        else:
            return max_score
    """
