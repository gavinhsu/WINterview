//MediaRecording
let inputVideo = document.querySelector('#inputVideo')
let outputVideo = document.querySelector('#outputVideo')
let startBtn = document.querySelector('#startBtn')
let stopBtn = document.querySelector('#stopBtn')
let blobURL = document.querySelector('#blobURL')
let file = document.getElementById('#file')

let chunks = []
let constraints = {
    audio: true,
    video: true
}

mediaRecorderSetup()
let mediaRecorder = null
let inputVideoURL = null
let outputVideoURL = null

startBtn.addEventListener('click', onStartRecording)
stopBtn.addEventListener('click', onStopRecording)

function onStartRecording(e) {
    e.preventDefault()
    e.stopPropagation()
    isRecordingBtn('stop')
    mediaRecorder.start()
    console.log('mediaRecorder.start()')
}

function onStopRecording(e) {
    e.preventDefault()
    e.stopPropagation()
    isRecordingBtn('reset')
    mediaRecorder.stop()
    console.log('mediaRecorder.stop()')
}

function mediaRecorderSetup() {
    // 設定顯示的按鍵
    isRecordingBtn('start')
    navigator.mediaDevices.getUserMedia(constraints).then(function (stream) {
        if ('srcObject' in inputVideo) {
            inputVideo.srcObject = stream
        } else {
            inputVideo.src = window.URL.createObjectURL(stream)
        }
        inputVideo.controls = false

        mediaRecorder = new MediaRecorder(stream, {
            mimeType: 'video/webm;codecs=VP9',
        })

        mediaRecorder.addEventListener(
            'dataavailable',
            mediaRecorderOnDataAvailable
        ) // 有資料傳入時觸發
        mediaRecorder.addEventListener('stop', mediaRecorderOnStop) // 停止錄影時觸發

        function mediaRecorderOnDataAvailable(e) {
            console.log('mediaRecorder on dataavailable', e.data)
            chunks.push(e.data)
        }

        function mediaRecorderOnStop(e) {
            console.log('mediaRecorder on stop')
            outputVideo.controls = true
            var blob = new Blob(chunks, { type: 'video/webm' }) //video/webm可透過chrome打開
            chunks = [] //清空chunks
            outputVideoURL = URL.createObjectURL(blob) //把影音連結丟給<video>
            outputVideo.src = outputVideoURL //錄製好的影片可以呈現於outputvideo
            console.log(blob)

            function blobToFile(blob, fileName) {
                var a = document.createElement("a");
                document.body.appendChild(a);
                a.style = "top: 1000px";
                var url = window.URL.createObjectURL(blob);
                a.href = url;
                a.download = fileName;
                a.textContent = "DOWNLOAD " + fileName;
                document.getElementById('blobURL').innerHTML = "BLOB URL: <b>" + url + "</b>";
                document.getElementById('download').appendChild(a);
            }
            var myFile = blobToFile(blob, "video.mp4");
            console.log(myFile)

            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }

            var csrftoken = getCookie('csrftoken');
            // function csrfSafeMethod(method) {
            //     // these HTTP methods do not require CSRF protection
            //     return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
            // }
            // $.ajaxSetup({
            //     beforeSend: function (xhr, settings) {
            //         if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            //             xhr.setRequestHeader("X-CSRFToken", csrftoken);
            //         }
            //     }
            // });
            console.log(csrftoken)
            var fd = new FormData()
            fd.append('video', blob)
            fd.append('csrfmiddlewaretoken', csrftoken);
            $.ajax({
            url: 'http://127.0.0.1:8000/speech_to_text/',
            enctype: 'multipart/form-data',
            method: 'POST',
            data:  fd,
            processData: false,
            contentType: false,
            cache: false,
            success: function (data) {
                console.log('response' + JSON.stringify(data));
            },
            error: function (e) {
                // handle error case here
                console.log("ERROR : ", e);
            }
            });

            // var xhr = new XMLHttpRequest
            // xhr.responseType = 'blob'
            // xhr.onload = function () {
            //     var recoveredBlob = xhr.response
            //     var reader = new FileReader
            //     reader.onload = function () {
            //         var blobAsDataUrl = reader.result
            //         window.location = blobAsDataUrl
            //     }
            //     reader.readAsDataURL(recoveredBlob)
            // }
            // xhr.open('GET', outputVideoURL)
            // console.log('OPENED', xhr.status);
            // xhr.send()

            stream.getTracks().forEach(function (track) {
                track.stop()

            })
        }
    })//取得當前裝置的stream的錯誤發生時
}



inputVideo.addEventListener('loadedmetadata', function () {
    inputVideo.play()
    console.log('inputVideo on loadedmetadata')
})

function isRecordingBtn(recordBtnState) {
    startBtn.style.display = 'none'
    stopBtn.style.display = 'none'
    switch (recordBtnState) {
        case 'start':
            startBtn.style.display = 'block' // show startBtn
            break
        case 'stop':
            stopBtn.style.display = 'block' // show stopBtn
            break
        default:
            console.warn('isRecordingBtn error')
    }
}


//countdown
var spn = document.getElementById("countStart");
var startRecord = document.getElementById("start-record-btn");
var pauseRecord = document.getElementById("pause-record-btn");

// Set count
var timer = null;  // For referencing the timer
var timer2 = null;

var submit = document.getElementById("submit");

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

        if (spn.style.display = "none") {
            spn.textContent = count1;
            spn.style.display = "block";

            // Run the function again every second if the count is not zero
            if (count1 !== 0) {
                timer2 = setTimeout(countDownStart, 1000);
                count1--; // decrease the timer
            } else {
                // Enable the button
                submit.click();
                pauseRecord.click();
                spn.style.display = "none"
            }
        }
    }
}());