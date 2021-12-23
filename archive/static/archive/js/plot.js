const trace1 = {
  x: [],
  y: [],
  type: "scatter",
};
width = document.getElementById("canvas").offsetWidth;

const data = [trace1];
const layout = {
  height: 450,
  width: Math.min(width * 0.9, 600),
  margin: { l: 50, r: 0, b: 3, t: 20, pad: 5 },
  showlegend: false,
};

Plotly.newPlot("canvas", data, layout);
