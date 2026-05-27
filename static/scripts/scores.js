let params = new URLSearchParams(document.location.search);

date = params.get("date");
searchConf = params.get("conf");
blockSize = params.get("view");

searchConf = searchConf ? searchConf.replace('-', ' ').toLowerCase() : 'all';
filterByConf(searchConf)

if (blockSize && ['small', 'wide'].includes(blockSize.toLowerCase())) {
	blockSize = blockSize.toLowerCase();
}
else {
	blockSize = 'small'
}

if (blockSize == 'wide') {
	blockSize = 'small'
	switchBlockSize();
}

setURL(date, searchConf.replace(' ', '-'), blockSize);
gamesEmpty()

// CHANGE URL

function setURL(date, conf, view) {
	params = new URLSearchParams()

	if (date) {
		params.set('date', date)
	}
	if (conf != 'all') {
		params.set('conf', conf)
	}
	if (view != 'small') {
		params.set('view', view)
	}

	url = '?' + params.toString()

	window.history.replaceState({}, '', url)

	return url;
}

// FORM BUTTONS

d3.select("#date-picker")
  .on("change", function(event) {
    d3.select("#date-picker")
      .attr("value", event.target.value)
})

d3.select("#conf-picker")
  .on("change", function(event) {
    searchConf = event.target.value;

    filterByConf(searchConf)
    gamesEmpty()
})

function scoresRedirect() {
    form = d3.select("form")

    date = d3.select("#date-picker")
             .attr("value")
             .replaceAll("-", "")

    action = setURL(date, searchConf.replace(' ', '-'), blockSize);
    form.attr("action", action)
}

// CONF SELECT

function filterByConf(conf) {
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

	searchConf = conf;
	setURL(date, searchConf.replace(' ', '-'), blockSize);
}

// LAYOUT SWITCH

function hideWideView() {
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
}

hideWideView()
window.addEventListener("resize", hideWideView)

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

	setURL(date, searchConf.replace(' ', '-'), blockSize);
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