document.addEventListener('DOMContentLoaded', function () {
    toggleDisplayBasedOnScreenWidth();
    // mobScreen();
    filterVenue();
    datePickerForm()
});

function toggleDisplayBasedOnScreenWidth() {
    const screenWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
    if (screenWidth < 550) {
        document.getElementById("venue_cal_PcDiv").style.display = "none";
        document.getElementById("venue_cal_MobDiv").style.display = "block";
    } else {
        document.getElementById("venue_cal_PcDiv").style.display = "block";
        document.getElementById("venue_cal_MobDiv").style.display = "none";
    }
}

function datePickerForm() {
    // Adjust the selector to target the specific form by ID
    const form = document.querySelector('#mobileDatePickerForm');
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const datePicker = document.getElementById('singleDay');
            const date = datePicker.value;
            const actionURL = `/venue_cal_single_day/${date}`;
            window.location.href = actionURL;
        });
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

    // velg ALLE properties (venues, events)
    const venues = document.querySelectorAll('[id^="venue-info-"]');
    console.log("Total Venues Found:", venues.length);
    const events = document.querySelectorAll('[id^="event-info-"]');
    console.log("Total Events Found:", events.length);


    // utgangspunkt - hide alle venues & events
    venues.forEach(venue => venue.style.display = 'none');
    events.forEach(event => event.style.display = 'none');

    // hvis ID -> show venue.id ELLER hvis "All -> show all venues
    venues.forEach(function (venue) {
        let venueId = venue.getAttribute('id').replace('venue-info-', '');
        console.log("Checking Venue ID:", venueId);

        // Vis venue hvis "all" er selected ELLER hvis venue matcher selection
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



document.querySelectorAll('.datePickerForm').forEach(form => {
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const startDate = form.querySelector('[name="start"]').value;
        const endDate = form.querySelector('[name="end"]').value;
        const actionURL = `/venue_calendar?start=${encodeURIComponent(startDate)}&end=${encodeURIComponent(endDate)}`;
        window.location.href = actionURL;
    });
});
