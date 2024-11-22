// Initialize Map and set View to Technikum
const map = L.map('map').setView([47.497234386445896, 8.729370936243816], 13);

// Load Map Image
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);


// Set User's Current Position
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
        (position) => {
            const { latitude, longitude } = position.coords;
            map.setView([latitude, longitude], 13);
            L.marker([latitude, longitude])
                .addTo(map)
                .bindPopup('You are here.')
                .openPopup();
        },
        (error) => {
            console.error("Error retrieving location: ", error.message);
        }
    );
}

