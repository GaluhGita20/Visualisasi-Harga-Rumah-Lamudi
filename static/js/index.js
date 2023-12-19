// SCATTERPLOT (LUAS BANGUNAN)
// set the dimensions and margins of the graph
var margin = {top: 10, right: 30, bottom: 40, left: 100},
    width = 460 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3.select("#scatterPlotLB")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

//Read the data
fetch('/get_scatterplot_dataLB')
.then(response => response.json()) // parse the response as JSON
    .then(data => {
    // do something with the data
    console.log(data);

    var dataEntries = d3.entries(data);

    // Add X axis
    var x = d3.scaleLinear()
      .domain([20, 100])
      .range([ 20, width]);

    var xAxis = svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

    // Add Y axis
    var y = d3.scaleLinear()
      .domain([0, 1000000000])
      .range([ height, 0]);
    svg.append("g")
      .call(d3.axisLeft(y));
    var yAxis = svg.append("g")
    .call(d3.axisLeft(y));


    // Line for X axis
    svg.append("line")
    .attr("x1", 0)
    .attr("x2", width)
    .attr("y1", height)
    .attr("y2", height)
    .attr("stroke", "black");
    
    // Line for Y axis
    svg.append("line")
    .attr("x1",  0)
    .attr("x2",  0)
    .attr("y1",  0)
    .attr("y2",  height)
    .attr("stroke", "black");

    var tooltip = d3.select("#scatterPlot")
      .append("div")
      .style("opacity", 0)
      .attr("class", "tooltip")
      .style("background-color", "white")
      .style("border", "solid")
      .style("border-width", "1px")
      .style("border-radius", "5px")
      .style("padding", "10px")

    var mouseover = function(d) {
      tooltip
        .style("opacity", 1)
    }

    var mousemove = function(d) {
      tooltip
        .html("The exact value of<br>the Building area is: " + d.key)
        .style("left", (d3.mouse(this)[0]+90) + "px") // It is important to put the +90: other wise the tooltip is exactly where the point is an it creates a weird effect
        .style("top", (d3.mouse(this)[1]) + "px")
    }

    // A function that change this tooltip when the leaves a point: just need to set opacity to 0 again
    var mouseleave = function(d) {
      tooltip
        .transition()
        .duration(200)
        .style("opacity", 0)
    }

    // Add dots
    svg.append('g')
      .selectAll("dot")
      .data(dataEntries) // the .filter part is just to keep a few dots on the chart, not all of them
      .enter()
      .append("circle")
        .attr("cx", function (d) { return x(d.key); } )
        .attr("cy", function (d) { return y(d.value); } )
        .attr("r", 7)
        .style("fill", "#69b3a2")
        .style("opacity", 0.3)
        .style("stroke", "white")
      .on("mouseover", mouseover )
      .on("mousemove", mousemove )
      .on("mouseleave", mouseleave )
})
.catch(error => console.error(error)); // handle any errors



// SCATTERPLOT (LUAS TANAH)
// set the dimensions and margins of the graph
var margin = {top: 10, right: 30, bottom: 40, left: 100},
    width = 460 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg2 = d3.select("#scatterPlotLT")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

//Read the data
fetch('/get_scatterplot_dataLT')
.then(response => response.json()) // parse the response as JSON
    .then(data => {
    // do something with the data
    console.log(data);

    var dataEntries = d3.entries(data);

    // Add X axis
    var x = d3.scaleLinear()
      .domain([30, 120])
      .range([ 30, width]);

    var xAxis = svg2.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

    // Add Y axis
    var y = d3.scaleLinear()
      .domain([0, 1000000000])
      .range([ height, 0]);
    svg2.append("g")
      .call(d3.axisLeft(y));
    var yAxis = svg2.append("g")
    .call(d3.axisLeft(y));


    // Line for X axis
    svg2.append("line")
    .attr("x1", 0)
    .attr("x2", width)
    .attr("y1", height)
    .attr("y2", height)
    .attr("stroke", "black");
    
    // Line for Y axis
    svg2.append("line")
    .attr("x1",  0)
    .attr("x2",  0)
    .attr("y1",  0)
    .attr("y2",  height)
    .attr("stroke", "black");

    var tooltip = d3.select("#scatterPlot")
      .append("div")
      .style("opacity", 0)
      .attr("class", "tooltip")
      .style("background-color", "white")
      .style("border", "solid")
      .style("border-width", "1px")
      .style("border-radius", "5px")
      .style("padding", "10px")

    var mouseover = function(d) {
      tooltip
        .style("opacity", 1)
    }

    var mousemove = function(d) {
      tooltip
        .html("The exact value of<br>the Building area is: " + d.key)
        .style("left", (d3.mouse(this)[0]+90) + "px") // It is important to put the +90: other wise the tooltip is exactly where the point is an it creates a weird effect
        .style("top", (d3.mouse(this)[1]) + "px")
    }

    // A function that change this tooltip when the leaves a point: just need to set opacity to 0 again
    var mouseleave = function(d) {
      tooltip
        .transition()
        .duration(200)
        .style("opacity", 0)
    }

    // Add dots
    svg2.append('g')
      .selectAll("dot")
      .data(dataEntries) // the .filter part is just to keep a few dots on the chart, not all of them
      .enter()
      .append("circle")
        .attr("cx", function (d) { return x(d.key); } )
        .attr("cy", function (d) { return y(d.value); } )
        .attr("r", 7)
        .style("fill", "#69b3a2")
        .style("opacity", 0.3)
        .style("stroke", "white")
      .on("mouseover", mouseover )
      .on("mousemove", mousemove )
      .on("mouseleave", mouseleave )
})
.catch(error => console.error(error)); // handle any errors



