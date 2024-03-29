function strip(string) {
    return string.replace(/^\s+|\s+$/g, '');
}

function checkName(input) {
    input = strip(input);
    let result = { status : true, message : "" }

    if (input.length > 70) {
        result.status = false;
        result.message = "Maximum length is 70 characters.";
        return result;
    } 

    if (input.length < 2) {
        result.status = false;
        result.message = "Minimum length is 2 characters.";
        return result;
    }
    return result
}

function checkEmail(input) {
    input = strip(input);
    let result = { status : true, message : "" }
    
    if (input.length > 60) {
        result.status = false;
        result.message = "Maximum length is 60 characters.";
        return result;
    } 

    const format = /^[A-Za-z0-9._-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$/;
    if (!input.match(format)) {
        result.status = false;
        result.message = "Invalid format, allowed alphanumeric characters and .-_@ characters.";
    }

    return result;
}


function validateCreateForm() {
    let firstNameElement = document.getElementById("id_first_name");
    let lastNameElement = document.getElementById("id_last_name");
    let emailElement = document.getElementById("id_email");
    
    err_section = document.getElementById("err");
    err_section.innerHTML = "";
    let no_err = true;

    let result = checkName(firstNameElement.value);
    if (!result.status) {
        err_section.innerHTML += "<li>First name : " + result.message + "</li>";
        no_err = false;
    } 

    result = checkName(lastNameElement.value);
    if (!result.status) {
        err_section.innerHTML += "<li>Second name : " + result.message + "</li>";
        no_err = false;
    } 

    result = checkEmail(emailElement.value);
    if (!result.status) {
        err_section.innerHTML += "<li>Email : " + result.message + "</li>";
        no_err = false;
    } 
    return no_err;
}


function validateUpdateForm() {
    let firstNameElement = document.getElementById("id_first_name");
    let lastNameElement = document.getElementById("id_last_name");
  
    let err_section = document.getElementById("err");
    err_section.innerHTML = "";
    let no_err = true;

    let result = checkName(firstNameElement.value);
    if (!result.status) {
        err_section.innerHTML += "<li>First name : " + result.message + "</li>";
        no_err = false;
    }

    result = checkName(lastNameElement.value);
    if (!result.status) {
        err_section.innerHTML += "<li>Second name : " + result.message + "</li>";
        no_err = false;
    } 

    return no_err;
}


