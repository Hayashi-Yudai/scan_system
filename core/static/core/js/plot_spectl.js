var ctx = document.getElementById("canvas");

// TODO: stream data
let data = {
  labels: x,
  datasets: [{ data: y, fill: false, borderColor: "rgba(255, 0, 0, 0.5)" }],
};
var myChart = new Chart(ctx, {
  type: "line",
  data: data,
});
