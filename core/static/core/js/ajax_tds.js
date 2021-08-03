const _sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

document
  .getElementById("tds-settings")
  .addEventListener("submit", async (e) => {
    e.preventDefault();
    tds_measurement();
  });

async function tds_measurement() {
  let url = tds_scan_url;
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
        trace1 = {
          x: x,
          y: y,
          type: "scatter",
        };

        data = [trace1];
        Plotly.newPlot("canvas", data, layout);
      })
      .catch((error) => {
        console.log(error);
        alert("Error while measurement");
        finished = true;
      });

    await _sleep(500);
  }
}

document.getElementById("save-data").addEventListener("submit", (e) => {
  e.preventDefault();

  const url = save_data;
  const type = "TDS";
  const path = document.getElementById("save-area").value;
  fetch(url, {
    method: "POST",
    body: `path=${path}&type=${type}`,
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
