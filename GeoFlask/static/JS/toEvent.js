document.addEventListener('DOMContentLoaded', function(){
    mobileScreen();
    markWeekend();

});

function mobileScreen(){
    var screenWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
    if (screenWidth < 550){
        document.getElementById("calendarPcDiv").style.display = "none";
        document.getElementById("calendarPcOptionsDiv").style.display = "none";

        const calPcLabel = document.getElementById("calPcLabel");
        calPcLabel.style.paddingLeft = "0px";
    }
    else {
        document.getElementById("calendarMobileDiv").style.display = "none";
        document.getElementById("calendarMobileOptionsDiv").style.display = "none";
    }

}

function markWeekend(){
    document.querySelectorAll(".calendarMobileDayDiv").forEach(function(elm){
        if(elm.dataset.weekday > 4){
            elm.style.background = "#e0e0d1";
        }
    });
    document.querySelectorAll(".calendarPcDayDiv").forEach(function(elm){
        if(elm.dataset.weekday > 4){
            elm.style.background = "#e0e0d1";
        }
    });
}

function getDays(startDate, num){
    const start = document.getElementById(startDate).value;
    const number = Number(document.getElementById(num).value);
    const anchor = document.createElement("a");
    anchor.href =`/calendar?start=${start}&num_days=${number}`;
    anchor.click();
}