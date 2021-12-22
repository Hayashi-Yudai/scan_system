const trace1 = {
  x: [],
  y: [],
  type: "scatter",
};

const data = [trace1];
const layout = {
  margin: { l: 50, r: 0, b: 3, t: 20, pad: 5 },
  showlegend: false,
};

Plotly.newPlot("canvas", data, layout);
