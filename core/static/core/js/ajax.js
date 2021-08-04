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
