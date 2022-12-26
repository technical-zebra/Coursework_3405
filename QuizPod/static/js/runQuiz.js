let qid = 0;
let length = 0;
let sec = 5;
let answer = 0
let identity = ""
let nickname = ""

function countDown() {
    let timerId = setInterval(() => setTimerText(), 1000);
    // after 15 seconds stop
    setTimeout(() => {
        clearInterval(timerId);
    }, 5000);
}

function loadImage(q,len){
    // alert(q,len)
    qid = q;
    length = len;
}

function setTimerText() {
    document.getElementById('js_timer').innerHTML = '00:' + sec + ' s';
    sec = sec - 1;
    if (sec <= 0) {

        // qid = document.getElementById('qid').textContent;
        // qid = qid.replace("Question ", "").replace(":", "");

        if (identity == "student") {

            fetch("/send-answer", {
                method: "POST",
                body: JSON.stringify({ans: answer, quizId: qid, nickname: nickname}),
            }).then((_res) => {
            });
        }
    }
}

function loadSetting() {
    countDown();

    identity = document.getElementById('identity').innerHTML;
    nickname  = document.getElementById('nickname').innerHTML;
    if (identity == "student"){
        document.getElementById('TeacherBlock').style.display = 'none';
    }


}


function SubmitAnswer(quizId, ans, length) {


    if (identity == "student"){
        document.getElementById('TeacherBlock').style.display = 'none';
        document.getElementById('waiting').style.display = 'inline-flex';
        document.getElementById('btnGroup1').style.display = 'none';
        document.getElementById('btnGroup2').style.display = 'none';
        answer = ans
    }


}

$(document).ready(function() {
    var socket = io();

    socket.on('redirect quiz', function() {
        socket.emit('my_event', {data: 'Q' + qid});
        if (qid >= length) {
                window.location.href = "/leaderboard";
            } else {
                window.location.href = "/run_test/" + qid;
            }
    });

});

function nextQuiz(){
    var socket = io();
    if (identity == "teacher"){
        socket.emit('next quiz', {data: "begin next quiz now"});
                return;
    }
}

