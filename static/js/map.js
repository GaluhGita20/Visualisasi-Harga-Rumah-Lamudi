//BAR=================================================================================================
  var myData = document.getElementById("myElement").dataset.data;
  json_data = JSON.parse(myData)
  // Data untuk chart
  var data1 = json_data
  console.log(data1)

  // Lebar dan tinggi grafik
  var width1 = 1100;
  var height1 = 400;

  // Skala x
  var x = d3.scaleBand()
      .domain(data1.map(function(d) {
        return d.kabupaten; }))
      .range([0, width1])
      .padding(0.2);

  // Skala y
  var y = d3.scaleLinear()
      .domain([0, d3.max(data1, function(d) {
        return d.hasil_prediksi +97000000; })])
      .range([height1, 0]);

  // Membuat grafik
  var svg1 = d3.select('#barchart')
      .attr('width', width1)
      .attr('height', height1);

  var target2 = null
  var kabTarget1 = document.getElementById("target");
  if (kabTarget1 == null){
    target2 = null
  }else{
    var target1 = kabTarget1.innerHTML;
    var valTarget1 = target1.toUpperCase();
    target2 = valTarget1
  }

  var bars = svg1.selectAll('.bar')
      .data(data1)
      .enter()
      .append('rect')
      .attr("fill",function(d){
        if(d.kabupaten === target2){
          return "#0cd113"
        }else{
          return "#014003"
        }
      })
      .attr('class', 'bar')
      .attr('x', function(d) { 

        return x(d.kabupaten); })
      .attr('y', function(d) { return y(d.hasil_prediksi); })
      .attr('width', x.bandwidth())
      .attr("font-weight","bold")
      .attr('height', function(d) { return height1 - y(d.hasil_prediksi); });

  // Menambahkan label pada setiap batang
  var labels = svg1.selectAll('.label')
      .data(data1)
      .enter()
      .append('text')
      .attr('class', 'label')
      .attr('x', function(d) { return x(d.kabupaten) + x.bandwidth() / 2; })
      .attr('y', function(d) { return y(d.hasil_prediksi)-10; })
      .attr('text-anchor', 'middle')
      .attr("font-weight","bold")
      .attr("fill","black")
      .text(function(d) { return d.hasil_prediksi.toLocaleString(); });

      svg1.selectAll('.bar')
      .data(data1)
      .enter()
      .append('rect')
      .attr('class', 'bar')
      .attr('x', function(d) { return x(d.kabupaten); })
      .attr('y', function(d) { return y(d.hasil_prediksi); })
      .attr('width', x.bandwidth())
      .attr('height', function(d) { return height1 - y(d.hasil_prediksi.toLocaleString()); })
      .attr('rx', 15) // Menambahkan sudut melengkung pada batang
      .attr('ry', 15) // Menambahkan sudut melengkung pada batang
      .attr('stroke', 'black') // Menambahkan garis tepi pada batang
      .attr("fill",function(d){
        if(d.kabupaten == "BADUNG"){
          return "#0cd113"
        }else{
          return "#014003"
        }
      })
      .attr('stroke-width', 2); // Menentukan ketebalan garis tepi

  // Menambahkan sumbu x
  svg1.append('g')
      .attr('transform', 'translate(0,' + height1 + ')')
      .attr("font-weight","bold")
      .call(d3.axisBottom(x));
   

  // Menambahkan sumbu y
  //svg1.append('g')
    //  .call(d3.axisLeft(y));


    

//MAPS====================================================================================================
    const width = 1200;
    const height = 400;

    const projection = d3.geoMercator()
    .center([115.1889, -8.4095]) // Koordinat tengah peta
    .scale(28000) // Skala peta
    .translate([width / 2, height / 2]); // Posisi peta di SVG
  
    const path = d3.geoPath()
      .projection(projection);

    //membuat elemen svg
    const svg = d3.select("#map")
      .append("svg")
      .attr("width", width)
      .attr("height", height);

    var myData = document.getElementById("myElement").dataset.data;
    json_data = JSON.parse(myData)
    console.log(json_data)

    //var jsonData = JSON.parse('{{ values[1]|tojson }}');
    //console.log(jsonData)

    var dataf = json_data
    //var dataf = myData;
    hasilPrediksi=[]
    //console.log(dataf[0].kepadatan_penduduk)
    dataf.forEach(item => {
      // Tambahkan elemen ke dalam array
      hasilPrediksi.push(item.hasil_prediksi);
    });
    var target = null
    var kabTarget = document.getElementById("target");
    if (kabTarget == null){
      target = null
    }else{
      var target1 = kabTarget.innerHTML;
      var valTarget1 = target1.toUpperCase();
      target = valTarget1
    }

    console.log(hasilPrediksi)
    console.log(dataf)
    var domain = [500000000, 1000000000, 2000000000]; // Rentang nilai kepadatan penduduk
    var range = ['#017805','#014003','#012003']

    var colorScale = d3.scaleThreshold()
      .domain(domain)
      .range(range);
    
    d3.json("https://raw.githubusercontent.com/teguha/peta-bali/main/kabupaten-bali.geojson").then(function(data){
        //console.log(data.features)
            //menampilkan peta bali
        svg.selectAll("path")
            .data(data.features)
            .enter()
            .append("path")
            .attr("d", path)
            .attr("stroke",'white')
            .attr("stroke-width",0.7)
            //.attr("x", 80) // Koordinat X posisi teks
            //.attr("y", -4) // Koordinat Y posisi teks
            //.text("Keterangan teks")
            .attr("class","district")
            .attr('fill',function(d){
                var rs = dataf.find(function(element) {
                    element.kabupaten === d.properties.nm_kabkota
                    return element.hasil_prediksi
                });
                
                if (rs != null){
                  return colorScale(rs.hasil_prediksi)
                }else{
                  return "#080202"
                }
            }).attr('fill',function(d){

                if (d.properties.nm_kabkota == "DENPASAR"){
                    console.log(d.properties.nm_kabkota)
                    return "#D3D04F";
                }
            })
            .on("mouseover", function(event, d) {
              d3.select(this)
              var result = dataf.find(function(element) {
                  return element.kabupaten === d.properties.nm_kabkota;
              });
                    
              if (result != undefined){
                  svg
                    .append("text")
                    //.attr("fill", colorScale(result.kepadatan_penduduk))
                    .attr("id", "tooltip1")
                    .attr("x", event.pageX -390)
                    .attr("y", event.pageY -430)
                    .style("font-weight", "bold")
                    .attr("fill",'orange')
                    .text("Rp."+result.hasil_prediksi.toLocaleString());
              }
              svg
                .append("text")
                .attr("id", "tooltip")
                .style("font-weight", "bold")
                .attr("fill",'orange')
                .attr("x", event.pageX -390)
                .attr("y", event.pageY - 410)
                .text(d.properties.nm_kabkota);

        })
        .on("mouseout", function() {
          //d3.select(this).attr("fill", "black");
          svg.select("#tooltip").remove();
          svg.select("#tooltip1").remove();
        }).attr("fill",function(d){
            
          var rs = dataf.find(function(element) {
            return element.kabupaten === d.properties.nm_kabkota
          });  

          if (d.properties.nm_kabkota==target){
            return "#0cd113"
          }

          //console.log(rs)
          if (rs != null){
            return colorScale(rs.hasil_prediksi)
          }else{
            return "#080202"
          }
        });
        
    })

