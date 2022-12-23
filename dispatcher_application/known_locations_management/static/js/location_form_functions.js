function checkCity(input) {
    const format = /^[A-Z][a-z]{1,69}$/;
    if (input.match(format)) {
        return true;
    }
    return false;
}

function checkCountry(input) {
    const format = /^[A-Z]{2,3}$/;
    if (input.match(format)) {
        return true;
    }
    return false;
}

function validateForm() {
    let zip_code = document.getElementById("id_zip_code").value;
    let city = document.getElementById("id_city").value;
    let country = document.getElementById("id_country").value;
   
    err_section = document.getElementById("err");
    err_section.innerHTML = "";
   
    let no_err = true;
    if (!checkCity(city)) {
        err_section.innerHTML += "<li>City : Must consist of letters and start with capital letter</li>";
        no_err = false;
    } 
    
    if (!checkCountry(country)) {
        err_section.innerHTML += "<li>Country : Must consist of capital letters, format(SK, SVK, FR, FRA)</li>";
        no_err = false;
    }
    return no_err;
}