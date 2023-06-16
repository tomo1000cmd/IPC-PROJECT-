from flask import Flask, render_template, request
from twilio.rest import Client
import googlemaps
import urllib.parse
import random

app = Flask(__name__,template_folder='/home/shubham/Google-map-distance-api-main/Distance cities')

# Define your Twilio credentials and Google Maps API key

account_sid = 'AC83ab7689e4ee07a25ae6429f7cc4a107'
auth_token = 'd4260ba36af5a2fa46913b92f4c19d37'
from_number = '+13613092761'
to_number = '+31616671573'
google_maps_api_key = 'AIzaSyDOLvTB0gfeg21cu2tUeBjXJDWkdUKVyb8'

@app.route('/')
def index():
    return render_template('index4.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    origin = request.form['origin']
    destination = request.form['destination']

    # Create a Google Maps client
    gmaps = googlemaps.Client(key=google_maps_api_key)

    # Get the distance and duration using the Google Maps Distance Matrix API
    distance_result = gmaps.distance_matrix(origin, destination, units='imperial')
    distance = distance_result['rows'][0]['elements'][0]['distance']['text']
    duration = distance_result['rows'][0]['elements'][0]['duration']['text']

    # Generate a random value between 10 and 30 for Available Parking Spot
    available_parking_spot = random.randint(10, 30)

    # Create a Twilio client
    client = Client(account_sid, auth_token)

    # URL encode the origin and destination
    encoded_origin = urllib.parse.quote(origin)
    encoded_destination = urllib.parse.quote(destination)

    # Construct the Google Maps URL
    maps_url = f"https://www.google.com/maps/dir/?api=1&origin={encoded_origin}&destination={encoded_destination}"

    # Send the message with the Google Maps link and Available Parking Spot
    message = client.messages.create(
        body=f'Origin: {origin}\nDestination: {destination}\nDistance: {distance}\nDuration: {duration}\nAvailable Parking Spot: {available_parking_spot}\n{maps_url}',
        from_=from_number,
        to=to_number
    )

    # Return a response or redirect to a success page
    return 'Message sent successfully. SID: ' + message.sid

if __name__ == '__main__':
    app.run(debug=True)
