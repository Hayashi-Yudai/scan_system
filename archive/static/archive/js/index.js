let table_elements = document.getElementsByName("data-element");
let counter = 0;

let colorMap = {
  0: "rgba(230, 0, 18, 0.4)",
  1: "rgba(235, 97, 0, 0.4)",
  2: "rgba(252, 200, 0, 0.4)",
  3: "rgba(143, 195, 31, 0.4)",
  4: "rgba(0, 153, 68, 0.4)",
  5: "rgba(0, 158, 150, 0.4)",
  6: "rgba(0, 160, 233, 0.4)",
  7: "rgba(0, 104, 183, 0.4)",
  8: "rgba(29, 32, 136, 0.4)",
  9: "rgba(146, 7, 131, 0.4)",
};

for (ele of table_elements) {
  ele.addEventListener("click", async (e) => {
    let target = e.currentTarget;
    if (target.classList.contains("colored")) {
      target.style.backgroundColor = "rgba(255, 255, 255, 1)";
      target.classList.toggle("colored");
    } else {
      target.style.backgroundColor = colorMap[counter % 10];
      target.classList.toggle("colored");

      let url = "http://localhost:8000/archive/get_archive_data/";
      await fetch(url, {
        method: "POST",
        body: `pk=${target.id}`,
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

          Plotly.addTraces(canvas, {
            x: x,
            y: y,
            type: "scatter",
            line: { color: colorMap[counter] },
            marker: { color: colorMap[counter] },
          });
        })
        .catch((error) => {
          console.log(error);
        });
      counter++;
    }
  });
}
