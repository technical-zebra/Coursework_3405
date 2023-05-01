let qid = 0;
let length = 0;
let sec = 5;
let answer = 0
let identity = ""
let nickname = ""

/**
 * The code includes a function to count down and another function to load images with parameters for
 * query and length.
 */
function countDown() {
    let timerId = setInterval(() => setTimerText(), 1000);
    // after 15 seconds stop
    setTimeout(() => {
        clearInterval(timerId);
    }, 5000);
}

/**
 * The function "loadImage" sets the values of "qid" and "length" based on the input parameters "q" and
 * "len".
 * @param q - The parameter "q" is the question id.
 * @param len - The "len" parameter is the length.
 */
function loadImage(q,len){
    // alert(q,len)
    qid = q;
    length = len;
}


/**
 * The function sets a timer text and sends an answer via AJAX if the timer reaches zero and the
 * identity is "student".
 */
function setTimerText() {
    document.getElementById('js_timer').innerHTML = '00:' + sec + ' s';
    sec = sec - 1;
    if (sec <= 0) {

        if (identity == "student") {

            $.ajax({
                url: "/send-answer",
                method: "POST",
                data: JSON.stringify({ ans: answer, quizId: qid, nickname: nickname }),
                contentType: "application/json",
                success: function(response) {
                    console.log("Answer successfully sent!");
                },
                error: function(xhr, textStatus, errorThrown) {
                    console.error("Failed to send answer. Error: " + errorThrown);
                }
            });
        }
    }
}

/**
 * The function loads settings and hides the teacher block if the user is a student.
 */
function loadSetting() {
    countDown();

    identity = document.getElementById('identity').innerHTML;
    nickname  = document.getElementById('nickname').innerHTML;
    if (identity == "student"){
        document.getElementById('TeacherBlock').style.display = 'none';
    }


}


/**
 * The function hides certain elements and sets the answer variable if the identity is "student".
 * @param quizId - The ID of the quiz being taken.
 * @param ans - The answer submitted by the student taking the quiz.
 * @param length - The length parameter is not used in the given function. It is not clear what it
 * represents or what its purpose is.
 */
function SubmitAnswer(quizId, ans, length) {


    if (identity == "student"){
        document.getElementById('TeacherBlock').style.display = 'none';
        document.getElementById('waiting').style.display = 'inline-flex';
        document.getElementById('btnGroup1').style.display = 'none';
        document.getElementById('btnGroup2').style.display = 'none';
        answer = ans
    }


}

/* This code block is using jQuery to wait for the document to be fully loaded before executing the
function. It then creates a socket connection and listens for the 'redirect quiz' event. When this
event is triggered, it sends a socket message with the data 'Q' + qid and redirects the user to
either the leaderboard or the next quiz page depending on the value of qid and length. */
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

/**
 * The function sends a socket message to begin the next quiz if the user is a teacher.
 * @returns nothing (undefined).
 */
function nextQuiz(){
    var socket = io();
    if (identity == "teacher"){
        socket.emit('next quiz', {data: "begin next quiz now"});
                return;
    }
}

