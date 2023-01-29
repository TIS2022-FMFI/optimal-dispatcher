function strip(string) {
    return string.replace(/^\s+|\s+$/g, '');
}

function checkLocation(input) {
    input = strip(input);
    const format = /([0-9]{5,10}),([A-Z][a-z]{1,69}),([A-Z]{2,4})/;
    if (input.match(format)) {
        return true;
    }
    return false;
}

function checkInfo(input) {
    input = strip(input);
    const format = /^[a-zA-Z0-9._ @-]*$/;
    if (input.match(format)) {
        return true;
    }
    return false;
}

function validateForm() {
    let from_location = document.getElementById("id_from_id");
    let to_location = document.getElementById("id_to_id");
    let departure_time = document.getElementById("id_departure_time");
    let arrival_time = document.getElementById("id_arrival_time");
    let weight = document.getElementById("id_weight");
    let ldm = document.getElementById("id_ldm");
    let info = document.getElementById("id_info");

    let err_section = document.getElementById("err");
    err_section.innerHTML = "";

    let no_err = true;
    if (!checkLocation(from_location.value)) {
        err_section.innerHTML += "<li>From : Invalid format, expected: zip code,city,country code.</li>";
        from_location.classList.add('errInput');
        no_err = false;
    } else {
        from_location.classList.value = '';
    }

    if (!checkLocation(to_location.value)) {
        err_section.innerHTML += "<li>To : Invalid format, expected: zip code,City,Country code.</li>";
        to_location.classList.add('errInput');
        no_err = false;
    } else {
        to_location.classList.value = '';
    }

    if (arrival_time.value < departure_time.value) {
        err_section.innerHTML += "<li>Arrival time : Date must be after departure time.</li>";
        departure_time.classList.add('errInput');
        no_err = false;
    } else {
        departure_time.classList.value = '';
    }


    if (ldm < 0 || ldm > 100) {
        err_section.innerHTML += "<li>Ldm : Value must be between 0 and 100.</li>";
        ldm.classList.add('errInput');
        no_err = false;
    } else {
        ldm.classList.value = '';
    }

    if (weight < 0 || weight > 100000) {
        err_section.innerHTML += "<li>Weight : Value must be between 0 and 100 000.</li>";
        weight.classList.add('errInput');
        no_err = false;
    } else {
        weight.classList.value = '';
    }

    if (!checkInfo(info.value)) {
        err_section.innerHTML += "<li>Info : Invalid format, allowed only alphanumeric characters, space and .@-_ characters.123</li>";
        info.classList.add('errInput');
        no_err = false;
    } else {
        info.classList.value = '';
    }

    return no_err;
}
