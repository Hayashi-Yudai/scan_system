const _sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

// Move the step motor stage to the specified position
document.getElementById("stage-move").addEventListener("submit", (e) => {
  e.preventDefault();

  const url = slow_stage;
  const position = document.getElementById("stage-position").value;
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
      console.log("Error in moving step stage");
    });
});

document.getElementById("save-data").addEventListener("submit", (e) => {
  e.preventDefault();

  const url = save_data;
  const type = document.getElementById("save-type").value;
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
      if (!responseJson.success) {
        alert("Invalid directory");
      }
    })
    .catch((_) => {
      console.log("error in save data");
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
      .catch((error) => {});

    trace1 = {
      x: x,
      y: y,
      type: "scatter",
    };

    data = [trace1];

    if (e.target.checked) {
      let log_layout = {
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
