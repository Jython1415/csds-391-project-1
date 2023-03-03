from EightPuzzle import *
from main import *
import random

randomizeMovesNum = 1000
puzzlesCount = 200

def main():
    
    r = random.Random()
    r.seed("hi")
    
    maxOriginal = 50
    
    puzzles = []
    for _ in range(puzzlesCount):
        game = EightPuzzle()
        randomizeState(randomizeMovesNum, game, r)
        puzzles.append(str(game))
    
    maxTests = []
    for i in range(15):
        max = int(maxOriginal * (1.5**(i+1)))
        maxString = f"maxNodes {max}"
        
        tests = []
        
        for puzzle in puzzles:
            setS = "setState " + puzzle
            a1 = "solve A-star h1"
            a2 = "solve A-star h2"
            b = "solve beam 15"
            
            commands = [setS, a1, setS, a2, setS, b]
            
            tests.append("\n".join(commands))
        
        maxTests.append(maxString + "\n" + ("\n".join(tests)))
    
    total = "\n\n".join(maxTests)
    
    with open("expFile.txt", "w") as f:
        f.write(total)

if __name__ == "__main__":
    main()