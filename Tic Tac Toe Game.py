# Tic Tac Toe Game (Player X vs Computer O)

from flask import Flask, render_template_string, request, jsonify
import random

app = Flask(__name__)
app.secret_key = "suraj_sahani_tictactoe"

# Initial Game State
def reset_board():
    return [' ' for _ in range(10)]

board = reset_board()

def isWinner(bo, le):
    # Standard Tic-Tac-Toe winning combinations
    return (
        (bo[7] == le and bo[8] == le and bo[9] == le) or
        (bo[4] == le and bo[5] == le and bo[6] == le) or
        (bo[1] == le and bo[2] == le and bo[3] == le) or
        (bo[7] == le and bo[4] == le and bo[1] == le) or
        (bo[8] == le and bo[5] == le and bo[2] == le) or
        (bo[9] == le and bo[6] == le and bo[3] == le) or
        (bo[7] == le and bo[5] == le and bo[3] == le) or
        (bo[9] == le and bo[5] == le and bo[1] == le)
    )

def compMove():
    possibleMoves = [i for i, letter in enumerate(board) if letter == ' ' and i != 0]
    if not possibleMoves: return 0

    # 1. Win or Block logic
    for let in ['O', 'X']:
        for i in possibleMoves:
            boardCopy = board[:]
            boardCopy[i] = let
            if isWinner(boardCopy, let): return i

    # 2. Add Randomness (Shuffle) so it's not predictable
    random.shuffle(possibleMoves)
    
    # 3. Smart preferences (Center > Corners > Edges) with slight randomness
    if 5 in possibleMoves and random.random() > 0.2: return 5
    
    corners = [i for i in possibleMoves if i in [1, 3, 7, 9]]
    if corners: return random.choice(corners)
    
    return possibleMoves[0]

@app.route("/")
def index():
    cells = ""
    for i in range(1, 10):
        val = board[i]
        disabled = "disabled" if val != ' ' else ""
        color = "#007bff" if val == 'X' else "#dc3545"
        cells += f'<button class="cell" style="color: {color}" onclick="makeMove({i})" {disabled}>{val}</button>'
    
    return render_template_string(HTML_TEMPLATE, cells=cells)

@app.route("/move/<int:pos>")
def move(pos):
    global board
    if board[pos] == ' ':
        board[pos] = 'X'
        if isWinner(board, 'X'): return jsonify({"status": "win", "msg": "🎉 You Won, Suraj! 🎉"})
        
        if board.count(' ') <= 1: return jsonify({"status": "draw", "msg": "It's a Tie!"})

        c_move = compMove()
        if c_move != 0:
            board[c_move] = 'O'
            if isWinner(board, 'O'): return jsonify({"status": "loss", "msg": "Computer Wins! Better luck next time."})
        
        return jsonify({"status": "continue"})
    return jsonify({"status": "error"})

@app.route("/reset")
def reset():
    global board
    board = reset_board()
    return "<script>window.location.href='/';</script>"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>X & O with Bot</title>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <style>
        body { font-family: 'Poppins', sans-serif; background: #f4f7f6; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .game-card { background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); text-align: center; }
        .grid { display: grid; grid-template-columns: repeat(3, 100px); gap: 10px; margin: 20px 0; }
        .cell { width: 100px; height: 100px; font-size: 2.5em; font-weight: bold; cursor: pointer; border: 2px solid #eee; background: #fff; border-radius: 12px; transition: 0.2s; }
        .cell:hover:not(:disabled) { border-color: #007bff; background: #f0f7ff; }
        .reset-btn { padding: 12px 30px; background: #333; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; }
    </style>
</head>
<body>
    <div class="game-card">
        <h2>🎮 X & O with Bot</h2>
        <div class="grid">{{cells|safe}}</div>
        <button class="reset-btn" onclick="location.href='/reset'">New Game</button>
    </div>
    <script>
        function celebrate() {
            confetti({ particleCount: 150, spread: 70, origin: { y: 0.6 } });
        }
        function makeMove(pos) {
            fetch('/move/' + pos).then(r => r.json()).then(data => {
                if (data.status === "win") {
                    celebrate();
                    setTimeout(() => { alert(data.msg); location.reload(); }, 500);
                } else if (data.status === "loss" || data.status === "draw") {
                    setTimeout(() => { alert(data.msg); location.reload(); }, 100);
                } else {
                    location.reload();
                }
            });
        }
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True)
