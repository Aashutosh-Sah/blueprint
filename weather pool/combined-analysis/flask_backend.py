from flask import Flask, jsonify
import random
from city_data import generate_city_data

app = Flask(__name__)

# Generate weather data for 1000+ cities including all Nepal cities
weather_data = generate_city_data()

@app.route('/weather/<city>', methods=['GET'])
def get_weather(city):
    city_lower = city.lower()
    
    # Find case-insensitive match
    matched_city = next(
        (c for c in weather_data.keys() if c.lower() == city_lower),
        None
    )
    
    if matched_city:
        return jsonify(weather_data[matched_city])
    else:
        # Generate random weather for unknown cities
        return jsonify({
            'temperature': random.randint(50, 90),
            'condition': random.choice(['Sunny', 'Cloudy', 'Rainy', 'Snowy']),
            'humidity': random.randint(30, 90),
            'note': 'Generated weather for unknown city'
        })

@app.route('/cities', methods=['GET'])
def get_cities():
    """Endpoint to get list of all available cities"""
    return jsonify({'cities': list(weather_data.keys())})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
