document.addEventListener("DOMContentLoaded", () => {
    const ctx = document.getElementById('amenityChart').getContext('2d');

    // Fetch the data from the backend
    fetch('/chart_data')
        .then(response => response.json())
        .then(data => {
            data.pop(); // removes the last item from the array
            // Extract labels (amenities) and counts
            const labels = data.map(item => item._id); // Amenity names
            const counts = data.map(item => item.count); // Counts

            // Create the bar chart
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels, // X-axis labels
                    datasets: [{
                        data: counts, // Y-axis data
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1,
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: false // Hide legend
                        },
                        tooltip: {
                            // Increase font size for tooltips
                            bodyFont: {
                                size: 14
                            }
                        }
                    },
                    scales: {
                        x: {
                            ticks: {
                                font: {
                                    size: 30 // Increase font size of X-axis labels
                                }
                            }
                        },
                        y: {
                            beginAtZero: true,  // Use a linear scale starting at zero
                            ticks: {
                                callback: function(value) {
                                    // Format ticks on the y-axis to show the value
                                    return value.toLocaleString();
                                },
                                font: {
                                    size: 16 // Increase font size of Y-axis labels
                                }
                            }
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error fetching chart data:', error);
        });
});
