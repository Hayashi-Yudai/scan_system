
class GraphInfo {
  constructor(pk, colorKey) {
    /*
     * pk: primary key (id in HTML)
     * colorKey: key of colorMap
     */
    this.pk = pk;
    this.colorKey = colorKey;
  }
}


class GraphList {
  constructor() {
    this.graphs = []; // List of GraphInfo objects
    this.counter = 0;
    this.colorMap = {
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
  }

  getPks() {
    return this.graphs.map((graph) => graph.pk);
  }

  getColors(opaque=false) {
    if (opaque) {
      return this.graphs.map((graph) => this.colorMap[graph.colorKey].replace("0.4", "1.0"));
    } else {
      return this.graphs.map((graph) => this.colorMap[graph.colorKey]);
    }
  }

  deleteIndex(idx) {
    let targetIndex = this.graphs.findIndex((e) => e.pk === idx);
    this.graphs.splice(targetIndex, 1);

    return targetIndex;
  }

  getPresentColor(opaque=false) {
    if (opaque) {
      return this.colorMap[this.counter % 10].replace("0.4", "1.0");
    } else {
      return this.colorMap[this.counter % 10];
    }
  }

  push(id) {
    this.graphs.push(new GraphInfo(id, this.counter % 10));
    this.counter++;
  }
}


let table_elements = document.getElementsByName("data-element");
let graphs = new GraphList();
let first = true;

for (ele of table_elements) {
  ele.addEventListener("click", async (e) => {
    let target = e.currentTarget;
    if (target.classList.contains("colored")) {
      target.style.backgroundColor = "rgba(255, 255, 255, 1)";
      target.classList.toggle("colored");

      let deleteIdx = graphs.deleteIndex(target.id);

      Plotly.deleteTraces(canvas, deleteIdx);
      if (first) {
        // bug in Plotly.js?
        Plotly.deleteTraces(canvas, deleteIdx);
        first = false;
      }

    } else {
      target.style.backgroundColor = graphs.getPresentColor();
      target.classList.toggle("colored");

      let fftIsChecked = document.querySelector("input[name = fft-checkbox]").checked;

      let url = "http://localhost:8000/archive/get_archive_data/";
      await fetch(url, {
        method: "POST",
        body: `pk=${target.id}&fft=${fftIsChecked}`,
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
            line: { color: graphs.getPresentColor(opaque=true) },
            marker: { color: graphs.getPresentColor(opaque=true) },
          });

          graphs.push(target.id);
        })
        .catch((error) => {
          console.log(error);
        });
    }
  });
}

document
  .querySelector("input[name=fft-checkbox]")
  .addEventListener("change", async (e) => {
    let url = fft_url;

    first = false;

    pks = graphs.getPks();

    await fetch(url, {
      method: "POST",
      body: JSON.stringify({ids: pks, fft: e.target.checked}),
      headers: {"Content-Type": "application/json"}
    })
      .then((response) => { return response.json(); })
      .then((responseJson) => {
        xs_resp = responseJson.xs;
        ys_resp = responseJson.ys;
      })
      .catch((_) => { console.log("Error in FFT");})

    data.length = 0;
    colors = graphs.getColors(opaque=true);
    for (i = 0; i < xs_resp.length; i++) {
      data.push({
        x: xs_resp[i],
        y: ys_resp[i],
        type: "scatter",
        line: { color: colors[i] },
        marker: { color: colors[i] },
      });
    }

    if (e.target.checked) {
      let log_layout = {
        height: 450,
        width: Math.min(width * 0.9, 550),
        margin: { l: 50, r: 0, b: 3, t: 20, pad: 5 },
        yaxis: {
          type: "log",
          autorange: true,
          showlegend: false,
        },
      };
      Plotly.newPlot("canvas", data, log_layout);
    } else {
      Plotly.newPlot("canvas", data, layout);
    }
  });
