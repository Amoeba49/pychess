from enum import Enum

Move = dict[tuple[int, int], int]


class Color(Enum):
    WHITE = 0
    BLACK = 1
    NONE = 2


class PieceType(Enum):
    PAWN = 0
    ROOK = 1
    KNIGHT = 2
    BISHOP = 3
    QUEEN = 4
    KING = 5
    NONE = 6


class Piece:
    def __init__(self, board, color: Color = Color.NONE) -> None:
        self.color: Color = color
        self.type: PieceType = PieceType.NONE
        self.symbol: str = ' '
        self.value: int = 0
        self.move_list: Move = {}
        self.board = board
        self.has_moved: bool = False

    def __str__(self) -> str:
        return str(self.color.name) + " " + str(self.type.name)

    def get_pos(self) -> tuple[int, int]:
        for row in self.board.board:
            if self in row:
                return self.board.board.index(row), row.index(self)
        return -1, -1

    def get_move_list(self) -> Move:
        return self.move_list


class Pawn(Piece):
    def __init__(self, board, color: Color) -> None:
        super().__init__(board, color)
        self.type: PieceType = PieceType.PAWN
        self.symbol: str = 'p'
        self.value: int = 1

    def __str__(self) -> str:
        pos: tuple[int, int] = self.get_pos()
        return super().__str__() + " @ " + str(pos)

    def get_move_list(self) -> Move:
        pos: tuple[int, int] = self.get_pos()
        x: int = pos[1]
        y: int = pos[0]
        piece: Piece
        piece_two: Piece
        if self.color == Color.WHITE:
            if y == 1:
                piece = self.board.get(y + 1, x)
                piece_two = self.board.get(y + 2, x)
                if piece.type == PieceType.NONE and piece_two.type == PieceType.NONE:
                    self.move_list[(y + 2, x)] = piece.value
            if y < 7:
                piece = self.board.get(y + 1, x)
                if piece.type == PieceType.NONE:
                    self.move_list[(y + 1, x)] = piece.value
            if y < 7 and x < 7:
                piece = self.board.get(y + 1, x + 1)
                if piece.type != PieceType.NONE and piece.color != self.color:
                    self.move_list[(y + 1, x + 1)] = piece.value
            if y < 7 and x > 0:
                piece = self.board.get(y + 1, x - 1)
                if piece.type != PieceType.NONE and piece.color != self.color:
                    self.move_list[(y + 1, x - 1)] = piece.value

        elif self.color == Color.BLACK:
            if y == 6:
                piece = self.board.get(y - 1, x)
                piece_two = self.board.get(y - 2, x)
                if piece.type == PieceType.NONE and piece_two.type == PieceType.NONE:
                    self.move_list[(y - 2, x)] = piece.value
            if y > 0:
                piece = self.board.get(y - 1, x)
                if piece.type == PieceType.NONE:
                    self.move_list[(y - 1, x)] = piece.value
            if y > 0 and x > 7:
                piece = self.board.get(y - 1, x + 1)
                if piece.type != PieceType.NONE and piece.color != self.color:
                    self.move_list[(y - 1, x + 1)] = piece.value
            if y > 0 and x > 0:
                piece = self.board.get(y - 1, x - 1)
                if piece.type != PieceType.NONE and piece.color != self.color:
                    self.move_list[(y - 1, x - 1)] = piece.value
        return self.move_list


class King(Piece):
    def __init__(self, board, color: Color) -> None:
        super().__init__(board, color)
        self.type: PieceType = PieceType.KING
        self.symbol: str = 'K'
        self.value: int = 1000000

    def __str__(self) -> str:
        pos: tuple[int, int] = self.get_pos()
        return super().__str__() + " @ " + str(pos)

    def get_move_list(self) -> Move:
        pos: tuple[int, int] = self.get_pos()
        x = pos[1]
        y = pos[0]
        piece: Piece
        piece_two: Piece
        piece_three: Piece
        piece_four: Piece
        if not self.has_moved:
            piece = self.board.get(y, x + 1)
            piece_two = self.board.get(y, x + 2)
            piece_three = self.board.get(y, x + 3)
            if piece.type == PieceType.NONE and piece_two.type == PieceType.NONE:
                if piece_three.type == PieceType.ROOK and piece_three.has_moved is False:
                    self.move_list[(y, x + 2)] = piece.value
            piece = self.board.get(y, x - 1)
            piece_two = self.board.get(y, x - 2)
            piece_three = self.board.get(y, x - 3)
            piece_four = self.board.get(y, x - 4)
            if piece.type == PieceType.NONE and piece_two.type == PieceType.NONE \
                    and piece_three.type == PieceType.NONE:
                if piece_four.type == PieceType.ROOK and piece_four.has_moved is False:
                    self.move_list[(y, x - 2)] = piece.value
        if y < 7:
            piece = self.board.get(y + 1, x)
            if piece.color != self.color:
                self.move_list[(y + 1, x)] = piece.value
        if y < 7 and x < 7:
            piece = self.board.get(y + 1, x + 1)
            if piece.color != self.color:
                self.move_list[(y + 1, x + 1)] = piece.value
            piece = self.board.get(y, x + 1)
            if piece.color != self.color:
                self.move_list[(y, x + 1)] = piece.value
        if y < 7 and x > 0:
            piece = self.board.get(y + 1, x - 1)
            if piece.color != self.color:
                self.move_list[(y + 1, x - 1)] = piece.value
            piece = self.board.get(y, x - 1)
            if piece.color != self.color:
                self.move_list[(y, x - 1)] = piece.value
        if y > 0:
            piece = self.board.get(y - 1, x)
            if piece.color != self.color:
                self.move_list[(y - 1, x)] = piece.value
        if y > 0 and x < 7:
            piece = self.board.get(y - 1, x + 1)
            if piece.color != self.color:
                self.move_list[(y - 1, x + 1)] = piece.value
        if y > 0 and x > 0:
            piece = self.board.get(y - 1, x - 1)
            if piece.color != self.color:
                self.move_list[(y - 1, x - 1)] = piece.value
        return self.move_list


