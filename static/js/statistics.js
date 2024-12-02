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
            const unknownData = data.map(item => item.fields.unknown);

            // Create the chart
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Yes',
                            data: yesData,
                            backgroundColor: 'rgba(0, 255, 0, 0.2)', // Green with alpha
                        },
                        {
                            label: 'No',
                            data: noData,
                            backgroundColor: 'rgba(0, 0, 255, 0.2)', // Blue with alpha
                        },
                        {
                            label: 'Unknown',
                            data: unknownData,
                            backgroundColor: 'rgba(128, 128, 128, 0.2)', // Gray with alpha
                        }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        tooltip: {
                            enabled: true,
                        },
                    },
                    scales: {
                        x: {
                            stacked: true,
                        },
                        y: {
                            stacked: true,
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error("Error fetching data:", error);
        });
});
