document.getElementById("ajax-slow-stage").addEventListener("submit", (e) => {
  e.preventDefault();

  const url = slow_stage;
  const position = document.getElementById("slow-stage-position").value;
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
      console.log(response.position);
    })
    .catch((error) => {
      console.log("Error");
    });
});

document.getElementById("save-data").addEventListener("submit", (e) => {
  e.preventDefault();

  const url = save_data;
  const path = document.getElementById("save-area").value;
  fetch(url, {
    method: "POST",
    body: `path=${path}`,
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
        myChart.destroy();

        let ctx = document.getElementById("canvas");
        let data = {
          labels: x,
          datasets: [
            { data: y, fill: false, borderColor: "rgba(255, 0, 0, 0.5)" },
          ],
        };
        myChart = new Chart(ctx, {
          type: "line",
          data: data,
          options: { animation: { duration: 0 } },
        });

        running = responseJson.running;
      })
      .catch((_) => {
        console.log("error in scanning");
        running = false;
      });

    await _sleep(1000);
  }
});

const _sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
