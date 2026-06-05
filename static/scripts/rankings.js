var conf = 'all'

d3.select("#conf-picker")
  .on("change", function(event) {
    conf = event.target.value;

    if (conf == 'all') {
        d3.selectAll(".metrics-row")
          .style("display", "table-row")
    }

    else {
        d3.selectAll(".metrics-row")
          .style("display", "none")

        d3.selectAll(".metrics-row[conf='" + conf + "']")
          .style("display", "table-row")
    }
})

var cols = [
	'KP', 'NET', 'WAB', 'SOR', 'TVK',
	'I', 'II', 'III', 'IV'
]

var sort = 0;
var asc = true;

function sortColumn(col) {
	let colIndex = cols.indexOf(col);
	console.log(colIndex)

	if (sort == colIndex) {
		asc = !asc;
	}
	else {
		sort = colIndex;
		asc = true;
	}

	d3.selectAll(".metrics-row")
	  .datum((d,i,nodes) => +nodes[i].children[colIndex+2].getAttribute("value"))
	  .sort((a,b) => (asc ? a-b : b-a))
}


function setWeek(week) {
	d3.selectAll(".polls-row")
	  .style("display", "none");

	d3.selectAll(".polls-row[week='" + week + "']")
	  .style("display", "table-row");
}

setWeek(1);