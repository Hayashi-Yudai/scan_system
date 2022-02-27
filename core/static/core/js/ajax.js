document.getElementById("rapid-scan").addEventListener("submit", async (e) => {
  e.preventDefault();

  const url = document.getElementById("rapid-scan").action;
  const duration = document.getElementById("measurement-time-area").value;
  const samplingRate = document.getElementById("sampling-rate-area").value;
  const magneticField = document.getElementsByClassName("magnetic-field");
  
  let first = true;

  for (let elem of magneticField) {
    if (elem.value == "" && !first) {
      break;
    }
    console.log(elem.value);
    first = false;
    if (elem.value != "") {
      await changeMagneticFieldRequest(elem.value);
    }
    let running = true;
    sendStartSignal(url, duration, samplingRate);

    const startButton = document.getElementById("start-button");
    startButton.classList.add("running");
    startButton.value = "Running...";

    // Fetch data and plot
    while (running) {
      await updateCanvas(running);
      await _sleep(1000);
    }

    startButton.classList.remove("running");
    startButton.value = "Start";
  }
});

async function sendStartSignal(url, duration, samplingRate) {
  fetch(url, {
      method: "POST",
      body: `duration=${duration}&sampling_rate=${samplingRate}`,
      headers: {
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
      },
  }).then((response)=> {
    return response.json();
  }).then((responseJson)=>{
    if (responseJson.status == "ok") {
      console.log("ok");
    }
  }).catch((_) => { console.log("Error to start scanning") });
}

async function updateCanvas(running) {
  fetch("http://localhost:8000/core/get-rapid-data/", {
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
}

async function changeMagneticFieldRequest(magneticField) {
  fetch("http://localhost:8000/core/change-magnetic-field/", {
    method: "POST",
    body: `target=${magneticField}`,
    headers: {
      "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
    }
  })
  .then((response) => {
    if (!response.ok) {
      console.log("Error in changing magnetic field");
    }
  })
  .catch((err) => { console.log(err) });
}