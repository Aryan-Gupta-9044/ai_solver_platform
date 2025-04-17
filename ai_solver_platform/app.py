from flask import Flask, render_template, request, jsonify
from solvers.wumpus_solver import WumpusWorld, WumpusSolverAgent
from solvers.cryptarithmetic import CryptarithmeticSolver
from solvers.tictactoe import TicTacToeGame, MinimaxSolver
from solvers.minimax_plotter import MinimaxPlotter
import json

app = Flask(__name__)

# Store active games
active_games = {
    'wumpus': {},
    'cryptarithmetic': {},
    'tictactoe': {},
    'minimax': {}
}

@app.route('/')
def index():
    """Render the main platform page"""
    return render_template('index.html')

@app.route('/wumpus')
def wumpus_page():
    """Render the Wumpus World game page"""
    return render_template('wumpus.html')

@app.route('/cryptarithmetic')
def cryptarithmetic_page():
    """Render the Cryptarithmetic solver page"""
    return render_template('cryptarithmetic.html')

@app.route('/tictactoe')
def tictactoe_page():
    """Render the TicTacToe game page"""
    return render_template('tictactoe.html')

@app.route('/minimax')
def minimax_page():
    """Render the Minimax visualization page"""
    return render_template('minimax.html')

# Wumpus World endpoints
@app.route('/api/wumpus/initialize', methods=['POST'])
def initialize_wumpus():
    try:
        data = request.json
        size = int(data.get('size', 4))
        wumpus_pos = data.get('wumpus_pos', None)
        gold_pos = data.get('gold_pos', None)
        pit_positions = data.get('pit_positions', None)
        
        game = WumpusWorld(size=size, wumpus_pos=wumpus_pos, 
                          gold_pos=gold_pos, pit_positions=pit_positions)
        
        game_id = str(len(active_games['wumpus']))
        active_games['wumpus'][game_id] = game
        
        return jsonify({
            'status': 'success',
            'world_id': game_id,
            'config': {
                'size': size,
                'wumpus_pos': game.wumpus_pos,
                'gold_pos': game.gold_pos,
                'pit_positions': game.pit_positions
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

# Cryptarithmetic endpoints
@app.route('/api/cryptarithmetic/solve', methods=['POST'])
def solve_cryptarithmetic():
    try:
        data = request.json
        equation = data.get('equation')
        solver = CryptarithmeticSolver(equation)
        solution = solver.solve()
        return jsonify({
            'status': 'success',
            'solution': solution
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

# TicTacToe endpoints
@app.route('/api/tictactoe/move', methods=['POST'])
def tictactoe_move():
    try:
        data = request.json
        game_id = data.get('game_id')
        position = data.get('position')
        
        if game_id not in active_games['tictactoe']:
            game = TicTacToeGame()
            active_games['tictactoe'][game_id] = game
        else:
            game = active_games['tictactoe'][game_id]
        
        result = game.make_move(position)
        return jsonify(result)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

# Minimax visualization endpoints
@app.route('/api/minimax/plot', methods=['POST'])
def plot_minimax():
    try:
        data = request.json
        depth = int(data.get('depth', 3))
        branching_factor = int(data.get('branching_factor', 2))
        
        plotter = MinimaxPlotter(depth, branching_factor)
        plot_data = plotter.generate_plot_data()
        
        return jsonify({
            'status': 'success',
            'plot_data': plot_data
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True) 