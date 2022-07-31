var loadChart = function( temperature, humidity, timestamps) {
    var ctx = $('#myChart');
    
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: timestamps,
            datasets: [
                {
                    label: "Temperature",
                    data: temperature,
                    fill: false,
                    borderColor: "rgb(255, 0, 0)",
                    lineTension: 0.1
                },
                {
                    label: "Humidity",
                    data: humidity,
                    fill: false,
                    borderColor: "rgb(0, 0, 255)",
                    lineTension: 0.1
                }
            ]
        },
        options: {
            title: {
                display: true,
                text: 'Timestamps',
                position: 'bottom'
            }
        }
    });
}
