const samplingRate = document.getElementById("sampling-rate-area");

samplingRate.addEventListener("input", validateSamplingRate);

function validateSamplingRate(event) {
  let rate = Number(event.currentTarget.value);
  if (rate > 100 || rate < 0) {
    // samplingRate.classList.toggle("invalid-value");
    samplingRate.classList.toggle("is-error");
    document.getElementById("sampling-rate-alert").classList.remove("hide");
  } else {
    samplingRate.classList.remove("is-error");
    document.getElementById("sampling-rate-alert").classList.add("hide");
  }
}

