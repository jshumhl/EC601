# Project 2: Quote Calculator for Business Services

## Introduction
This project provides an online quote calculation tool for various service-based businesses like restaurants, moving companies, and limo services. The tool takes user input through a web form and calculates a quote based on distance, time, and specific business parameters.

## Product Mission Statement
Our mission is to streamline the quote generation process for service-based businesses, providing a user-friendly interface that simplifies the calculation of service costs. We aim to empower businesses with a tool that accurately reflects their pricing structure, adapts to their unique operational hours, and handles the dynamics of location-based services, all while maintaining a high standard of user privacy and data security.

## Product User Stories

### As a restaurant owner, (MVP)

- I want to easily calculate delivery charges based on distance so that I can provide my customers with accurate quotes.
- I need to limit delivery services to within a certain radius to ensure timely deliveries and maintain service quality.

### As a moving company operator, (not implemented)

- I want to factor in peak hour traffic and out-of-state travel into my quotes to cover the additional costs incurred during busy times and longer trips.
- I need a system that remembers repeat customers' details to make the booking process quicker and more personalized.

### As a limo service provider, (not implemented)

- I want to offer instant quotes to my clients based on their travel needs, whether it's airport runs, city tours, or out-of-town trips, with a clear pricing structure that adapts to distance and time of the week.
- I need to ensure that my pricing adjusts for peak event times, such as proms or weddings, when demand is higher.

### As a customer, (MVP)

- I want to receive a quick and clear quote for the service I am interested in without having to make a phone call or wait for an email response.
- I need to feel secure in the information I provide online, knowing that my personal details are not being over-collected or misused.

## Product Features
- HTML/CSS/JS-based Web Form: A responsive web form that adapts to various devices, ensuring a seamless user experience across desktops, tablets, and smartphones.
- Google Maps API Integration: Utilizes the Google Maps API to calculate distances between two points for accurate quote generation based on travel requirements.
- Dynamic Quote Calculation: Factors in distance, time of the week, peak hours, and tiered pricing to provide customers with precise service quotes.
- Business Type Customization: Supports different business types such as restaurants, moving companies, repair services, courier services, and event planners, with customized web forms and calculations.
- Personal Information Collection: Gathers essential customer details like name, phone number, and email address for future follow-ups and relationship building.
- Cookie Management: Stores form data using cookies to retain user input even after the page refreshes, enhancing user convenience.
- Interactive Menu Selection: For restaurant businesses, the web form includes an interactive menu for customers to select items, which influences the delivery time estimate.

## Customization
Businesses can customize the quote calculation by adjusting the settings in the config.json file, such as base price, tiered distance rates, peak hours, and maximum allowed distance.

### Restaurant Specialized Functionalities
- Menu Item Selection: Customers must select at least one menu item before submitting a quote request. This ensures that there's a clear service being provided and calculated for.
- Mandatory Selection Enforcement: The web form now enforces the selection of at least one menu item with real-time validation, prompting the user if the condition is not met.
- Data Persistence: User selections, including menu items, are saved in cookies, allowing the form to remember the user's choices even after the page is refreshed.
- Menu Configuration: The backend configuration now includes menu items with individual preparation times, which are factored into the delivery time estimates.

## How It Works
The user fills out a web form with details about the service they need, including addresses, desired service date and time, and personal information. The backend uses this information to calculate distance and time using the Google Maps API and then applies the business-specific pricing rules to generate a quote.

## Setup
To set up the project, follow these steps:

- Ensure Python and Flask are installed on your system.
- Obtain a Google Maps API key and set it in the configuration.
- Configure the config.json file with your business specifics.
- Run the Flask server using python calculate_quote.py.

## Usage
After starting the Flask app, navigate to the hosted web address. Choose the service type and fill in the required fields. Click "Get Quote" to receive the calculated quote based on the input provided.

## Dependencies
- Flask
- googlemaps Python client
- Other Python dependencies listed in requirements.txt

## Demo
The first image is an empty form after running the command `python calculate_quote.py`. This is a Delivery Contact Form. A customer may choose the food using the checkbox. Each food in the backend has a food-preparation time for it that would be added for future use. Then Personal Information and Delievery Address would be prompted for food delievery purpose. Selecting the Date and Time will send the information to the backend for calculation.
<img width="554" alt="empty_form" src="[https://github.com/jshumhl/EC601/Project2/demo/empty_form.png](https://github.com/jshumhl/EC601/blob/main/Project2/demo/empty_form.png)">
In the backend calculation part, the function takes the food preparation time, if its a busy hour (dinner/lunch), add the busy hour extra time to calculate when the food driver need to leave the store. Then combine with MAPS API to calculate the distance to delievery address, and extra time due to busy traffic (MAPS API) to accomodate extra quote time shown on the completed form. All these Personal Information, Destination Address, and Food Order Details are saved in the website cookies for easy access from the customer and track the order. A copy of the information is also saved in the database for restaurant to keep track of the delievery order.
<img width="554" alt="empty_form" src="[https://github.com/jshumhl/EC601/Project2/demo/filled_form.png](https://github.com/jshumhl/EC601/blob/main/Project2/demo/empty_form.png)">
## License
Uncertain haha

## Contact
- Author: Hin Lui Shum
- Email: hinlui.shum@gmail.com
