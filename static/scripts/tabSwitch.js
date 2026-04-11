function switchTab(tab) {
    d3.select(".view-active")
      .classed("view-active", false)

    d3.select("#" + tab + "-btn")
      .classed("view-active", true)

    d3.selectAll(".view-section")
      .style("display", "none");

    d3.select("#" + tab)
      .style("display", "block")
}