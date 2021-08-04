document.getElementById("ajax-slow-stage").addEventListener("submit", (e) => {
  e.preventDefault();

  const url = slow_stage;
  const position = document.getElementById("slow-stage-position").value;
  fetch(url, {
    method: "POST",
    body: `position=${position}`,
    headers: {
      "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
    },
  })
    .then((response) => {
      return response.json();
    })
    .then((response) => {
      console.log(response.success);
    })
    .catch((error) => {
      console.log("Error");
    });
});

document.getElementById("save-data").addEventListener("submit", (e) => {
  e.preventDefault();

  const url = save_data;
  const type = "RAPID";
  const path = document.getElementById("save-area").value;
  fetch(url, {
    method: "POST",
    body: `path=${path}&type=${RAPID}`,
    headers: {
      "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
    },
  })
    .then((response) => {
      return response.json();
    })
    .then((responseJson) => {
      if (responseJson.success) {
        console.log("valid directory");
      } else {
        console.log("invlid directory");
      }
    })
    .catch((_) => {
      console.log("error in save data");
    });
});

document.getElementById("rapid-scan").addEventListener("submit", async (e) => {
  e.preventDefault();

  let url = scan_url;
  let duration = document.getElementById("measurement-time-area").value;
  let sampling_rate = document.getElementById("sampling-rate-area").value;

  let running = true;
  while (running) {
    await fetch(url, {
      method: "POST",
      body: `duration=${duration}&sampling_rate=${sampling_rate}`,
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

        trace1 = {
          x: x,
          y: y,
          type: "scatter",
        };

        data = [trace1];
        Plotly.newPlot("canvas", data, layout);
        running = responseJson.running;
      })
      .catch((_) => {
        console.log("error in scanning");
        running = false;
      });

    await _sleep(1000);
  }
});

document
  .querySelector("input[name=fft-checkbox]")
  .addEventListener("change", async (e) => {
    let url = fft_url;
    let fftx;
    let ffty;
    if (e.target.checked) {
      await fetch(url, {
        method: "POST",
        body: "fft=true&type=RAPID",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        },
      })
        .then((response) => {
          return response.json();
        })
        .then((responseJson) => {
          fftx = responseJson.x;
          ffty = responseJson.y;
        })
        .catch((error) => {});
    } else {
      await fetch(url, {
        method: "POST",
        body: "fft=false&type=RAPID",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        },
      })
        .then((response) => {
          return response.json();
        })
        .then((responseJson) => {
          fftx = responseJson.x;
          ffty = responseJson.y;
        })
        .catch((error) => {
          console.log("FFT error");
        });
    }
    trace1 = {
      x: fftx,
      y: ffty,
      type: "scatter",
    };

    data = [trace1];
    Plotly.newPlot("canvas", data, layout);
  });

window.addEventListener("load", async () => {
  setInterval(async () => {
    let gpib_intensity = document.getElementById("sr830-gpib-intensity");

    let url = "http://localhost:8000/core/gpib/";
    let intensity;
    let connection;
    await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
      },
    })
      .then((response) => response.json())
      .then((responseJson) => {
        intensity = responseJson.intensity;
        intensity = Math.round(intensity * 1e6) / 1e3;

        connection = responseJson.connection;
      })
      .catch((err) => {
        intensity = "NaN";
      });
    let text = `Intensity: ${intensity} mV`;
    if (!connection) {
      text += " (No GPIB connection)";
    }
    gpib_intensity.innerHTML = text;
  }, 2000);
});

const _sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
