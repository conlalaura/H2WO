$(document).ready(function () {
    const mapService = new MapService();
    mapService.initMap();
    mapService.loadAmenityData('/api?type=water', 'water');
    mapService.loadAmenityData('/api?type=toilets', 'restroom');
    mapService.loadAmenityData('/api?type=waste_basket', 'bins');
    // mapService.loadAmenityData('/api?type=shelter', 'shelter');  #TODO: @Alex tell my whyyyy nicht aktiv
    mapService.loadAmenityData('/api?type=bench', 'bench');

    // Set the initial state of checkboxes (set some to false when needed for performance)
    $('#fountains').prop('checked', true);
    $('#restrooms').prop('checked', true);
    $('#benches').prop('checked', true);
//    $('#shelter').prop('checked', true);
    $('#bins').prop('checked', true);

    // Apply the initial visibility based on checkbox states
    $('#fountains').trigger('change');
    $('#restrooms').trigger('change');
    $('#benches').trigger('change');
//    $('#shelter').trigger('change');
    $('#bins').trigger('change');

    // Add event listeners for filter checkboxes
    $('#fountains').on('change', function() {
        mapService.toggleAmenityVisibility('water', this.checked);
    });
    $('#restrooms').on('change', function() {
        mapService.toggleAmenityVisibility('restroom', this.checked);
    });
    $('#benches').on('change', function() {
        mapService.toggleAmenityVisibility('bench', this.checked);
    });
    $('#bins').on('change', function() {
        mapService.toggleAmenityVisibility('bins', this.checked);
    });

    // Add event listener for re-center button
    $('#recenter').on('click', function() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                function(position) {
                    // Directly set the map's view to the user's current position
                    mapService.map.setView([position.coords.latitude, position.coords.longitude], 17);
                }, // error handling
                function(error) {
                    console.error('Geolocation error:', error);
                }
            );
        } else {
            console.error('Geolocation is not supported by this browser.');
        }
    });

    window.mapServiceInstance = mapService;
});    


class MapService {
    constructor() {
        this.map = null;
        this.markers = {}; // Object to store marker instances, keyed by amenity IDs.
        this.amenitiesData = {}; // Store loaded amenities data by type.
        this.markerClusterGroup = {}; // Separate cluster groups for each amenity type.
        this.loadingCount = 0; // Track the number of pending data loads
        this.markerCounts = {}; // Track the number of markers added per amenity type
    }

    initMap() {
        this.createMap();
        this.setupGeolocation();
        // this.map.on('zoom', () => console.log('Current zoom level:', this.map.getZoom()));
        this.map.on('zoom', () => this.updateClusterRadius());  // Added this line
        $('#map').hide();
        $('#loader').show();
    }

    createMap() {
    // set initial location Winterthur (if user doesn't share location)
        this.map = L.map('map').setView([47.497234386445896, 8.729370936243816], 13);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {}).addTo(this.map);
    }

    setupGeolocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                this.handleGeolocationSuccess.bind(this),
                this.handleGeolocationError.bind(this)
            );
        } else {
            console.error("Geolocation is not supported by this browser.");
        }
    }

    handleGeolocationSuccess(position) {
        this.map.setView([position.coords.latitude, position.coords.longitude], 13);
        this.addUserLocationMarker(position.coords.latitude, position.coords.longitude);
    }

    addUserLocationMarker(lat, lon) {
        L.marker([lat, lon], { icon: redIcon }).addTo(this.map).bindPopup("You're here").openPopup();
    }

    handleGeolocationError(err) {
        console.error(err);
    }

