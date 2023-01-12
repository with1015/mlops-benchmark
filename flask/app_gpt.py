import argparse
import json
import flask

from flask import Flask, jsonify, request
from transformers import pipeline, set_seed

parser = argparse.ArgumentParser(description='')
parser.add_argument('--model', type=str, default='gpt2')
parser.add_argument('--gpu-mode', action='store_true')

args = parser.parse_args()
app = Flask(__name__)

set_seed(42)

if args.gpu_mode:
    generator = pipeline('text-generation', model=args.model, device=0)
else:
    generator = pipeline('text-generation', model=args.model, device=-1)


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        text = request.get_json()
        result = generator(text["input"],
                           max_length=30,
                           num_return_sequences=1)
        print("[DEBUG] generate:", result)
        return jsonify({'result': result})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='50000',
            use_reloader=False,
            threaded=False)
