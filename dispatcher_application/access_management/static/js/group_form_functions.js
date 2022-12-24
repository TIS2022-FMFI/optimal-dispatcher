function checkGroupName(input) {
    const format = /^[a-zA-Z0-9._-]{5,50}$/;
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
    let name = document.getElementById("id_name").value;
    let checkboxes = document.getElementsByName('branch');
    let checked = checkedCount(checkboxes);
    
    err_section = document.getElementById("err");
    err_section.innerHTML = "";

    let no_err = true;
    if (!checkGroupName(name)) {
        err_section.innerHTML += "<li>Group name: Allowed only alphanumeric characters and .-_</li>";
        no_err = false;
    } 
    
    if (checked == 0) {
        err_section.innerHTML += "<li>Branch: This field is required</li>";
        no_err = false;
    }
    return no_err;
}
