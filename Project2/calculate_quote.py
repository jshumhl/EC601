from datetime import datetime
import requests
from flask import Flask, request, jsonify


# Configurations
config = {
    "base_price": 10,
    "tier_1_distance": 10,
    "tier_1_price": 2,
    "tier_2_distance": 30,
    "tier_2_price": 1.5,
    "tier_3_price": 1,
    "weekend_multiplier": 1.2,
    "peak_multiplier": 1.5,
    "peak_start": 8,
    "peak_end": 10,
    "evening_peak_start": 17,
    "evening_peak_end": 19,
    "out_of_state_charge": 50,
    "max_distance": 50
}


GOOGLE_MAPS_API_KEY = "AIzaSyC2YoC_ujO9bCJAVHwM6RmHcVNOTXZE8HI"

app = Flask(__name__)

def calculate_distance(address_1, address_2=None):
    # If address_2 is not provided, use a default address (for businesses like restaurants)
    if not address_2:
        address_2 = "DEFAULT_BUSINESS_ADDRESS"
    
    # Construct the URL for the Distance Matrix API
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={address_1}&destinations={address_2}&key={GOOGLE_MAPS_API_KEY}"
    
    # Make the request
    response = requests.get(url)
    data = response.json()

    # Check if the request was successful
    if data["status"] == "OK":
        # Extract the distance value (in meters) from the response
        distance_meters = data["rows"][0]["elements"][0]["distance"]["value"]
        return distance_meters / 1000  # Convert to kilometers
    else:
        # Handle the error accordingly
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate-quote', methods=['POST'])
def calculate_cost(distance, time_of_week, out_of_state):
    # Base price
    base_price = config["base_price"]

    # Tiered distance-based cost
    if distance <= config["tier_1_distance"]:
        distance_cost = config["tier_1_price"] * distance
    elif distance <= config["tier_2_distance"]:
        distance_cost = config["tier_1_price"] * config["tier_1_distance"] + config["tier_2_price"] * (distance - config["tier_1_distance"])
    else:
        distance_cost = (config["tier_1_price"] * config["tier_1_distance"] +
                         config["tier_2_price"] * (config["tier_2_distance"] - config["tier_1_distance"]) +
                         config["tier_3_price"] * (distance - config["tier_2_distance"]))

    # Time of the week multiplier
    if time_of_week == "weekend":
        time_multiplier = config["weekend_multiplier"]
    else:
        time_multiplier = 1

    # Check if the current time falls within peak hours
    current_hour = datetime.now().hour
    if (config["peak_start"] <= current_hour <= config["peak_end"] or
        config["evening_peak_start"] <= current_hour <= config["evening_peak_end"]):
        peak_multiplier = config["peak_multiplier"]
    else:
        peak_multiplier = 1

    # Out of state charge
    out_of_state_charge = config["out_of_state_charge"] if out_of_state else 0

    # Maximum distance check
    if config["max_distance"] > 0 and distance > config["max_distance"]:
        return "Service not available for the specified distance."

    # Calculate the total cost
    total_cost = (base_price + distance_cost) * time_multiplier * peak_multiplier + out_of_state_charge

    return total_cost


@app.route('/calculate-quote', methods=['POST'])
def calculate_quote():
    data = request.json
    
    # Construct addresses from individual fields
    origin_address = f"{data['origin_street']}, {data['origin_city']}, {data['origin_state']} {data['origin_zip']}"
    dest_address = f"{data['dest_street']}, {data['dest_city']}, {data['dest_state']} {data['dest_zip']}"

    # Determine out-of-state condition
    out_of_state = data['origin_state'] != data['dest_state']
    
    # Extract service date and time and determine if it's a weekday or weekend
    service_datetime_str = f"{data['service_date']} {data['service_time']}"
    service_datetime = datetime.strptime(service_datetime_str, "%Y-%m-%d %H:%M")
    if service_datetime.weekday() < 5:  # 0-4 denotes Monday to Friday
        time_of_week = "weekday"
    else:
        time_of_week = "weekend"
    
    # Calculate distance using Google Maps API (pseudo-code for now)
    distance = calculate_distance(origin_address, dest_address)
    
    # Calculate cost based on distance, time of week, and other factors
    quote = calculate_cost(distance, time_of_week, out_of_state)
    
    return jsonify({'quote': quote})

if __name__ == '__main__':
    app.run(debug=True)
