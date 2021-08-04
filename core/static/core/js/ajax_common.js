const _sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

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

document
  .querySelector("input[name=fft-checkbox]")
  .addEventListener("change", async (e) => {
    let url = fft_url;
    let type = document.getElementById("fft-type").value;
    let fftx;
    let ffty;
    if (e.target.checked) {
      await fetch(url, {
        method: "POST",
        body: `fft=true&type=${type}`,
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
        body: `fft=false&type=${type}`,
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
