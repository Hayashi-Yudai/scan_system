let table_elements = document.getElementsByName("data-element");
let counter = 0;

let colorMap = {
  0: "rgba(230, 0, 18, 0.4)",
  1: "rgba(235, 97, 0, 0.4)",
  2: "rgba(252, 200, 0, 0.4)",
  3: "rgba(143, 195, 31, 0.4)",
  4: "rgba(0, 153, 68, 0.4)",
  5: "rgba(0, 158, 150, 0.4)",
  6: "rgba(0, 160, 233, 0.4)",
  7: "rgba(0, 104, 183, 0.4)",
  8: "rgba(29, 32, 136, 0.4)",
  9: "rgba(146, 7, 131, 0.4)",
};

let counters = [];
let pkInGraph = [];
let first = true;

for (ele of table_elements) {
  ele.addEventListener("click", async (e) => {
    let target = e.currentTarget;
    if (target.classList.contains("colored")) {
      target.style.backgroundColor = "rgba(255, 255, 255, 1)";
      target.classList.toggle("colored");

      let deleteIdx = pkInGraph.indexOf(target.id);

      pkInGraph.splice(deleteIdx, 1);
      Plotly.deleteTraces(canvas, deleteIdx);
      if (first) {
        Plotly.deleteTraces(canvas, deleteIdx);
        first = false;
      }

      counters = counters.splice(deleteIdx + 1, 1);
    } else {
      target.style.backgroundColor = colorMap[counter % 10];
      target.classList.toggle("colored");

      let url = "http://localhost:8000/archive/get_archive_data/";
      await fetch(url, {
        method: "POST",
        body: `pk=${target.id}`,
        headers: {
          "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        },
      })
        .then((response) => {
          return response.json();
        })
        .then((responseJson) => {
          let x = responseJson.x;
          let y = responseJson.y;

          Plotly.addTraces(canvas, {
            x: x,
            y: y,
            type: "scatter",
            line: { color: colorMap[counter % 10].replace("0.4", "1.0") },
            marker: { color: colorMap[counter % 10].replace("0.4", "1.0") },
          });

          counters.push(counter % 10);
        })
        .catch((error) => {
          console.log(error);
        });
      pkInGraph.push(target.id);
      counter++;
    }
  });
}

document
  .querySelector("input[name=fft-checkbox]")
  .addEventListener("change", async (e) => {
    let url = fft_url;

    await fetch(url, {
      method: "POST",
      body: JSON.stringify({ids: pkInGraph, fft: e.target.checked}),
      headers: {"Content-Type": "application/json"}
    })
      .then((response) => { return response.json(); })
      .then((responseJson) => {
        xs_resp = responseJson.xs;
        ys_resp = responseJson.ys;
      })
      .catch((err) => { console.log("Error in FFT");})

    data.length = 0;
    for (i = 0; i < xs_resp.length; i++) {
      data.push({
        x: xs_resp[i],
        y: ys_resp[i],
        type: "scatter",
        line: { color: colorMap[counters[i]].replace("0.4", "1.0") },
        marker: { color: colorMap[counters[i]].replace("0.4", "1.0") },
      });
    }

    if (e.target.checked) {
      let log_layout = {
        yaxis: {
          type: "log",
          autorange: true,
        },
      };
      Plotly.newPlot("canvas", data, log_layout);
    } else {
      Plotly.newPlot("canvas", data, layout);
    }
  });
