var payloadsForSubmission = [];
var modalOpen = true;
var selectedEvent = null;
var showDebug = false;
var curretUser;

var clr_db = {  }

$(document).ready(function() {
    $(this).keypress(function(e) {
        if (e.which == 96) {
            switchDebug();
        }
    })

    $('#calendar').fullCalendar({

        header: {
            left: 'title',
            right: ''
        },

        /* settings below */
        defaultView: 'agendaWeek',
        allDaySlot: false,
        slotLabelFormat: 'h a',
        slotDuration: '01:00:00',
        columnFormat: 'dddd',
        minTime: '08:00:00',
        maxTime: '21:00:00',
        agendaEventMinHeight: document.getElementById('calendar').offsetHeight / 14,
        height: "parent",
        contentHeight: "auto",
        displayEventTime: false,
        aspectRatio: 1,

        /* event binding */
        dayClick: handleDayClick,
        eventClick: handleEventClick
    })

    $('#modal-background').click(function (){
        switchModal();
    })

    $('.fc-left h2').text('');

    $('#submit-shifts').click(function(){submitNewShifts()});

    getEvents();
})

function switchDebug(){
    showDebug = !showDebug;

    if (showDebug)
        $('#debug-window').css({'visibility':'visible'});
    else
        $('#debug-window').css({'visibility':'hidden'})
}

function switchModal() {
    modalOpen = !modalOpen;
    if (modalOpen) {
        $('#modal').css({
            'visibility':'hidden'
        })
        $('#modal-background').css({
            'visibility':'hidden'
        })
    } else {
        $('#modal').css({
            'visibility':'visible'
        })
        $('#modal-background').css({
            'visibility':'visible'
        })
    }
}

/*
    This is a custom defined JavaScript object
    specifically made to easily communicate with
    the backend. It sends a payload which denotes
    if it is deleting/adding a shift, to whom,
    and when said thing starts.

    It error handles, but be careful.

    action: 
        'delete' - Deletes the [username]'s shift at [timeStart]
        'create' - Creates a shift for [username] at [timeStart]

    timeStart:
        '[hh:mm]' - Sent in military time, denotes when the shift starts.
                    This works since shifts should only be in hour intervals.
*/
function Payload(action, timeStart, dow) {
    if (typeof action != "string"){
        throw "Payload.action must be a string"
    }

    if (typeof timeStart != "string") {
        throw "Payload.timeStart must be a string"
    }

    if (action != 'create' && action != 'delete') {
        throw "Payload.action must be either 'create' or 'delete'"
    }

    if (timeStart.length != 5 && timeStart.length != 8) {
        throw "Payload.timeStart not correct length"
    }

    if (dow.length != 3) {
        throw "Payload.date format should be 'mon, tue, fri, sat'"
    }

    this.action = action;
    this.timeStart = timeStart;
    this.dow = dow;
}

function handleDayClick(data, jsEvent, view) {
    var startTime = moment(data);
    var endTime = moment(data).add(1, 'hours');

    var newEvent = {
        title: currentUserFullName,
        allDay: false,
        start: startTime,
        end: endTime,
    };

    var events = $('#calendar').fullCalendar('clientEvents');

    //Queue up for creation
    payloadsForSubmission.push(new Payload('create', startTime.format('HH:mm'), startTime.format('ddd')));
    $('#calendar').fullCalendar('renderEvent', newEvent, true);
}

function handleEventClick(data, jsEvent, view) {
    selectedEvent = data;
    console.log(data);
    //switchModal();
}

function handleModalDelete() {
    $('#calendar').fullCalendar('removeEvents', function(event) {
        return selectedEvent._id === event._id
    });

    var currentPayload = new Payload('delete', selectedEvent.start.format("HH:mm"), selectedEvent.start.format('ddd'));
    var found = false;

    for (i = 0; i < payloadsForSubmission.length; i++) {
        if (payloadsForSubmission[i].timeStart === currentPayload.timeStart &&
                payloadsForSubmission[i].dow === currentPayload.dow) {
            payloadsForSubmission.splice(i, 1);
            found = true;
        }
    }

    //Queue up for backend deletion
    if (!found) {
        payloadsForSubmission.push(currentPayload);
    }

    selectedEvent = null;
    switchModal();
}

/* 
    This method prepares shifts for submission

    TODO: Make all the setting of (visual) information
    is done in one function, shouldn't be spread everywhere.

*/
function submitNewShifts() {
    var token = $('#csrf_token input').val();
    var payloads = [];

    for (i = 0; i < payloadsForSubmission.length; i++) {
        payloads[i] = payloadsForSubmission[i];
    }

    console.log(payloads);

    $.ajax({
        type: 'POST',
        url: '/shifts/api/payload_dock/',
        data: {
            csrfmiddlewaretoken:token,
            payloads: payloads,
        },
        fail: function () {
            setError("Something went wrong - file a bug report. Please retry the submission");
        },
        success: function(data) {
            console.log(data);
        }
    })
    payloadsForSubmission = [];
}

function getEvents() {
    $.ajax({
        type:'GET',
        url:'/shifts/api/get_shifts/',
        dataType: 'json',
        success: function(data) {
            createEvents(data.details)
        }
    });
}

function createEvents(data) {
    data.forEach(function(el) {
        var ev = moment(el.datetime);
        var ene = moment(el.datetime);
        ene.add(1, 'hours');
        $('#calendar').fullCalendar('renderEvent', {
            title:el.name,
            start:ev,
            end: ene
        })
    });
}

function deleteShifts() {
    $.ajax({
        type: 'GET',
        url: 'shifts/api/deleteall/'
    })
}

function setError(msg) {
    $('#error-box').text(msg);
}

function checkForFailure(msg) {
    setError(msg);
}

function get_current_user() {
    $.ajax({
        type: 'GET',
        url: '/shifts/api/get_turn_user/',
        success: function(data) { user = data.details }
    })
}