document.getElementById("ajax-slow-stage").addEventListener("submit", (e) => {
  // デフォルトのイベントをキャンセルし、ページ遷移しないように!
  e.preventDefault();

  const url = slow_stage; //"http://localhost:8000/core/move/";
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
