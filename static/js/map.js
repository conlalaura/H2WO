$(document).ready(function () {
    const mapService = new MapService();
    const reviewPopup = document.getElementById("review-popup");
    mapService.initMap();
    mapService.loadAmenityData('/api/amenities/water', 'water');
    mapService.loadAmenityData('/api/amenities/toilets', 'restroom');
//  mapService.loadAmenityData('/api/amenities/waste_basket', 'bins');
//  mapService.loadAmenityData('/api/amenities/shelter', 'shelter');  #TODO: @Alex tell my whyyyy nicht aktiv
//  mapService.loadAmenityData('/api/amenities/bench', 'bench');

    // Set the initial state of checkboxes (set some to false when needed for performance)
    $('#fountains').prop('checked', true);
    $('#restrooms').prop('checked', true);
//  $('#benches').prop('checked', true);
//  $('#shelter').prop('checked', true);
//  $('#bins').prop('checked', true);

    // Apply the initial visibility based on checkbox states
    $('#fountains').trigger('change');
    $('#restrooms').trigger('change');
//  $('#benches').trigger('change');
//  $('#shelter').trigger('change');
//  $('#bins').trigger('change');

// Event Listeners
    // filter checkboxes
    $('#fountains').on('change', function() {
        mapService.toggleAmenityVisibility('water', this.checked);
    });
    $('#restrooms').on('change', function() {
        mapService.toggleAmenityVisibility('restroom', this.checked);
    });
    $('#benches').on('change', function() {
        mapService.toggleAmenityVisibility('bench', this.checked);
    });
    $('#shelter').on('change', function() {
        mapService.toggleAmenityVisibility('shelter', this.checked);
    });
    $('#bins').on('change', function() {
        mapService.toggleAmenityVisibility('bins', this.checked);
    });

    $('.sidebar-amenity-options .option').on('click', function () {
        const button = $(this);
        const option = button.data('option');
        button.toggleClass('active');
    });

    // recenter buttom
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

    // popup close functionality
    $('#popup-close').on('click', function () {
        $('#review-popup').fadeOut();
        $('#map').css('filter', 'none');
        $('.sidebar').css('filter', 'none');
    });

    // Review submission
    document.getElementById('submit-review').addEventListener('click', () => {
        const rating = document.getElementById('rating-value').value; // Get the rating value
        const comment = document.getElementById('comment').value; // Get the comment text
        const amenityId = document.getElementById('review-popup').getAttribute('data-amenity-id'); // Get the amenity ID from the popup
        const username = "Anonymous"; // Replace with logic to get the username if applicable

        // Ensure data is valid before submission
        if (!rating || !comment || !amenityId) {
            alert('Please provide a rating, a comment, and ensure an amenity is selected.');
            return;
        }

        // POST review data to the backend
        fetch(`/api/review/${amenityId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                rating: rating,
                comment: comment
            })
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.text(); // The server might not return JSON
            })
            .then(data => {
                alert('Review submitted successfully!');
                // Optionally reload reviews for the amenity
                loadReviews(amenityId);
            })
            .catch(error => {
            console.error('Error submitting review:', error);

            // Provide more detailed error messages
            if (error.name === 'TypeError') {
                // This typically happens for network errors or if fetch failed to make a request
                alert('Network error: Unable to connect to the server. Please check your internet connection and try again.');
            } else if (error.message.includes('HTTP error')) {
                // Detailed error when there is an HTTP status code error
                alert(`Server error: ${error.message}. Please try again later.`);
            } else {
                // Catch all other unexpected errors
                alert(`Unexpected error: ${error.message}. Please try again.`);
            }
        });
});






    document.addEventListener("click", (event) => {
        const reviewPopup = document.getElementById("review-popup");
        const amenityPopup = document.querySelector(".leaflet-popup");

        // Handle review popup close
        if (!reviewPopup.classList.contains("hidden")) {
            if (!reviewPopup.contains(event.target) && !event.target.closest(".write-review-btn")) {
                reviewPopup.classList.add("hidden");
                reviewPopup.style.display = "none";
            }
        }

        // Handle amenity popup close
        if (amenityPopup) {
            if (!amenityPopup.contains(event.target) && !event.target.closest(".leaflet-marker-icon")) {
                document.querySelector(".leaflet-popup-close-button")?.click();
            }
        }
    });

    document.querySelectorAll(".rating-star").forEach((star) => {
        star.addEventListener("click", function () {
            const value = this.getAttribute("data-value");
            document.getElementById("rating-value").value = value;

            document.querySelectorAll(".rating-star").forEach((s) => {
                if (s.getAttribute("data-value") <= value) {
                    s.src = "static/img/rating-star-selected.svg";
                } else {
                    s.src = "static/img/rating-star-unselected.svg";
                }
            });
        });
    });
    
    
    
    
    
    
    // Prevent outside click listener from being triggered when clicking inside the review popup
    document.getElementById("review-popup").addEventListener("click", (event) => {
        event.stopPropagation(); // Prevent triggering the document click listener
    });
    
    


    window.mapServiceInstance = mapService;
});    

// Class definition for map-related operations
class MapService {
    constructor() {
        this.map = null;
        this.markers = {}; 
        this.amenitiesData = {}; 
        this.markerClusterGroup = {};
        this.loadingCount = 0;
        this.markerCounts = {};
    }
    // Initialize the map and setup initial features
    initMap() {
        this.createMap();
        this.setupGeolocation();
        this.map.on('zoom', () => this.updateClusterRadius());  // Added this line
        $('#map').hide();
        $('#loader').show();
    }

    // Create the map instance
    createMap() {
        this.map = L.map('map').setView([47.497234386445896, 8.729370936243816], 13); //  initial location Winterthur (if user doesn't share location)
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {}).addTo(this.map);
    }

    // Setup geolocation to center map on user location
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
    // Handle successful geolocation
    handleGeolocationSuccess(position) {
        this.map.setView([position.coords.latitude, position.coords.longitude], 13);
        this.addUserLocationMarker(position.coords.latitude, position.coords.longitude);
    }
    // Add a marker at user's location
    addUserLocationMarker(lat, lon) {
        L.marker([lat, lon], { icon: redIcon }).addTo(this.map).bindPopup("You're here").openPopup();
    }
    // Handle geolocation error
    handleGeolocationError(err) {
        console.error(err);
    }

    // Re-center map to user's location
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

    // Load amenity data from API
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

    // Add amenity markers to the map
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

    // Check if all markers have been added    
    checkIfAllMarkersAdded() {
        const allMarkersAdded = Object.values(this.markerCounts).every(count => count > 0);
        if (allMarkersAdded) {
            // All data processed, hide the loader and show the map
            $('#loader').hide(); // Hide the loading animation
            $('#map').show();  // Show the map
        }
    }

    // Get or create a cluster group for the amenity
    getAmenityClusterGroup(amenityType) {
        if (!this.markerClusterGroup[amenityType]) {
            const clusterOptions = {
                maxClusterRadius: this.getClusterRadiusBasedOnZoom(),
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

    // Update cluster radius based on zoom level
    updateClusterRadius() {
        const zoomLevel = this.map.getZoom();
        Object.keys(this.markerClusterGroup).forEach(amenityType => {
            const clusterGroup = this.markerClusterGroup[amenityType];
            clusterGroup.options.maxClusterRadius = this.getClusterRadiusBasedOnZoom(zoomLevel);
        });
    }

    // Calculate cluster radius based on zoom level
    getClusterRadiusBasedOnZoom(zoomLevel) {
        // Adjust the cluster radius based on zoom level (Formula tbd)
        return 100
    }
    
    // TODO: Simplify / Split up into multiple smaller methods
    createAmenityMarker(amenity, amenityType) {
        const marker = this.createMarker(amenity, amenityType);
        const popupContent = this.generatePopupContent(amenity, amenityType);
        marker.bindPopup(popupContent);
        this.attachPopupListeners(marker, amenity);
        return marker;
    }
    
    // Create a Leaflet marker
    createMarker(amenity, amenityType) {
        const icon = this.createCustomIcon(amenityType);
        return L.marker([parseFloat(amenity.lat), parseFloat(amenity.lon)], { icon });
    }
    
    // Generate HTML content for the popup
    generatePopupContent(amenity, amenityType) {
        const formatText = (text) => text.replace(/_/g, ' ');
        const formattedAmenityType = formatText(amenityType);
    
        let leftContent = `
            <div>
                <h3 style="margin: 0; font-size: 1.8em;">${formattedAmenityType}</h3>
        `;
        Object.entries(amenity).forEach(([key, value]) => {
        // TODO add again "id"
            if (!['lat', 'lon', 'amenity', 'reviews'].includes(key)) {
                leftContent += `<p style="margin: 0.2rem 0;">${formatText(key)}: ${formatText(value.toString())}</p>`;
            }
        });
        leftContent += `</div>`;
    
        let rightContent = `<div class="reviews-section" style="flex: 1;">`;
        const reviews = amenity.reviews || [];
        if (reviews.length > 0) {
            const meanRating = (reviews.reduce((sum, review) => sum + review.rating, 0) / reviews.length).toFixed(1);
            const roundedRating = Math.round(meanRating);
            rightContent += `
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <h3 style="margin: 0; font-size: 1.2em;">Reviews</h3>
                    <strong style="margin-left: auto; font-size: 1.8em; color: black;">${meanRating}</strong>
                </div>
                <div style="color: gold; font-size: 1.2em; text-align: right;">
                    ${'★'.repeat(roundedRating)}${'☆'.repeat(5 - roundedRating)}
                </div>`;

            // Add individual reviews
            reviews.forEach((review) => {
                const username = review.username || 'Anonymous';
                const rating = review.rating || 0;
                const comment = review.comment || '';
                rightContent += `<p style="margin: 0.2rem 0;"><strong>${username} (${rating}):</strong> ${comment}</p>`;
            });
        } else {
            rightContent += `<p>No reviews yet</p>`;
        }
    
        const reviewButtonId = `add-review-btn-${amenity.id}`;
        rightContent += `
            <button id="${reviewButtonId}" class="write-review-btn">
                Add a Review
            </button>
        </div>`;
    
        return `
            <div style="display: flex; gap: 1rem; align-items: flex-start;">
                <div>${leftContent}</div>
                <div>${rightContent}</div>
            </div>
        `;
    }
    
    // Attach listeners to the marker popup
    attachPopupListeners(marker, amenity) {
        const reviewPopup = document.getElementById("review-popup");
        marker.on("popupopen", () => {
            const reviewBtn = document.getElementById(`add-review-btn-${amenity.id}`);
            if (reviewBtn) {
                reviewBtn.addEventListener("click", () => {
                    reviewPopup.setAttribute('data-amenity-id', amenity.id); // Set the amenity ID on the popup
                    reviewPopup.classList.remove("hidden");
                    reviewPopup.style.display = "block";
                });
            }
        });
    }
    
    
    
    
    
    // Create custom icon for an amenity
    createCustomIcon(amenityType) {
        const iconUrl = iconMapping[amenityType] || 'static/img/locate.svg';
        return L.icon({
            iconUrl,
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
        });
    }

    // Toggle the visibility of amenities based on checkbox state
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


