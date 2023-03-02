import sys
from EightPuzzle import *
import random

# Constants
goalState = "b12345678"

# MAIN
def main():
    random.seed(0)
    
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
        printState(game)
    elif command[0] == "move":
        move(command, game)
    elif command[0] == "randomizeState":
        randomizeState(command, game)
    elif command[0] == "solve":
        if command[1] == "A-star":
            print("run A-star")
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
    
    try:
        n = int(command[1])
    except:
        print("Invalid number of moves (not an integer)")
        return
    
    game.setState(goalState)
    
    for _ in range(n):
        game.move(random.choice(list(game.getValidMoves())))
    

if __name__ == "__main__":
    main()