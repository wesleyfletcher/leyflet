conf = 'all'

d3.select("#conf-picker")
  .on("change", function(event) {
    conf = event.target.value;

    if (conf == 'all') {
        d3.selectAll(".rankings-row")
          .style("display", "table-row")
    }

    else {
        d3.selectAll(".rankings-row")
          .style("display", "none")

        d3.selectAll(".rankings-row[conf='" + conf + "']")
          .style("display", "table-row")
    }
})