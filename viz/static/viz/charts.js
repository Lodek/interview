
function comboChartOptionFactory(hAxis) {
    return {
        vAxis: {
            title: 'Score',
            minValue: 0,
            maxValue: 10,
        },
        hAxis: {
            title: hAxis,
        },
        seriesType: 'bars',
        width: 900,
        height: 400,
    }
    

}
