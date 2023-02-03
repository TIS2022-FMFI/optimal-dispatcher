function strip(string) {
    return string.replace(/^\s+|\s+$/g, '');
}

function checkCity(input) {
    input = strip(input);
    const format = /^[A-Z][a-z]{1,69}$/;
    if (input.match(format)) {
        return true;
    }
    return false;
}

function checkCountry(input) {
    input = strip(input);
    const format = /^[A-Z]{2,3}$/;
    if (input.match(format)) {
        return true;
    }
    return false;
}

function checkZipCode(input) {
    input = strip(input);
    const format = /^[0-9A-Za-z- _]{4,13}$/;
    if (input.match(format)) {
        return true;
    }
    return false;
}

function validateForm() {
    let zip_code = document.getElementById("id_zip_code");
    let city = document.getElementById("id_city");
    let country = document.getElementById("id_country");
   
    let err_section = document.getElementById("err");
    err_section.innerHTML = "";
   
    let no_err = true;
    if (!checkZipCode(zip_code.value)) {
        err_section.innerHTML += "<li>Zip code : Invalid format, allowed alphanumeric characters, space, - and _.</li>";
        no_err = false;
    }


    if (!checkCity(city.value)) {
        err_section.innerHTML += "<li>City : Invalid format, allowed alphabet characters, must start with capital letter.</li>";
        no_err = false;
    }
    
    if (!checkCountry(country.value)) {
        err_section.innerHTML += "<li>Country : Invalid format, allowed capital letters, format(SK, SVK, FR, FRA).</li>";
        no_err = false;
    } 
    return no_err;
}