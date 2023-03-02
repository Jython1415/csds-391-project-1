import sys

def main():
    print(getCommands())
    
def getCommands() -> list[str]:
    with open(sys.argv[1], "r") as f:
        return map(lambda i: i.replace("\n", ""), f.readLines())
        

    
    
if __name__ == "__main__":
    main()