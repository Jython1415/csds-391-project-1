import sys
from EightPuzzle import *

# MAIN
def main():
    commands = getCommands()
    game = EightPuzzle()
    
    for command in commands:
        run(command, game)
    
# Reads the commands from the inputted text file
def getCommands() -> list:
    with open(sys.argv[1], "r") as f:        
        return list(map(lambda i: i.replace("\n", ""), f.readlines()))

# Interprets and runs the input command
def run(command: str, game: EightPuzzle):
    words = command.split(" ")

    if words[0] == "setState":
        setState(words, game)
    elif words[0] == "printState":
        printState(game)
    elif words[0] == "move":
        print("run move")
    elif words[0] == "randomizeState":
        print("run randomizeState")
    elif words[0] == "solve":
        if words[1] == "A-star":
            print("run A-star")
        elif words[1] == "beam":
            print("run beam")
        else:
            print("invalid solve algorithm")
    elif words[0] == "maxNodes":
        print("run maxNodes")
    else:
        print("invalid command")

# setState
def setState(command: list, game: EightPuzzle):
    game.setState(' '.join(command[1:4]))

# printState
def printState(game: EightPuzzle):
    print(game)

if __name__ == "__main__":
    main()