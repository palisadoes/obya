
  function drawCabinetLineChart( url, div_id, kw_commit, solo_chart, heading, subheading_1, subheading_2, subheading_3, y_label ) {
    //
    // This script creates the charts for customer cabinet power and bandwidth data
    //
    // Args:
    //  url: URL from which to retrieve data.tsv file
    //  div_id: Div ID to match chart to javascript
    //  kw_commit: Value for kw commit to be drawn if this is a solo chart
    //  solo_chart: If True then this is a single line chart that needs to be drawn and the kw_commit shown
    //  heading: Heading for chart
    //  subheading_1: First sub heading
    //  subheading_2: Second sub heading
    //  subheading_3: Third sub heading
    //  y_label: Label to use for y axis
    //
    // Initialise key variables
    var margin = {top: 20, right: 250, bottom: 50, left: 80};
    var headingVOffset = 0;
    var outerWidth = 1100;
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
      var ymax = Math.max(kw_max, kw_commit);
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
      if (kw_commit != 0) {

        // Maximum value line
        g.append('line')
            .attr('x1', 0)
            .attr('x2', innerWidth)
            .attr('y1', kwMaxScale(kw_max))
            .attr('y2', kwMaxScale(kw_max))
            .style('stroke-width', 1)
            .style('stroke', '#808080');

        // Maximum value text
        g.append('text')
            .attr('x', innerWidth + 5)
            .attr('y', kwMaxScale(kw_max))
            .style('font', '10px sans-serif')
            .text('Max kW');

        // Maximum value line
        g.append('line')
            .attr('x1', 0)
            .attr('x2', innerWidth)
            .attr('y1', kwCommitScale(kw_commit))
            .attr('y2', kwCommitScale(kw_commit))
            .style('stroke-width', 1)
            .style('stroke', '#DC143C');

        // Maximum value text
        g.append('text')
            .attr('x', innerWidth + 5)
            .attr('y', kwCommitScale(kw_commit))
            .style('font', '10px sans-serif')
            .text('Commit');

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
        .attr('y', 180 + headingVOffset)
        .style('font', '15px sans-serif')
        .style('fill', '#AAAAAA')
        .text(subheading_3);

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

      // Add descriptive text to the end of each plot
      //whip.append('text')
      //    .datum(function(d) { return {id: d.id, value: d.values[d.values.length - 1]}; })
      //    .attr('transform', function(d) { return 'translate(' + x(d.value.date) + ',' + y(d.value.watts) + ')'; })
      //    .attr('x', 3)
      //    .attr('dy', '0.35em')
      //    .style('font', '10px sans-serif')
      //    .text(function(d) { return d.id; });

      // Clean up line
      whip.exit().remove();

      // Do mouseover if this is the only chart on the page
      if (solo_chart == 1) {

        // Mouse stuff - Taken from https://bl.ocks.org/larsenmtl/e3b8b7c2ca4787f77d78f58d41c3da91
        var mouseG = svg.append('g')
          // Make the x,y mouse positions over the chart map to the 'g' area via a left margin offset
          .attr('transform', 'translate(' + margin.left + ', ' + (0) + ')')
          .attr('class', 'mouse-over-effects');

        mouseG.append('path') // this is the black vertical line to follow mouse
          .attr('class', 'mouse-line')
          .style('stroke', '#b9d3a4')
          .style('stroke-width', '1px')
          .style('opacity', '0');

        var lines = document.getElementsByClassName('line');

        var mousePerLine = mouseG.selectAll('.mouse-per-line')
          .data(whips)
          .enter()
          .append('g')
          .attr('class', 'mouse-per-line');

        mousePerLine.append('circle')
          .attr('r', 7)
          .style('stroke', function(d) {
            return standard_colors(d.id);
          })
          .style('fill', 'none')
          .style('stroke-width', '1px')
          .style('opacity', '0');

        mousePerLine.append('text')
          .attr('transform', 'translate(10,3)');

        // Clean upn line
        mousePerLine.exit().remove();

        mouseG.append('svg:rect') // append a rect to catch mouse movements on canvas
          .attr('width', innerWidth) // can't catch mouse events on a g element
          .attr('height', innerHeight)
          .attr('fill', 'none')
          .attr('pointer-events', 'all')
          .on('mouseout', function() { // on mouse out hide line, circles and text
            d3.select('.mouse-line')
              .style('opacity', '0');
            d3.selectAll('.mouse-per-line circle')
              .style('opacity', '0');
            d3.selectAll('.mouse-per-line text')
              .style('opacity', '0');
          })
          .on('mouseover', function() { // on mouse in show line, circles and text
            d3.select('.mouse-line')
              .style('opacity', '1');
            d3.selectAll('.mouse-per-line circle')
              .style('opacity', '1');
            d3.selectAll('.mouse-per-line text')
              .style('opacity', '1');
          })
          .on('mousemove', function() { // mouse moving over canvas
            var mouseX = d3.mouse(this)[0];
            d3.select('.mouse-line')
              .attr('d', function() {
                // Positions vertical line at mouse that fits in the vertical height of 'g'
                var d = 'M' + mouseX + ',' + (outerHeight - margin.bottom);
                d += ' ' + mouseX + ',' + margin.top;
                return d;
              });

            d3.selectAll('.mouse-per-line')
              .attr('transform', function(d, i) {
                //console.log(width/mouseX)
                var xDate = x.invert(mouseX),
                    bisect = d3.bisector(function(d) { return d.date; }).right;
                    idx = bisect(d.values, xDate);

                var beginning = 0,
                    end = lines[i].getTotalLength(),
                    target = null;

                while (true){
                  target = Math.floor((beginning + end) / 2);
                  pos = lines[i].getPointAtLength(target);
                  if ((target === end || target === beginning) && pos.x !== mouseX) {
                      break;
                  }
                  if (pos.x > mouseX)      end = target;
                  else if (pos.x < mouseX) beginning = target;
                  else break; //position found
                }

                d3.select(this).select('text')
                  .text(y.invert(pos.y).toFixed(2));

                return 'translate(' + mouseX + ',' + (pos.y + margin.top) +')';
              });
          });
        } // solo_chart chart - mouse over end if

    });
  }
