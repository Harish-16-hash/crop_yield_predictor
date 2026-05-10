document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips if any
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Dashboard Chart Initialization
    const chartCanvas = document.getElementById('yieldChart');
    if (chartCanvas) {
        fetch('/chart_data')
            .then(response => response.json())
            .then(data => {
                if(data.length > 0) {
                    const labels = data.map(item => item.crop_name);
                    const values = data.map(item => item.avg_yield);
                    
                    const ctx = chartCanvas.getContext('2d');
                    new Chart(ctx, {
                        type: 'bar',
                        data: {
                            labels: labels,
                            datasets: [{
                                label: 'Average Predicted Yield (tons/ha)',
                                data: values,
                                backgroundColor: 'rgba(96, 173, 94, 0.7)',
                                borderColor: 'rgba(46, 125, 50, 1)',
                                borderWidth: 1,
                                borderRadius: 5
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            scales: {
                                y: {
                                    beginAtZero: true
                                }
                            },
                            plugins: {
                                legend: {
                                    position: 'top',
                                }
                            }
                        }
                    });
                } else {
                    chartCanvas.parentElement.innerHTML = '<p class="text-center text-muted">No data available for charts yet.</p>';
                }
            })
            .catch(error => console.error('Error fetching chart data:', error));
    }
});

// Delete Record Functionality
function deleteRecord(id) {
    if (confirm('Are you sure you want to delete this record?')) {
        fetch('/delete/' + id, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Remove row from table
                const row = document.getElementById('row-' + id);
                row.style.animation = 'fadeInUp 0.5s ease reverse';
                setTimeout(() => row.remove(), 500);
            } else {
                alert('Error deleting record: ' + data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    }
}
