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
var submit = document.getElementById("submit");
submit.addEventListener('click', simulateClick);

function simulateClick() {
    stopBtn.click()
}


(function () {
    // set flag to indicate whether we should wait or actually submit
    var delaySubmit = true;
    // get form el
    var form = document.getElementById('ans');
    form.addEventListener("submit", function (e) {
        document.getElementById("submit").value = "Next question";
        // if we've already waited the 2 seconds, submit
        if (!delaySubmit)
            return;

        // otherwise, stop the submission
        e.preventDefault();
        // set the flag for next time
        delaySubmit = false;

        // and resubmit in 2 seconds. 
        window.setTimeout(function () {
            this.submit();
        }, 2000);
    });
})();

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
            var reader = new FileReader();
            reader.readAsDataURL(blob);
            reader.onloadend = function () {
                var base64data = reader.result;
                var text = document.getElementById("video")
                // var decodedString = atob(base64data);
                text.value = base64data
                // video.src = base64data              
                console.log(base64data);
            }
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

