document.addEventListener("DOMContentLoaded", () => {
    const toggleBtn = document.querySelector("#toggle-btn");
    const navbar = document.querySelector(".nav-m-container");
    const navLinks = document.querySelectorAll(".nav-m-container a");
    let clicked = false;
    toggleBtn.addEventListener('click', () => {
        if (clicked) {
            navbar.style.height = "0px";
        } else {
            navbar.style.height = navLinks.length * 50 + "px";
        }
        clicked = !clicked;
    })
    
})