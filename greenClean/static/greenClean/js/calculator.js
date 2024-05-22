document.addEventListener("DOMContentLoaded", () => {

    let allFormSections = document.querySelectorAll(".form-section");
    let allSecondQuestions = document.querySelectorAll(".form-section > .form-field-container:nth-child(3) input");
    let allFormHeaders = document.querySelectorAll(".form-heading")
    let allNextBtns = document.querySelectorAll(".form-btn-container.next button")
    let allBackBtns = document.querySelectorAll(".form-btn-container.back button")

    calculations();
    for (let i = 0; i < allNextBtns.length; i++) {
        allNextBtns[i].addEventListener("click", (event) => {
            if (allSecondQuestions[i].value != "") {
                allFormSections[i].classList.remove("active");
                allFormSections[i].classList.add("last")
                allFormSections[i+1].classList.add("active");
            } else {
                alert("Please input a valid value for each input!")
            }
        })
    }

    for (let i = 0; i < allBackBtns.length; i++) {
        allBackBtns[i].addEventListener("click", () => {
            let curIdx = i+1;
            allFormSections[curIdx].classList.remove("active");
            allFormSections[curIdx-1].classList.remove("last")
            allFormSections[curIdx-1].classList.add("active");
        })
    }
    

})

function calculations() {
    // Electricity Carbon Footprint
    const elec_country = document.querySelector("#id_location")
    const elec_usage = document.querySelector("#id_energy")
    const elec_carbon_footprint = document.querySelector("#energy_co2")
    const elec_co2_input = document.querySelector("#co2_energy"); // Hidden input sent through form
    
    let carbonIntensitiesObject = JSON.parse(carbonIntensities);

    let emissionFactor = 0;

    elec_country.addEventListener('change', () => {
        emissionFactor = carbonIntensitiesObject[elec_country.value];
        if (elec_usage.value != 0) {
            const co2 = Math.round(emissionFactor * elec_usage.value * 52).toLocaleString("en-US");
            elec_carbon_footprint.innerHTML = "Grams of CO<sub>2</sub> Produced Yearly: <strong>" + (co2) + " gCO<sub>2</sub></strong>"
            elec_co2_input.value = co2;
        }
    })
    elec_usage.addEventListener("input", () => {
        if (elec_usage.value < 0) {
            elec_usage.value = 0;
        } else {
            emissionFactor = carbonIntensitiesObject[elec_country.value];
            const co2 = Math.round(emissionFactor * elec_usage.value * 52).toLocaleString("en-US");
            elec_carbon_footprint.innerHTML = "Grams of CO<sub>2</sub> Produced Yearly: <strong>" + (co2) + " gCO<sub>2</sub></strong>"
            elec_co2_input.value = co2;
        }
    })

    
    // Public Transportation (Reason for x1000 multiplication is to convert from kg to g)
    const publicEmissionFactors = {
        "Taxi": 0.17699 * 1000,
        "Bus": 0.14986 * 1000,
        "Coach": 0.03471 * 1000,
        "Subway": 0.08154 * 1000,
        "Light Rail": 0.07659 * 1000,
        "National Train": 0.06715 * 1000
    }
    const transit_type = document.querySelector("#id_transport_type");
    const transit_dist = document.querySelector("#id_distance");
    const transit_co2 = document.querySelector("#transport_co2");
    const transit_co2_input = document.querySelector("#co2_transport")

    transit_type.addEventListener('change', () => {
        emissionFactor = publicEmissionFactors[transit_type.value];

        if (transit_dist.value != 0) {
            const co2 = Math.round(emissionFactor * transit_dist.value * 52).toLocaleString("en-US"); // x52 due to data being weekly
            transit_co2.innerHTML = "Grams of CO<sub>2</sub> Produced Yearly: <strong>" + (co2) + " gCO<sub>2</sub></strong>"
            transit_co2_input.value = co2;
        }
    })
    transit_dist.addEventListener("input", () => {
        if (transit_dist.value < 0) {
            transit_dist.value = 0;
        } else {
            emissionFactor = publicEmissionFactors[transit_type.value]
            const co2 = Math.round(emissionFactor * transit_dist.value * 52).toLocaleString("en-US");
            transit_co2.innerHTML = "Grams of CO<sub>2</sub> Produced Yearly: <strong>" + (co2) + " gCO<sub>2</sub></strong>"
            transit_co2_input.value = co2;
        }
    })


    // Flight
    const flightEmissionFactors = {
        "Domestic Flight": 0.20124 * 1000,
        "Short Economy Class Flight": 0.10946 * 1000,
        "Short Business Class Flight": 0.16419 * 1000,
        "Long Economy Class Flight": 0.09594 * 1000,
        "Long Business Class Flight": 0.27823 * 1000,
    }
    const flight_type = document.querySelector("#id_flight_type");
    const flight_dist = document.querySelector("#id_flight_dist");
    const flight_co2 = document.querySelector("#flight_co2");
    const flight_co2_input = document.querySelector("#co2_flight");

    flight_type.addEventListener('change', () => {
        emissionFactor = flightEmissionFactors[flight_type.value];

        if (flight_dist.value != 0) {
            const co2 = Math.round(emissionFactor * flight_dist.value).toLocaleString("en-US");
            flight_co2.innerHTML = "Grams of CO<sub>2</sub> Produced Yearly: <strong>" + (co2) + " gCO<sub>2</sub></strong>"
            flight_co2_input.value = co2;
        }
    })
    flight_dist.addEventListener("input", () => {
        if (flight_dist.value < 0) {
            flight_dist.value = 0;
        } else {
            emissionFactor = flightEmissionFactors[flight_type.value]
            const co2 = Math.round(emissionFactor * flight_dist.value).toLocaleString("en-US");
            flight_co2.innerHTML = "Grams of CO<sub>2</sub> Produced Yearly: <strong>" + (co2) + " gCO<sub>2</sub></strong>"
            flight_co2_input.value = co2;
        }
    })


    // Car
    const carEmissionFactors = {
        "Diesel Car": 0.21291 * 1000,
        "Petrol Car": 0.24927 * 1000,
        "Hybrid Car": 0.13984 * 1000,
        "Petrol Van": 0.31079 * 1000,
        "Diesel Van": 0.27402 * 1000
    }
    const car_type = document.querySelector("#id_car_type");
    const car_dist = document.querySelector("#id_car_dist");
    const car_co2 = document.querySelector("#car_co2");
    const car_co2_input = document.querySelector("#co2_car");

    car_type.addEventListener('change', () => {
        emissionFactor = carEmissionFactors[car_type.value];

        if (car_dist.value != 0) {
            const co2 = Math.round(emissionFactor * car_dist.value * 52).toLocaleString("en-US");
            car_co2.innerHTML = "Grams of CO<sub>2</sub> Produced Yearly: <strong>" + (co2) + " gCO<sub>2</sub></strong>"
            car_co2_input.value = co2;
        }
    })
    car_dist.addEventListener("input", () => {
        if (car_dist.value < 0) {
            car_dist.value = 0;
        } else {
            emissionFactor = carEmissionFactors[car_type.value]
            const co2 = Math.round(emissionFactor * car_dist.value * 52).toLocaleString("en-US");
            car_co2.innerHTML = "Grams of CO<sub>2</sub> Produced Yearly: <strong>" + (co2) + " gCO<sub>2</sub></strong>"
            car_co2_input.value = co2;
        }
    })


    emissionFactor = carbonIntensitiesObject[elec_country.value];
    let co2 = Math.round(emissionFactor * elec_usage.value * 52).toLocaleString("en-US");
    elec_carbon_footprint.innerHTML = "Grams of CO<sub>2</sub> Produced Yearly: <strong>" + (co2) + " gCO<sub>2</sub></strong>"
    elec_co2_input.value = co2;

    emissionFactor = publicEmissionFactors[transit_type.value]
    co2 = Math.round(emissionFactor * transit_dist.value * 52).toLocaleString("en-US");
    transit_co2.innerHTML = "Grams of CO<sub>2</sub> Produced Yearly: <strong>" + (co2) + " gCO<sub>2</sub></strong>"
    transit_co2_input.value = co2;

    emissionFactor = flightEmissionFactors[flight_type.value]
    co2 = Math.round(emissionFactor * flight_dist.value).toLocaleString("en-US");
    flight_co2.innerHTML = "Grams of CO<sub>2</sub> Produced Yearly: <strong>" + (co2) + " gCO<sub>2</sub></strong>"
    flight_co2_input.value = co2;
    
    emissionFactor = carEmissionFactors[car_type.value]
    co2 = Math.round(emissionFactor * car_dist.value * 52).toLocaleString("en-US");
    car_co2.innerHTML = "Grams of CO<sub>2</sub> Produced Yearly: <strong>" + (co2) + " gCO<sub>2</sub></strong>"
    car_co2_input.value = co2;
}