from flask import Flask, jsonify, request
import parser
import os
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/compile', methods=['POST'])
def compile():
    json = request.get_json(force=True)

    if json.get('code') is None:
        return jsonify({'message': 'Bad request'}), 400
    code = str(json['code'])
    f = open("input.txt", "w")
    f.write(code)
    f.close()
    input_file = open("input.txt", "r")
    inputData = input_file.read()
    input_file.close()
    parser.runProgram(inputData)
    text_file = open("output.txt", "r")
    data = text_file.read()
    text_file.close()
    os.remove("input.txt")
    return jsonify({'response': data})

@app.route('/output')
def output():
    input_file = open("input.txt", "r")
    inputData = input_file.read()
    input_file.close()
    parser.runProgram(inputData)
    text_file = open("output.txt", "r")
    data = text_file.read()
    text_file.close()
    os.remove("input.txt")
    return jsonify({'response': data})

if __name__ == '__main__':
    app.run()
