from typing import List

from flask import Flask, request, jsonify

app = Flask(__name__)

LOADED_WORDS = {}


@app.route('/')
def index():
    return 'Hello World'


@app.route('/load', methods=['POST'])
def load():
    words = request.get_json()

    if (
            not isinstance(words, list)
            or not all(isinstance(word, str) for word in words)
    ):
        return jsonify({'error': 'List of words was expected'}), 400

    global LOADED_WORDS
    LOADED_WORDS = {}

    for word in words:
        sorted_word = ''.join(sorted(word.lower()))
        LOADED_WORDS[sorted_word] = LOADED_WORDS.get(sorted_word, []) + [word]

    return jsonify({'status': 'OK'})


@app.route('/get', methods=['GET'])
def get():
    word = request.args.get('word')

    if not isinstance(word, str):
        return jsonify({'error': 'String parameter \'word\' is required'}), 400

    global LOADED_WORDS
    sorted_word = ''.join(sorted(word.lower()))

    return jsonify(LOADED_WORDS.get(sorted_word))


if __name__ == "__main__":
    app.run()
