var trace1 = {
  x: x,
  y: y,
  type: "scatter",
};

var data = [trace1];
var layout = {
  width: 550,
  height: 400,
  margin: { l: 30, r: 0, b: 3, t: 3, pad: 5 },
  showlegend: true,
  legend: { orientation: "h" },
};

Plotly.newPlot("canvas", data, layout);
