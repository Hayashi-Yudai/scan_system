let tds_boot_url = "http://localhost:8000/core/tds-boot/";

document
  .getElementById("tds-settings")
  .addEventListener("submit", async (e) => {
    e.preventDefault();
    tds_measurement();
  });

async function tds_measurement() {
  let url = document.getElementById("tds-settings").action;
  let boot = tds_boot_url;

  let start = Number(document.getElementById("start-position").value);
  let end = Number(document.getElementById("end-position").value);
  let step = Number(document.getElementById("moving-step").value);
  let lockin = Number(document.getElementById("lockin-time").value);
  let multiscan = Number(document.getElementById("multiscan").value);
  let path = document.getElementById("save-area").value;
  let scanStatus = document.getElementById("scan-status");

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

  let url = document.getElementById("sr830-sensitivity").action;
  let num = document.getElementsByName("sensitivity-num");
  let order = document.getElementsByName("sensitivity-order");
  let unit = document.getElementsByName("sensitivity-unit");

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
    }).catch((error) => {
      alert("Failed to change sensitivity");
    });
  }
});

document.getElementById("sr830-time-const").addEventListener("change", (e) => {
  e.preventDefault();

  let url = document.getElementById("sr830-time-const").action;
  let num = document.getElementsByName("time-num");
  let order = document.getElementsByName("time-order");
  let unit = document.getElementsByName("time-unit");

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
    }).catch((error) => {
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
  }).catch((error) => {});
});