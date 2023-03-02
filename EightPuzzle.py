from enum import Enum

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
    
    # Initializer
    def __init__(self):
        self.state = ["b", "1", "2", "3", "4", "5", "6", "7", "8"]
        self.bPos = 0
    
    # Default string representation
    def __str__(self):
        base = ''.join(self.state)
        return base[0:3] + " " + base[3:6] + " " + base[6:9]
    
    # Set state
    def setState(self, newState: str):
        self.state = [i for i in newState]
    
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
        moves = set([Direction.RIGHT, Direction.UP, Direction.LEFT, Direction.DOWN])
        
        if self.bPos == 2 or self.bPos == 5 or self.bPos == 8:
            moves.remove(Direction.RIGHT)
        if self.bPos == 0 or self.bPos == 1 or self.bPos == 2:
            moves.remove(Direction.UP)
        if self.bPos == 0 or self.bPos == 3 or self.bPos == 6:
            moves.remove(Direction.LEFT)
        if self.bPos == 6 or self.bPos == 7 or self.bPos == 8:
            moves.remove(Direction.DOWN)

        return moves
    
    # Move
    def move(self, direction: Direction):
        match direction:
            case Direction.RIGHT:
                match self.bPos:
                    case 0:
                        self.swapSquares(0, 1)
                        self.bPos = 1
                    case 3:
                        self.swapSquares(3, 4)
                        self.bPos = 4
                    case 6:
                        self.swapSquares(6, 7)
                        self.bPos = 7
                    case 1:
                        self.swapSquares(1, 2)
                        self.bPos = 2
                    case 4:
                        self.swapSquares(4, 5)
                        self.bPos = 5
                    case 7:
                        self.swapSquares(6, 7)
                        self.bPos = 7
                    case _:
                        print(f"invalid move: move right on rightmost column. b is {self.bPos}")
            case Direction.UP:
                match self.bPos:
                    case 6:
                        self.swapSquares(6, 3)
                        self.bPos = 3
                    case 7:
                        self.swapSquares(7, 4)
                        self.bPos = 4
                    case 8:
                        self.swapSquares(8, 5)
                        self.bPos = 5
                    case 3:
                        self.swapSquares(3, 0)
                        self.bPos = 0
                    case 4:
                        self.swapSquares(4, 1)
                        self.bPos = 1
                    case 5:
                        self.swapSquares(5, 2)
                        self.bPos = 2
                    case _:
                        print(f"invalid move: move up on top column. b is {self.bPos}")
            case Direction.LEFT:
                match self.bPos:
                    case 2:
                        self.swapSquares(2, 1)
                        self.bPos = 1
                    case 5:
                        self.swapSquares(5, 4)
                        self.bPos = 4
                    case 8:
                        self.swapSquares(8, 7)
                        self.bPos = 7
                    case 1:
                        self.swapSquares(1, 0)
                        self.bPos = 0
                    case 4:
                        self.swapSquares(4, 3)
                        self.bPos = 3
                    case 7:
                        self.swapSquares(7, 6)
                        self.bPos = 6
                    case _:
                        print(f"invalid move: move left on leftmost column. b is {self.bPos}")
            case Direction.DOWN:
                match self.bPos:
                    case 0:
                        self.swapSquares(0, 3)
                        self.bPos = 3
                    case 1:
                        self.swapSquares(1, 4)
                        self.bPos = 4
                    case 2:
                        self.swapSquares(2, 5)
                        self.bPos = 5
                    case 3:
                        self.swapSquares(3, 6)
                        self.bPos = 6
                    case 4:
                        self.swapSquares(4, 7)
                        self.bPos = 7
                    case 5:
                        self.swapSquares(5, 8)
                        self.bPos = 8
                    case _:
                        print(f"invalid move: move left on leftmost column. b is {self.bPos}")
            case _:
                print(f"invalid move: {direction}")