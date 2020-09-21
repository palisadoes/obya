  function invertvisibility(d){
      //Invert line visibility
      var active   = d.active ? false : true,
      newOpacity = active ? 0 : 1;
      // Hide or show the elements based on the ID
      thetag = '#whip' + d.id.replace(/ |\/|\./g,'');
      d3.selectAll(thetag)
        .transition().duration(1000)
        .style("opacity", newOpacity);
      // Update whether or not the elements are active
      d.active = active;
  }
  function drawAllPDUPanelFailoverBarChart( url, div_id, heading, subheading_1, subheading_2, y_label ) {
    //This script will draw bar charts for PDU loading, failover version
    var margin = {top: 20, right: 50, bottom: 20, left: 50};
    var phaseWidth = 900;
    var phaseHeight = 5;
    var phasePadding = 1;
    var panelWidth = 15;
    var panelPadding = 2;
    var panelHeight = 3 * (phaseHeight + phasePadding) + panelPadding;
    var totalPanels = 72;
    var deviceWidth = 120;
    var devicePadding = 10;
    var topLabelBox = 20;
    var innerWidth = phaseWidth + panelWidth + deviceWidth;
    var outerWidth = innerWidth + margin.left + margin.right;
    var innerHeight = totalPanels * panelHeight;
    var outerHeight = innerHeight + topLabelBox + margin.top + margin.bottom;

    var legendBoxSize = 10;
    var legendStartYAxis = outerHeight - margin.bottom - margin.top - legendBoxSize;

    // Setup standard colors
    var standard_colors = d3.scaleOrdinal(d3.schemeCategory10);
    var breaker_colors = d3.scaleOrdinal(['#FFC000', '#FF0000', '#FFFF00', '#C0FF00', '#C0C000', '#C00000']);

    // Define the limits of the SVG canvas
    var svg = d3.select(div_id).append('svg')
      .attr('width', outerWidth)
      .attr('height', outerHeight);

    // Put labels above the graph area
    var tlb = svg.append('g')
      .attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')');
    var devicelabel = tlb.append('text')
      .attr('x', 0)
      .attr('y', 0)
      .style('font', '15px sans-serif')
      .style('fill', '#000000')
      .text('Device');
    var panellabel = tlb.append('text')
      .attr('x', deviceWidth)
      .attr('y', 0)
      .style('font', '15px sans-serif')
      .style('text-anchor', 'middle')
      .style('fill', '#000000')
      .text('Panel');
    var ampslabel = tlb.append('text')
      .attr('x', deviceWidth + panelWidth + phaseWidth / 2)
      .attr('y', 0)
      .style('font', '15px sans-serif')
      .style('fill', '#000000')
      .style('text-anchor', 'middle')
      .text('Amps');
    var breakerlabel = tlb.append('text')
      .attr('x', deviceWidth + panelWidth + phaseWidth)
      .attr('y', 0)
      .style('font', '15px sans-serif')
      .style('fill', '#000000')
      .style('text-anchor', 'middle')
      .text('Breaker');

    // Define the graph area on the canvas
    var g = svg.append('g')
      .attr('transform', 'translate(' + margin.left + ', ' + (topLabelBox + margin.top) + ')');

    // Add please wait text
    var pleasewait = g.append('text')
      .attr('x', innerWidth / 2)
      .attr('y', innerHeight / 4)
      .style('font', '45px sans-serif')
      .style('fill', '#404040')
      .style('text-anchor', 'middle')
      .text('Loading data, please stand by...');

    // Load the chart data
    d3.tsv(url, function(error, data) {
      if (error) {pleasewait.text = error; throw error;}
      // remove the please wait text
      pleasewait.remove();

      //clean up the data fields
      data.forEach(function(d) {
          d.load = parseInt(+d.load);
          d.headroom = +d.headroom;
          d.panel = +d.panel;
          d.phase = ['A', 'B', 'C'][+d.phase-1];
          d.breaker = +d.breaker;
      });
      var phaseBarBlue = [0, 63, 127];
      // group data by PDU, Panel, Phase
      var pdus = d3.nest()
        .key(function(d) {return d.device;}).sortKeys(d3.ascending)
        .key(function(d) {return d.panel;}).sortKeys(d3.ascending)
        .key(function(d) {return d.phase;}).sortKeys(d3.ascending)
        .entries(data);

      var nextDeviceTop = 0
      pdus.forEach(function(devices) {
        var barscale = d3.scaleLinear().range([0, phaseWidth]);
        // This is a PDU device
        pdu=g.append('g')
          .attr('transform', 'translate(0, ' + nextDeviceTop + ')');
        var deviceHeight = panelHeight * devices.values.length;
        nextDeviceTop = nextDeviceTop + devicePadding;
        pdu.append('text')
          .attr('x', 0)
          .attr('y', deviceHeight / 2)
          .style('font', '12px sans-serif')
          .style('fill', standard_colors(devices.key))
          .style('text-anchor', 'left')
          .text(devices.key);
        devices.values.forEach(function(panels, pnli) {
          // Create each panel
          nextDeviceTop = nextDeviceTop + panelHeight;
          device = pdu.append('g')
            .attr('transform', 'translate(' + deviceWidth + ', ' + pnli * (panelHeight + panelPadding) + ')');
          device.append('text')
            .attr('x', 0)
            .attr('y', panelHeight / 2)
            .style('font', '10px sans-serif')
            .style('fill', standard_colors(panels.key))
            .style('text-anchor', 'left')
            .text(panels.key);
          panels.values.forEach(function(phases, phi) {
            // Create one bar per phase
            panel = device.append('g')
              .attr('transform', 'translate(' + panelWidth + ', ' + phi * (phaseHeight + phasePadding) + ')');
            phaseHeadroom = phases.values[0].headroom;
            breakerPop = phases.values[0].breaker;
            phaseCurrent = phases.values[0].load;
            barscale.domain([0,breakerPop]);
            // start with a green bar
            phaseRed = 0;
            phaseGreen = 255;
            if(phaseHeadroom < 30) { //green to yellow bar
              phaseRed = (phaseHeadroom - 20) * 255 / 10;
              phaseGreen = 255;
            }
            if(phaseHeadroom < 20) { //yellow to red bar
              phaseRed = 255;
              phaseGreen = (phaseHeadroom - 10) * 255 / 10;
            }
            if(phaseHeadroom < 10) { //red bar
              phaseRed = 255;
              phaseGreen = 0;
            }
            phasebar = panel.append('rect')
              .attr('x', 0)
              .attr('y', 0)
              .attr('width', barscale(phaseCurrent))
              .attr('height', phaseHeight)
              .attr('class', 'bar')
              .style('fill', d3.rgb(phaseRed, phaseGreen, phaseBarBlue[phi]));
            phasetext = phasebar.append('svg:title')
              .text(devices.key +
                    ' Panel ' +
                    panels.key +
                    ' Phase ' +
                    phases.key +
                    ': ' +
                    phases.values[0].load +
                    ' Amps');
            breakerline = panel.append('rect')
              .attr('x', barscale(breakerPop))
              .attr('y', 0)
              .attr('width', 2)
              .attr('height', phaseHeight + phasePadding + devicePadding + panelPadding)
              .attr('fill', breaker_colors(breakerPop))
              .append('svg:title')
                .text('Breaker: ' + breakerPop + ' Amps');
          });
        });
      });
    });
  }


  function drawPDUFailoverLineChart( url, div_id, max_value_line, heading, subheading_1, subheading_2, subheading_3, subheading_4, y_label ) {
    //
    // This script creates the charts for customer cabinet power and bandwidth data
    //
    // Args:
    //  url: URL from which to retrieve data.tsv file
    //  div_id: Div ID to match chart to javascript
    //  max_value_line: Maximum value that should have a line
    //  heading: Heading for chart
    //  subheading_1: First sub heading
    //  subheading_2: Second sub heading
    //  subheading_3: Third sub heading
    //  subheading_4: Fourth sub heading
    //  y_label: Label to use for y axis
    //
    // Initialise key variables
    var margin = {top: 20, right: 300, bottom: 50, left: 80};
    var headingVOffset = 0;
    var outerWidth = 1300;
    var outerHeight = 650;
    var innerWidth = outerWidth - margin.left - margin.right;
    var innerHeight = outerHeight - margin.top - margin.bottom;

    var legendBoxSize = 10;
    var legendStartYAxis = outerHeight - margin.bottom - margin.top - legendBoxSize;

    // Setup standard colors
    var standard_colors = d3.scaleOrdinal(d3.schemeCategory10);

    // Define the limits of the SVG canvas
    var svg = d3.select(div_id).append('svg')
      .attr('width', outerWidth)
      .attr('height', outerHeight);

    // Define the graph area on the canvas
    var g = svg.append('g')
      .attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')');

    // Set scales and colors for chart area
    var x = d3.scaleTime().range([0, innerWidth]),
        y = d3.scaleLinear().range([innerHeight, 0]),
        kwMaxScale = d3.scaleLinear().range([innerHeight, 0]),
        kwCommitScale = d3.scaleLinear().range([innerHeight, 0]);

    // Define each line
    var line = d3.line()
        .curve(d3.curveBasis)
        .x(function(d) { return x(d.date); })
        .y(function(d) { return y(d.watts); });

    // Get the data, parse out the columns for dates and watts
    d3.json(url, function(error, data) {
      if (error) throw error;
      // https://bl.ocks.org/jqadrad/a58719d82741b1642a2061c071ae2375

      // Get the labels for the line charts based on the very
      // first dictionary in the list
      standard_colors.domain(d3.keys(data[0]).filter(function(key) {
        return key !== 'date';
      }));

      // Convert the 'date' keys from Epoch timestamps to date values
      data.forEach(function(d) {
        d.date = new Date(d.date * 1000);
      });

      // Create separate lists date-value key-value pairs for charting
      var whips = standard_colors.domain().map(function(id) {
        return {
          id: id,
          values: data.map(function(d) {
            return {date: d.date, watts: d[id]};
          })
        };
      });

      // Define the min / max limits (extent) of the X domain
      x.domain(d3.extent(data, function(d) { return d.date; }));

      // Define the min / max limits of the Y domain. In this case we don't use the extent.
      // We use '0' as the minimum, and the max value as the max watts.
      // We could set the minimum to be the minimum watts by replacing the '0' with
      // d3.min(whips, function(c) { return d3.min(c.values, function(d) { return d.watts; }); })
      var kw_max = d3.max(whips, function(c) { return d3.max(c.values, function(d) { return d.watts; }); });
      if (max_value_line == 0) {
          var ymax = kw_max;
      } else {
          var ymax = Math.max(kw_max, max_value_line);
      }
      y.domain([0, ymax]);

      // Define the min / max limits (extent) of the kW commits and max
      kwMaxScale.domain([0, ymax]);
      kwCommitScale.domain([0, ymax]);

      // Define the domain for the colors
      standard_colors.domain(whips.map(function(c) { return c.id; }));

      // Define formatting for X axis lines and labels
      g.append('g')
          .attr('class', 'axis axis--x')
          .attr('transform', 'translate(0,' + innerHeight + ')')
          .call(d3.axisBottom(x)
            .tickFormat(d3.timeFormat('%Y-%m-%d %H:%M')))
          .selectAll("text")
                  .style("text-anchor", "end")
                  .attr("dx", "-.8em")
                  .attr("dy", ".15em")
                  .attr("transform", "rotate(-20)");

      // Define formatting for Y axis lines and labels (Rotation)
      g.append('g')
          .attr('class', 'axis axis--y')
          .call(d3.axisLeft(y))
        .append('text')
          .attr('transform', 'rotate(-90)')
          .attr('y', 6)
          .attr('dy', '0.71em')
          .attr('fill', '#000000')
          .text(y_label);

      // Draw the max line on chart
      if (max_value_line != 0) {

        // Maximum value line
        g.append('line')
            .attr('x1', 0)
            .attr('x2', innerWidth)
            .attr('y1', kwCommitScale(max_value_line))
            .attr('y2', kwCommitScale(max_value_line))
            .style('stroke-width', 1)
            .style('stroke', '#DC143C');

        // Maximum value text
        g.append('text')
            .attr('x', innerWidth + 5)
            .attr('y', kwCommitScale(max_value_line))
            .style('font', '10px sans-serif')
            .text('Breaker Size');

            //headingVOffset = innerHeight - 100;
            headingVOffset = 50;
      }

      // Add a heading
      var mainHeading = g.append('text')
        .attr('x', innerWidth + (legendBoxSize * 2))
        .attr('y', 20 + headingVOffset)
        .style('font', '30px sans-serif')
        .style('fill', '#404040')
        .text(heading);

      // Add a sub-heading
      var subHeading_1 = g.append('text')
        .attr('x', innerWidth + (legendBoxSize * 2))
        .attr('y', 50 + headingVOffset)
        .style('font', '20px sans-serif')
        .style('fill', '#808080')
        .text(subheading_1);

      var subHeading_2 = g.append('text')
        .attr('x', innerWidth + (legendBoxSize * 2))
        .attr('y', 80 + headingVOffset)
        .style('font', '15px sans-serif')
        .style('fill', '#AAAAAA')
        .text(subheading_2);

      var subHeading_3 = g.append('text')
        .attr('x', innerWidth + (legendBoxSize * 2))
        .attr('y', 110 + headingVOffset)
        .style('font', '15px sans-serif')
        .style('fill', '#AAAAAA')
        .text(subheading_3);

      var subHeading_4 = g.append('text')
        .attr('x', innerWidth + (legendBoxSize * 2))
        .attr('y', 140 + headingVOffset)
        .style('font', '15px sans-serif')
        .style('fill', '#AAAAAA')
        .text(subheading_4);

      // Put in a legend for each whip
      var legend = g.selectAll('.whip')
        .data(whips)
        .enter()
        .append('g')
        .attr('class', 'legend');

      // Location and colors of legend icon squares for each line
      legend.append('rect')
        .attr('x', innerWidth + (legendBoxSize * 2))
        .attr('y', function(d, i) {
          return legendStartYAxis - (i * legendBoxSize * 2);
        })
        .attr('width', legendBoxSize)
        .attr('height', legendBoxSize)
        .attr('id', function(d) { return 'whip' + d.id.replace(/ |\/|\./g,'')})
        .on("click", function(d) {invertvisibility(d)})
        .style('fill', function(d) {
          return standard_colors(d.id);
        });

      legend.append('text')
        .attr('x', innerWidth + (legendBoxSize * 4))
        .attr('y', function(d, i) {
          return legendStartYAxis - (i * legendBoxSize * 2) + legendBoxSize;
        })
        .on("click", function(d) {invertvisibility(d)})
        .text(function(d) {
          return d.id;
        })
        .style('font', '10px sans-serif');

      // Make the chart area aware of the data to be placed
      var whip = g.selectAll('.whip')
        .data(whips)
        .enter().append('g')
          .attr('class', 'whip');

      // Define the colors to be used for each line path
      whip.append('path')
          .attr('class', 'line')
          .attr('d', function(d) { return line(d.values); })
          .attr('id', function(d) { return 'whip' + d.id.replace(/ |\/|\./g,'')})
          .on("click", function(d) {invertvisibility(d)})
          .style('stroke', function(d) { return standard_colors(d.id); });

      // Clean up line
      whip.exit().remove();

    });

  }

  function drawPDUPanelLineChart( url, div_id, heading, subheading_1, subheading_2, y_label ) {
    //
    // This script creates the charts for customer cabinet power and bandwidth data
    //
    // Args:
    //  url: URL from which to retrieve data.tsv file
    //  div_id: Div ID to match chart to javascript
    //  heading: Heading for chart
    //  subheading_1: First sub heading
    //  subheading_2: Second sub heading
    //  y_label: Label to use for y axis
    //
    // Initialise key variables
    var margin = {top: 20, right: 250, bottom: 50, left: 50};
    var headingVOffset = 0;
    var outerWidth = 1050;
    var outerHeight = 400;
    var innerWidth = outerWidth - margin.left - margin.right;
    var innerHeight = outerHeight - margin.top - margin.bottom;

    var legendBoxSize = 10;
    var legendStartYAxis = outerHeight - margin.bottom - margin.top - legendBoxSize;

    // Setup standard colors
    var standard_colors = d3.scaleOrdinal(d3.schemeCategory10);

    // Define the limits of the SVG canvas
    var svg = d3.select(div_id).append('svg')
      .attr('width', outerWidth)
      .attr('height', outerHeight);

    // Define the graph area on the canvas
    var g = svg.append('g')
      .attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')');

    // Set scales and colors for chart area
    var x = d3.scaleTime().range([0, innerWidth]),
        y = d3.scaleLinear().range([innerHeight, 0]),
        kwMaxScale = d3.scaleLinear().range([innerHeight, 0]),
        kwCommitScale = d3.scaleLinear().range([innerHeight, 0]);

    // Define each line
    var line = d3.line()
        .curve(d3.curveBasis)
        .x(function(d) { return x(d.date); })
        .y(function(d) { return y(d.watts); });

    // Get the data, parse out the columns for dates and watts
    d3.json(url, function(error, data) {
      if (error) throw error;
      // https://bl.ocks.org/jqadrad/a58719d82741b1642a2061c071ae2375

      // Get the labels for the line charts based on the very
      // first dictionary in the list
      standard_colors.domain(d3.keys(data[0]).filter(function(key) {
        return key !== 'date';
      }));

      // Convert the 'date' keys from Epoch timestamps to date values
      data.forEach(function(d) {
        d.date = new Date(d.date * 1000);
      });

      // Create separate lists date-value key-value pairs for charting
      var whips = standard_colors.domain().map(function(id) {
        return {
          id: id,
          values: data.map(function(d) {
            return {date: d.date, watts: d[id]};
          })
        };
      });

      // Define the min / max limits (extent) of the X domain
      x.domain(d3.extent(data, function(d) { return d.date; }));

      // Define the min / max limits of the Y domain. In this case we don't use the extent.
      // We use '0' as the minimum, and the max value as the max watts.
      // We could set the minimum to be the minimum watts by replacing the '0' with
      // d3.min(whips, function(c) { return d3.min(c.values, function(d) { return d.watts; }); })
      var kw_max = d3.max(whips, function(c) { return d3.max(c.values, function(d) { return d.watts; }); });
      var ymax = kw_max;
      y.domain([0, ymax]);

      // Define the min / max limits (extent) of the kW commits and max
      kwMaxScale.domain([0, ymax]);
      kwCommitScale.domain([0, ymax]);

      // Define the domain for the colors
      standard_colors.domain(whips.map(function(c) { return c.id; }));

      // Define formatting for X axis lines and labels
      g.append('g')
          .attr('class', 'axis axis--x')
          .attr('transform', 'translate(0,' + innerHeight + ')')
          .call(d3.axisBottom(x)
            .tickFormat(d3.timeFormat('%Y-%m-%d')))
          .selectAll("text")
                  .style("text-anchor", "end")
                  .attr("dx", "-.8em")
                  .attr("dy", ".15em")
                  .attr("transform", "rotate(-20)");

      // Define formatting for Y axis lines and labels (Rotation)
      g.append('g')
          .attr('class', 'axis axis--y')
          .call(d3.axisLeft(y))
        .append('text')
          .attr('transform', 'rotate(-90)')
          .attr('y', 6)
          .attr('dy', '0.71em')
          .attr('fill', '#000000')
          .text(y_label);

      // Add a heading
      var mainHeading = g.append('text')
        .attr('x', innerWidth + (legendBoxSize * 2))
        .attr('y', 20 + headingVOffset)
        .style('font', '30px sans-serif')
        .style('fill', '#404040')
        .text(heading);

      // Add a sub-heading
      var subHeading_1 = g.append('text')
        .attr('x', innerWidth + (legendBoxSize * 2))
        .attr('y', 50 + headingVOffset)
        .style('font', '20px sans-serif')
        .style('fill', '#808080')
        .text(subheading_1);

      var subHeading_2 = g.append('text')
        .attr('x', innerWidth + (legendBoxSize * 2))
        .attr('y', 80 + headingVOffset)
        .style('font', '15px sans-serif')
        .style('fill', '#AAAAAA')
        .text(subheading_2);

      // Put in a legend for each whip
      var legend = g.selectAll('.whip')
        .data(whips)
        .enter()
        .append('g')
        .attr('class', 'legend');

      // Location and colors of legend icon squares for each line
      legend.append('rect')
        .attr('x', innerWidth + (legendBoxSize * 2))
        .attr('y', function(d, i) {
          return legendStartYAxis - (i * legendBoxSize * 2);
        })
        .attr('width', legendBoxSize)
        .attr('height', legendBoxSize)
        .style('fill', function(d) {
          return standard_colors(d.id);
        });

      legend.append('text')
        .attr('x', innerWidth + (legendBoxSize * 4))
        .attr('y', function(d, i) {
          return legendStartYAxis - (i * legendBoxSize * 2) + legendBoxSize;
        })
        .text(function(d) {
          return d.id;
        })
        .style('font', '10px sans-serif');

      // Make the chart area aware of the data to be placed
      var whip = g.selectAll('.whip')
        .data(whips)
        .enter().append('g')
          .attr('class', 'whip');

      // Define the colors to be used for each line path
      whip.append('path')
          .attr('class', 'line')
          .attr('d', function(d) { return line(d.values); })
          .style('stroke', function(d) { return standard_colors(d.id); });

      // Clean up line
      whip.exit().remove();

    });

  }
