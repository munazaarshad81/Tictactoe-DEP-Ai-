import tkinter as tk
import math

def check_winner(board):
    # Check rows, columns, and diagonals for a winner
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != ' ':
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != ' ':
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
        return board[0][2]
    return None

def is_board_full(board):
    return all(cell != ' ' for row in board for cell in row)

def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    if winner == 'X':
        return 1
    if winner == 'O':
        return -1
    if is_board_full(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ' '
                    best_score = min(score, best_score)
        return best_score

def best_move(board):
    best_score = -math.inf
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'X'
                score = minimax(board, 0, False)
                board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

def make_move(row, col):
    global current_player, player_O_name, player_X_name
    if board[row][col] == ' ' and current_player == 'O':
        board[row][col] = 'O'
        buttons[row][col].config(text='O', fg='blue', bg='black')
        current_player = 'X'
        if check_winner(board) or is_board_full(board):
            end_game()
        else:
            computer_move()

def computer_move():
    global current_player
    move = best_move(board)
    if move:
        board[move[0]][move[1]] = 'X'
        buttons[move[0]][move[1]].config(text='X', fg='red', bg='black')
        current_player = 'O'
        if check_winner(board) or is_board_full(board):
            end_game()

def end_game():
    global player_O_name, player_X_name, player_O_score, player_X_score
    winner = check_winner(board)
    if winner:
        if winner == 'O':
            player_O_score += 1
            label.config(text=f"{player_O_name} wins!", fg='blue')
        else:
            player_X_score += 1
            label.config(text=f"{player_X_name} wins!", fg='red')
    else:
        label.config(text="It's a tie!", fg='white')
    update_scorecard()
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(state=tk.DISABLED)

def update_scorecard():
    scorecard.config(text=f"{player_O_name}: {player_O_score} | {player_X_name}: {player_X_score}", fg='white')

def reset_game():
    global board, current_player
    board = [[' ' for _ in range(3)] for _ in range(3)]
    current_player = 'O'
    label.config(text=f"{player_O_name}'s turn", fg='white')
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(text=' ', state=tk.NORMAL, bg='black')

def start_game():
    global player_O_name, player_X_name, player_O_score, player_X_score
    player_O_name = player_O_entry.get()
    player_X_name = "Computer"
    player_O_score = 0
    player_X_score = 0
    update_scorecard()
    reset_game()
    start_frame.pack_forget()
    game_frame.pack()

root = tk.Tk()
root.title("Tic Tac Toe")
root.config(bg='black')

player_O_name = "Player O"
player_X_name = "Computer"
player_O_score = 0
player_X_score = 0
current_player = 'O'

start_frame = tk.Frame(root, bg='black')
start_frame.pack()

tk.Label(start_frame, text="Enter Player O's name:", bg='black', fg='white').pack()
player_O_entry = tk.Entry(start_frame)
player_O_entry.pack()

tk.Button(start_frame, text="Start Game", command=start_game, bg='gray', fg='black').pack()

game_frame = tk.Frame(root, bg='black')

label = tk.Label(game_frame, text="Player O's turn", font=('Helvetica', 14), bg='black', fg='white')
label.pack()

scorecard = tk.Label(game_frame, text=f"{player_O_name}: {player_O_score} | {player_X_name}: {player_X_score}", font=('Helvetica', 12), bg='black', fg='white')
scorecard.pack()

frame = tk.Frame(game_frame, bg='black')
frame.pack()

buttons = [[None for _ in range(3)] for _ in range(3)]
board = [[' ' for _ in range(3)] for _ in range(3)]

for i in range(3):
    for j in range(3):
        button = tk.Button(frame, text=' ', font='normal 20', width=5, height=2, command=lambda i=i, j=j: make_move(i, j), bg='black', fg='white')
        button.grid(row=i, column=j)
        buttons[i][j] = button

reset_button = tk.Button(game_frame, text="Reset Game", command=reset_game, bg='gray', fg='black')
reset_button.pack()

root.mainloop()