function strip(string) {
    return string.replace(/^\s+|\s+$/g, '');
}

function checkName(input) {
    input = strip(input);
    let result = { status : true, message : "" }
    if (input.length < 2) {
        result.status = false;
        result.message = "Must be at least 2 characters long.";
        return result;
    }

    const format = /^[A-Z][a-z]{1,69}$/;
    if (!input.match(format)) {
        result.status = false;
        result.message = "Allowed only alphabet characters, must start with capital letter.";
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

function checkPassword(pass1, pass2) {
    pass1 = strip(pass1);
    pass2 = strip(pass2);
    let result = { status : true, message : "" }

    if (pass1 != pass2) {
        result.status = false;
        result.message = "The two password fields didn\’t match."
    }

    if (pass1.length < 8) {
        result.status = false;
        result.message = "This password is too short. It must contain at least 8 characters."
    }
    return result
}


function validateCreateForm() {
    let firstNameElement = document.getElementById("id_first_name");
    let lastNameElement = document.getElementById("id_last_name");
    let emailElement = document.getElementById("id_email");
    let pass1Element = document.getElementById("id_password1");
    let pass2Element = document.getElementById("id_password2");
    
    err_section = document.getElementById("err");
    err_section.innerHTML = "";
    let no_err = true;

    let result = checkName(firstNameElement.value);
    if (!result.status) {
        err_section.innerHTML += "<li>First name : " + result.message + "</li>";
        firstNameElement.classList.add('errInput');
        no_err = false;
    } else {
        firstNameElement.classList.value = '';
    }

    result = checkName(lastNameElement.value);
    if (!result.status) {
        err_section.innerHTML += "<li>Second name : " + result.message + "</li>";
        lastNameElement.classList.add('errInput');
        no_err = false;
    } else {
        lastNameElement.classList.value = '';
    }

    result = checkEmail(emailElement.value);
    if (!result.status) {
        err_section.innerHTML += "<li>Email : " + result.message + "</li>";
        emailElement.classList.add('errInput');
        no_err = false;
    } else {
        emailElement.classList.value = '';
    }

    result = checkPassword(pass1Element.value, pass2Element.value);
    if (!result.status) {
        err_section.innerHTML += "<li> Password confirmation : " + result.message + "</li>"
        pass1Element.classList.add('errInput');
        pass2Element.classList.add('errInput');
        no_err = false;
    } else {
        pass1Element.classList.value = '';
        pass2Element.classList.value = '';
    }

    return no_err;
}


function validateUpdateForm() {
    let firstNameElement = document.getElementById("id_first_name");
    let lastNameElement = document.getElementById("id_last_name");
  
    err_section = document.getElementById("err");
    err_section.innerHTML = "";
    let no_err = true;

    let result = checkName(firstNameElement.value);
    if (!result.status) {
        err_section.innerHTML += "<li>First name : " + result.message + "</li>";
        firstNameElement.classList.add('errInput');
        no_err = false;
    } else {
        firstNameElement.classList.value = '';
    }

    result = checkName(lastNameElement.value);
    if (!result.status) {
        err_section.innerHTML += "<li>Second name : " + result.message + "</li>";
        lastNameElement.classList.add('errInput');
        no_err = false;
    } else {
        lastNameElement.classList.value = '';
    }

    return no_err;
}