class Queen(Piece):
    def __init__(self, board, color: Color) -> None:
        super().__init__(board, color)
        self.type: PieceType = PieceType.QUEEN
        self.symbol: str = 'Q'
        self.value: int = 9

    def __str__(self) -> str:
        pos: tuple[int, int] = self.get_pos()
        return super().__str__() + " @ " + str(pos)

    def get_move_list(self) -> Move:
        pos: tuple[int, int] = self.get_pos()
        x: int = pos[1]
        y: int = pos[0]
        i: int = 1
        piece: Piece
        while y + i < 8 and x + i < 8:
            piece = self.board.get(y + i, x + i)
            if piece.color == Color.NONE:
                self.move_list[(y + i, x + i)] = piece.value
                i += 1
            elif piece.color != self.color and piece.color != Color.NONE:
                self.move_list[(y + i, x + i)] = piece.value
                break
            else:
                break
        i = 1
        while y + i < 8 and x - i >= 0:
            piece = self.board.get(y + i, x - i)
            if piece.color != self.color:
                self.move_list[(y + i, x - i)] = piece.value
                i += 1
            elif piece.color != self.color and piece.color != Color.NONE:
                self.move_list[(y + i, x - i)] = piece.value
                break
            else:
                break
        i = 1
        while y - i >= 0 and x + i < 8:
            piece = self.board.get(y - i, x + i)
            if piece.color != self.color:
                self.move_list[(y - i, x + i)] = piece.value
                i += 1
            elif piece.color != self.color and piece.color != Color.NONE:
                self.move_list[(y - i, x + i)] = piece.value
                break
            else:
                break
        i = 1
        while y - i >= 0 and x - i >= 0:
            piece = self.board.get(y - i, x - i)
            if piece.color != self.color:
                self.move_list[(y - i, x - i)] = piece.value
                i += 1
            elif piece.color != self.color and piece.color != Color.NONE:
                self.move_list[(y - i, x - i)] = piece.value
                break
            else:
                break
        i = 1
        while y + i < 8:
            piece = self.board.get(y + i, x)
            if piece.color == Color.NONE:
                self.move_list[(y + i, x)] = piece.value
                i += 1
            elif piece.color != self.color and piece.color != Color.NONE:
                self.move_list[(y + i, x)] = piece.value
                break
            else:
                break
        i = 1
        while y - i >= 0:
            piece = self.board.get(y - i, x)
            if piece.color == Color.NONE:
                self.move_list[(y - i, x)] = piece.value
                i += 1
            elif piece.color != self.color and piece.color != Color.NONE:
                self.move_list[(y - i, x)] = piece.value
                break
            else:
                break
        i = 1
        while x + i < 8:
            piece = self.board.get(y, x + i)
            if piece.color == Color.NONE:
                self.move_list[(y, x + i)] = piece.value
                i += 1
            elif piece.color != self.color and piece.color != Color.NONE:
                self.move_list[(y, x + i)] = piece.value
                break
            else:
                break
        i = 1
        while x - i >= 0:
            piece = self.board.get(y, x - i)
            if piece.color == Color.NONE:
                self.move_list[(y, x - i)] = piece.value
                i += 1
            elif piece.color != self.color and piece.color != Color.NONE:
                self.move_list[(y, x - i)] = piece.value
                break
            else:
                break
        return self.move_list


