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
