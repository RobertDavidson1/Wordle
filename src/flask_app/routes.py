from flask import Flask, jsonify, render_template, request
import json
import os

app = Flask(__name__)

DATA_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
SOLVED_JSON_PATH = os.path.join(DATA_DIRECTORY, 'decision_tree.json')

# Load precomputed JSON when the app starts
with open(SOLVED_JSON_PATH) as f:
    guesses = json.load(f)

def init_app(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/traverse', methods=['POST'])
    def traverse():
        data = request.json
        path = data['path']

        node = guesses
        try:
            for step in path:
                node = node['next states'][step]
            return jsonify(node)
        except KeyError:
            return jsonify({'error': 'Invalid path'}), 400
