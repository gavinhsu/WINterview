from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
from io import StringIO
from MockInterview.settings import BASE_DIR
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
import os, re, string
import numpy
import time
from questions.models import *
from background_task import background

class AjaxSaveAudio(TemplateView):
    template_name = 'videoUploadTest.html'
    def post(self, request):
        """Save recorded audio blob sent by user."""
        audio_file = request.FILES.get('video')
        myObj = MyModel() # Put aurguments to properly according to your model
        myObj.voice_record = audio_file
        myObj.save()
        return JsonResponse({
            'success': True,
        })


def blink():
    start = time.time()
    PERIOD_OF_TIME = 5

    def eye_aspect_ratio(eye):
        # compute the euclidean distances between the two sets of
        # vertical eye landmarks (x, y)-coordinates
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])

        # compute the euclidean distance between the horizontal
        # eye landmark (x, y)-coordinates
        C = dist.euclidean(eye[0], eye[3])

        # compute the eye aspect ratio
        ear = (A + B) / (2.0 * C)

        # return the eye aspect ratio
        return ear

    # define two constants, one for the eye aspect ratio to indicate
    # blink and then a second constant for the number of consecutive
    # frames the eye must be below the threshold
    EYE_AR_THRESH = 0.3
    EYE_AR_CONSEC_FRAMES = 3

    # initialize the frame counters and the total number of blinks
    COUNTER = 0
    TOTAL = 0

    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    print("[INFO] loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()

    file_path = os.path.join(BASE_DIR, 'shape_predictor_68_face_landmarks.dat')
    predictor = dlib.shape_predictor(file_path)
    # predictor = dlib.shape_predictor(r'C:\Users\asus\misproject\MockInterview\shape_predictor_68_face_landmarks.dat')

    # grab the indexes of the facial landmarks for the left and
    # right eye, respectively
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    # start the video stream thread
    print("[INFO] starting video stream thread...")

    USE_WEBCAM = False
    vs = None
    if (USE_WEBCAM == True):
        vs = cv2.VideoCapture(0) # Webcam source
    else:
        #vs = cv2.VideoCapture(r"C:\Users\asus\Desktop\Emotion\demo\dinner.mp4") # Video file source
        vs = FileVideoStream(r"C:\Users\asus\Desktop\Emotion\demo\dinner.mp4").start()

    fileStream = True



    # loop over frames from the video stream
    while True:
    
        # if this is a file video stream, then we need to check if
        # there any more frames left in the buffer to process

        # grab the frame from the threaded video file stream, resize
        # it, and convert it to grayscale
        # channels)
        frame = vs.read()
        #ret, bgr_image = vs.read()
        frame = imutils.resize(frame, width=450)
        # 改
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #gray = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)

        # detect faces in the grayscale frame
        rects = detector(gray, 0)

        # loop over the face detections
        for rect in rects:
            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy
            # array
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            # extract the left and right eye coordinates, then use the
            # coordinates to compute the eye aspect ratio for both eyes
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)

            # average the eye aspect ratio together for both eyes
            ear = (leftEAR + rightEAR) / 2.0

            # compute the convex hull for the left and right eye, then
            # visualize each of the eyes
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            # 改frame變bgr_image
            # cv2.drawContours(bgr_image, [leftEyeHull], -1, (0, 255, 0), 1)
            # cv2.drawContours(bgr_image, [rightEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

            # check to see if the eye aspect ratio is below the blink
            # threshold, and if so, increment the blink frame counter
            if ear < EYE_AR_THRESH:
                COUNTER += 1

            # otherwise, the eye aspect ratio is not below the blink
            # threshold
            else:
                # if the eyes were closed for a sufficient number of
                # then increment the total number of blinks
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    TOTAL += 1

                # reset the eye frame counter
                COUNTER = 0

            # draw the total number of blinks on the frame along with
            # the computed eye aspect ratio for the frame

            # 改frame變bgr_image
            cv2.putText(frame, "Blinks: {}".format(TOTAL), (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # show the frame
        cv2.imshow("Frame", frame)
        print(TOTAL)

        # if the `q` key was pressed, break from the loop
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

        if time.time() > start + PERIOD_OF_TIME: 
            break

    # do a bit of cleanup
    cv2.destroyAllWindows()
    #vs.release()
    vs.stop()

    total_blinks = int(TOTAL)
    print('Your total blinks ===> ', total_blinks)


    # save total_blinks to model RESULT
    uid = Answer.objects.all().order_by('-id')[:1].values('id') 
    res = Result.objects.get(id=uid)
    res.b1 = total_blinks
    res.save()
<<<<<<< HEAD
# blink()
=======
#blink()
>>>>>>> 3ae425e78e267f147651607eb4364a749c4ec871


@background()
def blink1(runtime):
    start = time.time()
    PERIOD_OF_TIME = runtime

    def eye_aspect_ratio(eye):
        # compute the euclidean distances between the two sets of
        # vertical eye landmarks (x, y)-coordinates
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])

        # compute the euclidean distance between the horizontal
        # eye landmark (x, y)-coordinates
        C = dist.euclidean(eye[0], eye[3])

        # compute the eye aspect ratio
        ear = (A + B) / (2.0 * C)

        # return the eye aspect ratio
        return ear



    # define two constants, one for the eye aspect ratio to indicate
    # blink and then a second constant for the number of consecutive
    # frames the eye must be below the threshold
    EYE_AR_THRESH = 0.3
    EYE_AR_CONSEC_FRAMES = 3

    # initialize the frame counters and the total number of blinks
    COUNTER = 0
    TOTAL = 0

    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    print("[INFO] loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()

    file_path = os.path.join(BASE_DIR, 'shape_predictor_68_face_landmarks.dat')
    predictor = dlib.shape_predictor(file_path)
    # predictor = dlib.shape_predictor(r'C:\Users\asus\misproject\MockInterview\shape_predictor_68_face_landmarks.dat')

    # grab the indexes of the facial landmarks for the left and
    # right eye, respectively
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    # start the video stream thread
    print("[INFO] starting video stream thread...")

    USE_WEBCAM = True
    vs = None
    if (USE_WEBCAM == True):
        vs = cv2.VideoCapture(0) # Webcam source
    else:
        #vs = cv2.VideoCapture(r"C:\Users\asus\Desktop\Emotion\demo\dinner.mp4") # Video file source
        vs = FileVideoStream(r"C:\Users\asus\Desktop\Emotion\demo\dinner.mp4").start()

    fileStream = True



    # loop over frames from the video stream
    while True:
    
        # if this is a file video stream, then we need to check if
        # there any more frames left in the buffer to process

        # grab the frame from the threaded video file stream, resize
        # it, and convert it to grayscale
        # channels)
        frame = vs.read()
        ret, bgr_image = vs.read()
        #frame = imutils.resize(frame1, width=450)
        # 改
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)

        # detect faces in the grayscale frame
        rects = detector(gray, 0)

        # loop over the face detections
        for rect in rects:
            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy
            # array
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            # extract the left and right eye coordinates, then use the
            # coordinates to compute the eye aspect ratio for both eyes
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)

            # average the eye aspect ratio together for both eyes
            ear = (leftEAR + rightEAR) / 2.0

            # compute the convex hull for the left and right eye, then
            # visualize each of the eyes
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            # 改frame變bgr_image
            cv2.drawContours(bgr_image, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(bgr_image, [rightEyeHull], -1, (0, 255, 0), 1)

            # check to see if the eye aspect ratio is below the blink
            # threshold, and if so, increment the blink frame counter
            if ear < EYE_AR_THRESH:
                COUNTER += 1

            # otherwise, the eye aspect ratio is not below the blink
            # threshold
            else:
                # if the eyes were closed for a sufficient number of
                # then increment the total number of blinks
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    TOTAL += 1

                # reset the eye frame counter
                COUNTER = 0

            # draw the total number of blinks on the frame along with
            # the computed eye aspect ratio for the frame

            # 改frame變bgr_image
            cv2.putText(bgr_image, "Blinks: {}".format(TOTAL), (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(bgr_image, "EAR: {:.2f}".format(ear), (300, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # show the frame
        #cv2.imshow("Frame", bgr_image)
        print(TOTAL)

        # if the `q` key was pressed, break from the loop
        key = cv2.waitKey(1) & 0xFF
        # if key == ord("q"):
        #     break

        if time.time() > start + PERIOD_OF_TIME : 
            break

    # do a bit of cleanup
    #cv2.destroyAllWindows()
    vs.release()

    total_blinks = int(TOTAL)
    print('Your total blinks ===> ', total_blinks)


    # save total_blinks to model RESULT
    uid = Answer.objects.all().order_by('-id')[:1].values('id') 
    res = Result.objects.get(id=uid)
    res.b1 = total_blinks
    res.save()


@background()
def blink2(runtime):
    start = time.time()
    PERIOD_OF_TIME = runtime

    def eye_aspect_ratio(eye):
        # compute the euclidean distances between the two sets of
        # vertical eye landmarks (x, y)-coordinates
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])

        # compute the euclidean distance between the horizontal
        # eye landmark (x, y)-coordinates
        C = dist.euclidean(eye[0], eye[3])

        # compute the eye aspect ratio
        ear = (A + B) / (2.0 * C)

        # return the eye aspect ratio
        return ear



    # define two constants, one for the eye aspect ratio to indicate
    # blink and then a second constant for the number of consecutive
    # frames the eye must be below the threshold
    EYE_AR_THRESH = 0.3
    EYE_AR_CONSEC_FRAMES = 3

    # initialize the frame counters and the total number of blinks
    COUNTER = 0
    TOTAL = 0

    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    print("[INFO] loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()

    file_path = os.path.join(BASE_DIR, 'shape_predictor_68_face_landmarks.dat')
    predictor = dlib.shape_predictor(file_path)
    # predictor = dlib.shape_predictor(r'C:\Users\asus\misproject\MockInterview\shape_predictor_68_face_landmarks.dat')

    # grab the indexes of the facial landmarks for the left and
    # right eye, respectively
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    # start the video stream thread
    print("[INFO] starting video stream thread...")

    USE_WEBCAM = True
    vs = None
    if (USE_WEBCAM == True):
        vs = cv2.VideoCapture(0) # Webcam source
    else:
        #vs = cv2.VideoCapture(r"C:\Users\asus\Desktop\Emotion\demo\dinner.mp4") # Video file source
        vs = FileVideoStream(r"C:\Users\asus\Desktop\Emotion\demo\dinner.mp4").start()

    fileStream = True



    # loop over frames from the video stream
    while True:
    
        # if this is a file video stream, then we need to check if
        # there any more frames left in the buffer to process

        # grab the frame from the threaded video file stream, resize
        # it, and convert it to grayscale
        # channels)
        frame = vs.read()
        ret, bgr_image = vs.read()
        #frame = imutils.resize(frame1, width=450)
        # 改
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)

        # detect faces in the grayscale frame
        rects = detector(gray, 0)

        # loop over the face detections
        for rect in rects:
            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy
            # array
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            # extract the left and right eye coordinates, then use the
            # coordinates to compute the eye aspect ratio for both eyes
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)

            # average the eye aspect ratio together for both eyes
            ear = (leftEAR + rightEAR) / 2.0

            # compute the convex hull for the left and right eye, then
            # visualize each of the eyes
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            # 改frame變bgr_image
            cv2.drawContours(bgr_image, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(bgr_image, [rightEyeHull], -1, (0, 255, 0), 1)

            # check to see if the eye aspect ratio is below the blink
            # threshold, and if so, increment the blink frame counter
            if ear < EYE_AR_THRESH:
                COUNTER += 1

            # otherwise, the eye aspect ratio is not below the blink
            # threshold
            else:
                # if the eyes were closed for a sufficient number of
                # then increment the total number of blinks
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    TOTAL += 1

                # reset the eye frame counter
                COUNTER = 0

            # draw the total number of blinks on the frame along with
            # the computed eye aspect ratio for the frame

            # 改frame變bgr_image
            cv2.putText(bgr_image, "Blinks: {}".format(TOTAL), (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(bgr_image, "EAR: {:.2f}".format(ear), (300, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # show the frame
        #cv2.imshow("Frame", bgr_image)
        print(TOTAL)

        # if the `q` key was pressed, break from the loop
        key = cv2.waitKey(1) & 0xFF
        # if key == ord("q"):
        #     break

        if time.time() > start + PERIOD_OF_TIME : 
            break

    # do a bit of cleanup
    #cv2.destroyAllWindows()
    vs.release()

    total_blinks = int(TOTAL)
    print('Your total blinks ===> ', total_blinks)


    # save total_blinks to model RESULT
    uid = Answer.objects.all().order_by('-id')[:1].values('id')
    res = Result.objects.get(id=uid)
    res.b2 = total_blinks
    res.save()


@background()
def blink3(runtime):
    start = time.time()
    PERIOD_OF_TIME = runtime

    def eye_aspect_ratio(eye):
        # compute the euclidean distances between the two sets of
        # vertical eye landmarks (x, y)-coordinates
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        # compute the euclidean distance between the horizontal
        # eye landmark (x, y)-coordinates
        C = dist.euclidean(eye[0], eye[3])
        # compute the eye aspect ratio
        ear = (A + B) / (2.0 * C)
        # return the eye aspect ratio
        return ear

    # define two constants, one for the eye aspect ratio to indicate
    # blink and then a second constant for the number of consecutive
    # frames the eye must be below the threshold
    EYE_AR_THRESH = 0.3
    EYE_AR_CONSEC_FRAMES = 3

    # initialize the frame counters and the total number of blinks
    COUNTER = 0
    TOTAL = 0

    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    print("[INFO] loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()

    file_path = os.path.join(BASE_DIR, 'shape_predictor_68_face_landmarks.dat')
    predictor = dlib.shape_predictor(file_path)
    # grab the indexes of the facial landmarks for the left and
    # right eye, respectively
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    # start the video stream thread
    print("[INFO] starting video stream thread...")

    USE_WEBCAM = True
    vs = None
    if (USE_WEBCAM == True):
        vs = cv2.VideoCapture(0) # Webcam source
    else:
        vs = FileVideoStream(r"C:\Users\asus\Desktop\Emotion\demo\dinner.mp4").start()
    fileStream = True

    while True:
        frame = vs.read()
        ret, bgr_image = vs.read()
        gray = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)

        # detect faces in the grayscale frame
        rects = detector(gray, 0)

        # loop over the face detections
        for rect in rects:
            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy
            # array
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            # extract the left and right eye coordinates, then use the
            # coordinates to compute the eye aspect ratio for both eyes
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)

            # average the eye aspect ratio together for both eyes
            ear = (leftEAR + rightEAR) / 2.0

            # compute the convex hull for the left and right eye, then
            # visualize each of the eyes
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            # 改frame變bgr_image
            cv2.drawContours(bgr_image, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(bgr_image, [rightEyeHull], -1, (0, 255, 0), 1)

            # check to see if the eye aspect ratio is below the blink
            # threshold, and if so, increment the blink frame counter
            if ear < EYE_AR_THRESH:
                COUNTER += 1

            # otherwise, the eye aspect ratio is not below the blink
            # threshold
            else:
                # if the eyes were closed for a sufficient number of
                # then increment the total number of blinks
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    TOTAL += 1

                # reset the eye frame counter
                COUNTER = 0

            # draw the total number of blinks on the frame along with
            # the computed eye aspect ratio for the frame
            cv2.putText(bgr_image, "Blinks: {}".format(TOTAL), (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(bgr_image, "EAR: {:.2f}".format(ear), (300, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # show the frame
        #cv2.imshow("Frame", bgr_image)
        print(TOTAL)

        # if the `q` key was pressed, break from the loop
        key = cv2.waitKey(1) & 0xFF
        # if key == ord("q"):
        #     break
        if time.time() > start + PERIOD_OF_TIME : 
            break

    # do a bit of cleanup
    #cv2.destroyAllWindows()
    vs.release()

    total_blinks = int(TOTAL)
    print('Your total blinks ===> ', total_blinks)

    # save total_blinks to model RESULT
    uid = Answer.objects.all().order_by('-id')[:1].values('id')
    res = Result.objects.get(id=uid)
    res.b3 = total_blinks
    res.save()


@background()
def blink4(runtime):
    start = time.time()
    PERIOD_OF_TIME = runtime

    def eye_aspect_ratio(eye):
        # compute the euclidean distances between the two sets of
        # vertical eye landmarks (x, y)-coordinates
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        # compute the euclidean distance between the horizontal
        # eye landmark (x, y)-coordinates
        C = dist.euclidean(eye[0], eye[3])
        # compute the eye aspect ratio
        ear = (A + B) / (2.0 * C)
        # return the eye aspect ratio
        return ear

    # define two constants, one for the eye aspect ratio to indicate
    # blink and then a second constant for the number of consecutive
    # frames the eye must be below the threshold
    EYE_AR_THRESH = 0.3
    EYE_AR_CONSEC_FRAMES = 3

    # initialize the frame counters and the total number of blinks
    COUNTER = 0
    TOTAL = 0

    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    print("[INFO] loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()

    file_path = os.path.join(BASE_DIR, 'shape_predictor_68_face_landmarks.dat')
    predictor = dlib.shape_predictor(file_path)
    # grab the indexes of the facial landmarks for the left and
    # right eye, respectively
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    # start the video stream thread
    print("[INFO] starting video stream thread...")

    USE_WEBCAM = True
    vs = None
    if (USE_WEBCAM == True):
        vs = cv2.VideoCapture(0) # Webcam source
    else:
        vs = FileVideoStream(r"C:\Users\asus\Desktop\Emotion\demo\dinner.mp4").start()
    fileStream = True

    while True:
        frame = vs.read()
        ret, bgr_image = vs.read()
        gray = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)

        # detect faces in the grayscale frame
        rects = detector(gray, 0)

        # loop over the face detections
        for rect in rects:
            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy
            # array
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            # extract the left and right eye coordinates, then use the
            # coordinates to compute the eye aspect ratio for both eyes
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)

            # average the eye aspect ratio together for both eyes
            ear = (leftEAR + rightEAR) / 2.0

            # compute the convex hull for the left and right eye, then
            # visualize each of the eyes
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            # 改frame變bgr_image
            cv2.drawContours(bgr_image, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(bgr_image, [rightEyeHull], -1, (0, 255, 0), 1)

            # check to see if the eye aspect ratio is below the blink
            # threshold, and if so, increment the blink frame counter
            if ear < EYE_AR_THRESH:
                COUNTER += 1

            # otherwise, the eye aspect ratio is not below the blink
            # threshold
            else:
                # if the eyes were closed for a sufficient number of
                # then increment the total number of blinks
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    TOTAL += 1

                # reset the eye frame counter
                COUNTER = 0

            # draw the total number of blinks on the frame along with
            # the computed eye aspect ratio for the frame
            cv2.putText(bgr_image, "Blinks: {}".format(TOTAL), (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(bgr_image, "EAR: {:.2f}".format(ear), (300, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # show the frame
        #cv2.imshow("Frame", bgr_image)
        print(TOTAL)

        # if the `q` key was pressed, break from the loop
        key = cv2.waitKey(1) & 0xFF
        # if key == ord("q"):
        #     break
        if time.time() > start + PERIOD_OF_TIME : 
            break

    # do a bit of cleanup
    #cv2.destroyAllWindows()
    vs.release()

    total_blinks = int(TOTAL)
    print('Your total blinks ===> ', total_blinks)

    # save total_blinks to model RESULT
    uid = Answer.objects.all().order_by('-id')[:1].values('id')
    res = Result.objects.get(id=uid)
    res.b4 = total_blinks
    res.save()



@background()
def blink5(runtime):
    start = time.time()
    PERIOD_OF_TIME = runtime

    def eye_aspect_ratio(eye):
        # compute the euclidean distances between the two sets of
        # vertical eye landmarks (x, y)-coordinates
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        # compute the euclidean distance between the horizontal
        # eye landmark (x, y)-coordinates
        C = dist.euclidean(eye[0], eye[3])
        # compute the eye aspect ratio
        ear = (A + B) / (2.0 * C)
        # return the eye aspect ratio
        return ear

    # define two constants, one for the eye aspect ratio to indicate
    # blink and then a second constant for the number of consecutive
    # frames the eye must be below the threshold
    EYE_AR_THRESH = 0.3
    EYE_AR_CONSEC_FRAMES = 3

    # initialize the frame counters and the total number of blinks
    COUNTER = 0
    TOTAL = 0

    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    print("[INFO] loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()

    file_path = os.path.join(BASE_DIR, 'shape_predictor_68_face_landmarks.dat')
    predictor = dlib.shape_predictor(file_path)
    # grab the indexes of the facial landmarks for the left and
    # right eye, respectively
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    # start the video stream thread
    print("[INFO] starting video stream thread...")

    USE_WEBCAM = True
    vs = None
    if (USE_WEBCAM == True):
        vs = cv2.VideoCapture(0) # Webcam source
    else:
        vs = FileVideoStream(r"C:\Users\asus\Desktop\Emotion\demo\dinner.mp4").start()
    fileStream = True

    while True:
        frame = vs.read()
        ret, bgr_image = vs.read()
        gray = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)

        # detect faces in the grayscale frame
        rects = detector(gray, 0)

        # loop over the face detections
        for rect in rects:
            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy
            # array
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            # extract the left and right eye coordinates, then use the
            # coordinates to compute the eye aspect ratio for both eyes
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)

            # average the eye aspect ratio together for both eyes
            ear = (leftEAR + rightEAR) / 2.0

            # compute the convex hull for the left and right eye, then
            # visualize each of the eyes
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            # 改frame變bgr_image
            cv2.drawContours(bgr_image, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(bgr_image, [rightEyeHull], -1, (0, 255, 0), 1)

            # check to see if the eye aspect ratio is below the blink
            # threshold, and if so, increment the blink frame counter
            if ear < EYE_AR_THRESH:
                COUNTER += 1

            # otherwise, the eye aspect ratio is not below the blink
            # threshold
            else:
                # if the eyes were closed for a sufficient number of
                # then increment the total number of blinks
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    TOTAL += 1

                # reset the eye frame counter
                COUNTER = 0

            # draw the total number of blinks on the frame along with
            # the computed eye aspect ratio for the frame
            cv2.putText(bgr_image, "Blinks: {}".format(TOTAL), (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(bgr_image, "EAR: {:.2f}".format(ear), (300, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # show the frame
        #cv2.imshow("Frame", bgr_image)
        print(TOTAL)

        # if the `q` key was pressed, break from the loop
        key = cv2.waitKey(1) & 0xFF
        # if key == ord("q"):
        #     break
        if time.time() > start + PERIOD_OF_TIME : 
            break

    # do a bit of cleanup
    #cv2.destroyAllWindows()
    vs.release()

    total_blinks = int(TOTAL)
    print('Your total blinks ===> ', total_blinks)

    # save total_blinks to model RESULT
    uid = Answer.objects.all().order_by('-id')[:1].values('id')
    res = Result.objects.get(id=uid)
    res.b5 = total_blinks
    res.save()


@background()
def blink6(runtime):
    start = time.time()
    PERIOD_OF_TIME = runtime

    def eye_aspect_ratio(eye):
        # compute the euclidean distances between the two sets of
        # vertical eye landmarks (x, y)-coordinates
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        # compute the euclidean distance between the horizontal
        # eye landmark (x, y)-coordinates
        C = dist.euclidean(eye[0], eye[3])
        # compute the eye aspect ratio
        ear = (A + B) / (2.0 * C)
        # return the eye aspect ratio
        return ear

    # define two constants, one for the eye aspect ratio to indicate
    # blink and then a second constant for the number of consecutive
    # frames the eye must be below the threshold
    EYE_AR_THRESH = 0.3
    EYE_AR_CONSEC_FRAMES = 3

    # initialize the frame counters and the total number of blinks
    COUNTER = 0
    TOTAL = 0

    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    print("[INFO] loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()

    file_path = os.path.join(BASE_DIR, 'shape_predictor_68_face_landmarks.dat')
    predictor = dlib.shape_predictor(file_path)
    # grab the indexes of the facial landmarks for the left and
    # right eye, respectively
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    # start the video stream thread
    print("[INFO] starting video stream thread...")

    USE_WEBCAM = True
    vs = None
    if (USE_WEBCAM == True):
        vs = cv2.VideoCapture(0) # Webcam source
    else:
        vs = FileVideoStream(r"C:\Users\asus\Desktop\Emotion\demo\dinner.mp4").start()
    fileStream = True

    while True:
        frame = vs.read()
        ret, bgr_image = vs.read()
        gray = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)

        # detect faces in the grayscale frame
        rects = detector(gray, 0)

        # loop over the face detections
        for rect in rects:
            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy
            # array
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            # extract the left and right eye coordinates, then use the
            # coordinates to compute the eye aspect ratio for both eyes
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)

            # average the eye aspect ratio together for both eyes
            ear = (leftEAR + rightEAR) / 2.0

            # compute the convex hull for the left and right eye, then
            # visualize each of the eyes
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            # 改frame變bgr_image
            cv2.drawContours(bgr_image, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(bgr_image, [rightEyeHull], -1, (0, 255, 0), 1)

            # check to see if the eye aspect ratio is below the blink
            # threshold, and if so, increment the blink frame counter
            if ear < EYE_AR_THRESH:
                COUNTER += 1

            # otherwise, the eye aspect ratio is not below the blink
            # threshold
            else:
                # if the eyes were closed for a sufficient number of
                # then increment the total number of blinks
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    TOTAL += 1

                # reset the eye frame counter
                COUNTER = 0

            # draw the total number of blinks on the frame along with
            # the computed eye aspect ratio for the frame
            cv2.putText(bgr_image, "Blinks: {}".format(TOTAL), (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(bgr_image, "EAR: {:.2f}".format(ear), (300, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # show the frame
        #cv2.imshow("Frame", bgr_image)
        print(TOTAL)

        # if the `q` key was pressed, break from the loop
        key = cv2.waitKey(1) & 0xFF
        # if key == ord("q"):
        #     break
        if time.time() > start + PERIOD_OF_TIME : 
            break

    # do a bit of cleanup
    #cv2.destroyAllWindows()
    vs.release()

    total_blinks = int(TOTAL)
    print('Your total blinks ===> ', total_blinks)

    # save total_blinks to model RESULT
    uid = Answer.objects.all().order_by('-id')[:1].values('id')
    res = Result.objects.get(id=uid)
    res.b6 = total_blinks
    res.save()









