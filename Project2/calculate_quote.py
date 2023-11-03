from datetime import datetime, timedelta
import requests
from flask import Flask, request, jsonify, render_template
import googlemaps


# Configurations

general_config = {
    "weekend_multiplier": 1.2,
    "peak_start": 8,
    "peak_end": 10,
    "evening_peak_start": 17,
    "evening_peak_end": 19,
}

all_config = {
    "restaurant": {
        "base_price": 5,
        "max_distance": 15,  # in miles
        "business_address": "58 Beach St #2017, Boston, MA, 02111",
        "opening_time": "09:00",  # 9 AM
        "closing_time": "22:00",  # 10 PM
        "peak_multiplier": 1.1,
        "tier_1_distance": 0.5,
        "tier_1_price": 0.8,
        "tier_2_distance": 4,
        "tier_2_price": 1,
        "tier_3_price": 1.2,
        "out_of_state_charge": 50,
        "menu": [
            {
                "name": "Margherita Pizza",
                "price": 12.99,
                "prep_time": 20  # minutes
            },
            {
                "name": "Caesar Salad",
                "price": 8.99,
                "prep_time": 10  # minutes
            },
            {
                "name": "Spaghetti Carbonara",
                "price": 15.99,
                "prep_time": 25  # minutes
            }
            ],
    },
    "moving_company": {
        # Configurations specific to the moving company
    },
    # More business types can be added with their specific configurations
}

GOOGLE_MAPS_API_KEY = ""
# types: restaurant, moving_company, courier_service, 
# Not implemented cuz im lazy af: repair_service, event_planners
business_type = "restaurant"
config = all_config[business_type]




app = Flask(__name__)


@app.route('/')
def index():
    template = business_type + '.html'
    today = datetime.now().strftime("%Y-%m-%d")
    if business_type == "restaurant":
        opening_time = config['opening_time']
        closing_time = config['closing_time']
        menu_items = config['menu']
        return render_template(template, today=today, opening_time=opening_time, closing_time=closing_time, menu_items=menu_items)
    else:
        return render_template(template)


# Function to calculate the clock time when the delivery is expected to arrive
def calculate_expected_arrival_time(user_delivery_datetime, longest_prep_time, travel_duration_minutes):
    # Parse the user-specified delivery datetime
    service_datetime = datetime.strptime(user_delivery_datetime, "%Y-%m-%d %H:%M")

    # Check if the user-specified time is in the future
    if service_datetime < datetime.now():
        raise ValueError("The specified delivery time is in the past!")

    # Add the longest preparation time to the user-specified delivery time
    departure_time = service_datetime + timedelta(minutes=longest_prep_time)

    # Add the travel duration to the departure time to get the arrival time
    expected_arrival_time = departure_time + timedelta(minutes=travel_duration_minutes)

    # Format the expected arrival time to a string that shows the clock time
    expected_arrival_clock_time = expected_arrival_time.strftime("%H:%M")

    return expected_arrival_clock_time

def calculate_distance(address_1, address_2=None, service_datetime=None, longest_prep_time=None):
    # If address_2 is not provided, use a default address (for businesses like restaurants)
    if not address_2:
        address_2 = "DEFAULT_BUSINESS_ADDRESS"
    
    gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
    
    # If service_datetime is provided, convert it to a timestamp
    if service_datetime:
        # Check if the service_datetime is in the past
        if service_datetime < datetime.now():
            raise ValueError('The service date and time must be in the future.')
        if business_type == "restaurant":
            service_datetime += timedelta(minutes=longest_prep_time)
        departure_timestamp = int(service_datetime.timestamp())
    else:
        departure_timestamp = None
        

    # Get directions between the two addresses
    directions_result = gmaps.directions(
        address_1, 
        address_2, 
        mode="driving", 
        departure_time=departure_timestamp
    )

    # Check the response for the 'legs' of the journey
    if directions_result and 'legs' in directions_result[0]:
        distance_meters = directions_result[0]['legs'][0]["distance"]["value"]
        distance_miles = distance_meters / 1609.34  # Convert meters to miles

        # Use duration in traffic if available, otherwise use standard duration
        if 'duration_in_traffic' in directions_result[0]['legs'][0]:
            duration_minutes = directions_result[0]['legs'][0]['duration_in_traffic']['value'] / 60
        else:
            duration_minutes = directions_result[0]['legs'][0]['duration']['value'] / 60

        return round(distance_miles, 1), round(duration_minutes)
    else:
        raise ValueError('Directions request failed or returned no routes.')

