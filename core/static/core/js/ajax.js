document.getElementById("rapid-scan").addEventListener("submit", async (e) => {
  e.preventDefault();

  const url = document.getElementById("rapid-scan").action;
  const duration = document.getElementById("measurement-time-area").value;
  const samplingRate = document.getElementById("sampling-rate-area").value;
  const magneticField = document.getElementsByClassName("magnetic-field");

  let firstScan = true;
  
  const startButton = document.getElementById("start-button");
  startButton.classList.add("running");
  startButton.value = "Running...";

  for (let [idx, elem] of Object.entries(magneticField)) {
    if (elem.value == "" && !firstScan) {
      // End of the measurement
      // If this is the single-scan, do not end the measurement at this point
      break;
    }
    firstScan = false;
    if (elem.value != "") {
      magneticField[idx].classList.add("current-field");
      await changeMagneticFieldRequest(elem.value);
    }
    let running = true;
    sendStartSignal(url, duration, samplingRate);

    // Fetch data and plot at every 1000 ms
    while (running) {
      running = await updateCanvas();
      await _sleep(1000);
    }

    // If measuring multiple magnetic fields, save the data automatically
    if (elem.value != "") {
      magneticField[idx].classList.remove("current-field");
      await saveData(elem.value);
    }
  }
  startButton.classList.remove("running");
  startButton.value = "Start";
});

async function sendStartSignal(url, duration, samplingRate) {
  await fetch(url, {
      method: "POST",
      body: `duration=${duration}&sampling_rate=${samplingRate}`,
      headers: {
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
      },
  }).then((response)=> {
    if (!response.ok) {
      response.text().then(text => alert(text));
    }
  }).catch((_) => { console.log("Error to start scanning") });

  return;
}

async function updateCanvas() {
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
    .catch((err) => {
      console.log("error in scanning");
      console.log(err);
      running = false;
    });

  return;
}

// TODO: Set proper time-out
async function changeMagneticFieldRequest(magneticField) {
  let running;
  const controller = new AbortController();
  // Set timeout to 1 hour
  const timeout = setTimeout(() => { controller.abort() }, 1000 * 60 * 60);

  await fetch("http://localhost:8000/core/change-magnetic-field/", {
    method: "POST",
    body: `target=${magneticField}`,
    headers: {
      "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
    },
    signal: controller.signal,
  })
  .then((response) => {
    if (!response.ok) {
      response.text().then(text => alert(text));
    }
  })
  .catch((err) => { console.log(err) });

  clearTimeout(timeout);

  return running;
}

async function saveData(suffix) {
  const url = document.getElementById("save-data").action;
  const type = document.getElementById("save-type").value;
  let path = document.getElementById("save-area").value;

  path += "_" + suffix + "T.csv";

  await fetch(url, {
    method: "POST",
    body: `path=${path}&type=${type}`,
    headers: {
      "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
    },
  })
    .then((response) => {
      if (!response.ok) {
        response.text().then(text => alert(text));
      }
    })
    .catch((_) => {
      alert("Invalid directory");
    });

  return;
}
