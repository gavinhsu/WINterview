'use strict'
/* global MediaRecorder, Blob, URL */

/**
 * Get DOM element
 */
// <video> element
let inputVideo = document.querySelector('#inputVideo')
let outputVideo = document.querySelector('#outputVideo')

// <button> element
let startBtn = document.querySelector('#startBtn')
let stopBtn = document.querySelector('#stopBtn')
let resetBtn = document.querySelector('#resetBtn')

// error message
let errorElement = document.querySelector('#errorMsg')

// is-recording icon
let isRecordingIcon = document.querySelector('.is-recording')

/**
 * Global variables
 */
//透過start(只觸發一次，一次送回整包資料) 或 start(1000)每隔一定時間回傳一包資料(把取得資料推進chunk[])
let chunks = [] // 在 mediaRecord 要用的 chunks

// 在 getUserMedia 使用的 constraints 變數
//定義要取得的影音內容(影像和聲音)
let constraints = {
  audio: true,
  video: true
}

// 第一次啟動攝影機
mediaRecorderSetup()

/**
 * MediaRecorder Related Event Handler
 */
let mediaRecorder = null
let inputVideoURL = null
let outputVideoURL = null

startBtn.addEventListener('click', onStartRecording)
stopBtn.addEventListener('click', onStopRecording)
resetBtn.addEventListener('click', onReset)

/**
 * MediaRecorder Methods
 */
// Start Recording: mediaRecorder.start()
function onStartRecording (e) {
  e.preventDefault()
  e.stopPropagation()
  isRecordingBtn('stop')
  mediaRecorder.start()
  console.log('mediaRecorder.start()')
}

// Stop Recording: mediaRecorder.stop()
function onStopRecording (e) {
  e.preventDefault()
  e.stopPropagation()
  isRecordingBtn('reset')
  mediaRecorder.stop()
  inputVideo.style.display="none"
  console.log('mediaRecorder.stop()')
}

// Reset Recording
function onReset (e) {
  e.preventDefault()
  e.stopPropagation()
  inputVideo.style.display="block"

  // 釋放記憶體
  URL.revokeObjectURL(inputVideoURL)
  URL.revokeObjectURL(outputVideoURL)
  outputVideo.src = ''
  outputVideo.controls = false
  inputVideo.src = ''

  // 重新啟動攝影機
  mediaRecorderSetup()
}

/**
 * Setup MediaRecorder
 **/
//再次錄製需要重新啟動，所以把啟動到錄製的步驟包在mediaRecorderSetup
function mediaRecorderSetup () {
  // 設定顯示的按鍵
  isRecordingBtn('start')

  // mediaDevices.getUserMedia() 取得使用者媒體影音檔/即時播放於瀏覽器
  //請求開啟影音裝置
  navigator.mediaDevices
    .getUserMedia(constraints)
    .then(function (stream) {
      // 瀏覽器會去請求使用者的麥克風和相機權限
      /**
       * inputVideo Element
       * 將串流的 inputVideo 設定到 <video> 上
       * HTMLMediaElement.srcObject或URL.createObjectURL()
       **/
      // Older browsers may not have srcObject
      if ('srcObject' in inputVideo) {
        inputVideo.srcObject = stream
      } else {
        // Avoid using this in new browsers, as it is going away.
        inputVideo.src = window.URL.createObjectURL(stream)
      }
      inputVideo.controls = false //是否顯示播放控制器

      /**
       * 透過 MediaRecorder 錄製影音串流
       */
      // 建立 MediaRecorder 準備錄影
      // 如果沒有指定 mimeType，錄下來的 webm 影片在 Firefox 上可能不能看（Firefox 也不支援 h264)
      mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'video/webm;codecs=VP9',
        // bitsPerSecond: '512000',
      })

      /* MediaRecorder EventHandler */
      mediaRecorder.addEventListener(
        'dataavailable',
        mediaRecorderOnDataAvailable
      ) // 有資料傳入時觸發
      mediaRecorder.addEventListener('stop', mediaRecorderOnStop) // 停止錄影時觸發

      //e.data: 有可用資料傳入時利用dataavailable事件取得
      //丟回整包錄製好的檔案，取得資料
      function mediaRecorderOnDataAvailable (e) {
        console.log('mediaRecorder on dataavailable', e.data)
        chunks.push(e.data)
      }

      //chunk array轉成Blob物件(=檔案)
      function mediaRecorderOnStop (e) {
        console.log('mediaRecorder on stop')
        outputVideo.controls = true
        var blob = new Blob(chunks, { type: 'video/webm' }) //video/webm可透過chrome打開
        chunks = [] //清空chunks
        outputVideoURL = URL.createObjectURL(blob) //把影音連結丟給<video>
        outputVideo.src = outputVideoURL //錄製好的影片可以呈現於outputvideo
        //saveData(outputVideoURL)

        // 停止所有的輸入或輸出的串流裝置（例如，關攝影機）
        stream.getTracks().forEach(function (track) {
          track.stop()
        })
      }
    })//取得當前裝置的stream的錯誤發生時
    .catch(function (error) {
      if (error.name === 'ConstraintNotSatisfiedError') {
        errorMsg(
          'The resolution ' +
            constraints.video.width.exact +
            'x' +
            constraints.video.width.exact +
            ' px is not supported by your device.'
        )
      } else if (error.name === 'PermissionDeniedError') {
        errorMsg('Permissions have not been granted to use your media devices')
      }
      errorMsg('getUserMedia error: ' + error.name, error)
    })
}

