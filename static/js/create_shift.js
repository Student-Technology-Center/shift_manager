var shiftsToBeSubmitted = [];

$(document).ready(function() {
    $('#calendar').fullCalendar({

        //customs
        customButtons: {
            confirmShifts: {
                text: 'Submit Shifts',
                click: submitNewShifts
            }
        },

        header: {
            left: '',
            right: 'confirmShifts'
        },

        /* settings below */
        defaultView: 'agendaWeek',
        allDaySlot: false,
        slotLabelFormat: 'h a',
        slotDuration: '01:00:00',
        columnFormat: 'dddd',
        minTime: '08:00:00',
        maxTime: '21:00:00',

        /* event binding */
        dayClick: handleDayClick,
    })
})

function handleDayClick(data, jsEvent, view) {
    //We have to add 7 because theres a bug in the lib we use,
    //if this line is acting weird, remove the .add().
    var newEvent = {
        title: "Test",
        allDay: false,
        start: moment(data._d).add(8, 'hours'),
        end: moment(data._d).add(9, 'hours')
    };

    $('#calendar').fullCalendar('renderEvent', newEvent);
}

function submitNewShifts() {
    alert('Submitted. (This does nothing right now)')
}