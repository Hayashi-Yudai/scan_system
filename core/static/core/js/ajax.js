document.getElementById("rapid-scan").addEventListener("submit", async (e) => {
  e.preventDefault();

  const url = document.getElementById("rapid-scan").action;
  const duration = document.getElementById("measurement-time-area").value;
  const samplingRate = document.getElementById("sampling-rate-area").value;

  let running = true;
  // Start scanning
  fetch(url, {
      method: "POST",
      body: `duration=${duration}&sampling_rate=${samplingRate}`,
      headers: {
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
      },
  });

  // Fetch data and plot
  while (running) {
    await fetch("http://localhost:8000/core/get-rapid-data/", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
      },
    })
      .then((response) => {
        return response.json();
      })
      .then((responseJson) => {
        const x = responseJson.x;
        const y = responseJson.y;

        data[0].x = x;
        data[0].y = y;
        Plotly.update("canvas", data, layout);
        running = responseJson.running;
      })
      .catch((_) => {
        console.log("error in scanning");
        running = false;
      });

    await _sleep(1000);
  }
});
