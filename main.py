import sys
from EightPuzzle import *
import random
import queue
from dataclasses import dataclass, field
from typing import Any
import copy

# Constants
goalState = "b12345678"
r:random.Random = None

# MAIN
def main():
    global r
    r = random.Random()
    r.seed(0)
    
    for i in range(10):
        print(r.randint(1,2))
    
    commands = getCommands()
    game = EightPuzzle()
    
    for command in commands:
        run(command, game)
    
# Reads the commands from the inputted text file
def getCommands() -> list:
    with open(sys.argv[1], "r") as f:        
        return list(map(lambda i: i.replace("\n", ""), f.readlines()))

# Interprets and runs the input command
def run(rawCommand: str, game: EightPuzzle):
    command = rawCommand.split(" ")

    if command[0] == "setState":
        setState(command, game)
    elif command[0] == "printState":
        printState(f"{game} {game.isGoal()}")
    elif command[0] == "move":
        move(command, game)
    elif command[0] == "randomizeState":
        randomizeState(command, game)
    elif command[0] == "solve":
        if command[1] == "A-star":
            game = aStar(command, game)
        elif command[1] == "beam":
            print("run beam")
        else:
            print("invalid solve algorithm")
    elif command[0] == "maxNodes":
        print("run maxNodes")
    else:
        print("invalid command")

# setState
def setState(command: list, game: EightPuzzle):
    game.setState((''.join(command[1:4])))

# printState
def printState(game: EightPuzzle):
    print(game)

# move <direction>
def move(command: list, game: EightPuzzle):
    direction = None
    
    print(command[0])
    
    if command[1] == "right":
        direction = Direction.RIGHT
    elif command[1] == "up":
        direction = Direction.UP
    elif command[1] == "left":
        direction = Direction.LEFT
    elif command[1] == "down":
        direction = Direction.DOWN
    else:
        print(f"invalid direction: {command[1]}")
    
    game.move(direction)

# randomizeState <n>
def randomizeState(command: list, game: EightPuzzle):
    global r
    
    try:
        n = int(command[1])
    except:
        print("Invalid number of moves (not an integer)")
        return
    
    game.setState(goalState)
    
    for _ in range(n):
        game.move(r.choice(list(game.getValidMoves())))

@dataclass(order=True)
class PrioritizedGame:
    priority: int
    item: Any=field(compare=False)

def aStar(command: list, game: EightPuzzle) -> EightPuzzle:
    currentGame: EightPuzzle = game
    currentGame.resetMoves()
    currentGame.heuristic = command[2]
    
    frontier: queue.PriorityQueue = queue.PriorityQueue()
    frontier.put(PrioritizedGame(currentGame.f(), currentGame))
    reached = dict()
    reached[str(currentGame)] = currentGame
    
    while frontier.qsize() != 0:
        currentGame = frontier.get().item
        print()
        
        if currentGame.isGoal():
            return currentGame
        
        for childGame in expand(currentGame):
            if str(childGame) not in reached:
                reached[str(childGame)] = childGame
                frontier.put(PrioritizedGame(childGame.f(), childGame))
            elif childGame.g() < reached[str(childGame)].g():
                reached[str(childGame)] = childGame
                frontier.put(PrioritizedGame(childGame.f(), childGame))
       
def expand(game: EightPuzzle) -> list:
    
    newGames = list()
    
    for move in game.getValidMoves():
        newGame = copy.deepcopy(game)
        newGame.move(move)
        newGame.parent = game
        newGames.append(newGame)
    
    return newGames

if __name__ == "__main__":
    main()