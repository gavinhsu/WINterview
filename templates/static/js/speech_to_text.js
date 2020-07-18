try {
  var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  var recognition = new SpeechRecognition();
}
catch (e) {
  console.error(e);
  // $('.no-browser-support').show();
  $('.app').show();
}


var noteTextarea = $('#note-textarea');
var instructions = $('#recording-instructions');
var notesList = $('ul#notes');

var noteContent = '';

// Get all notes from previous sessions and display them.
var notes = getAllNotes();
renderNotes(notes);

/*-----------------------------
      Voice Recognition 
------------------------------*/

// If false, the recording will stop after a few seconds of silence.
// When true, the silence period is longer (about 15 seconds),
// allowing us to keep recording even when the user pauses. 
recognition.continuous = true;
recognition.lang = "en-US";

// This block is called every time the Speech APi captures a line. 
recognition.onresult = function (event) {

  // event is a SpeechRecognitionEvent object.
  // It holds all the lines we have captured so far. 
  // We only need the current one.
  var current = event.resultIndex;

  // Get a transcript of what was said.
  var transcript = event.results[current][0].transcript;

  // Add the current transcript to the contents of our Note.
  // There is a weird bug on mobile, where everything is repeated twice.
  // There is no official solution so far so we have to handle an edge case.
  var mobileRepeatBug = (current == 1 && transcript == event.results[0][0].transcript);

  if (!mobileRepeatBug) {
    noteContent += transcript;
    noteTextarea.val(noteContent);
  }
};

recognition.onstart = function () {
  instructions.text('Voice recognition activated. Try speaking into the microphone.');
}

recognition.onspeechend = function () {
  instructions.text('You cannot answer anymore.');
}

recognition.onerror = function (event) {
  if (event.error == 'no-speech') {
    instructions.text('No speech was detected. Try again.');
  };
}

/*-----------------------------
      App buttons and input 
------------------------------*/

$('#start-record-btn').on('click', function (e) {
  if (noteContent.length) {
    noteContent += ' ';
  }
  recognition.start();
});


$('#pause-record-btn').on('click', function (e) {
  recognition.stop();
  instructions.text('Voice recognition paused.');
});

// Sync the text inside the text area with the noteContent variable.
noteTextarea.on('input', function () {
  noteContent = $(this).val();
})


/*-----------------------------
      Speech Synthesis 
------------------------------*/
$(document).ready(function () {
  $("#speak").click()
})

function speak() {
  var question = document.getElementById("question").innerHTML;
  readOutLoud(question);
}

function readOutLoud(message) {
  var speech = new SpeechSynthesisUtterance();

  // Set the text and voice attributes.
  speech.text = message;
  speech.volume = 1;
  speech.rate = 1;
  speech.pitch = 1;
  speech.lang = 'en-US';

  window.speechSynthesis.speak(speech);

}

/*-----------------------------
      countdown function 
------------------------------*/
var spn = document.getElementById("countStart");
var startRecord = document.getElementById("start-record-btn");
var pauseRecord = document.getElementById("pause-record-btn");

var count = 5;     // Set count
var timer = null;  // For referencing the timer
var timer2 = null; 
var count1 = 100;

(function countDownStart() {
  // Display counter and start counting down
  spn.textContent = count;

  // Run the function again every second if the count is not zero
  if (count !== 0) {
    timer = setTimeout(countDownStart, 1000);
    count--; // decrease the timer
  } else {
    // Enable the button
    startRecord.click();
    spn.style.display = "none"

    if(spn.style.display = "none"){
      spn.textContent = count1;
      spn.style.display = "block";

      // Run the function again every second if the count is not zero
      if (count1 !== 0) {
        timer2 = setTimeout(countDownStart, 1000);
        count1--; // decrease the timer
      } else {
        // Enable the button
        pauseRecord.click();
        spn.style.display = "none"
      }
    }
  }
}());



/*-----------------------------
      Helper Functions 
------------------------------*/

function renderNotes(notes) {
  var html = '';
  notesList.html(html);
}


function saveNote(dateTime, content) {
  localStorage.setItem('note-' + dateTime, content);
}

function getAllNotes() {
  var notes = [];
  var key;
  for (var i = 0; i < localStorage.length; i++) {
    key = localStorage.key(i);

    if (key.substring(0, 5) == 'note-') {
      notes.push({
        date: key.replace('note-', ''),
        content: localStorage.getItem(localStorage.key(i))
      });
    }
  }
  return notes;
}




