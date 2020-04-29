<!-- Code from d3-graph-gallery.com -->
<!DOCTYPE html>
<html>
  <head>
    <title>Earth Dashboard</title>


<meta charset="utf-8">

<!-- Load d3.js -->
<script src="https://d3js.org/d3.v5.js"></script>

<!-- Color palette -->
<script src="https://d3js.org/d3-scale-chromatic.v1.min.js"></script>
<script src="https://d3js.org/d3-color.v1.min.js"></script>
<script src="https://d3js.org/d3-interpolate.v1.min.js"></script>
<script src="https://d3js.org/d3-scale-chromatic.v1.min.js"></script>
<script>

var yellow = d3.interpolateYlGn(0), // "rgb(255, 255, 229)"
    yellowGreen = d3.interpolateYlGn(0.5), // "rgb(120, 197, 120)"
    green = d3.interpolateYlGn(1); // "rgb(0, 69, 41)"

</script>
<div id="title-text">

          <h1>Biases in Bubbles:</h1>
          <h2>The Spread of COVID-19: Confirmed Cases vs Population</h2>
          <p>One goal of data visualization is to communicate information that accounts for both accuracy and depth. In this case, we have a high level of accuracy, but no accounting for the different populations of each country. </p>

        </div>
<!-- Create a div where the graph will take place -->
<div id="bubble"></div>

<style>
.node:hover{
  stroke-width: 7px !important;
  opacity: 1 !important;
}
</style>

<script>

// set the dimensions and margins of the graph
var width = 960
var height = 460

// append the svg object to the body of the page
var svg = d3.select("#bubble")
  .append("svg")
    .attr("width", width)
    .attr("height", height)

// Read data
// d3.csv("https://raw.githubusercontent.com/Lambda-School-Labs/earth-dashboard-ds/feature/flask_rc1/FLASK_RC1/static/merged.csv", function(data) {
  d3.json('static/summary.json').then(function(data) {
      console.log(data);
      document.getElementById("d3-write-here").innerHTML = data;
  // Filter a bit the data -> more than 1 confirmed case
  data = data.filter(function(d){ return d.TotalConfirmed>0 })

  // Color palette for continents?
  var color = d3.scaleOrdinal()
    .range(d3.schemeTableau10);

  // Size scale for countries
  var size = d3.scaleLinear()
    .domain([0, 800000])
    .range([7,75])  // circle will be between 7 and 55 px wide

  // create a tooltip
  var Tooltip = d3.select("#bubble")
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
    Tooltip
      .style("opacity", 1)
  }
  var mousemove = function(d) {
    Tooltip
      .html('<u>' + d.Country + '</u>' + "<br>" + d.TotalConfirmed + " confirmed cases to date")
      .style("left", (d3.mouse(this)[0]+20) + "px")
      .style("top", (d3.mouse(this)[1]) + "px")
  }
  var mouseleave = function(d) {
    Tooltip
      .style("opacity", 0)
  }

  // Initialize the circle: all located at the center of the svg area
  var node = svg.append("g")
    .selectAll("circle")
    .data(data)
    .enter()
    .append("circle")
      .attr("class", "node")
      .attr("r", function(d){ return size(d.TotalConfirmed)})
      .attr("cx", width / 2)
      .attr("cy", height / 2)
      .style("fill", function(d){ return color(d.Country)})
      .style("fill-opacity", 0.8)
      .attr("stroke", "black")
      .style("stroke-width", 1)
      .on("mouseover", mouseover) // What to do when hovered
      .on("mousemove", mousemove)
      .on("mouseleave", mouseleave)
      .call(d3.drag() // call specific function when circle is dragged
           .on("start", dragstarted)
           .on("drag", dragged)
           .on("end", dragended));

  // Features of the forces applied to the nodes:
  var simulation = d3.forceSimulation()
      .force("center", d3.forceCenter().x(width / 2).y(height / 2)) // Attraction to the center of the svg area
      .force("charge", d3.forceManyBody().strength(.1)) // Nodes are attracted one each other of value is > 0
      .force("collide", d3.forceCollide().strength(.2).radius(function(d){ return (size(d.TotalConfirmed)+3) }).iterations(1)) // Force that avoids circle overlapping

  // Apply these forces to the nodes and update their positions.
  // Once the force algorithm is happy with positions ('alpha' value is low enough), simulations will stop.
  simulation
      .nodes(data)
      .on("tick", function(d){
        node
            .attr("cx", function(d){ return d.x; })
            .attr("cy", function(d){ return d.y; })
      });

  // What happens when a circle is dragged?
  function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(.03).restart();
    d.fx = d.x;
    d.fy = d.y;
  }
  function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
  }
  function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(.03);
    d.fx = null;
    d.fy = null;
  }

})


</script>
<br><br>
<div id="title-text">
          <p>The better way to illustrate this data would be to look at confirmed cases per 100,000 people in each country.</p>
          <p>This way we could determine if one country has a higher rate of infection than another.</p>
          <br><br><br><br>

        </div>


      </body>
    </html>
