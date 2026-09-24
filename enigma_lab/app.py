from flask import Flask, jsonify, render_template, request
from enigma import Enigma, VERSIONS, version_details

app = Flask(__name__)

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/api/versions')
def versions():
    return jsonify(version_details())

@app.post('/api/encrypt')
def encrypt():
    data = request.get_json(force=True) or {}
    try:
        machine = Enigma(
            rotors=data.get('rotors', ['I','II','III']),
            reflector=data.get('reflector', 'B'),
            positions=data.get('positions', 'AAA'),
            rings=data.get('rings', 'AAA'),
            plugs=data.get('plugs', ''),
        )
        return jsonify({'ciphertext': machine.transform(data.get('text', '')), 'steps': machine.steps})
    except (ValueError, KeyError) as exc:
        return jsonify({'error': str(exc)}), 400

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
