from typing import Type, Any
from piece import Move
import ast


class Tree:
    def __init__(self, name: str = '') -> None:
        self.node_list: list[Node] = []
        self.name = name

    def __str__(self, indent: str = '') -> str:
        return_str: str = indent + self.name + "\n"
        for node in self.node_list:
            if node.type == Tree:
                return_str += node.object.__str__(indent + "     ")
            else:
                return_str += indent + "     " + str(node)
            return_str += "\n"
        return return_str

    def add(self, node: 'Node') -> None:
        self.node_list.append(node)


class Node:
    def __init__(self, node_type: Type[Any], obj: Any = None) -> None:
        self.type: Type[Any] = node_type
        self.object = obj

    def __str__(self) -> str:
        return str(self.object)

    def obj_set(self, obj: Any) -> None:
        self.object = obj


class MoveTree(Tree):
    def __init__(self, name: str, game) -> None:
        super().__init__(name)
        self.node_list: list[MoveNode] = []
        self.game = game

    def __str__(self, indent: str = '') -> str:
        return_str: str = indent + self.name + " " + str(self.max_value()) + "\n"
        node: MoveNode
        for node in self.node_list:
            if node.type == Tree:
                if node.object.max_value() != 0:
                    return_str += node.object.__str__(indent + "     ")
            elif node.value != 0:
                return_str += indent + "     " + str(node) + "\n"
        return return_str

    def max_value(self) -> int:
        node: MoveNode
        max_value: int = -1
        for node in self.node_list:
            if node.type == Tree:
                if abs(node.object.max_value()) > max_value:
                    max_value = node.object.max_value()
            else:
                if abs(node.value) > max_value:
                    max_value = node.value
        return max_value

    def best_move(self, depth: int = 0) -> list[tuple[tuple[int, int]]]:
        node: MoveNode
        max_value: int = -1
        best_moves: list[tuple[tuple[int, int]]] = [(-1, -1)]
        for node in self.node_list:
            if node.type == Tree:
                if abs(node.object.max_value()) > max_value and depth == 0:
                    max_value = node.object.max_value()
                    best_moves.clear()
                    best_moves.append(tuple(ast.literal_eval(node.object.name)))
                elif abs(node.object.max_value()) == max_value and depth == 0:
                    max_value = node.object.max_value()
                    best_moves.append(tuple(ast.literal_eval(node.object.name)))
            else:
                if abs(node.value) > max_value and depth == 0:
                    max_value = node.value
                    best_moves.clear()
                    best_moves.append(node.move)
                elif abs(node.value) == max_value and depth == 0:
                    max_value = node.value
                    best_moves.append(node.move)
        return best_moves


class MoveNode(Node):
    def __init__(self, move: dict[tuple[tuple[int, int]], int]) -> None:
        super().__init__(Type[Move])
        self.move: tuple[tuple[int, int]] = list(move.keys())[0]
        self.value = move.get(self.move)

    def __str__(self) -> str:
        return str(self.move) + " " + str(self.value)

    def get_value(self):
        return self.value
