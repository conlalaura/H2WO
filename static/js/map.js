$(document).ready(function () {
    const mapService = new MapService();
    mapService.initMap();
    mapService.loadAmenityData('/api/water_data', 'water');
    mapService.loadAmenityData('/api/toilet_data', 'restroom');
    mapService.loadAmenityData('/api/waste_basket_data', 'bins');
    // Add more amenity loading functions as needed
    window.mapServiceInstance = mapService;
});

    // mapService.loadAmenityData('/api/shelter_data', 'shelter');
    // mapService.loadAmenityData('/api/waste_basket_data', 'bins');
    // mapService.loadAmenityData('/api/bench_data', 'bench');
class MapService {
    constructor() {
        this.map = null;
        this.markers = {}; // Object to store marker instances, keyed by amenity IDs.
        this.amenitiesData = {}; // Store loaded amenities data by type.
        this.markerClusterGroup = {}; // Separate cluster groups for each amenity type.
    }

    initMap() {
        this.createMap();
        this.setupGeolocation();
        // this.map.on('zoom', () => console.log('Current zoom level:', this.map.getZoom()));
        this.map.on('zoom', () => this.updateClusterRadius());  // Added this line
    }

    createMap() {
        this.map = L.map('map').setView([0, 0], 13);
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

    loadAmenityData(apiUrl, amenityType) {
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
        });

        this.map.addLayer(clusterGroup);
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
        console.log(zoomLevel, console.log(zoomLevel*10))

        // Adjust the cluster radius based on zoom level
        // You can tweak the formula as needed for your use case
        return 100
        //return Math.max(50, Math.min(zoomLevel * 10, 100)); // Adjust cluster radius based on zoom
    }
    
    

    createAmenityMarker(amenity, amenityType) {
        const icon = this.createCustomIcon(amenityType);
        const marker = L.marker([parseFloat(amenity.lat), parseFloat(amenity.lon)], { icon });
        const popupContent = `<h3>${amenity.amenity || 'Amenity'}</h3>`;
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
}

const redIcon = L.icon({
    iconUrl: 'static/img/locate.svg',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
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
