// Map setup
const map = L.map('map').setView([0, 0], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

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




// Sidebar interactions 

// Handle tag selection
document.querySelectorAll('.tag').forEach((tag) => {
    tag.addEventListener('click', () => {
        tag.classList.toggle('active');
    });
});

// Radius slider
const radiusSlider = document.getElementById('radius-slider');
const radiusValue = document.getElementById('radius-value');

radiusSlider.addEventListener('input', () => {
    radiusValue.textContent = `${radiusSlider.value} m`;
});
// Map setup
const map = L.map('map').setView([0, 0], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

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




// Sidebar interactions 

// Handle tag selection
document.querySelectorAll('.tag').forEach((tag) => {
    tag.addEventListener('click', () => {
        tag.classList.toggle('active');
    });
});

// Radius slider
const radiusSlider = document.getElementById('radius-slider');
const radiusValue = document.getElementById('radius-value');

radiusSlider.addEventListener('input', () => {
    radiusValue.textContent = `${radiusSlider.value} m`;
});
