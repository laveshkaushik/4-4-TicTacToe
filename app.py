from flask import Flask, render_template, jsonify, request
from game import Agent, emptystate, gameover, NAMES
import pickle

app = Flask(__name__)

a1 = Agent(2, lossval=-1)
a2 = Agent(2, lossval=-1)
with open('/Users/lavesh/PycharmProjects/tictactoe/filename.pickle', 'rb') as handle:
    b = pickle.load(handle)
a1.values = b

with open('/Users/lavesh/PycharmProjects/tictactoe/notdraw.pickle', 'rb') as handle:
    c = pickle.load(handle)
a2.values = c

@app.route('/')
def index():
    return render_template('index.html')


def is_board_full(state):
    for i in range(4):
        for j in range(4):
            if state[i][j] == 0:
                return False
    return True


@app.route('/move', methods=['POST'])
def move():
    post = request.get_json()
    board = post.get('board')
    chance = post.get('chance')
    print (board, chance)
    state = emptystate()
    for i in range(4):
        for j in range(4):
            if board[i][j] == ' ':
                state[i][j] = 0
            elif board[i][j] == 'X':
                state[i][j] = 1
            else:
                state[i][j] = 2

    player = post.get('player')
    computer = post.get('computer')

    winner = gameover(state)
    # Check if player won
    if winner == 3:
        return jsonify(tied = True, computer_wins = False, player_wins = False, board = board)
    elif NAMES[winner] == player:
        return jsonify(tied = False, computer_wins = False, player_wins = True, board = board)


    if chance:
        computer_move = a2.greedy(state)
    else:
        computer_move = a1.greedy(state)

    # Make the next move
    board[computer_move[0]][computer_move[1]] = computer
    state[computer_move[0]][computer_move[1]] = 2
    winner = gameover(state)
    # Check if computer won
    if winner == 3:
        return jsonify(computer_row = computer_move[0], computer_col = computer_move[1],
                      computer_wins = False, player_wins = False, tied=True, board=board)
    # Check if game is over
    elif NAMES[winner] == computer:
        return jsonify(computer_row = computer_move[0], computer_col = computer_move[1],
                       computer_wins = True, player_wins = False, tied=False, board = board)
    # Game still going
    return jsonify(computer_row = computer_move[0], computer_col = computer_move[1],
                   computer_wins = False, player_wins = False, board = board)

if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0')