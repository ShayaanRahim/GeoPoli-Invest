#Main Flask app

# backend/app.py
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/api/news')
def get_news():
    return "Geopolitical News"

@app.route('/api/impact')
def analyze_impact():
    return "Geopolitical Impact"

@app.route('/api/historical')
def get_historical():
    return "Get Historical"





if __name__ == '__main__':
    app.run(debug=True)