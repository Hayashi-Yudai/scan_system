var trace1 = {
  x: x,
  y: y,
  type: "scatter",
};

var data = [trace1];
var layout = {
  width: 600,
  height: 400,
  margin: { l: 50, r: 0, b: 3, t: 20, pad: 5 },
  showlegend: true,
  legend: { orientation: "h" },
};

Plotly.newPlot("canvas", data, layout);
