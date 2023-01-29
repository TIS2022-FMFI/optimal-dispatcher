function cleanFields() {
    // clear filters
    document.getElementById('owner-id').value = "";
    document.getElementById('from-location-id').value = "";
    document.getElementById('departure-date-id').value = "";
    document.getElementById('arrival-date-id').value = "";

    // submit with cleared filters 
    document.getElementById("transport-searchbar").submit();
}
