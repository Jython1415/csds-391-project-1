import sys

def main():
    commands = getCommands()
    
    for command in commands:
        run(command)
    
def getCommands() -> list:
    with open(sys.argv[1], "r") as f:        
        return list(map(lambda i: i.replace("\n", ""), f.readlines()))

def run(command: str):
    words = command.split(" ")

    if words[0] == "setState":
        print("run setState")
    elif words[0] == "printState":
        print("run printState")
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

if __name__ == "__main__":
    main()