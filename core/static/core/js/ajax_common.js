let fft_url = "http://localhost:8000/core/calc-fft/";

const _sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

// Move the step motor stage to the specified position
document.getElementById("stage-move").addEventListener("submit", (e) => {
  e.preventDefault();

  const url = document.getElementById("stage-move").action;
  const position = document.getElementById("stage-position").value;
  fetch(url, {
    method: "POST",
    body: `position=${position}`,
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
      console.log("Error in moving step stage");
    });
});

document.getElementById("save-data").addEventListener("submit", (e) => {
  e.preventDefault();

  const url = document.getElementById("save-data").action;
  const filename = document.getElementById("save-area").value;
  const type = document.getElementById("save-type").value;
  console.log("Filename: " + filename);
  fetch(url, {
    method: "POST",
    body: `filename=${filename}&measure_type=${type}`,
    headers: {
      "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
    },
  })
    .then((response) => {
      if (response.ok) {
        alert("Saved successfully");
      } else {
        response.text().then(text => alert(text));
      }
    })
    .catch((_) => {
      alert("Invalid directory");
    });
});

// Calculate the FFT or back to the raw wave by the toggle button
document
  .querySelector("input[name=fft-checkbox]")
  .addEventListener("change", async (e) => {
    let url = fft_url;
    let type = document.getElementById("fft-type").value;
    await fetch(url, {
      method: "POST",
      body: `fft=${e.target.checked}&type=${type}`,
      headers: {
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
      },
    })
      .then((response) => {
        return response.json();
      })
      .then((responseJson) => {
        x = responseJson.x;
        y = responseJson.y;
      })
      .catch((_) => {
        console.log("error in fft");
      });

    data[0].x = x;
    data[0].y = y;

    if (e.target.checked) {
      let log_layout = {
        height: 450,
        width: Math.min(width * 0.9, 600),
        margin: { l: 50, r: 0, b: 3, t: 20, pad: 5 },
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