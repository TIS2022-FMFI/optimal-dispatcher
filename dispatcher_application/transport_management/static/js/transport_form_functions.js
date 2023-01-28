function strip(string) {
    return string.replace(/^\s+|\s+$/g, '');
}

function checkLocation(input) {
    input = strip(input);
    const format = /([0-9]{5,10})[ ,/.]([A-Z][a-z]{1,69})[ ,/.]([A-Z]{2,4})/;
    if (input.match(format)) {
        return true;
    }
    return false;
}

function checkInfo(input) {
    input = strip(input);
    const format = /^[a-zA-Z0-9._ -]/;
    if (input.match(format)) {
        return true;
    }
    return false;
}

function validateForm() {
    let from_location = document.getElementById("from_id");
    let to_location = document.getElementById("to_id");
    let departure_time = document.getElementById("departure_time");
    let arrival_time = document.getElementById("arrival_time");
    let weight = document.getElementById("weight");
    let ldm = document.getElementById("ldm");
    let info = document.getElementById("info");

    let err_section = document.getElementById("err");
    err_section.innerHTML = "";

    let no_err = true;
    if (!checkLocation(from_location.value)) {
        err_section.innerHTML += "<li>From location: Invalid format, expected: zip code,City,Country code</li>";
        from_location.classList.add('errInput');
        no_err = false;
    } else {
        from_location.classList.value = '';
    }

    if (!checkLocation(to_location.value)) {
        err_section.innerHTML += "<li>To location: Invalid format, expected: zip code,City,Country code.</li>";
        to_location.classList.add('errInput');
        no_err = false;
    } else {
        to_location.classList.value = '';
    }

    if (!departure_time < arrival_time) {
        err_section.innerHTML += "<li>Departure time must be before arrival time.</li>";
        departure_time.classList.add('errInput');
        no_err = false;
    } else {
        departure_time.classList.value = '';
    }


    if (ldm < 0 || ldm > 13.6) {
        err_section.innerHTML += "<li>Ldm must be between 0 and 13.6.</li>";
        ldm.classList.add('errInput');
        no_err = false;
    } else {
        ldm.classList.value = '';
    }

    if (weight < 0 || weight > 24000) {
        err_section.innerHTML += "<li>Weight must be between 0 and 24000.</li>";
        weight.classList.add('errInput');
        no_err = false;
    } else {
        weight.classList.value = '';
    }

    if (!checkInfo(info.value)) {
        err_section.innerHTML += "<li>Info: Invalid format, allowed only alphanumeric characters, space and .-_ characters.</li>";
        info.classList.add('errInput');
        no_err = false;
    } else {
        info.classList.value = '';
    }

    return no_err;
}
