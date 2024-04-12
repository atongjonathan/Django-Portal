document.addEventListener("DOMContentLoaded", function () {
    let children = document.querySelectorAll(".flex-item");
    children.forEach(element => {
      element.addEventListener("click", () => {
        const button = element.querySelector('button');
        button.click()
      });
    });
  });