function strip(string) {
    return string.replace(/^\s+|\s+$/g, '');
}

function checkGroupName(input) {
    input = strip(input);
    const format = /^[a-zA-Z0-9._ -]{5,50}$/;
    if (input.match(format)) {
        return true;
    }
    return false;
}

function checkedCount(checkboxes) {
    let checked = 0;
    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            checked++;
        }
    }
    return checked;
}

function validateForm() {
    let groupName = document.getElementById("id_name");
    let checkboxes = document.getElementsByName('branch');
    let checked = checkedCount(checkboxes);
    
    err_section = document.getElementById("err");
    err_section.innerHTML = "";

    let no_err = true;
    if (!checkGroupName(groupName.value)) {
        err_section.innerHTML += "<li>Group name: Invalid format, allowed only alphanumeric characters, space and .-_ characters.</li>";
        groupName.classList.add('errInput');
        no_err = false;
    } else {
        groupName.classList.value = '';
    }
    
    if (checked == 0) {
        err_section.innerHTML += "<li>Branch: This field is required</li>";
        no_err = false;
    } 

    return no_err;
}
