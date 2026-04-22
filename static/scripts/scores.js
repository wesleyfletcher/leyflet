// FORM BUTTONS

d3.select("#date-picker")
  .on("change", function(event) {
    d3.select("#date-picker")
      .attr("value", event.target.value)
    })

d3.select("#conf-picker")
  .on("change", function(event) {
    d3.select("#conf-picker")
      .attr("value", event.target.value);
    })

function scoresRedirect() {
    form = d3.select("form")

    date = d3.select("#date-picker")
             .attr("value")
             .replaceAll("-", "")

    conf = d3.select("#conf-picker")
             .attr("value")
             .replace(" ", "-")

    action = "?date=" + date;
    if (conf != "all") {
      action += ("&conf=" + conf);
    }

    form.attr("action", action)
}

// GAME STATUS TABS

function showAllByStatus() {
    d3.selectAll(".scoreboard-block")
      .style("display", "flex")

    d3.select(".view-active")
      .classed("view-active", false)

    d3.select("#all-scores-btn")
      .classed("view-active", true)
}

function filterByStatus(status) {
    d3.selectAll(".scoreboard-block")
      .style("display", "none")

    d3.selectAll(".scoreboard-block[status='" + status + "']")
      .style("display", "flex")

    d3.select(".view-active")
      .classed("view-active", false)

    d3.select("#" + status + "-scores-btn")
      .classed("view-active", true)
}

// LAYOUT SWITCH

blockSize = 'small';
d3.select(".one-column")
  .style("display", "none")

window.addEventListener("resize", function(event) {
    containerWidth = 1080;
    toggleWidth = +d3.select(".layout-toggle")
                    .style("width")
                    .slice(0, -2)

    if (window.innerWidth < containerWidth + 3*toggleWidth) {
        d3.select(".layout-toggle")
          .style("visibility", "hidden")

        if (blockSize == 'wide') {
            switchBlockSize();
        }
    }
    else {
        d3.select(".layout-toggle")
          .style("visibility", "visible")
    }
})

function switchBlockSize() {
    d3.select(".toggle-active")
      .classed("toggle-active", false)

    if (blockSize == 'small') {
        d3.select(".three-column")
          .style("display", "none")

        d3.select(".one-column")
          .style("display", "grid")

        d3.select("#toggle-one-col")
          .classed("toggle-active", true)

        blockSize = 'wide'
    }

    else {
        d3.select(".one-column")
          .style("display", "none")

        d3.select(".three-column")
          .style("display", "grid")

        d3.select("#toggle-three-col")
          .classed("toggle-active", true)
        
        blockSize = 'small'
    }
}