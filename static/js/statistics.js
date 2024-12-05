document.addEventListener("DOMContentLoaded", () => {
    const ctx = document.getElementById('toiletChart').getContext('2d');

    // Fetch the data from the backend
    fetch('/api/toilet_statistics_data')
        .then(response => response.json())
        .then(data => {
            // Process data into labels and datasets
            const labels = data.map(item => item.fields.key);
            const yesData = data.map(item => item.fields.yes);
            const noData = data.map(item => item.fields.no);

            // Create the chart
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                            label: 'Yes',
                            data: yesData,
                            backgroundColor: 'rgba(79, 195, 247, 0.4)',
                        },
                        {
                            label: 'No',
                            data: noData,
                            backgroundColor: 'rgba(124, 179, 66, 0.4)',
                        }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top',
                            labels: {
                                font: {
                                    family: 'inherit',
                                    size: 25
                                }
                            }
                        },
                        tooltip: {
                            enabled: true,
                        },
                    },
                    scales: {
                        x: {
                            stacked: true,
                            ticks: {
                                font: {
                                    size: 25
                                }
                            }
                        },
                        y: {
                            stacked: true,
                            ticks: {
                                font: {
                                    family: 'inherit', // Inherit font family for y-axis labels
                                    size: 25,
                                },
                                padding: 50, // Add padding to avoid overlap
                                callback: function(value) {
                                    return value + '%'; // Add a percent sign if needed
                                }
                            },
                        },
                    }
                }
            });
        })
        .catch(error => {
            console.error("Error fetching data:", error);
        });
});