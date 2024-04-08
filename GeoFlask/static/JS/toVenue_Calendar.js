document.addEventListener('DOMContentLoaded', function () {
    mobScreen("venue_cal_PcDiv", "venue_cal_MobDiv");
    mobScreen("venue_booking_PcDiv", "venue_booking_MobDiv");
    filterVenue(); // Call it once to apply initial filter based on default or URL parameters
    datePickerForm()


});


function datePickerForm() {
    // Adjust the selector to target the specific form by ID
    const form = document.querySelector('#mobileDatePickerForm');  // sjekk at id stemmer
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const datePicker = document.getElementById('singleDay'); // sjekk at id stemmer
            const date = datePicker.value;
            const actionURL = `/venue_cal_single_day/${date}`;
            window.location.href = actionURL;
        });
    }
}



function mobScreen(pcDivId, mobDivId) {


    let screenWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;

    let pcDiv = document.getElementById(pcDivId);
    let mobDiv = document.getElementById(mobDivId);

    if (pcDiv && mobDiv) {
        if (screenWidth < 550) {
            pcDiv.style.display = "none";
            mobDiv.style.display = "block";
        } else {
            pcDiv.style.display = "block";
            mobDiv.style.display = "none";
        }
    } else {
        console.log("One or both elements not found:", pcDivId, mobDivId);
    }
}

function filterVenue() {
    let selectedVenue = null;
    let selectedDate = null;

    // Get all properties by ID
    const venueDropdown = document.getElementById("venueDropdown");
    if (venueDropdown) {selectedVenue = venueDropdown.value; }
    const filterDate = document.getElementById("filterDate");
    if (filterDate) {selectedDate = filterDate.value;}

    console.log("Selected Venue:", selectedVenue)
    console.log("Selected Date:", selectedDate)

    // Select all properties (venues, events)
    const venues = document.querySelectorAll('[id^="venue-info-"]');
    console.log("Total Venues Found:", venues.length);
    const events = document.querySelectorAll('[id^="event-info-"]');
    console.log("Total Events Found:", events.length);


    // Initially hide all venues & events.
    venues.forEach(venue => venue.style.display = 'none');
    events.forEach(event => event.style.display = 'none');

    // If ID -> show venue.id OR if "All -> show all venues
    venues.forEach(function (venue) {
        let venueId = venue.getAttribute('id').replace('venue-info-', '');
        console.log("Checking Venue ID:", venueId);

        // Show venue if "all" is selected OR if venue matches selection
        if (selectedVenue === 'all' || venueId === selectedVenue) {
            console.log("Displaying Venue ID:", venueId); // Debugging log
            venue.style.display = 'block';

            // Within this venue: filter and show events based on the selected date
            let venueEvents = venue.querySelectorAll('.event'); // Ensure your events have a class 'event'

            // loop through the events
            venueEvents.forEach(function(event) {
                let eventDate = event.getAttribute('data-date');

                if (!selectedDate || eventDate === selectedDate) {
                    event.style.display = 'block';
                } else {
                    event.style.display = 'none';
                }
            });
        }
    });
}
