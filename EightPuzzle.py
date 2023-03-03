from enum import Enum
import copy

class Direction(Enum):
    RIGHT = 0
    UP = 1
    LEFT = 3
    DOWN = 4

# Represents an 8-puzzle game
# 012
# 345
# 678


class EightPuzzle():

    goalStateList = ["b", "1", "2", "3", "4", "5", "6", "7", "8"]

    # Initializer
    def __init__(self, heuristic="h1", parent=None):
        self.state = ["b", "1", "2", "3", "4", "5", "6", "7", "8"]
        self.moves = 0
        self.heuristic = heuristic
        self.parent = parent

    # Default string representation
    def __str__(self):
        base = ''.join(self.state)
        return base[0:3] + " " + base[3:6] + " " + base[6:9]

    # bPos
    def getBlankPos(self):
        return self.state.index("b")

    # Set state
    def setState(self, newState: list):
        if type(newState) == str:
            l = list()
            for char in newState:
                l.append(char)
            newState = l
        self.state = copy.copy(newState)

    # Get square
    def getSquare(self, square: int) -> str:
        return self.state[square]

    # Set square
    def setSquare(self, square: int, newSquare: str):
        self.state[square] = newSquare

    # Swap squares
    def swapSquares(self, s1: int, s2: int):
        self.state[s1], self.state[s2] = self.state[s2], self.state[s1]

    # Get valid moves
    def getValidMoves(self) -> set:
        moves = [Direction.RIGHT, Direction.UP,
                    Direction.LEFT, Direction.DOWN]

        if self.getBlankPos() == 2 or self.getBlankPos() == 5 or self.getBlankPos() == 8:
            moves.remove(Direction.RIGHT)
        if self.getBlankPos() == 0 or self.getBlankPos() == 1 or self.getBlankPos() == 2:
            moves.remove(Direction.UP)
        if self.getBlankPos() == 0 or self.getBlankPos() == 3 or self.getBlankPos() == 6:
            moves.remove(Direction.LEFT)
        if self.getBlankPos() == 6 or self.getBlankPos() == 7 or self.getBlankPos() == 8:
            moves.remove(Direction.DOWN)

        return moves

    # Reset moves
    def resetMoves(self):
        self.moves = 0

    # Distance from start position
    def g(self) -> int:
        return self.moves

    # Heuristic 1
    # Number of misplaced tiles
    def h1(self) -> int:
        count = 0
        for (a, b) in zip(self.state, EightPuzzle.goalStateList):
            if a != b:
                count += 1
        return count

    # get current position of a tile
    def getCurrentPos(self, tile: str):
        index = self.state.index(tile)
        return (int(index / 3), index % 3)

    # get the goal position of a tile
    def getGoalPos(tile: str):
        match tile:
            case "b":
                return (0, 0)
            case "1":
                return (0, 1)
            case "2":
                return (0, 2)
            case "3":
                return (1, 0)
            case "4":
                return (1, 1)
            case "5":
                return (1, 2)
            case "6":
                return (2, 0)
            case "7":
                return (2, 1)
            case "8":
                return (2, 2)
            case _:
                print("invalid tile")

    # Heuristic 2
    # Distance of each tile from its goal position
    def h2(self) -> int:
        totalDistance = 0
        for tile in self.state:
            currentPos = self.getCurrentPos(tile)
            goalPos = EightPuzzle.getGoalPos(tile)
            totalDistance += abs(currentPos[0] - goalPos[0]) + abs(currentPos[1] - goalPos[1])
        return totalDistance

    def h(self) -> int:
        if self.heuristic == "h1":
            return self.h1()
        else:
            return self.h2()
    
    # F
    def f(self) -> int:
        return self.g() + self.h()

    # is Goal
    def isGoal(self) -> bool:
        
        # print(self.state)
        # print(EightPuzzle.goalStateList)
        
        for (a, b) in zip(self.state, EightPuzzle.goalStateList):
            if a != b:
                return False
        return True

    # Move
    def move(self, direction: Direction):

        isValid = True

        match direction:
            case Direction.RIGHT:
                match self.getBlankPos():
                    case 0:
                        self.swapSquares(0, 1)
                    case 3:
                        self.swapSquares(3, 4)
                    case 6:
                        self.swapSquares(6, 7)
                    case 1:
                        self.swapSquares(1, 2)
                    case 4:
                        self.swapSquares(4, 5)
                    case 7:
                        self.swapSquares(7, 8)
                    case _:
                        print(
                            f"invalid move: move right on rightmost column. b is {self.getBlankPos()}")
                        isValid = False
            case Direction.UP:
                match self.getBlankPos():
                    case 6:
                        self.swapSquares(6, 3)
                    case 7:
                        self.swapSquares(7, 4)
                    case 8:
                        self.swapSquares(8, 5)
                    case 3:
                        self.swapSquares(3, 0)
                    case 4:
                        self.swapSquares(4, 1)
                    case 5:
                        self.swapSquares(5, 2)
                    case _:
                        print(
                            f"invalid move: move up on top column. b is {self.getBlankPos()}")
                        isValid = False
            case Direction.LEFT:
                match self.getBlankPos():
                    case 2:
                        self.swapSquares(2, 1)
                    case 5:
                        self.swapSquares(5, 4)
                    case 8:
                        self.swapSquares(8, 7)
                    case 1:
                        self.swapSquares(1, 0)
                    case 4:
                        self.swapSquares(4, 3)
                    case 7:
                        self.swapSquares(7, 6)
                    case _:
                        print(
                            f"invalid move: move left on leftmost column. b is {self.getBlankPos()}")
                        isValid = False
            case Direction.DOWN:
                match self.getBlankPos():
                    case 0:
                        self.swapSquares(0, 3)
                    case 1:
                        self.swapSquares(1, 4)
                    case 2:
                        self.swapSquares(2, 5)
                    case 3:
                        self.swapSquares(3, 6)
                    case 4:
                        self.swapSquares(4, 7)
                    case 5:
                        self.swapSquares(5, 8)
                    case _:
                        print(f"invalid move: move left on leftmost column. b is {self.getBlankPos()}")
                        isValid = False
            case _:
                print(f"invalid move: {direction}")
                isValid = False

        if isValid:
            self.moves += 1
        
        # if self.state[self.getBlankPos()] != "b":
            # print(f"invalid bPos: {self.getBlankPos()} {self.state}")
        # else:
            # print("valid move")
