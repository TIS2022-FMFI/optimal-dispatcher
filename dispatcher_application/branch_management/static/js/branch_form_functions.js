function strip(string) {
    return string.replace(/^\s+|\s+$/g, '');
}

function checkBranchName(input) {
    input = strip(input);
    let result = { status : true, message : "" }
    if (input.length > 70) {
        result.status = false;
        result.message = "Maximum length is 70 characters.";
        return result;
    }

    if (input.length < 4) {
        result.status = false;
        result.message = "Minimum length is 4 characters.";
        return result;
    }

    const format = /^[a-zA-Z0-9_ -]{4,70}$/;
    if (!input.match(format)) {
        result.status = false;
        result.message = "Invalid format, allowed alphanumeric characters, space and _- characters.";
        return result;
    }
    return result
}


function validateForm() {
    let branchName = document.getElementById("id_name");
  
    err_section = document.getElementById("err");
    err_section.innerHTML = "";
    let no_err = true;

    let result = checkBranchName(branchName.value);
    if (!result.status) {
        err_section.innerHTML += "<li>Name : " + result.message + "</li>";
        branchName.classList.add('errInput');
        no_err = false;
    } else {
        branchName.classList.value = '';
    }

    return no_err;
}