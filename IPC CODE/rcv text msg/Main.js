//javascript.js
//set map options
var myLatLng = { lat: 52.2073245, lng: 3.96049 };
var mapOptions = {
    center: myLatLng,
    zoom: 7,
    mapTypeId: google.maps.MapTypeId.ROADMAP

};


//create map
var map = new google.maps.Map(document.getElementById('googleMap'), mapOptions);

//create a DirectionsService object to use the route method and get a result for our request
var directionsService = new google.maps.DirectionsService();

//create a DirectionsRenderer object which we will use to display the route
var directionsDisplay = new google.maps.DirectionsRenderer();

//bind the DirectionsRenderer to the map
directionsDisplay.setMap(map);


//define calcRoute function
function calcRoute() {
    // Create the request object
    var request = {
        origin: document.getElementById("from").value,
        destination: document.getElementById("to").value,
        travelMode: google.maps.TravelMode.DRIVING,
        unitSystem: google.maps.UnitSystem.IMPERIAL
    };

    // Pass the request to the route method
    directionsService.route(request, function(result, status) {
        if (status == google.maps.DirectionsStatus.OK) {
            // Get distance and time
            const output = document.querySelector('#output');
            output.innerHTML = "<div class='alert-info'>From: " + document.getElementById("from").value + ".<br />To: " + document.getElementById("to").value + ".<br /> Driving distance <i class='fas fa-road'></i> : " + result.routes[0].legs[0].distance.text + ".<br />Duration <i class='fas fa-hourglass-start'></i> : " + result.routes[0].legs[0].duration.text + ".<br />Parking Spots Available<i class='fas fa-hourglass-start'></i> : " + result.routes[0].legs[0].duration.text + "</div>";
        
            // Display route
            directionsDisplay.setDirections(result);

            // Your Twilio account SID, auth token, and phone numbers
            var accountSid = 'ACCOUNT ID';
            var authToken = 'AUTHCODE';
            var fromNumber = 'TWILIO NO';
            var toNumber = 'PHONE NO';

            // Create a Twilio client
            var client = Twilio(accountSid, authToken);

            // Send the message
            client.messages
                .create({
                    body: 'Origin: ' + document.getElementById("from").value + '\nDestination: ' + document.getElementById("to").value + '\nDistance: ' + result.routes[0].legs[0].distance.text + '\nDuration: ' + result.routes[0].legs[0].duration.text,
                    from: fromNumber,
                    to: toNumber
                })
                .then(function(message) {
                    console.log('Message sent successfully. SID: ' + message.sid);
                    // Display success message on the page
                    output.innerHTML = "<div class='alert-success'>Message sent successfully. SID: " + message.sid + "</div>";
                })
                .catch(function(error) {
                    console.error('Error sending message: ' + error);
                    // Display error message on the page
                    output.innerHTML = "<div class='alert-danger'><i class='fas fa-exclamation-triangle'></i> Failed to send message.</div>";
                });

        } else {
            // Delete route from map
            directionsDisplay.setDirections({ routes: [] });
            // Center map in London
            map.setCenter(myLatLng);

            // Show error message
            output.innerHTML = "<div class='alert-danger'><i class='fas fa-exclamation-triangle'></i> Could not retrieve driving distance.</div>";
        }
    });
}



//create autocomplete objects for all inputs


var input1 = document.getElementById("from");
var autocomplete1 = new google.maps.places.Autocomplete(input1);

var input2 = document.getElementById("to");
var autocomplete2 = new google.maps.places.Autocomplete(input2);
