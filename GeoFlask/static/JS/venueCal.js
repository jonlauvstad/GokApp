function filterVenue() {
    var selectedVenue = document.getElementById("venueDropdown").value;
    var rows = document.querySelectorAll("table tr");

    rows.forEach(function(row) {
        if(selectedVenue == "all" || row.getAttribute("data-venue-id") === selectedVenue) {
            row.style.display = ""; // Show row
        } else {
            row.style.display = "none"; // Hide row
        }
    });
}
