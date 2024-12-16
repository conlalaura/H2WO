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
                            backgroundColor: 'rgba(4, 147, 114, 0.6)', // Green
                        },
                        {
                            label: 'No',
                            data: noData,
                            backgroundColor: 'rgba(214, 69, 65, 0.6)', // Red
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'top',
                            labels: {
                                font: {
                                    family: 'DMSans',
                                    size: 18
                                },
                                boxWidth: 20, // Width of coloured box.
                                boxHeight: 20
                            }
                        },
                        tooltip: {
                            enabled: true,
                            position: 'nearest',
                            xAlign: 'center',
                            yAlign: 'bottom',
                            backgroundColor: '#24252a', // Background color of the tooltip
                            caretSize: 5, // Size, in px, of the tooltip arrow.
                            cornerRadius: 10, // Radius of tooltip corner curves.
                            titleFont: {
                                family: 'Satoshi',
                                size: 14
                            },
                            titleColor: '#e8e8e8', // Color of title text.
                            titleMarginBottom: 10, // Margin to add on bottom of title section.
                            bodyFont: {
                                family: 'DMSans',
                                size: 12
                            },
                            boxPadding: 10, // Padding between the color box and the text.

                        }
                    },
                    scales: {
                        x: {
                            stacked: true,
                            ticks: {
                                font: {
                                    family: 'DMSans',
                                    size: 14
                                },
                                padding: 10
                            }
                        },
                        y: {
                            stacked: true,
                            ticks: {
                                font: {
                                    family: 'DMSans',
                                    size: 14
                                },
                                padding: 20, // Add padding to avoid overlap
                                callback: function(value) {
                                    return value + '%'; // Add a percent sign
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

document.addEventListener("DOMContentLoaded", () => {
    const ctx = document.getElementById('sparsityChart').getContext('2d');

    // Fetch the data from the backend
    fetch('/api/sparsity_statistics_data')
        .then(response => response.json())
        .then(data => {
            // Process data into labels and datasets
            const labels = data.map(item => Object.keys(item)[0]); // Extract keys as labels
            const sparsityData = data.map(item => Object.values(item)[0]); // Extract values as data

            // Create the chart
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Key Sparsity (%)',
                        data: sparsityData,
                        backgroundColor: 'rgba(214, 69, 65, 0.6)',
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'top',
                            labels: {
                                font: {
                                    family: 'DMSans',
                                    size: 18
                                },
                                boxWidth: 20,
                                boxHeight: 20
                            }
                        },
                        tooltip: {
                            enabled: true,
                            position: 'nearest',
                            xAlign: 'center',
                            yAlign: 'bottom',
                            backgroundColor: '#24252a',
                            caretSize: 5,
                            cornerRadius: 10,
                            titleFont: {
                                family: 'Satoshi',
                                size: 14
                            },
                            titleColor: '#e8e8e8',
                            titleMarginBottom: 10,
                            bodyFont: {
                                family: 'DMSans',
                                size: 12
                            },
                            boxPadding: 10,
                        }
                    },
                    scales: {
                        x: {
                            ticks: {
                                font: {
                                    family: 'DMSans',
                                    size: 14
                                },
                                padding: 10
                            }
                        },
                        y: {
                            ticks: {
                                font: {
                                    family: 'DMSans',
                                    size: 14
                                },
                                padding: 20,
                                callback: function(value) {
                                    return value + '%'; // Add a percent sign
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