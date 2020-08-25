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
            $('#submit').prop('disabled', false);
            $('#submit').removeClass('disable-btn');
            $('#submit').on('click', function(){
                var btn = $(this);
                btn.html('Saving...').prop('disabled', true).addClass('disable-btn');
                outputVideo.controls = true
                var blob = new Blob(chunks, { type: 'video/webm' }) //video/webm可透過chrome打開
                chunks = [] //清空chunks
                outputVideoURL = URL.createObjectURL(blob) //把影音連結丟給<video>
                outputVideo.src = outputVideoURL //錄製好的影片可以呈現於outputvideo
                console.log(blob)
                console.log(outputVideoURL)
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
                var csrf = $('input[name="csrfmiddlewaretoken"]').val();
                console.log(csrf)
                var csrftoken = getCookie('csrftoken');
                console.log(csrftoken)
                var data = new FormData();
                data.append('video', blob);
                data.append('csrfmiddlewaretoken', csrftoken);
                $.ajax({
                    url: "http://127.0.0.1:8000/videoUploadTest/",
                    method: 'post',
                    data: data,
                    success: function(data){
                        if(data.success){
                            btn.html('Re Submit');
                            $('.upload-comp').show();
                        }
                        else{
                            btn.html('Error').prop('disabled', false).removeClass('disable-btn');
                        }
                    },
                    cache: false,
                    contentType: false,
                    processData: false
                })
            stream.getTracks().forEach(function (track) {
                track.stop()
            })
        })}
    })}//取得當前裝置的stream的錯誤發生時



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