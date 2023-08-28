function createPlot(frequencies, displayElement) {
    let letras = frequencies.map(function (item) {
        return item[0];
    });


    let percentages = frequencies.map(function (item) {
        return item[1];
    });

    let trace = {
        x: letras, y: percentages, text: percentages.map(function (valor) {
            return valor.toFixed(2) + '%';
        }), type: 'bar', marker: {
            color: 'blue' // Puedes personalizar el color de las barras aquí
        }
    };

    let layout = {
        title: 'Frecuencia de letras en porcentaje', xaxis: {
            title: 'Letra'
        }, yaxis: {
            title: 'Porcentaje (%)'
        }, paper_bgcolor: 'white', plot_bgcolor: 'white', font: {
            color: 'black'
        }, autosize: true,
    };
    var config = {
        displayModeBar: true,
        displaylogo: false,
        toImageButtonOptions: {
            format: 'png', filename: 'grafico', width: 800, height: 600
        },
        modeBarButtonsToRemove: ['sendDataToCloud', 'pan2d', 'pan3d', 'resetScale2d', 'hoverClosestCartesian', 'hoverCompareCartesian'],
        responsive: true
    };

    var data = [trace];

    // Crea el gráfico en el elemento con el ID 'tuDiv'
    Plotly.newPlot(displayElement, data, layout, config);
}