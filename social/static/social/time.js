var margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var formatDate = d3.time.format("%Y/%m/%d");

var x = d3.time.scale()
    .range([0, width]);

var y = d3.scale.linear()
    .range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom")
    .tickFormat(d3.time.format("%d/%m"));

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var line = d3.svg.line()
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.count); });

$(function() {var svg = d3.select("#lineChartContainer").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");});

d3.csv('/static/social/data.csv', function (error, data) {
  if (error) throw error;

    var maxDate = 0;
    var minDate = new Date();
    data.forEach(function(d) {
        d.dateString = d.Year + "/" + d.Month + "/" + d.Day;
        d.date = formatDate.parse(d.dateString);
        if(maxDate <= new Date(d.date)) maxDate = new Date(d.date);
        if(minDate >= new Date(d.date)) minDate = new Date(d.date);
    })

    var dateRange = ((maxDate - minDate)/(1000*60*60*24) + 1);
    var dateArray = [];
    for (var i = 0; i < dateRange; i++) {
        dateArray.push({"date": new Date().setTime(minDate.getTime() + (1000*60*60*24)*i), "count": 0});
    }

    for (var i = 0; i < data.length; i++) {
        dateArray[(data[i].date - minDate)/(1000*60*60*24)].count += 1;
    }

  x.domain(d3.extent(dateArray, function(d) { return d.date; }));
  y.domain([0, d3.max(dateArray, function(d) { return d.count; })]);

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Frequency");

  svg.append("path")
      .datum(dateArray)
      .attr("class", "line")
      .attr("d", line);
  });
