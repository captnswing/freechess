var chart;
$(document).ready(function() {

    var options = {
        chart: {
            renderTo: 'highchart',
            type: 'line'
        },
        title: {
            text: 'Elohist'
        },
        series: [{}]
    };

    $.ajax({
        url: 'http://127.0.0.1:8000/api/elohist',
        dataType: 'json',
        success: function(data) {
            console.log(data)
            options.series[0].data = data;
            chart = new Highcharts.Chart(options);
        }
    });
});
