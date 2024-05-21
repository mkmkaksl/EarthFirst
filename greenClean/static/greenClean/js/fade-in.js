document.addEventListener("DOMContentLoaded", () => {
    const fadeIns = document.querySelectorAll(".fade-out");
    window.addEventListener("scroll", () => fadeIn(fadeIns))
    fadeIn(fadeIns);
})

function fadeIn(fadeIns) {
    for (let i = 0; i < fadeIns.length; i++) {
        let elem = fadeIns[i];
        var distInView = elem.getBoundingClientRect().top - window.innerHeight + 100;
        if (distInView < 0) {
            elem.classList.remove("fade-out");
            elem.classList.add("fade-in");
        } else {
            elem.classList.remove("fade-in")
            elem.classList.add("fade-out")
        }
    }
}