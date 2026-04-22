conf = 'all';
blockSize = 'small';
gamesEmpty()

// FORM BUTTONS

d3.select("#date-picker")
  .on("change", function(event) {
    d3.select("#date-picker")
      .attr("value", event.target.value)
})

d3.select("#conf-picker")
  .on("change", function(event) {
    conf = event.target.value;

    if (conf == 'all') {
        d3.selectAll(".scoreboard-block")
          .style("display", "flex")
    }

    else {
        d3.selectAll(".scoreboard-block")
          .style("display", "none")

        d3.selectAll(".scoreboard-block[home-conf='" + conf + "']")
          .style("display", "flex")
        d3.selectAll(".scoreboard-block[away-conf='" + conf + "']")
          .style("display", "flex")
    }

    gamesEmpty()
})

function scoresRedirect() {
    form = d3.select("form")

    date = d3.select("#date-picker")
             .attr("value")
             .replaceAll("-", "")

    action = "?date=" + date;
    form.attr("action", action)
}

// GAME STATUS TABS

function showAllByStatus() {
    if (conf == 'all') {
        d3.selectAll(".scoreboard-block")
          .style("display", "flex")
    }

    else {
        d3.selectAll(".scoreboard-block[home-conf='" + conf + "']")
          .style("display", "flex")
        d3.selectAll(".scoreboard-block[away-conf='" + conf + "']")
          .style("display", "flex")
    }

    d3.select(".view-active")
      .classed("view-active", false)

    d3.select("#all-scores-btn")
      .classed("view-active", true)

    gamesEmpty()
}

function filterByStatus(status) {
    d3.selectAll(".scoreboard-block")
      .style("display", "none")

    if (conf == 'all') {
        d3.selectAll(".scoreboard-block[status='" + status + "']")
          .style("display", "flex")
    }

    else {
        d3.selectAll(".scoreboard-block[status='" + status + "'][home-conf='" + conf + "']")
          .style("display", "flex")
        d3.selectAll(".scoreboard-block[status='" + status + "'][away-conf='" + conf + "']")
          .style("display", "flex")
    }

    d3.select(".view-active")
      .classed("view-active", false)

    d3.select("#" + status + "-scores-btn")
      .classed("view-active", true)

    gamesEmpty()
}

// LAYOUT SWITCH

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

// PRINT NO GAMES FOUND

function gamesEmpty() {
    games = d3.selectAll(".container")
              .filter(function(){return getComputedStyle(this).display == "grid"})
              .selectAll(".scoreboard-block")
              .filter(function(){return getComputedStyle(this).display == "flex"})
              .size()

    d3.select(".content")
      .selectAll("h3")
      .remove()

    if (games == 0) {
        d3.select(".content")
          .append("h3")
          .text("No games found.")
    }
}