// Document ready function: This runs as soon as the HTML document is fully loaded and ready.
$(document).ready(function () {
    // Create an instance of MapService, which handles all map-related functionalities.
    const mapService = new MapService();
    // Initialize the map on the page.
    mapService.initMap();
    // Load data for stations and reservations.
    mapService.loadWaterData();
    mapService.loadRestroomData();
    mapService.loadBenchData();
    mapService.loadBinData();
    mapService.loadShelterData();


    // Make the mapService instance globally accessible, particularly for the reserveSpot function.
    window.mapServiceInstance = mapService;
});


class MapService {
    constructor() {
        this.map = null;  // Instance of the Leaflet map.
        this.markers = {}; // Object to store marker instances, keyed by station IDs.
        this.routingControl = null; // Newest Routing-Control
        this.amenitiesData = {};
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
            .bindPopup("You're here").openPopup();
    }

    // Handle geolocation errors.
    handleGeolocationError(err) {
        console.error(err);
    }

    //  Data Loading  //////////////////////////////////////////////////////////////////////////////
    //  Load data for water amenities
    loadWaterData() {
        this.loadAmenityData('/api/water_data', 'water');
    }

    // Load data for restroom amenities
    loadRestroomData() {
        this.loadAmenityData('/api/toilet_data', 'restroom');
    }

    // Load data for benches
    loadBenchData() {
        this.loadAmenityData('/api/bench_data', 'bench');
    }

    // Load data for shelters
    loadShelterData() {
        this.loadAmenityData('/api/shelter_data', 'shelter');
    }

    // Load data for bins
    loadBinData() {
        this.loadAmenityData('/api/waste_basket_data', 'bin');
    }

    // Generic method to load amenity data
    loadAmenityData(apiUrl, amenityType) {
        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                console.log(`${amenityType} Data:`, data);
                this.amenitiesData[amenityType] = data; // Store data for this amenity type
                this.updateVisibleAmenities(); // Update markers on the map
                this.setupMapEventListeners(); // Add listeners for map interactions
            })
            .catch(error => console.error(`Error loading ${amenityType} data:`, error));
    }


    // /////////////////////////////////////////////////////////////////
    // Display all the stations on the map with their respective reservation status.
    displayAmenities(amenities) {
        // Iterate through each station and add a marker to the map.
        amenities.forEach(amenity => this.addAmenityMarker(amenity));
    }

    // Update visible amenities for all types based on the current map bounds
    updateVisibleAmenities() {
        // Get current map bounds
        const bounds = this.map.getBounds();

        // Clear existing markers
        Object.values(this.markers).forEach(marker => this.map.removeLayer(marker));
        this.markers = {}; // Reset markers object

        // Iterate through all amenity types and display visible ones
        Object.values(this.amenitiesData).forEach(amenities => {
            if (amenities) {
                const visibleAmenities = amenities.filter(amenity => {
                    const lat = parseFloat(amenity.lat);
                    const lon = parseFloat(amenity.lon);
                    return bounds.contains([lat, lon]);
                });

                // Add markers for visible amenities
                visibleAmenities.forEach(amenity => this.addAmenityMarker(amenity));
            }
        });
    }

    addAmenityMarker(amenity) {
        console.log('Amenity Location:', amenity.lat, amenity.lon);

        // Determine the icon based on the amenity type
        const amenityType = amenity.amenity || 'default'; // Default if type is missing
        const customIcon = this.createCustomIcon(amenityType);

        // Create the marker
        const marker = L.marker([parseFloat(amenity.lat), parseFloat(amenity.lon)], { icon: customIcon }).addTo(this.map);

        // Bind popup content
        const popupContent = this.buildPopupContent(amenity);
        marker.bindPopup(popupContent);

        // Cache the marker
        this.markers[amenity.id] = marker;
    }


    createCustomIcon(amenityType) {
        const iconUrl = iconMapping[amenityType] || 'static/img/locate.svg'; // Default icon if type not found
        return L.icon({
            iconUrl: iconUrl,
            iconSize: [25, 41],  // Adjust size as needed
            iconAnchor: [12, 41], // Anchor point
            popupAnchor: [1, -34], // Popup position relative to the icon
            shadowSize: [41, 41]  // Shadow size
        });
    }

    buildPopupContent(amenity) {
        let popupContent = `<h3>${amenity.amenity}</h3><ul>`;
        popupContent += '</ul>';
        return popupContent;
    }

    debounce(func, delay) {
        let timer;
        return function (...args) {
            clearTimeout(timer);
            timer = setTimeout(() => func.apply(this, args), delay);
        };
    }

    setupMapEventListeners() {
        const debouncedUpdate = this.debounce(this.updateVisibleAmenities.bind(this), 200);
        this.map.on('moveend', debouncedUpdate);
        this.map.on('zoomend', debouncedUpdate);
    }
}

const redIcon = L.icon({
    iconUrl: 'static/img/locate.svg', // Provide the path to your icon image
    iconSize: [25, 41],  // Size of the icon
    iconAnchor: [12, 41], // Point of the icon which will correspond to marker's location
    popupAnchor: [1, -34], // Point from which the popup should open relative to the iconAnchor
    shadowSize: [41, 41]  // Size of the shadow
});

const iconMapping = {
    // Water
    fountain: 'static/img/pin_fountain.svg',
    drinking_water: 'static/img/pin_fountain.svg',
    water_tap: 'static/img/pin_fountain.svg',
    water_point: 'static/img/pin_fountain.svg',
    // Restroom
    toilets: 'static/img/pin_restroom.svg',
    // Bench
    bench: 'static/img/pin_bench.svg',
    // Shelter
    shelter: 'static/img/pin_shelter.svg',
    // Waste baskets
    waste_basket: 'static/img/pin_bin.svg'
};