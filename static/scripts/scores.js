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

    form.attr("action", "?date="+date + 
        (conf == "all" ? "" : "&conf=" + conf)
    )
}