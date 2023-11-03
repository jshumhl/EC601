# Project 2: Quote Calculator for Business Services

## Introduction
This project provides an online quote calculation tool for various service-based businesses like restaurants, moving companies, and limo services. The tool takes user input through a web form and calculates a quote based on distance, time, and specific business parameters.

## Product Mission Statement
Our mission is to streamline the quote generation process for service-based businesses, providing a user-friendly interface that simplifies the calculation of service costs. We aim to empower businesses with a tool that accurately reflects their pricing structure, adapts to their unique operational hours, and handles the dynamics of location-based services, all while maintaining a high standard of user privacy and data security.

## Product User Stories

### As a restaurant owner,

- I want to easily calculate delivery charges based on distance so that I can provide my customers with accurate quotes.
- I need to limit delivery services to within a certain radius to ensure timely deliveries and maintain service quality.

### As a moving company operator,

- I want to factor in peak hour traffic and out-of-state travel into my quotes to cover the additional costs incurred during busy times and longer trips.
- I need a system that remembers repeat customers' details to make the booking process quicker and more personalized.

### As a limo service provider,

- I want to offer instant quotes to my clients based on their travel needs, whether it's airport runs, city tours, or out-of-town trips, with a clear pricing structure that adapts to distance and time of the week.
- I need to ensure that my pricing adjusts for peak event times, such as proms or weddings, when demand is higher.

### As a customer,

- I want to receive a quick and clear quote for the service I am interested in without having to make a phone call or wait for an email response.
- I need to feel secure in the information I provide online, knowing that my personal details are not being over-collected or misused.

## Features
- Interactive web form with HTML5 validation.
- Calculates distance using the Google Maps API.
- Configurable pricing tiers based on distance.
- Peak hour pricing adjustments.
- Out-of-state travel charge calculation.
- User personal information collection for follow-ups.
- Responsive design for mobile and tablet use.
- Stores user input in cookies for session persistence.
  
## How It Works
The user fills out a web form with details about the service they need, including addresses, desired service date and time, and personal information. The backend uses this information to calculate distance and time using the Google Maps API and then applies the business-specific pricing rules to generate a quote.

### Setup
To set up the project, follow these steps:

- Ensure Python and Flask are installed on your system.
- Obtain a Google Maps API key and set it in the configuration.
- Configure the config.json file with your business specifics.
- Run the Flask server using python calculate_quote.py.

## Usage
After starting the Flask app, navigate to the hosted web address. Choose the service type and fill in the required fields. Click "Get Quote" to receive the calculated quote based on the input provided.

## Customization
Businesses can customize the quote calculation by adjusting the settings in the config.json file, such as base price, tiered distance rates, peak hours, and maximum allowed distance.

## Dependencies
- Flask
- googlemaps Python client
- Other Python dependencies listed in requirements.txt

## License
Uncertain haha

## Contact
- Author: Hin Lui Shum
- Email: hinlui.shum@gmail.com
