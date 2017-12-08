var payloadsForSubmission = [];
var modalOpen = true;
var selectedEvent = null;

$(document).ready(function() {
    //Add all events
    getEvents();

    $('#calendar').fullCalendar({

        customButtons: {
            passOnTurn: {
                text: 'Pass',
                click: function () {
                    passOnTurn();
                }
            }
        },

        header: {
            left: 'title',
            right: 'passOnTurn'
        },

        /* settings below */
        defaultView: 'agendaWeek',
        allDaySlot: false,
        slotLabelFormat: 'h a',
        slotDuration: '01:00:00',
        columnFormat: 'dddd',
        minTime: '08:00:00',
        maxTime: '21:00:00',
        contentHeight: "auto",
        height: "auto",
        agendaEventMinHeight: 100,

        /* event binding */
        dayClick: handleDayClick,
        eventClick: handleEventClick
    })

    $('#modal-background').click(function (){
        switchModal();
    })

    $('.fc-left h2').text('');

    setCurrentUser(currentUserUsername)
})

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

    username:
        '[username]' - Who the action acts upon

    timeStart:
        '[hh:mm]' - Sent in military time, denotes when the shift starts.
                    This works since shifts should only be in hour intervals.
*/
function Payload(action, username, timeStart, dow) {
    if (typeof action != "string"){
        throw "Payload.action must be a string"
    }

    if (typeof username != "string") {
        throw "Payload.username must be a string"
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
    this.username = username;
    this.timeStart = timeStart;
    this.dow = dow;
}

function handleDayClick(data, jsEvent, view) {
    //We have to add 7 because theres a bug in the lib we use,
    //if this line is acting weird, remove the .add()

    var startTime = moment(data);
    var endTime = moment(data).add(1, 'hours');

    var newEvent = {
        title: currentUserFullName,
        allDay: false,
        start: startTime,
        end: endTime,
        user: currentUserUsername
    };

    //Queue up for creation
    payloadsForSubmission.push(new Payload('create', currentUserUsername, startTime.format('HH:mm'), startTime.format('ddd')));
    $('#calendar').fullCalendar('renderEvent', newEvent, true);
    submitNewShifts();
}

function handleEventClick(data, jsEvent, view) {
    selectedEvent = data;
    switchModal();
}

function handleModalDelete() {
    $('#calendar').fullCalendar('removeEvents', function(event) {
        return selectedEvent._id === event._id
    });

    var currentPayload = new Payload('delete', selectedEvent.user, selectedEvent.start.format("HH:mm"), selectedEvent.start.format('ddd'));
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
    submitNewShifts();
    switchModal();
}

function passOnTurn() {
    var token = $('#csrf_token input').val();
    $.ajax({
        type: 'POST',
        url: '/shifts/api/create/',
        data: {
            csrfmiddlewaretoken:token,
            'pass':currentUserUsername
        },
        fail: function () {
            alert("Something went wrong - file a bug report. Please retry the submission");
        },
        success: function(data) {
            if (data.status === "failure") {
                checkForFailure(data.message);
            } else {
                if (data.action === 'create') {
                    setCurrentUser(data.next_user);
                    currentUserFullName = data.first + " " + data.last;
                    $('#amt_left_' + data.current_username).text(data.turns_left_current);
                }

                //Happens when shift is deleted.
                if(data.username) {
                    $('#amt_left_' + data.username).text(data.turns_left_current);                        
                }
            }
        }
    })  
}

/* 
    This method prepares shifts for submission

    TODO: Make all the setting of (visual) information
    is done in one function, shouldn't be spread everywhere.

*/
function submitNewShifts() {
    var token = $('#csrf_token input').val();
    for (i = 0; i < payloadsForSubmission.length; i++) {
        $.ajax({
            type: 'POST',
            url: '/shifts/api/create/',
            data: {
                csrfmiddlewaretoken:token,
                payload:payloadsForSubmission[i]
            },
            fail: function () {
                alert("Something went wrong - file a bug report. Please retry the submission");
            },
            success: function(data) {
                if (data.status === "failure") {
                    checkForFailure(data.message);
                } else {
                    if (data.action === 'create') {
                        setCurrentUser(data.next_user);
                        currentUserFullName = data.first + " " + data.last;
                        $('#amt_left_' + data.current_username).text(data.turns_left_current);
                    }

                    //Happens when shift is deleted.
                    if(data.username) {
                        $('#amt_left_' + data.username).text(data.turns_left_current);                        
                    }
                }
            }
        })
    }
    payloadsForSubmission = [];
}

function getEvents() {
    var data;

    $.ajax({
        type:'GET',
        url:'/shifts/api/getallshifts/',
        dataType: 'json',
        success: function(data) { createEvents(data); }
    });
}

function createEvents(data) {
    var DOW = {
        "Sun":[0],
        "Mon":[1],
        "Tue":[2],
        "Wed":[3],
        "Thu":[4],
        "Fri":[5],
        "Sat":[6]
    }

    for (var key in data) {
        if (data.hasOwnProperty(key)) {
            var newEvent = {
                title: data[key].first_name + " " + data[key].last_name,
                allDay: false,
                start: data[key].start,
                end: data[key].end,
                dow: DOW[data[key].day_of_week],
                user: data[key].username
            };
            $('#calendar').fullCalendar('renderEvent', newEvent, true);
        }
    }
}

function deleteShifts() {
    $.ajax({
        type: 'GET',
        url: 'shifts/api/deleteall/'
    })
}

//lul
function checkForFailure(msg) {
    $('.fc-left h2').text(msg);
}

function setCurrentUser(new_user) {
    $('#' + currentUserUsername).css({
        'color':'black'
    })
    currentUserUsername = new_user
    $('#' + currentUserUsername).css({
        'color':'red'
    })
}