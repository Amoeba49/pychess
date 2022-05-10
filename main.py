from piece import Color, PieceType
from game import Game, min_max_tree, clear
from tree import *
import random

white_check: bool = False
black_check: bool = False
game_state: bool = True
move_num: int = 0


def reset(game: Game) -> None:
    clear()
    del game
    main()


def game_loop(game: Game) -> None:
    global game_state
    global move_num
    global white_check
    global black_check
    depth: int = 2

    while game_state:
        if move_num % 2 == 0:
            mov: str = input()
            mov = mov.replace(" ", "")
            if mov == "reset":
                reset(game)
            if len(mov) == 2:
                moves: dict = game.get_move_list(int(mov[0]), int(mov[1]))
                print(moves)
                continue
            if len(mov) < 4:
                print("invalid move format")
                game_loop(game)
            if not game.move(int(mov[0]), int(mov[1]), int(mov[2]), int(mov[3])):
                moves: dict = game.get_move_list(int(mov[2]), int(mov[3]))
                for piece_move in moves.keys():
                    piece = game.board.get(piece_move[0], piece_move[1])
                    if piece.type == PieceType.KING:
                        black_check = True
                print(game.board)
                print("black check: " + str(black_check))
                continue
        else:
            # time.sleep(1)
            print("calculating next move")

            tree: MoveTree = MoveTree("root", game)
            move: MoveTree = min_max_tree(Color.BLACK, game, tree, depth)
            best_moves = move.best_move()
            best_move: tuple
            if len(best_moves) > 1:
                best_move = random.choice(best_moves)
            else:
                best_move = best_moves[0]
            game.move(best_move[0][0], best_move[0][1], best_move[1][0], best_move[1][1])
        move_num += 1
    print("game over")


def main() -> None:
    chess: Game = Game()
    game_loop(chess)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
