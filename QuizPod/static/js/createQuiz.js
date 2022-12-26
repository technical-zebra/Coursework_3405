function SelectRadioValue() {
    
    var radios = document.getElementsByName('QuizMode');

    //alert(radios[0].checked);


    if (radios[0].checked) {
        //alert(radios[0].value); testing only
        document.getElementById('choice1Block').style.display = 'block';
        document.getElementById('choice2Block').style.display = 'block';
        document.getElementById('choice3Block').style.display = 'none';
        document.getElementById('choice4Block').style.display = 'none';
        document.getElementById('choice1').setAttribute('value', 'True');
        document.getElementById('choice2').setAttribute('value', 'False');
        document.getElementById('choice1').readOnly = true;
        document.getElementById('choice2').readOnly = true;
    } else {
        //alert(radios[1].value); testing only
        document.getElementById('choice1Block').style.display = 'block';
        document.getElementById('choice2Block').style.display = 'block';
        document.getElementById('choice3Block').style.display = 'block';
        document.getElementById('choice4Block').style.display = 'block';
        document.getElementById('choice1').setAttribute('value', '');
        document.getElementById('choice2').setAttribute('value', '');
        document.getElementById('choice1').readOnly = false;
        document.getElementById('choice2').readOnly = false;
    }
}