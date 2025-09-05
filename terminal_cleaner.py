import os

class TerminalOperator:

    def clear():
        # Para Windows
        if os.name == "nt":
            os.system("cls")
        # Para Linux/Mac
        else:
            os.system("clear")
