from flask import Flask, request, jsonify, render_template
import requests
import os
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

TRAVELPAYOUTS_TOKEN = os.getenv('TRAVELPAYOUTS_TOKEN')

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
    app.run(debug=True, port=5000)
