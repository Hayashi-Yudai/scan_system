const tds_boot_url = "http://localhost:8000/core/tds-boot/";

document
  .getElementById("tds-settings")
  .addEventListener("submit", async (e) => {
    e.preventDefault();
    tds_measurement();
  });

async function tds_measurement() {
  const url = document.getElementById("tds-settings").action;
  const boot = tds_boot_url;

  const start = Number(document.getElementById("start-position").value);
  const end = Number(document.getElementById("end-position").value);
  const step = Number(document.getElementById("moving-step").value);
  const lockin = Number(document.getElementById("lockin-time").value);
  const multiscan = Number(document.getElementById("multiscan").value);
  const path = document.getElementById("save-area").value;
  const scanStatus = document.getElementById("scan-status");

  if (start >= end || start < 0 || end <= 0 || step <= 0 || lockin <= 0 || multiscan <= 0) {
    alert("Invalid Parameters");
    return;
  }

  if (multiscan > 1 && (path == "" || path.endsWith("/"))) {
    alert("Invalid path. If multiscanning, specify the path to 'file' where data are saved.");
    return;
  }

  for (let i = 0; i < multiscan; i++) {
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
        // body: "",
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

          Plotly.update(canvas, data, layout);
          scanStatus.innerText = `Scanning ${i + 1}/${multiscan}...`;
        })
        .catch((error) => {
          console.log(error);
          alert("Error while measurement");
          finished = true;
        });

      await _sleep(300);
    }

    if (multiscan > 1) {
      const url = document.getElementById("save-data").action;
      const type = document.getElementById("save-type").value;
      let path = document.getElementById("save-area").value;

      if (!path.endsWith(".csv") && !path.endsWith(".txt")) {
        path += ".csv";
      }

      let path_split = path.split(".");
      path = path_split
        .slice(0, path_split.length - 1)
        .join(".") + `_${i}`
      path = path + "." + path_split[path_split.length - 1];

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
    }
  }
  scanStatus.innerText = "";
}

document.getElementById("sr830-sensitivity").addEventListener("change", (e) => {
  e.preventDefault();

  const url = document.getElementById("sr830-sensitivity").action;
  const num = document.getElementsByName("sensitivity-num");
  const order = document.getElementsByName("sensitivity-order");
  const unit = document.getElementsByName("sensitivity-unit");

  for (let i = 0; i < num.length; i++) {
    if (num.item(i).checked) {
      checkedNum = num.item(i).value;
    }
  }
  for (let i = 0; i < order.length; i++) {
    if (order.item(i).checked) {
      checkedOrder = order.item(i).value;
    }
  }
  for (let i = 0; i < unit.length; i++) {
    if (unit.item(i).checked) {
      checkedUnit = unit.item(i).value;
    }
  }

  if (
    typeof checkedNum !== "undefined" &&
    typeof checkedOrder !== "undefined" &&
    typeof checkedUnit !== "undefined"
  ) {
    const value = Number(checkedNum) * Number(checkedOrder);

    fetch(url, {
      method: "POST",
      body: `value=${value}&unit=${checkedUnit}`,
      headers: {
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
      },
    }).then((response)=>{
      if (!response.ok) {
        alert("GPIB connection error");
      }
    }).catch((_) => {
      alert("Failed to change sensitivity");
    });
  }
});

document.getElementById("sr830-time-const").addEventListener("change", (e) => {
  e.preventDefault();

  const url = document.getElementById("sr830-time-const").action;
  const num = document.getElementsByName("time-num");
  const order = document.getElementsByName("time-order");
  const unit = document.getElementsByName("time-unit");

  for (let i = 0; i < num.length; i++) {
    if (num.item(i).checked) {
      checkedNum = num.item(i).value;
    }
  }
  for (let i = 0; i < order.length; i++) {
    if (order.item(i).checked) {
      checkedOrder = order.item(i).value;
    }
  }
  for (let i = 0; i < unit.length; i++) {
    if (unit.item(i).checked) {
      checkedUnit = unit.item(i).value;
    }
  }

  if (
    typeof checkedNum !== "undefined" &&
    typeof checkedOrder !== "undefined" &&
    typeof checkedUnit !== "undefined"
  ) {
    let value = Number(checkedNum) * Number(checkedOrder);

    fetch(url, {
      method: "POST",
      body: `value=${value}&unit=${checkedUnit}`,
      headers: {
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
      },
    }).then((response) => {
      if (!response.ok) {
        alert("GPIB connection error");
      }
    }).catch((_) => {
      alert("Failed to change sensitivity");
    });
  }
});

document.getElementById("auto-phase").addEventListener("submit", (e) => {
  e.preventDefault();
  url = document.getElementById("auto-phase").action;

  fetch(url, {
    method: "POST",
    body: "",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
    },
  }).catch((_) => {
    alert("Failed to auto phase");
  });
});
