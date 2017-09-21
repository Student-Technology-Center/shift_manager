$(document).ready(function(){
    $('#calendar').fullCalendar({
        defaultView: "agendaWeek",
        weekNumbers: false,
        firstDay: 1,
    });
    $('#submit_shift').click(function() {

        var day = document.getElementById('id_day_of_week').value
        var start = document.getElementById('id_start').value
        var end = document.getElementById('id_end').value

        $.ajax({
            url: '/shifts/api/add_shift/',
            type: 'POST',
            data: {
                "csrfmiddlewaretoken": csrf_token,
                "day": day,
                "start": start,
                "end": end
            },
            success: function(data) {
                console.log(data);
            }
        })
    });
})
