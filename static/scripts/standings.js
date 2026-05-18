conf = 'all'

d3.select("#conf-picker")
  .on("change", function(event) {
    conf = event.target.value;

    if (conf == 'all') {
        d3.selectAll(".standings-header")
          .style("display", "flex")
        d3.selectAll(".standings-table")
          .style("display", "table-row")
    }

    else {
        d3.selectAll(".standings-header")
          .style("display", "none")
        d3.selectAll(".standings-table")
          .style("display", "none")

        d3.selectAll(".standings-header[conf='" + conf + "']")
          .style("display", "flex")
        d3.selectAll(".standings-table[conf='" + conf + "']")
          .style("display", "table-row")
    }
})