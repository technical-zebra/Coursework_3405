let identity = ""
let nickname = ""
function loadSetting() {
    identity = document.getElementById('identity').innerHTML;
    nickname = document.getElementById('nickname').innerHTML;

    if (identity == "student"){
        document.getElementById('TeacherBlock').style.display = 'none';

        var socket = io();

        socket.emit('join hall', {data: nickname});
    }

}

function startQuiz(){
    var socket = io();
    if (identity == "teacher"){
        socket.emit('begin quiz', {data: "begin quiz now"});
                return;
    }
}

$(document).ready(function() {
    var socket = io();

    socket.on('redirect', function() {
        socket.emit('my_event', {data: 'Q1'});
        window.location.href = "/run_test/0";
    });

    socket.on('new student', function(msg) {
                $('#log').append('<div  class="col">' + $('<div/>').text(msg.data).html());
    });

});
