let x;
let y;

const trace1 = {
  x: x,
  y: y,
  type: "scatter",
};

const data = [trace1];
const layout = {
  margin: { l: 50, r: 0, b: 3, t: 20, pad: 5 },
  showlegend: true,
  legend: { orientation: "h" },
};

Plotly.newPlot("canvas", data, layout);
