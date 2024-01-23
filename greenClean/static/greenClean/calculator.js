document.addEventListener("DOMContentLoaded", () => {

    // Tooltip Child
    // const tooltipChild = document.querySelectorAll(".tooltip-child");
    // const tooltipParent = document.querySelectorAll(".tooltip-parent");
    // // tooltipChild.forEach((x, idx) => {
    // //     x.style.display = "inline-flex";
    // //     const height = x.offsetHeight;
    // //     x.style.display = "none";
    // //     console.log((tooltipParent[idx].offsetTop));
    // //     x.style.top = (tooltipParent[idx].offsetTop - height) + "px";
    // // })

    let allFormSections = document.querySelectorAll(".form-section");
    let allFormHeaders = document.querySelectorAll(".form-header")
    let activeHeader = document.querySelector(".active-header")
    
    let carbonFootprints = document.querySelector(".carbon-footprint")

    // Electricity Carbon Footprint
    const elec_country = document.querySelector("#id_location")
    const elec_usage = document.querySelector("#id_energy")
    const elec_carbon_footprint = document.querySelector("#energy_co2")
    
    let carbonIntensitiesObject = JSON.parse(carbonIntensities);

    let emissionFactor = 0;

    elec_country.addEventListener('change', () => {
        emissionFactor = carbonIntensitiesObject[elec_country.value];
        if (elec_usage.value != 0) {
            const co2 = Math.round(emissionFactor * elec_usage.value * 12)
            elec_carbon_footprint.innerHTML = "Grams of CO<sub>2</sub> Produced Yearly: <strong>" + (co2) + " gCO<sub>2</sub></strong>"
        }
    })
    elec_usage.addEventListener("input", () => {
        emissionFactor = carbonIntensitiesObject[elec_country.value];
        const co2 = Math.round(emissionFactor * elec_usage.value * 12);
        elec_carbon_footprint.innerHTML = "Grams of CO<sub>2</sub> Produced Yearly: <strong>" + (co2) + " gCO<sub>2</sub></strong>"
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

    transit_type.addEventListener('change', () => {
        emissionFactor = publicEmissionFactors[transit_type.value];

        if (transit_dist.value != 0) {
            const co2 = Math.round(emissionFactor * transit_dist.value * 52) // x52 due to data being weekly
            transit_co2.innerHTML = "Grams of CO<sub>2</sub> Produced Yearly: <strong>" + (co2) + " gCO<sub>2</sub></strong>"
        }
    })
    transit_dist.addEventListener("input", () => {
        emissionFactor = publicEmissionFactors[transit_type.value]
        const co2 = Math.round(emissionFactor * transit_dist.value * 52);
        transit_co2.innerHTML = "Grams of CO<sub>2</sub> Produced Yearly: <strong>" + (co2) + " gCO<sub>2</sub></strong>"
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

    flight_type.addEventListener('change', () => {
        emissionFactor = flightEmissionFactors[flight_type.value];

        if (flight_dist.value != 0) {
            const co2 = Math.round(emissionFactor * flight_dist.value)
            flight_co2.innerHTML = "Grams of CO<sub>2</sub> Produced Yearly: <strong>" + (co2) + " gCO<sub>2</sub></strong>"
        }
    })
    flight_dist.addEventListener("input", () => {
        emissionFactor = flightEmissionFactors[flight_type.value]
        const co2 = Math.round(emissionFactor * flight_dist.value);
        flight_co2.innerHTML = "Grams of CO<sub>2</sub> Produced Yearly: <strong>" + (co2) + " gCO<sub>2</sub></strong>"
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

    car_type.addEventListener('change', () => {
        emissionFactor = carEmissionFactors[car_type.value];

        if (car_dist.value != 0) {
            const co2 = Math.round(emissionFactor * car_dist.value * 52)
            car_co2.innerHTML = "Grams of CO<sub>2</sub> Produced Yearly: <strong>" + (co2) + " gCO<sub>2</sub></strong>"
        }
    })
    car_dist.addEventListener("input", () => {
        emissionFactor = carEmissionFactors[car_type.value]
        const co2 = Math.round(emissionFactor * car_dist.value * 52);
        car_co2.innerHTML = "Grams of CO<sub>2</sub> Produced Yearly: <strong>" + (co2) + " gCO<sub>2</sub></strong>"
    })


    allFormSections.forEach((x, idx) => {
        x.addEventListener("focusin", () => {
            activeHeader.style.height = allFormHeaders[idx].offsetHeight + "px";
            activeHeader.style.top = allFormHeaders[idx].offsetTop + "px";
        })
        x.addEventListener("focusout", () => {
            activeHeader.style.height = 0;
        })


    })

})