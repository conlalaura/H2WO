// Document ready function: This runs as soon as the HTML document is fully loaded and ready.
$(document).ready(function () {
    // Create an instance of MapService, which handles all map-related functionalities.
    const mapService = new MapService();
    // Initialize the map on the page.
    mapService.initMap();
    // Load data for stations and reservations.
    mapService.loadWaterData();

    // Make the mapService instance globally accessible, particularly for the reserveSpot function.
    window.mapServiceInstance = mapService;
});


class MapService {
    constructor() {
        this.map = null;  // Instance of the Leaflet map.
        this.markers = {}; // Object to store marker instances, keyed by station IDs.
        this.routingControl = null; // Newest Routing-Control
    }
    // Initialize the map with default settings.
    initMap() {
        this.createMap();
        this.setupGeolocation();
    }

    // Create the map and set initial view.
    createMap() {
        this.map = L.map('map').setView([0, 0], 13);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {}).addTo(this.map);
    }

    // set Location
    setupGeolocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(this.handleGeolocationSuccess.bind(this), this.handleGeolocationError.bind(this));
        } else {
            console.error("Geolocation is not supported by this browser.");
        }
    }

    // Successful geolocation.
    handleGeolocationSuccess(position) {
        this.map.setView([position.coords.latitude, position.coords.longitude], 13);
        this.addUserLocationMarker(position.coords.latitude, position.coords.longitude);
    }

    // Add a marker for the user's location.
    addUserLocationMarker(lat, lon) {
        L.marker([lat, lon], { icon: redIcon }).addTo(this.map)
            .bindPopup('Your location within a radius of 10 kilometers').openPopup();
    }

    // Handle geolocation errors.
    handleGeolocationError(err) {
        console.error(err);
    }

    // Function to load data for stations and reservations from the server.
    loadWaterData() {
        // Use fetch to make the HTTP request to get water data
        fetch('/api/water_data')
            .then(response => response.json()) // Parse the JSON response
            .then(water_amenities => {
                console.log('Water Amenities Data:', water_amenities); // Log the fetched data
                this.displayAmenities(water_amenities); // Display amenities on the map
            })
            .catch(error => console.error("Error loading data: ", error)); // Log any errors
    }

    // Display all the stations on the map with their respective reservation status.
    displayAmenities(amenities) {
        // Iterate through each station and add a marker to the map.
        amenities.forEach(amenity => this.addAmenityMarker(amenity));
    }


    addAmenityMarker(amenity) {
        console.log('Amenity Location:', amenity.lat, amenity.lon);
        const popupContent = this.buildPopupContent(amenity); // Move this line inside the function
        const marker = L.marker([parseFloat(amenity.lat), parseFloat(amenity.lon)]).addTo(this.map);
        marker.bindPopup(popupContent);
        marker.amenityId = amenity.id;
        marker.amenityLat = amenity.lat;
        marker.stationLon = amenity.lon;
        this.markers[amenity.id] = marker;
    }

    // Build and return HTML content for the popups of each station.
    buildPopupContent(amenity) {
        let popupContent = `<h3>Amenity ID: ${amenity.id}</h3><ul>`;
        popupContent += '</ul>';
        return popupContent;
    }

}


const redIcon = L.icon({
    iconUrl: 'static/img/locate.svg', // Provide the path to your icon image
    iconSize: [25, 41],  // Size of the icon
    iconAnchor: [12, 41], // Point of the icon which will correspond to marker's location
    popupAnchor: [1, -34], // Point from which the popup should open relative to the iconAnchor
    shadowSize: [41, 41]  // Size of the shadow
});
