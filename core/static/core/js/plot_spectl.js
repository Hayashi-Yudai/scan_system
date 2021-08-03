var trace1 = {
  x: [1, 2, 3, 4],
  y: [10, 15, 13, 17],
  type: "scatter",
};

var trace2 = {
  x: [1, 2, 3, 4],
  y: [16, 5, 11, 9],
  type: "scatter",
};

var data = [trace1, trace2];
var layout = {
  width: 550,
  height: 400,
  margin: { l: 30, r: 0, b: 3, t: 3, pad: 5 },
  showlegend: true,
  legend: { orientation: "h" },
};

Plotly.newPlot("coord", data, layout);
