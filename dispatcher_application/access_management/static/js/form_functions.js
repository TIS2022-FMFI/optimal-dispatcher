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

function validateForm(form) {
    let name = form.id_name.value;
    let checkboxes = document.getElementsByName('branch');
    let checked = checkedCount(checkboxes);
    
    if (checkGroupName(name) & checked) return true;   
    
    console.log('false');
    x = document.getElementsByClassName("error-class")//.innerHTML += "<p>djkajdkajsdka<p>";
    x.innerHTML += "<li> text : error sprava</li>";
    console.log(x);
    return false;
}

