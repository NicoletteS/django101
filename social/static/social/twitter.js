d3.csv('/static/social/data-hashtag.csv', function (error, data) {

    var width = document.body.clientWidth, height = 800;
    var svg = d3.select("body").append("svg")
        .attr("width", width)
        .attr("height", height);

    data.forEach(function(d) {
        d.Positive = +d.Positive;
        d.Neutral = +d.Neutral;
        d.Negative = +d.Negative;
    })

    for (var i = 0; i < data.length; i++) {
        if (data[i].Positive >= data[i].Negative && data[i].Positive >= data[i].Neutral) {
            data[i].value = data[i].Positive;
            data[i].color = "#008000";
        } else if (data[i].Negative > data[i].Neutral) {
            data[i].value = data[i].Negative;
            data[i].color = "#D40000";
        } else {
            data[i].value = data[i].Neutral;
            data[i].color = "#F0C64E";
        }

        data[i].radius = +data[i].value * 50;
        data[i].x = Math.random() * width;
        data[i].y = Math.random() * height;
    }

    var padding = 4;
    var maxRadius = d3.max(_.pluck(data, 'radius'));

    function getCenters(name, size) {
        var centers, map;
        centers = _.uniq(_.pluck(data, name)).map(function (d) {
            return {name: d, value: 1};
        });

        map = d3.layout.pack().size(size);
        map.nodes({children: centers});
		
		var middleX = size[0]/2;
		for(var i = 0; i < centers.length; i++) {
			centers[i].x = (centers[i].x - middleX)*2 + middleX;
		}
		var middleY = size[1]/2;
		for(var i = 0; i < centers.length; i++) {
			centers[i].y = (centers[i].y - middleY)*1.3 + middleY;
		}
		
        return centers;
    }

    var nodes = svg.selectAll("circle")
      .data(data);

    nodes.enter().append("circle")
      .attr("class", "node")
      .attr("cx", function (d) { return d.x; })
      .attr("cy", function (d) { return d.y; })
      .attr("r", 2)
      .style("fill", function (d) { return shadeColor(d.color, 0.5-d.value); })
      .on("mouseover", function (d) { showPopover.call(this, d); })
      .on("mouseout", function (d) { removePopovers(); })

    nodes.transition().duration(1000)
      .attr("r", function (d) { return d.radius; })

    var force = d3.layout.force();

    draw('Hashtag');

    $( ".btn" ).click(function() {
      draw(this.id);
    });

    function draw (varname) {
      var centers = getCenters(varname, [width, height]);
      force.on("tick", tick(centers, varname));
      labels(centers)
      force.start();
    }

    function tick (centers, varname) {
      var foci = {};
      for (var i = 0; i < centers.length; i++) {
        foci[centers[i].name] = centers[i];
      }
      return function (e) {
        for (var i = 0; i < data.length; i++) {
          var o = data[i];
          var f = foci[o[varname]];
          o.y += (f.y - o.y) * e.alpha;
          o.x += (f.x - o.x) * e.alpha;
        }
        nodes.each(collide(.11))
          .attr("cx", function (d) { return d.x; })
          .attr("cy", function (d) { return d.y; });
      }
    }

    function labels (centers) {
      svg.selectAll(".label").remove();

      svg.selectAll(".label")
      .data(centers).enter().append("text")
      .attr("class", "label")
      .style("font-size", "24px")
      .text(function (d) { return d.name })
      .attr("transform", function (d) {
        return "translate(" + (d.x - ((d.name.length)*3)) + ", " + (d.y - d.r) + ")";
      });
    }

    function removePopovers () {
      $('.popover').each(function() {
        $(this).remove();
      });
    }

    function showPopover (d) {
      $(this).popover({
        placement: 'auto top',
        container: 'body',
        trigger: 'manual',
        html : true,
        content: function() {
          return "Hashtag: " + d.Hashtag + "<br/>Positive: " + d.Positive + "<br/>Neutral: " + d.Neutral +
                 "<br/>Negative: " + d.Negative; }
      });
      $(this).popover('show')
    }

    function collide(alpha) {
      var quadtree = d3.geom.quadtree(data);
      return function(d) {
        var r = d.radius + maxRadius + padding,
            nx1 = d.x - r,
            nx2 = d.x + r,
            ny1 = d.y - r,
            ny2 = d.y + r;
        quadtree.visit(function(quad, x1, y1, x2, y2) {
          if (quad.point && (quad.point !== d)) {
            var x = d.x - quad.point.x,
                y = d.y - quad.point.y,
                l = Math.sqrt(x * x + y * y),
                r = d.radius + quad.point.radius + padding;
            if (l < r) {
              l = (l - r) / l * alpha;
              d.x -= x *= l;
              d.y -= y *= l;
              quad.point.x += x;
              quad.point.y += y;
            }
          }
          return x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
        });
      };
    }

  function shadeColor(color, percent) {
    var f=parseInt(color.slice(1),16),t=percent<0?0:255,p=percent<0?percent*-1:percent,R=f>>16,G=f>>8&0x00FF,B=f&0x0000FF;
    return "#"+(0x1000000+(Math.round((t-R)*p)+R)*0x10000+(Math.round((t-G)*p)+G)*0x100+(Math.round((t-B)*p)+B)).toString(16).slice(1);
  }
  });
