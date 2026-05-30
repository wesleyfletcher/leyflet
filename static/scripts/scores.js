let params = new URLSearchParams(document.location.search);
let form = d3.select("form");

let today = new Date();
var date = params.get("date");
if (!date) {
	date = 10000*today.getFullYear() + 100*(today.getMonth()+1) + today.getDate();
}

var conf = params.get("conf");
var view = params.get("view");

let datePicker = d3.select("#date-picker")
let confPicker = d3.select("#conf-picker")

let confList = []
confPicker.selectAll("option").each(function(d,i){
	confList.push(d3.select(this).attr("value"))
})

viewList = ['small', 'wide']

if (!confList.includes(conf ? conf.toLowerCase() : null)) {
    conf = 'all';
}
if (!viewList.includes(view ? view.toLowerCase() : null)) {
    view = 'small'
}

selectConf(conf);
toggleView();toggleView();

datePicker.on("change", function(event) {
    datePicker.attr("value", event.target.value)
    date = event.target.value.replaceAll("-", "")
    updateParams()
})
confPicker.on("change", function(event) {
    selectConf(event.target.value)
})

function selectConf(inConf) {
    if (inConf == 'all') {
        d3.selectAll(".scoreboard-block")
          .style("display", "flex")
    }
    else {
        d3.selectAll(".scoreboard-block")
          .style("display", "none")

        d3.selectAll("[home-conf='"+inConf+"']")
          .style("display", "flex")
        d3.selectAll("[away-conf='"+inConf+"']")
          .style("display", "flex")
    }

    conf = inConf;
    updateParams()
}

function toggleView() {
    d3.selectAll(".container")
      .style("display", "none");

    d3.selectAll(".toggle-option")
      .classed("toggle-active", false);
    
    if (view == 'small') {
        d3.select(".one-column")
          .style("display", "grid");

        d3.select("#toggle-one-col")
          .classed("toggle-active", true);

        view = 'wide';
    }
    else {
        d3.select(".three-column")
          .style("display", "grid");

        d3.select("#toggle-three-col")
          .classed("toggle-active", true);

        view = 'small';
    }

    updateParams()
}

function truncateView() {
    containerWidth = 1080;
    toggleWidth = +d3.select(".layout-toggle")
                     .style("width")
                     .slice(0, -2)

    toggle = d3.select(".layout-toggle");
    
    if (window.innerWidth < containerWidth+3*toggleWidth) {
        toggle.style("visibility", "hidden");
        if (view == 'wide') {
            toggleView();
        }
    }
    else {
        toggle.style("visibility", "visible");
    }
}
truncateView();
window.addEventListener("resize", truncateView);

// print if games empty
function gamesEmpty() {
    games = d3.selectAll(".scoreboard-block")
              .filter(function(){
                return getComputedStyle(this).display == "flex"
              }).size()

    d3.select(".content")
      .selectAll("h3")
      .remove()

    if (games == 0) {
        d3.select(".content")
          .append("h3")
          .text("No games found.")
    }
}

function updateParams() {
    // update url
    let inParams = new URLSearchParams();
    params.set('date', date);
    params.set('conf', conf);
    params.set('view', view);

    url = '?' + params.toString()
	window.history.replaceState({}, '', url)

    form.attr("action", url)

    gamesEmpty()
}
