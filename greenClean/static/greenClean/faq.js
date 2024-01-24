document.addEventListener("DOMContentLoaded", () => {
    const faqQuestions = document.querySelectorAll(".faq-question")
    const faqQuestionValues = document.querySelectorAll(".faq-question h3");
    const faqAnswer = document.querySelectorAll(".faq-answer")
    let clicked = []

    faqQuestions.forEach((x, idx) => {
        clicked.push(false)
        x.addEventListener("click", () => {
            console.log("Click")
            if (clicked[idx]) {
                faqQuestionValues[idx].innerHTML = faqQuestionValues[idx].innerText + " <i class='fa-solid fa-caret-down'></i>"
                faqAnswer[idx].style.height = "0px";
            } else {
                faqQuestionValues[idx].innerHTML = faqQuestionValues[idx].innerText + " <i class='fa-solid fa-caret-up'></i>"
                faqAnswer[idx].style.height = "200px";
            }
            console.log(clicked[idx])
            clicked[idx] = !clicked[idx];
        })

    })

})