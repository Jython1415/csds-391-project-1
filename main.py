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
    r.seed("hi")
        
    commands = getCommands()
    game = EightPuzzle()
    
    for command in commands:
        game = run(command, game)
    
# Reads the commands from the inputted text file
def getCommands() -> list:
    with open(sys.argv[1], "r") as f:        
        return list(map(lambda i: i.replace("\n", ""), f.readlines()))

# Interprets and runs the input command
def run(rawCommand: str, game: EightPuzzle) -> EightPuzzle:
    command = rawCommand.split(" ")

    if command[0] == "setState":
        setState(command, game)
        return game
    elif command[0] == "printState":
        printState(game)
        return game
    elif command[0] == "move":
        move(command, game)
        return game
    elif command[0] == "randomizeState":
        randomizeState(command, game)
        return game
    elif command[0] == "solve":
        if command[1] == "A-star":
            newGame = aStar(command, game)
            if newGame == None:
                print("no return")
                return game
            else:
                return newGame
        elif command[1] == "beam":
            print("run beam")
            return game
        else:
            print("invalid solve algorithm")
            return game
    elif command[0] == "maxNodes":
        print("run maxNodes")
        return game
    else:
        print("invalid command")
        return game

# setState
def setState(command: list, game: EightPuzzle):
    stateStr = "".join(command[1:4])
    stateList = list()
    for char in stateStr:
        stateList.append(char)
    game.setState(stateList)

# printState
def printState(game: EightPuzzle):
    print(str(game) + " " + str(game.moves))

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
    elif command != []:
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
    game.resetMoves()
    
    for _ in range(n):
        game.move(r.choice(game.getValidMoves()))

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
    
    minH = currentGame.h()
    topMoves = currentGame.moves
    
    while frontier.qsize() != 0:
        currentGame = frontier.get().item
        # print(currentGame.f())
        
        if currentGame.h() < minH:
            minH = currentGame.h()
            # print(f"new min:{minH} {str(currentGame)} {currentGame.moves}")
            
        if currentGame.moves > topMoves:
            topMoves = currentGame.moves
            # print(f"new max:{topMoves} {str(currentGame)} {currentGame.h()}")
        
        if currentGame.isGoal():
            return currentGame
        
        for childGame in expand(currentGame):
            if str(childGame) not in reached:
                reached[str(childGame)] = childGame
                frontier.put(PrioritizedGame(childGame.f(), childGame))
            elif childGame.g() < reached[str(childGame)].g():
                reached[str(childGame)] = childGame
                frontier.put(PrioritizedGame(childGame.f(), childGame))
    
    return None
       
def expand(game: EightPuzzle) -> list:
    
    newGames = []
    
    for move in game.getValidMoves():
        newGame = copy.deepcopy(game)
        newGame.move(move)
        newGame.parent = game
        newGames.append(newGame)
    
    return newGames

if __name__ == "__main__":
    main()