/**
 * DOM EventListener
 * 畫面卡頻問題
 * 媒體檔的metadata完成載入時被觸發(播放媒體)
 */
inputVideo.addEventListener('loadedmetadata', function () {
  inputVideo.play()
  console.log('inputVideo on loadedmetadata')
})

/**
 * Other Function
 */
function errorMsg (msg, error) {
  console.log('errorElement', errorElement)
  errorElement.classList.add('alert', 'alert-warning')
  errorElement.innerHTML += msg
  if (typeof error !== 'undefined') {
    console.error(error)
  }
}

// // 自動下載
// function saveData (dataURL) {
//   var fileName = 'my-download-' + Date.now() + '.webm'
//   var a = document.createElement('a')
//   document.body.appendChild(a)
//   a.style = 'display: none'
//   a.href = dataURL
//   a.download = fileName
//   a.click()
// }

function isRecordingBtn (recordBtnState) {
  startBtn.style.display = 'none'
  stopBtn.style.display = 'none'
  resetBtn.style.display = 'none'
  isRecordingIcon.style.display = 'none'
  switch (recordBtnState) {
    case 'start':
      startBtn.style.display = 'block' // show startBtn
      break
    case 'stop':
      stopBtn.style.display = 'block' // show stopBtn
      isRecordingIcon.style.display = 'block'
      break
    case 'reset':
      resetBtn.style.display = 'block' // show resetBtn
      break
    default:
      console.warn('isRecordingBtn error')
  }
}


try {
  var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  var recognition = new SpeechRecognition();
}
catch(e) {
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
recognition.onresult = function(event) {

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

  if(!mobileRepeatBug) {
    noteContent += transcript;
    noteTextarea.val(noteContent);
  }
};

recognition.onstart = function() { 
  instructions.text('Voice recognition activated. Try speaking into the microphone.');
}

recognition.onspeechend = function() {
  instructions.text('You were quiet for a while so voice recognition turned itself off.');
}

recognition.onerror = function(event) {
  if(event.error == 'no-speech') {
    instructions.text('No speech was detected. Try again.');  
  };
}

/*-----------------------------
      App buttons and input 
------------------------------*/

$('#start-record-btn').on('click', function(e) {
  if (noteContent.length) {
    noteContent += ' ';
  }
  recognition.start();
});


$('#pause-record-btn').on('click', function(e) {
  recognition.stop();
  instructions.text('Voice recognition paused.');
});

// Sync the text inside the text area with the noteContent variable.
noteTextarea.on('input', function() {
  noteContent = $(this).val();
})

//Save noteContent to database Answer model
// $(document).ready(function(){
//   function onchange(evt){
//     $.ajax({
//       url:'/speech_to_text/',
//       type: 'POST',
//       data: {'noteContent':noteContent},
//     }).
//   }
// })



////////////////////////////////////////////////////////////////////////////////////////
$('#save-note-btn').on('click', function(e) {
  recognition.stop();

  if(!noteContent.length) {
    instructions.text('Could not clear empty message. Please say something to your microphone.');
  }
  else {
    // Save note to localStorage.
    // The key is the dateTime with seconds, the value is the content of the note.
    saveNote(new Date().toLocaleString(), noteContent);

    // Reset variables and update UI.
    noteContent = '';
    renderNotes(getAllNotes());
    noteTextarea.val('');
    instructions.text('Speech cleared successfully.');
  }
      
})

  

notesList.on('click', function(e) {
  e.preventDefault();
  var target = $(e.target);

  // Listen to the selected note.
  if(target.hasClass('listen-note')) {
    var content = target.closest('.note').find('.content').text();
    readOutLoud(content);
  }

  // Delete note.
  if(target.hasClass('delete-note')) {
    var dateTime = target.siblings('.date').text();  
    deleteNote(dateTime);
    target.closest('.note').remove();
  }
});

/*-----------------------------
      Speech Synthesis 
------------------------------*/
function speak(){
  document.getElementById("question").style.display ="inline";
  var question = document.getElementById("question").innerHTML;
  readOutLoud(question);
  }

// function() disappear(){
//   var speakButton = document.getElementById("speak");
//   speakButton.style.display="none";
// }

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
      Helper Functions 
------------------------------*/

function renderNotes(notes) {
  var html = '';
  if(notes.length) {
    notes.forEach(function(note) {
      html+= `<li class="note">
        <p class="header">
          <span class="date">${note.date}</span>
          <a href="#" class="listen-note" title="Listen to Note">Listen to Note</a>
          <a href="#" class="delete-note" title="Delete">Delete</a>
        </p>
        <p class="content">${note.content}</p>
      </li>`;    
    });
  }
  else {
    html = '<li><p class="content">You don\'t have any notes yet.</p></li>';
  }
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

    if(key.substring(0,5) == 'note-') {
      notes.push({
        date: key.replace('note-',''),
        content: localStorage.getItem(localStorage.key(i))
      });
    } 
  }
  return notes;
}


function deleteNote(dateTime) {
  localStorage.removeItem('note-' + dateTime); 
}

document.getElementById("next").addEventListener("click", audio2video);

function audio2video(){
  document.getElementById("audio").style.display="none"
  document.getElementById("video").style.display="block"

}