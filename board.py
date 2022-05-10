from piece import *


class Board:
    def __init__(self) -> None:
        self.board: list[list[Piece]] = []

        for i in range(8):
            row: list[Piece] = []
            for j in range(8):
                if i == 0 and (j == 0 or j == 7):
                    row.append(Rook(self, Color.WHITE))
                if i == 0 and (j == 1 or j == 6):
                    row.append(Knight(self, Color.WHITE))
                if i == 0 and (j == 2 or j == 5):
                    row.append(Bishop(self, Color.WHITE))
                if i == 0 and j == 3:
                    row.append(Queen(self, Color.WHITE))
                if i == 0 and j == 4:
                    row.append(King(self, Color.WHITE))
                if i == 1:
                    row.append(Pawn(self, Color.WHITE))

                if i == 6:
                    row.append(Pawn(self, Color.BLACK))
                if i == 7 and (j == 0 or j == 7):
                    row.append(Rook(self, Color.BLACK))
                if i == 7 and (j == 1 or j == 6):
                    row.append(Knight(self, Color.BLACK))
                if i == 7 and (j == 2 or j == 5):
                    row.append(Bishop(self, Color.BLACK))
                if i == 7 and j == 3:
                    row.append(Queen(self, Color.BLACK))
                if i == 7 and j == 4:
                    row.append(King(self, Color.BLACK))
                if 1 < i < 6:
                    row.append(Piece(self))
            self.board.append(row)

    def __str__(self) -> str:
        return_str: str = ""
        i: int = 7
        j: int = 0
        while i >= 0:
            while j < 8:
                bg: int
                fg: int
                space: Piece = self.board[i][j]
                if (i + j) % 2 == 0:
                    bg = 43
                else:
                    bg = 44
                if space.color == Color.WHITE:
                    fg = 37
                else:
                    fg = 30
                str_format: str = ';'.join([str(0), str(fg), str(bg)])
                return_str += '\x1b[%sm %s \x1b[0m' % (str_format, str(space.symbol) + " ")
                j += 1
            return_str += "\n"
            j = 0
            i -= 1
        return return_str

    def get(self, r: int, c: int) -> Piece:
        return self.board[r][c]

    def get_pieces(self, color: Color = Color.NONE) -> list[Piece]:
        pieces: list[Piece] = []
        piece: Piece
        if color == Color.NONE:
            for row in range(8):
                for col in range(8):
                    piece = self.get(row, col)
                    if piece.color != Color.NONE:
                        pieces.append(piece)
        else:
            for row in range(8):
                for col in range(8):
                    piece = self.get(row, col)
                    if piece.color == color:
                        pieces.append(piece)
        return pieces
