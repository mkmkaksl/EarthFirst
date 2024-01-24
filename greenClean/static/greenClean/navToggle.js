document.addEventListener("DOMContentLoaded", () => {
    const toggleBtn = document.querySelector("#toggle-btn");
    const navbar = document.querySelector(".nav-m-container");
    let clicked = false;
    console.log(toggleBtn);
    toggleBtn.addEventListener('click', () => {
        if (clicked) {
            navbar.style.height = "0px";
        } else {
            navbar.style.height = "200px";
        }
        clicked = !clicked;
    })
})