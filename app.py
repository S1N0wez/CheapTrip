import os
from flask import Flask, request, jsonify, render_template
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Получаем токен из переменных окружения
TRAVELPAYOUTS_TOKEN = os.environ.get('TRAVELPAYOUTS_TOKEN', 'temp_token')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search')
def search_tickets():
    origin = request.args.get('origin', 'MOW')
    destination = request.args.get('destination', 'LED')
    depart_date = request.args.get('depart_date', '2025-05-01')
    return_date = request.args.get('return_date', '2025-05-10')

    url = "https://api.travelpayouts.com/v1/prices/cheap"
    params = {
        'origin': origin,
        'destination': destination,
        'depart_date': depart_date,
        'return_date': return_date
    }
    headers = {
        'X-Access-Token': TRAVELPAYOUTS_TOKEN
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Важно: используем порт из переменной окружения
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)