// HEATMAP
// set the dimensions and margins of the graph
var margin = {top: 10, right: 30, bottom: 40, left: 100},
    width = 900 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg4 = d3.select("#heatmap")
.append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
.append("g")
  .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");
        
//Read the data
d3.csv("static/data/heatmap_data.csv", function(data) {

  // Labels of row and columns -> unique identifier of the column called 'group' and 'variable'
  var myGroups = d3.map(data, function(d){return d.group;}).keys()
  var myVars = d3.map(data, function(d){return d.variable;}).keys()

  // Build X scales and axis:
  var x = d3.scaleBand()
    .range([ 0, 800 ])
    .domain(myGroups)
    .padding(0.05);
  svg4.append("g")
    .style("font-size", 15)
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x).tickSize(0))
    .select(".domain").remove()

  // Build Y scales and axis:
  var y = d3.scaleBand()
    .range([ height, 0 ])
    .domain(myVars)
    .padding(0.05);
  svg4.append("g")
    .style("font-size", 15)
    .call(d3.axisLeft(y).tickSize(0))
    .select(".domain").remove()

  // Build color scale
  var myColor = d3.scaleSequential()
    .interpolator(d3.interpolateInferno)
    .domain([-1,1])

  // create a tooltip
  var tooltip = d3.select("#heatmap")
    .append("div")
    .style("opacity", 0)
    .attr("class", "tooltip")
    .style("background-color", "white")
    .style("border", "solid")
    .style("border-width", "2px")
    .style("border-radius", "5px")
    .style("padding", "5px")

  // Three function that change the tooltip when user hover / move / leave a cell
  var mouseover = function(d) {
    tooltip
      .style("opacity", 1)
    d3.select(this)
      .style("stroke", "black")
      .style("opacity", 1)
  }
  var mousemove = function(d) {
    tooltip
      .html("The exact value of<br>this cell is: " + d.value)
      .style("left", (d3.mouse(this)[0]+70) + "px")
      .style("top", (d3.mouse(this)[1]) + "px")
  }
  var mouseleave = function(d) {
    tooltip
      .style("opacity", 0)
    d3.select(this)
      .style("stroke", "none")
      .style("opacity", 0.8)
  }

  // add the squares
  svg4.selectAll()
    .data(data, function(d) {return d.group+':'+d.variable;})
    .enter()
    .append("rect")
      .attr("x", function(d) { return x(d.group) })
      .attr("y", function(d) { return y(d.variable) })
      .attr("rx", 4)
      .attr("ry", 4)
      .attr("width", x.bandwidth() )
      .attr("height", y.bandwidth() )
      .style("fill", function(d) { return myColor(d.value)} )
      .style("stroke-width", 4)
      .style("stroke", "none")
      .style("opacity", 0.8)
    .on("mouseover", mouseover)
    .on("mousemove", mousemove)
    .on("mouseleave", mouseleave)
})

// Add title to graph
svg4.append("text")
        .attr("x", 0)
        .attr("y", -50)
        .attr("text-anchor", "left")
        .style("font-size", "22px")
        .text("A d3.js heatmap");

// Add subtitle to graph
svg4.append("text")
        .attr("x", 0)
        .attr("y", -20)
        .attr("text-anchor", "left")
        .style("font-size", "14px")
        .style("fill", "grey")
        .style("max-width", 400)
        .text("A short description of the take-away message of this chart.");
        
// LOLIPOP CHART
var margin = {top: 10, right: 30, bottom: 40, left: 100},
    width = 460 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg3 = d3.select("#lolipopchart")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

fetch('/get_lolipopchart_data')
.then(response => response.json()) // parse the response as JSON
    .then(data => {
    // do something with the data
    console.log(data);

    var dataEntries = d3.entries(data);
  // Add X axis
  var x = d3.scaleLinear()
    .domain([0, 5800])
    .range([ 0, width]);
  
  var xAxis = svg3.append("g")
  .attr("transform", "translate(0," + height + ")")
  .call(d3.axisBottom(x))
  .selectAll("text")
  .attr("transform", "translate(-10,0)rotate(-45)")
  .style("text-anchor", "end");
  
  // Y axis
  var y = d3.scaleBand()
    .range([ 0, height ])
    .domain(dataEntries.map(function(d) { return d.key; }))
    .padding(1);
  
  var yAxis = svg3.append("g")
    .call(d3.axisLeft(y));
  
  // Line for X axis
  svg3.append("line")
  .attr("x1", 0)
  .attr("x2", width)
  .attr("y1", height)
  .attr("y2", height)
  .attr("stroke", "black");
  
  // Line for Y axis
  svg3.append("line")
  .attr("x1",  0)
  .attr("x2",  0)
  .attr("y1",  0)
  .attr("y2",  height)
  .attr("stroke", "black");
  
  
  // Lines
  svg3.selectAll("myline")
    .data(dataEntries)
    .enter()
    .append("line")
      .attr("x1", function(d) { return x(d.value); })
      .attr("x2", x(0))
      .attr("y1", function(d) { return y(d.key); })
      .attr("y2", function(d) { return y(d.key); })
      .attr("stroke", "grey")
  
  // Circles
  svg3.selectAll("mycircle")
    .data(dataEntries)
    .enter()
    .append("circle")
      .attr("cx", function(d) { return x(d.value); })
      .attr("cy", function(d) { return y(d.key); })
      .attr("r", "4")
      .style("fill", "#69b3a2")
      .attr("stroke", "black")
})
.catch(error => console.error(error)); // handle any errors