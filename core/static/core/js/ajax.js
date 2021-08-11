document.getElementById("rapid-scan").addEventListener("submit", async (e) => {
  e.preventDefault();

  let url = document.getElementById("rapid-scan").action;
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
