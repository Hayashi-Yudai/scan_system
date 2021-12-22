const tabs = document.getElementsByClassName("tab-item");

for (tab of tabs) {
  (function(t) {
    t.addEventListener("click", () => {
      document
        .getElementsByClassName("active")[1]
        .classList
        .remove("active");
      t.classList.add("active");

      const tabContent = document.getElementsByClassName("show")[0];
      tabContent.classList.remove("show");
      tabContent.classList.add("hide");
      const arrayTabs = Array.prototype.slice.call(tabs);
      const index = arrayTabs.indexOf(t);
      document.getElementsByClassName("tab-content")[index].classList.add("show")
      document.getElementsByClassName("tab-content")[index].classList.remove("hide")
    });
  })(tab)
}
