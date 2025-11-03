board = ["*","*","*","*","*","*","*","*","*"]
current = "X"
play = True

def printBoard():
    print(f"{board[0]} | {board[1]} | {board[2]}")
    print("--+---+--")
    print(f"{board[3]} | {board[4]} | {board[5]}")
    print("--+---+--")
    print(f"{board[6]} | {board[7]} | {board[8]}")

def checkWin():
    win = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for a,b,c in win:
        if board[a] == board[b] == board[c] != "*":
            print(f"Spieler {board[a]} gewinnt")
            return True
    return False

def checkTie():
    if "*" not in board:
        print("Unentschieden!")
        return True
    return False

while play:
    printBoard()
    pos = int(input(f"Spieler {current}, Feld 1–9: ")) - 1
    
    if not (0 <= pos <= 8):
        print("nur 1–9")
        continue
    if board[pos] != "*":
        print("Feld schon belegt!")
        continue

    board[pos] = current

    if checkWin() or checkTie():
        printBoard()
        break

    current = "O" if current == "X" else "X"