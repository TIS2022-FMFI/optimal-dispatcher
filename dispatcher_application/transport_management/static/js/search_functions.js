function cleanFields() {
    // clear filters
    document.getElementById('owner_id').value = "";
    document.getElementById('from_location_id').value = "";
    document.getElementById('departure_date_id').value = "";
    document.getElementById('arrival_date_id').value = "";

    // submit with cleared filters 
    document.getElementById("transport-searchbar").submit();
}
