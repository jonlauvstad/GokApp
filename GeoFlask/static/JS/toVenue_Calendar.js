document.addEventListener('DOMContentLoaded', function (){
    mobScreen();
});

function mobScreen()
{
    var screenWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
    if (screenWidth < 550)
    {
        document.getElementById("venue_cal_PcDiv").style.display = "none";
    }
    else {
        document.getElementById("venue_cal_MobDiv").style.display = "none";
    }
}

function filterVenue()
{
    // selectedVenue -> dropdown choice
    // selectedVenueDiv -> refererer til div'en

    var selectedVenue = document.getElementById("venueDropdown").value;
    var selectedDate = document.getElementById("filterDate").value;
    var events = document.querySelectorAll('.event');
    var venues = document.querySelectorAll('[id^="venue-info-"]');
    //var rows = document.querySelectorAll("table tr");

    // hide alle Events først ..
    events.forEach(function (event)
    {
        event.style.display = 'none'
    });

    // hide alle Venues først ..
    venues.forEach(function (div)
    {
        div.style.display = 'none';
    });



    // display bare den valgte venue basert på id
    if (selectedVenue !== 'all')
    {
        var selectedVenueDiv = document.getElementById('venue-info-' + selectedVenue);
        if (selectedVenueDiv)
        {
            selectedVenueDiv.style.display = 'block';
        }
    }
    else
    {
        // dersom "All Venues" er selected..
        venues.forEach(function (div)
        {
            div.style.display = "block";

        });
    }

    // display event basert på valgt venue.
    events.forEach(function (event)
    {
        var eventVenueId = event.getAttribute('data-venue-id');
        var eventDate = event.getAttribute('data-date');

        if ((selectedVenue === 'all' || eventVenueId === selectedVenue) && eventDate === selectedDate)
        {
            event.style.display = 'block';
        }
        else
        {
            event.style.display = 'none';

        }
    });



    // logging ..
    console.log("selected date:", selectedDate);
    events.forEach(function (event){
        var eventVenueId = event.getAttribute('data-venue-id');
        var eventDate = event.getAttribute('data-date');

        console.log("Event date:", eventDate, "Venue ID:", eventVenueId);

        if ((selectedVenue === 'all' || eventVenueId === selectedVenue) && eventDate === selectedDate){
            console.log("VISER EVENTS FOR ROM:", eventVenueId, "PÅ DATO", eventDate);
            event.style.display = 'block';
        }
    });
}