//    method to center map to user's current location
    centerToUserLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                this.handleGeolocationSuccess.bind(this),
                this.handleGeolocationError.bind(this)
            );
        } else {
            console.error("Geolocation is not supported by this browser.");
        }
    }

    loadAmenityData(apiUrl, amenityType) {
        this.loadingCount++;
        this.markerCounts[amenityType] = 0; // Initialize the count of markers for this amenity type
        
        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                this.amenitiesData[amenityType] = data;
                this.addAmenitiesToMap(amenityType, data);
            })
            .catch(error => console.error(`Error loading ${amenityType} data:`, error));
    }



    addAmenitiesToMap(amenityType, amenities) {
        const clusterGroup = this.getAmenityClusterGroup(amenityType);
        amenities.forEach(amenity => {
            const marker = this.createAmenityMarker(amenity, amenityType);
            clusterGroup.addLayer(marker);
            this.markers[amenity.id] = marker;
            this.markerCounts[amenityType]++; // Increment the marker count for this amenity type
        });

        this.map.addLayer(clusterGroup);

        // Check if all points for this amenity type have been added
        this.checkIfAllMarkersAdded();
    }

    checkIfAllMarkersAdded() {
        // Check if all amenity types have their markers fully added
        const allMarkersAdded = Object.values(this.markerCounts).every(count => count > 0);
        
        if (allMarkersAdded) {
            // All data processed, hide the loader and show the map
            $('#loader').hide(); // Hide the loading animation
            $('#map').show();  // Show the map
        }
    }

    getAmenityClusterGroup(amenityType) {
        if (!this.markerClusterGroup[amenityType]) {
            const clusterOptions = {
                maxClusterRadius: this.getClusterRadiusBasedOnZoom(), // Changed this line
               // maxClusterRadius: 50,
                iconCreateFunction: cluster => {
                    const childCount = cluster.getChildCount();
    
                    return L.divIcon({
                        html: `
                            <div class="custom-cluster cluster-${amenityType}">
                                <div class="icon">
                                    <img src="static/img/cluster_${amenityType}.svg" alt="${amenityType}">
                                </div>
                                <div class="count">${childCount}</div>
                            </div>
                        `,
                        className: "", // No additional Leaflet classes
                        iconSize: [30, 30] // Adjust as needed
                    });
                }
            };
    
            this.markerClusterGroup[amenityType] = L.markerClusterGroup(clusterOptions);
        }
        return this.markerClusterGroup[amenityType];
    }
    
    updateClusterRadius() {
        const zoomLevel = this.map.getZoom();
        Object.keys(this.markerClusterGroup).forEach(amenityType => {
            const clusterGroup = this.markerClusterGroup[amenityType];
            clusterGroup.options.maxClusterRadius = this.getClusterRadiusBasedOnZoom(zoomLevel);
        });
    }

    getClusterRadiusBasedOnZoom(zoomLevel) {
        // Adjust the cluster radius based on zoom level (Formula tbd)
        return 100
    }
    
    

    createAmenityMarker(amenity, amenityType) {
        const formatText = (text) => text.replace(/_/g, ' ');
        const formattedAmenityType = formatText(amenityType);
        const icon = this.createCustomIcon(amenityType);
        const marker = L.marker([parseFloat(amenity.lat), parseFloat(amenity.lon)], { icon });
        let popupContent = `<h3>${formattedAmenityType}</h3>`;
        Object.entries(amenity).forEach(([key, value]) => {
            if (!['lat', 'lon', 'amenity', 'id'].includes(key)) { // Skip lat, lon, amenity, and id keys
                const formattedKey = formatText(key);
                const formattedValue = formatText(value.toString());
                popupContent += `<p>${formattedKey}: ${formattedValue}</p>`;
            }
    });
        marker.bindPopup(popupContent);
        return marker;
    }

    createCustomIcon(amenityType) {
        const iconUrl = iconMapping[amenityType] || 'static/img/locate.svg';
        return L.icon({
            iconUrl,
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
        });
    }
    // Method to toggle the visibility of amenities based on checkbox state
    toggleAmenityVisibility(amenityType, isVisible) {
        const clusterGroup = this.markerClusterGroup[amenityType];
        if (clusterGroup) {
            if (isVisible) {
                this.map.addLayer(clusterGroup);
            } else {
                this.map.removeLayer(clusterGroup);
            }
        }
    }
}

const redIcon = L.icon({
    iconUrl: 'static/img/locate.svg',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [-47, -35],
});

const iconMapping = {
    water: 'static/img/pin_fountain.svg',
    restroom: 'static/img/pin_restroom.svg',
    bench: 'static/img/pin_bench.svg',
    shelter: 'static/img/pin_shelter.svg',
    bins: 'static/img/pin_bin.svg',
};

const clusterColors = {
    water: '#6995BB',
    restroom: '#419074',
    bench: '#7D5F5D',
    shelter: '#C45C24',
    bins: '#3A3A3A',
};
