let x;
let y;

const trace1 = {
  x: x,
  y: y,
  type: "scatter",
};

const canvas = document.getElementById("canvas");
const height = canvas.offsetHeight;
const width = canvas.offsetWidth;

const data = [trace1];
const layout = {
  height: Math.min(height * 0.9, 500),
  width: Math.min(width * 0.9, 600),
  margin: { l: 50, r: 0, b: 3, t: 20, pad: 5 },
  showlegend: true,
  legend: { orientation: "h" },
};

Plotly.newPlot("canvas", data, layout);
