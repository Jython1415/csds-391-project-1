
class EightPuzzle():
    
    # Initializer
    def __init__(self):
        self.state = "b12 345 678"
    
    # Default string representation
    def __str__(self):
        return self.state
    
    # Set state
    def setState(self, newState: str):
        self.state = newState