class Rook(Piece):
    def __init__(self, board, color: Color) -> None:
        super().__init__(board, color)
        self.type: PieceType = PieceType.ROOK
        self.symbol: str = 'r'
        self.value: int = 5

    def __str__(self) -> str:
        pos: tuple[int, int] = self.get_pos()
        return super().__str__() + " @ " + str(pos)

    def get_move_list(self) -> Move:
        pos: tuple[int, int] = self.get_pos()
        x: int = pos[1]
        y: int = pos[0]
        i: int = 1
        piece: Piece
        while y + i < 8:
            piece = self.board.get(y + i, x)
            if piece.color == Color.NONE:
                self.move_list[(y + i, x)] = piece.value
                i += 1
            elif piece.color != self.color and piece.color != Color.NONE:
                self.move_list[(y + i, x)] = piece.value
                break
            else:
                break
        i = 1
        while y - i >= 0:
            piece = self.board.get(y - i, x)
            if piece.color == Color.NONE:
                self.move_list[(y - i, x)] = piece.value
                i += 1
            elif piece.color != self.color and piece.color != Color.NONE:
                self.move_list[(y - i, x)] = piece.value
                break
            else:
                break
        i = 1
        while x + i < 8:
            piece = self.board.get(y, x + i)
            if piece.color == Color.NONE:
                self.move_list[(y, x + i)] = piece.value
                i += 1
            elif piece.color != self.color and piece.color != Color.NONE:
                self.move_list[(y, x + i)] = piece.value
                break
            else:
                break
        i = 1
        while x - i >= 0:
            piece = self.board.get(y, x - i)
            if piece.color == Color.NONE:
                self.move_list[(y, x - i)] = piece.value
                i += 1
            elif piece.color != self.color and piece.color != Color.NONE:
                self.move_list[(y, x - i)] = piece.value
                break
            else:
                break
        return self.move_list


class Knight(Piece):
    def __init__(self, board, color: Color) -> None:
        super().__init__(board, color)
        self.type: PieceType = PieceType.KNIGHT
        self.symbol: str = 'k'
        self.value: int = 3

    def __str__(self) -> str:
        pos: tuple[int, int] = self.get_pos()
        return super().__str__() + " @ " + str(pos)

    def get_move_list(self) -> Move:
        pos: tuple[int, int] = self.get_pos()
        x: int = pos[1]
        y: int = pos[0]
        piece: Piece
        if y > 0 and x > 1:
            piece = self.board.get(y - 1, x - 2)
            if piece.color != self.color:
                self.move_list[(y - 1, x - 2)] = piece.value
        if y > 0 and x < 6:
            piece = self.board.get(y - 1, x + 2)
            if piece.color != self.color:
                self.move_list[(y - 1, x + 2)] = piece.value
        if y > 1 and x > 0:
            piece = self.board.get(y - 2, x - 1)
            if piece.color != self.color:
                self.move_list[(y - 2, x - 1)] = piece.value
        if y > 1 and x < 7:
            piece = self.board.get(y - 2, x + 1)
            if piece.color != self.color:
                self.move_list[(y - 2, x + 1)] = piece.value
        if y < 6 and x > 0:
            piece = self.board.get(y + 2, x - 1)
            if piece.color != self.color:
                self.move_list[(y + 2, x - 1)] = piece.value
        if y < 6 and x < 7:
            piece = self.board.get(y + 2, x + 1)
            if piece.color != self.color:
                self.move_list[(y + 2, x + 1)] = piece.value
        if y < 7 and x > 1:
            piece = self.board.get(y + 1, x - 2)
            if piece.color != self.color:
                self.move_list[(y + 1, x - 2)] = piece.value
        if y < 7 and x < 6:
            piece = self.board.get(y + 1, x + 2)
            if piece.color != self.color:
                self.move_list[(y + 1, x + 2)] = piece.value
        return self.move_list


class Bishop(Piece):
    def __init__(self, board, color: Color) -> None:
        super().__init__(board, color)
        self.type: PieceType = PieceType.BISHOP
        self.symbol: str = 'b'
        self.value: int = 3

    def __str__(self) -> str:
        pos: tuple[int, int] = self.get_pos()
        return super().__str__() + " @ " + str(pos)

    def get_move_list(self) -> Move:
        pos: tuple[int, int] = self.get_pos()
        x: int = pos[1]
        y: int = pos[0]
        i: int = 1
        piece: Piece
        while y + i < 8 and x + i < 8:
            piece = self.board.get(y + i, x + i)
            if piece.color == Color.NONE:
                self.move_list[(y + i, x + i)] = piece.value
                i += 1
            elif piece.color != self.color and piece.color != Color.NONE:
                self.move_list[(y + i, x + i)] = piece.value
                break
            else:
                break
        i = 1
        while y + i < 8 and x - i >= 0:
            piece = self.board.get(y + i, x - i)
            if piece.color != self.color:
                self.move_list[(y + i, x - i)] = piece.value
                i += 1
            elif piece.color != self.color and piece.color != Color.NONE:
                self.move_list[(y + i, x - i)] = piece.value
                break
            else:
                break
        i = 1
        while y - i >= 0 and x + i < 8:
            piece = self.board.get(y - i, x + i)
            if piece.color == Color.NONE:
                self.move_list[(y - i, x + i)] = piece.value
                i += 1
            elif piece.color != self.color and piece.color != Color.NONE:
                self.move_list[(y - i, x + i)] = piece.value
                break
            else:
                break
        i = 1
        while y - i >= 0 and x - i >= 0:
            piece = self.board.get(y - i, x - i)
            if piece.color != self.color:
                self.move_list[(y - i, x - i)] = piece.value
                i += 1
            elif piece.color != self.color and piece.color != Color.NONE:
                self.move_list[(y - i, x - i)] = piece.value
                break
            else:
                break
        return self.move_list
