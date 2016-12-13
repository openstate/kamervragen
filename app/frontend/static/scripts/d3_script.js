//
// Subsidietrekker.nl
//
//  d3_script.js
//

var chart;
var chart_data;
var data;

d3.json('/_viz_streamer', function(error, json) {
    if (error) return console.warn(error);
    data = json;

    nv.addGraph(function() {
        chart = nv.models.pieChart()
            .x(function(d) {return d.key})
            .y(function(d) {return d.realisatie.sum})
            .showLabels(false).showLegend(false)
            .tooltipContent(function(obj, x, y, e) {
              return '<h3>' + obj.data.key + '</h3><p>' + accounting.formatMoney(obj.data.realisatie.sum, "€", 2, ".", ",") + '</p>';
            });

        chart_data = d3.select("#chart svg").datum(data);
        chart_data.transition().duration(350)
            .call(chart);

        nv.utils.windowResize(chart.update);
        return chart;
    });
});
