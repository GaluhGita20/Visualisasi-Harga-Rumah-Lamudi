// Variabel lebar dan tinggi svg
var width = 800;
var height = 600;

// Proyeksi dan path
var projection = d3.geoMercator()
  .center([110, -7])
  .scale(5000)
  .translate([width / 2, height / 2]);
               //400 , 300
var path = d3.geoPath()
  .projection(projection);

// Buat elemen svg
var svg = d3.select("#map")
  .append("svg")
  .attr("width", width)
  .attr("height", height);

// Memuat data GeoJSON
d3.json("C://web data viz/visualisasi-harga-rumah-lamudi/templates/kabupaten-bali.geojson").then(function(data) {
  // Menggambar fitur-fitur peta
  svg.selectAll("path")
    .data(data.features)
    .enter()
    .append("path")
    .attr("class", "province")
    .attr("d", path);
});
