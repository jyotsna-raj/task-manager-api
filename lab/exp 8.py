board = [" "] * 9

def print_board():
    for i in range(0, 9, 3):
        print(board[i], "|", board[i+1], "|", board[i+2])
        if i < 6:
            print("--+---+--")

def check_winner(p):
    wins = [(0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)]
    return any(board[a]==board[b]==board[c]==p for a,b,c in wins)

player = "X"

for _ in range(9):
    print_board()
    move = int(input(f"{player} move (1-9): ")) - 1

    if board[move] != " ":
        print("Invalid")
        continue

    board[move] = player

    if check_winner(player):
        print_board()
        print(player, "wins!")
        break

    player = "O" if player == "X" else "X"
else:
    print_board()
    print("Draw")
