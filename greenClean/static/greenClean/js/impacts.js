document.addEventListener("DOMContentLoaded", () => {
    const allImpacts = document.querySelectorAll(".impact-card");
    const outerImpactsContainer = document.querySelector(".impact-cards");
    const innerImpactsContainer = document.querySelector(".impacts-container")
    const positions = document.querySelector(".positions")
    let allPositions = []
    let carouselInterval

    for (let i = 0; i < allImpacts.length; i++) {
        let pos = document.createElement("div")
        pos.classList.add("position")

        pos.addEventListener("click", () => {
            allPositions[curPos].classList.remove("active");
            curPos = i;
            allPositions[curPos].classList.add("active")
            innerImpactsContainer.style.left = -1 * width * curPos + "px";
            clearInterval(carouselInterval)
            carouselInterval = setInterval(() => {
                allPositions[curPos].classList.remove("active")
                curPos++;
                if (curPos >= allImpacts.length) {
                    curPos = 0;
                }
                allPositions[curPos].classList.add("active")
        
                innerImpactsContainer.style.left = -1 * width * curPos + "px";
                // for (let i = 0; i < allImpacts.length; i++) {
                //     allImpacts[i].style.left = -1 * width * curPos + "px";
                // }
            }, 10000)
        })

        allPositions.push(pos)
        positions.append(pos)
    }
    allPositions[0].classList.add("active")

    let curPos = 0;

    let width = allImpacts[0].clientWidth;
    width += width * 0.05;

    let distLeft = innerImpactsContainer.getBoundingClientRect().left;

    carouselInterval = setInterval(() => {
        moveRight();
    }, 10000)


    innerImpactsContainer.addEventListener('click', (e) => {
        let pos = e.clientX;
        pos -= distLeft;

        let p1 = width/3;
        let p2 = (2*width)/3;

        if (pos > p2) {
            moveRight();
            clearInterval(carouselInterval);
            carouselInterval = setInterval(() => {
                moveRight();
            }, 10000)
        } else if (pos < p1) {
            moveLeft();
            clearInterval(carouselInterval);
            carouselInterval = setInterval(() => {
                moveRight();
            }, 10000)
        }
    })


    function moveRight() {
        allPositions[curPos].classList.remove("active")
        curPos++;
        if (curPos >= allImpacts.length) {
            curPos = 0;
        }
        allPositions[curPos].classList.add("active")

        innerImpactsContainer.style.left = -1 * width * curPos + "px";
    }
    function moveLeft() {
        allPositions[curPos].classList.remove("active")
        curPos--;
        if (curPos < 0) {
            curPos = allPositions.length-1;
        }
        allPositions[curPos].classList.add("active")

        innerImpactsContainer.style.left = -1 * width * curPos + "px";
    }


})