def calculate_cost(distance, time_of_week, out_of_state):
    # Base price
    base_price = config["base_price"]

    # Tiered distance-based cost
    if "max_distance" in config:
        if distance >= config["max_distance"] :
            return None
        
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
        time_multiplier = general_config["weekend_multiplier"]
    else:
        time_multiplier = 1

    # Check if the current time falls within peak hours
    current_hour = datetime.now().hour
    if (general_config["peak_start"] <= current_hour <= general_config["peak_end"] or
        general_config["evening_peak_start"] <= current_hour <= general_config["evening_peak_end"]):
        peak_multiplier = config["peak_multiplier"]
    else:
        peak_multiplier = 1

    # Out of state charge
    out_of_state_charge = config["out_of_state_charge"] if out_of_state else 0

    # Maximum distance check
    #if config["max_distance"] > 0 and distance > config["max_distance"]:
    #    return "Service not available for the specified distance."

    # Calculate the total cost
    total_cost = (base_price + distance_cost) * time_multiplier * peak_multiplier + out_of_state_charge

    return round(total_cost, 2)


@app.route('/calculate-quote', methods=['POST'])
def calculate_quote():
    data = request.json
    # personal info for future use
    customer_name = data.get('customer_name')
    customer_email = data.get('customer_email')
    customer_phone = data.get('customer_phone')
    
    # Construct addresses from individual fields
    if business_type == "restaurant":
        origin_address = config["business_address"]
        out_of_state = False
        selected_items = data.get('menu_items')
        max_prep_times = max([item['prep_time'] for item in config["menu"] if item['name'] in selected_items])  
    else:
        origin_address = f"{data['origin_address']}"
        out_of_state = data['origin_state'] != data['dest_state']
    dest_address = f"{data['dest_address']}"
    print(origin_address)
    print(dest_address)

    # Extract service date and time and determine if it's a weekday or weekend
    service_datetime_str = f"{data['service_date']} {data['service_time']}"
    service_datetime = datetime.strptime(service_datetime_str, "%Y-%m-%d %H:%M")
    if service_datetime.weekday() < 5:  # 0-4 denotes Monday to Friday
        time_of_week = "weekday"
    else:
        time_of_week = "weekend"
    
    # Calculate distance using Google Maps API (pseudo-code for now)
    if business_type == "restaurant":
        distance, p2ptime = calculate_distance(origin_address, dest_address, service_datetime, max_prep_times)
        expected_arrival_clock_time = calculate_expected_arrival_time(service_datetime_str, max_prep_times, p2ptime)
    else:
        expected_arrival_clock_time = service_datetime + timedelta(minutes=p2ptime)
        distance, p2ptime = calculate_distance(origin_address, dest_address, service_datetime)
    print("distance:", distance)
    print("time:", p2ptime)
    
    # Calculate cost based on distance, time of week, and other factors
    cost = calculate_cost(distance, time_of_week, out_of_state)
    if cost is None:
        quote = "The address is too far"
        duration = ""
    else:
        quote = "Estimated quote is: $" + str(cost)
        arrival_time = "Estimated arrival time is " + str(expected_arrival_clock_time)
        #duration = 'The approximate time is ' + str(p2ptime) + ' minutes'
        
    print("quote:", quote)
    
    return jsonify({
        'quote': quote, 
        'arrival': arrival_time,
        #'time': duration
    })


if __name__ == '__main__':
    app.run(debug=True)

