
  function drawOIDCurrentLineChart( url, div_id, heading, subheading_1, subheading_2, subheading_3, subheading_4, y_label ) {
    //
    // This script creates the charts for customer cabinet power and bandwidth data
    //
    // Args:
    //  url: URL from which to retrieve data.tsv file
    //  div_id: Div ID to match chart to javascript
    //  heading: Heading for chart
    //  subheading_1: First sub heading
    //  subheading_2: Second sub heading
    //  subheading_3: Third sub heading
    //  subheading_4: Fourth sub heading
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
      // standard_colors.domain(whips.map(function(c) { return c.id; }));

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
