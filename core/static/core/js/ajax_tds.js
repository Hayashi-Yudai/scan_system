document
  .getElementById("tds-settings")
  .addEventListener("submit", async (e) => {
    e.preventDefault();
    tds_measurement();
  });

async function tds_measurement() {
  let url = document.getElementById("tds-settings").action;
  let boot = tds_boot_url;

  let start = document.getElementById("start-position").value;
  let end = document.getElementById("end-position").value;
  let step = document.getElementById("moving-step").value;
  let lockin = document.getElementById("lockin-time").value;

  if (start > end || start < 0 || end < 0 || step < 0 || lockin < 0) {
    alert("Invalid Parameters");
    return;
  }

  let finished = false;
  fetch(boot, {
    method: "POST",
    body: `start=${start}&end=${end}&step=${step}&lockin=${lockin}`,
    headers: {
      "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
    },
  }).catch((error) => {
    finished = true;
  });
  await _sleep(1000);
  while (!finished) {
    await fetch(url, {
      method: "POST",
      body: "",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
      },
    })
      .then((response) => {
        return response.json();
      })
      .then((responseJson) => {
        if (responseJson.status === "finished") {
          finished = true;
        }
        let x = responseJson.x;
        let y = responseJson.y;
        data[0].x = x;
        data[0].y = y;

        Plotly.update("canvas", data, layout);
      })
      .catch((error) => {
        console.log(error);
        alert("Error while measurement");
        finished = true;
      });

    await _sleep(500);
  }
}
