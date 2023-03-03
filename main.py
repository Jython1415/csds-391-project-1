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
printResultMessages = False

# Data collecting
aStar1Results = []
aStar2Results = []
# beam1Results = []
beam2Results = []

# MAIN
def main():
    global r
    global aStar1Results
    global aStar2Results
    # global beam1Results 
    global beam2Results 

    r = random.Random()
    r.seed("hi")
        
    commands = getCommands()
    game = EightPuzzle()
    maxNodes = [-1]
    
    print(f"{len(commands)} to run")
    i = 0
    for command in commands:
        if (i % int(len(commands)/1000) == 0):
            print(f"{int((i/len(commands))*1000)/10}% done")
        game = run(command, game, maxNodes)
        i += 1
    
    allResults = []
    allResults.extend(aStar1Results)
    allResults.extend(aStar2Results)
    allResults.extend(beam2Results)
    numberSolved = dict()
    for result in allResults:
        if result[0] == "solved":
            if result[3] in numberSolved:
                numberSolved[result[3]] = numberSolved[result[3]] + 1
            else:
                numberSolved[result[3]] = 1
    for key in numberSolved.keys():
        print(f"{key}, {numberSolved[key]}")

    a1Solved = 0
    a2Solved = 0
    bSolved = 0
    a1Nodes = 0
    a2Nodes = 0
    bNodes = 0
    a1Length = 0
    a2Length = 0
    bLength = 0
    for result in aStar1Results:
        if result[0] == "solved":
            a1Nodes += result[2]
            a1Solved += 1
            a1Length += result[1].getPath()[1]

    for result in aStar2Results:
        if result[0] == "solved":
            a2Nodes += result[2]
            a2Solved += 1
            a2Length += result[1].getPath()[1]
    
    for result in beam2Results:
        if result[0] == "solved":
            bNodes += result[2]
            bSolved += 1
            bLength += result[1].getPath()[1]
           
    print(f"nodesGenerated: {a1Nodes}, {a2Nodes}, {bNodes}")
    print(f"numSolved: {a1Solved}, {a2Solved}, {bSolved}")
    print(f"lengthTotal: {a1Length}, {a2Length}, {bLength}")

    
# Reads the commands from the inputted text file
def getCommands() -> list:
    with open(sys.argv[1], "r") as f:        
        return list(map(lambda i: i.replace("\n", ""), f.readlines()))

# Interprets and runs the input command
def run(rawCommand: str, game: EightPuzzle, maxNodes) -> EightPuzzle:
    global r
    global aStar1Results
    global aStar2Results
    global beam1Results 
    global beam2Results
    
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
        randomizeState(command, game, r)
        return game
    elif command[0] == "solve":
        if command[1] == "A-star":
            result = aStar(command, game, maxNodes[0])
            if command[2] == "h1":
                aStar1Results.append(result)
            else:
                aStar2Results.append(result)
            if result[0] == "solved":
                path = result[1].getPath()
                if printResultMessages:
                    print(f"solved in {path[1]} moves: {path[2]}")
                return result[1]
            elif result[0] == "maxNodes":
                if printResultMessages:
                    print(f"Could not be solved within the node limit: generated {result[2]} nodes")
                return result[1]
            else:
                return game
        elif command[1] == "beam":
            result = beam(command, game, maxNodes[0])
            beam2Results.append(result)
            if result[0] == "solved":
                path = result[1].getPath()
                if printResultMessages:
                    print(f"solved in {path[1]} moves: {path[2]}")
                return result[1]
            elif result[0] == "maxNodes":
                if printResultMessages:
                    print(f"Could not be solved within the node limit: generated {result[2]} nodes")
                return result[1]
            else:
                return game
        else:
            print("invalid solve algorithm")
            return game
    elif command[0] == "maxNodes":
        try:
            maxNodes[0] = int(command[1])
        except:
            print("Invalid input: must be an integer value")
            
        return game
    else:
        print("")
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
    print(str(game))

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
        print(command)
    
    game.move(direction)

# randomizeState <n>
def randomizeState(command: list, game: EightPuzzle, r):    
    try:
        n = int(command[1])
    except:
        if type(command) == int:
            n = command
        else:
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

def aStar(command: list, game: EightPuzzle, maxNodes: int) -> EightPuzzle:
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
        
        if currentGame.h() < minH:
            minH = currentGame.h()
            
        if currentGame.moves > topMoves:
            topMoves = currentGame.moves
        
        if currentGame.isGoal():
            return ("solved", currentGame, len(reached), maxNodes)
        
        for childGame in expand(currentGame):
            if str(childGame) not in reached:
                reached[str(childGame)] = childGame
                frontier.put(PrioritizedGame(childGame.f(), childGame))
            elif childGame.g() < reached[str(childGame)].g():
                reached[str(childGame)] = childGame
                frontier.put(PrioritizedGame(childGame.f(), childGame))
        
        if len(reached) > maxNodes and maxNodes != -1:
            return ("maxNodes", currentGame, len(reached), maxNodes)
    
    return None
       
def expand(game: EightPuzzle) -> list:
    
    newGames = []
    
    for move in game.getValidMoves():
        newGame = copy.deepcopy(game)
        newGame.move(move)
        newGame.parent = game
        newGames.append(newGame)
    
    return newGames

def beam(command: list, game: EightPuzzle, maxNodes: int) -> EightPuzzle:
    try:
        k = int(command[2])
    except:
        print(f"invalid k input {command[2]}")
        return game
    
    currentStates = list()
    game.resetMoves()
    game.heuristic = "h2"
    
    reached = dict()
    reached[str(game)] = game
    
    for _ in range(k):
        currentStates.append(copy.deepcopy(game))
    
    minH = game.h()
    
    while len(currentStates) != 0:
        newStates = bestNeighbors(currentStates, reached, k)
        
        foundNewBestState = False
        for state in newStates:
            if state.h() == 0:
                return ("solved", state, len(reached), maxNodes)
            elif state.h() < minH:
                minH = state.h()
                foundNewBestState = True
        
        currentStates = newStates
        if len(reached) > maxNodes and maxNodes != -1:
            return ("maxNodes", currentStates[0], len(reached), maxNodes)

def bestNeighbors(games: list, reached: dict, k: int) -> list:
    
    candidates = list()
    
    for game in games:
        for candidate in expand(game):
            if not str(candidate) in reached:
                reached[str(candidate)] = candidate
                candidates.append(candidate)
            elif candidate.h() < reached[str(candidate)].h():
                reached[str(candidate)] = candidate
                candidates.append(candidate)
    
    candidates.sort(key=lambda s: s.h())
    
    result = []
    i = 0
    while i < len(candidates) and i < k:
        result.append(candidates[i])
        i += 1
    return result

if __name__ == "__main__":
    main()