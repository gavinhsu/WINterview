from django.shortcuts import render
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from statistics import mode
from Emotion.utils.datasets import get_labels
from Emotion.utils.inference import detect_faces
from Emotion.utils.inference import draw_text
from Emotion.utils.inference import draw_bounding_box
from Emotion.utils.inference import apply_offsets
from Emotion.utils.inference import load_detection_model
from Emotion.utils.preprocessor import preprocess_input
from background_task import background
from questions.models import *
import time


@background(schedule=1)
def emotion1(vid_path, account_name, duration, curr_path):
    a = 0
    current = curr_path
    while current == '/speech_to_text/' and a==0:
        # get rid of cpu warning
        import os
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

        USE_WEBCAM = False # If false, loads video file source
        # parameters for loading data and images
        emotion_model_path = './Emotion/models/emotion_model.hdf5'
        emotion_labels = get_labels('fer2013')
        # hyper-parameters for bounding boxes shape
        frame_window = 10
        emotion_offsets = (20, 40)
        # loading models
        face_cascade = cv2.CascadeClassifier('./Emotion/models/haarcascade_frontalface_default.xml')
        emotion_classifier = load_model(emotion_model_path)
        # getting input model shapes for inference
        emotion_target_size = emotion_classifier.input_shape[1:3]
        # starting lists for calculating modes
        emotion_window = []
        # starting video streaming
        cv2.namedWindow('window_frame')
        video_capture = cv2.VideoCapture(0)

        # Select video or webcam feed
        cap = None
        if (USE_WEBCAM == True):
            cap = cv2.VideoCapture(0) # Webcam source
        else:
            path = vid_path
            cap = cv2.VideoCapture(path)
            length = duration
            start = time.time()
            PERIOD_OF_TIME = length

        emotion_list = []
        i = 0
        while cap.isOpened() and i==0:
            ret, bgr_image = cap.read()

            #bgr_image = video_capture.read()[1]

            gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
            rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)

            faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5,
                    minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

            for face_coordinates in faces:

                x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
                gray_face = gray_image[y1:y2, x1:x2]
                try:
                    gray_face = cv2.resize(gray_face, (emotion_target_size))
                except:
                    continue

                gray_face = preprocess_input(gray_face, True)
                gray_face = np.expand_dims(gray_face, 0)
                gray_face = np.expand_dims(gray_face, -1)
                emotion_prediction = emotion_classifier.predict(gray_face)
                emotion_probability = np.max(emotion_prediction)
                emotion_label_arg = np.argmax(emotion_prediction)
                global emotion_text
                emotion_text = emotion_labels[emotion_label_arg]
                emotion_window.append(emotion_text)

                # getting the emotion text for MockInterview
                print('Your emotions ===> ', emotion_text)

                if len(emotion_window) > frame_window:
                    emotion_window.pop(0)
                try:
                    emotion_mode = mode(emotion_window)
                except:
                    continue

                if emotion_text == 'angry':
                    color = emotion_probability * np.asarray((255, 0, 0))
                    emotion_list.append('angry')
                elif emotion_text == 'sad':
                    color = emotion_probability * np.asarray((0, 0, 255))
                    emotion_list.append('sad')
                elif emotion_text == 'happy':
                    color = emotion_probability * np.asarray((255, 255, 0))
                    emotion_list.append('happy')
                elif emotion_text == 'surprise':
                    color = emotion_probability * np.asarray((0, 255, 255))
                    emotion_list.append('surprise')
                elif emotion_text == 'fear':
                    color = emotion_probability * np.asarray((0, 255, 255))
                    emotion_list.append('fear')
                else:
                    color = emotion_probability * np.asarray((0, 255, 0))
                    emotion_list.append('neutral')


                color = color.astype(int)
                color = color.tolist()

                draw_bounding_box(face_coordinates, rgb_image, color)
                draw_text(face_coordinates, rgb_image, emotion_mode,
                        color, 0, -45, 1, 1)


            bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
            cv2.imshow('window_frame', bgr_image)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #   break
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            if time.time() > start + PERIOD_OF_TIME: 
                i += 1
                break

        cap.release()
        print('The emotion list is ===> ', emotion_list)

        # calculate the portion of each emotion
        neutral_res = emotion_list.count('neutral')/len(emotion_list)*100
        happy_res = emotion_list.count('happy')/len(emotion_list)*100
        angry_res = emotion_list.count('angry')/len(emotion_list)*100
        fear_res = emotion_list.count('fear')/len(emotion_list)*100
        surprise_res = emotion_list.count('surprise')/len(emotion_list)*100

        # save emotion results to Result model
        account_instance = Member.objects.get(Account=account_name)
        uid = Answer.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')

        res = Result.objects.get(id=uid)
        
        res.neutral_1 = neutral_res
        res.happy_1 = happy_res
        res.angry_1 = angry_res
        res.fear_1 = fear_res
        res.surprise_1 = surprise_res
        res.save()

        cv2.destroyAllWindows()
        a += 1


@background(schedule=1)
def emotion2(vid_path, account_name, curr_path):
    current = curr_path
    while current == '/speech_to_text/':
        # get rid of cpu warning
        import os
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
        USE_WEBCAM = False # If false, loads video file source

        # parameters for loading data and images
        emotion_model_path = './Emotion/models/emotion_model.hdf5'
        emotion_labels = get_labels('fer2013')
        # hyper-parameters for bounding boxes shape
        frame_window = 10
        emotion_offsets = (20, 40)
        # loading models
        face_cascade = cv2.CascadeClassifier('./Emotion/models/haarcascade_frontalface_default.xml')
        emotion_classifier = load_model(emotion_model_path)
        # getting input model shapes for inference
        emotion_target_size = emotion_classifier.input_shape[1:3]
        # starting lists for calculating modes
        emotion_window = []
        # starting video streaming
        cv2.namedWindow('window_frame')
        video_capture = cv2.VideoCapture(0)
        # Select video or webcam feed
        cap = None
        if (USE_WEBCAM == True):
            cap = cv2.VideoCapture(0) # Webcam source
        else:
            path = vid_path
            cap = cv2.VideoCapture(path)
            # countdown
            # frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            # fps = cap.get(cv2.CAP_PROP_FPS)
            # duration = frame_count / fps 
            start = time.time()
            PERIOD_OF_TIME = 10

        emotion_list = []
        while cap.isOpened(): # True:
            ret, bgr_image = cap.read()

            #bgr_image = video_capture.read()[1]

            gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
            rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
            faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5,
                    minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

            for face_coordinates in faces:
                x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
                gray_face = gray_image[y1:y2, x1:x2]
                try:
                    gray_face = cv2.resize(gray_face, (emotion_target_size))
                except:
                    continue

                gray_face = preprocess_input(gray_face, True)
                gray_face = np.expand_dims(gray_face, 0)
                gray_face = np.expand_dims(gray_face, -1)
                emotion_prediction = emotion_classifier.predict(gray_face)
                emotion_probability = np.max(emotion_prediction)
                emotion_label_arg = np.argmax(emotion_prediction)
                global emotion_text
                emotion_text = emotion_labels[emotion_label_arg]
                emotion_window.append(emotion_text)

                # getting the emotion text for MockInterview
                print('Your emotions ===> ', emotion_text)

                if len(emotion_window) > frame_window:
                    emotion_window.pop(0)
                try:
                    emotion_mode = mode(emotion_window)
                except:
                    continue

                if emotion_text == 'angry':
                    color = emotion_probability * np.asarray((255, 0, 0))
                    emotion_list.append('angry')
                elif emotion_text == 'sad':
                    color = emotion_probability * np.asarray((0, 0, 255))
                    emotion_list.append('sad')
                elif emotion_text == 'happy':
                    color = emotion_probability * np.asarray((255, 255, 0))
                    emotion_list.append('happy')
                elif emotion_text == 'surprise':
                    color = emotion_probability * np.asarray((0, 255, 255))
                    emotion_list.append('surprise')
                elif emotion_text == 'fear':
                    color = emotion_probability * np.asarray((0, 255, 255))
                    emotion_list.append('fear')
                else:
                    color = emotion_probability * np.asarray((0, 255, 0))
                    emotion_list.append('neutral')

                color = color.astype(int)
                color = color.tolist()

                draw_bounding_box(face_coordinates, rgb_image, color)
                draw_text(face_coordinates, rgb_image, emotion_mode,
                        color, 0, -45, 1, 1)

            bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
            cv2.imshow('window_frame', bgr_image)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            if time.time() > start + PERIOD_OF_TIME: 
                break

        cap.release()
        print('The emotion list is ===> ', emotion_list)

        # calculate the portion of each emotion
        neutral_res = emotion_list.count('neutral')/len(emotion_list)*100
        happy_res = emotion_list.count('happy')/len(emotion_list)*100
        angry_res = emotion_list.count('angry')/len(emotion_list)*100
        fear_res = emotion_list.count('fear')/len(emotion_list)*100
        surprise_res = emotion_list.count('surprise')/len(emotion_list)*100

        # save emotion results to Result model
        account_instance = Member.objects.get(Account=account_name)
        uid = Answer.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')
        res = Result.objects.get(id=uid)
        
        res.neutral_2 = neutral_res
        res.happy_2 = happy_res
        res.angry_2 = angry_res
        res.fear_2 = fear_res
        res.surprise_2 = surprise_res
        res.save()

        cv2.destroyAllWindows()


@background(schedule=1)
def emotion3(vid_path, account_name):
    # get rid of cpu warning
    import os
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    USE_WEBCAM = False # If false, loads video file source

    # parameters for loading data and images
    emotion_model_path = './Emotion/models/emotion_model.hdf5'
    emotion_labels = get_labels('fer2013')
    # hyper-parameters for bounding boxes shape
    frame_window = 10
    emotion_offsets = (20, 40)
    # loading models
    face_cascade = cv2.CascadeClassifier('./Emotion/models/haarcascade_frontalface_default.xml')
    emotion_classifier = load_model(emotion_model_path)
    # getting input model shapes for inference
    emotion_target_size = emotion_classifier.input_shape[1:3]
    # starting lists for calculating modes
    emotion_window = []
    # starting video streaming
    cv2.namedWindow('window_frame')
    video_capture = cv2.VideoCapture(0)
    # Select video or webcam feed
    cap = None
    if (USE_WEBCAM == True):
        cap = cv2.VideoCapture(0) # Webcam source
    else:
        path = vid_path
        cap = cv2.VideoCapture(path)
        # countdown
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = frame_count / fps 
        start = time.time()
        PERIOD_OF_TIME = duration

    emotion_list = []
    while cap.isOpened(): # True:
        ret, bgr_image = cap.read()

        #bgr_image = video_capture.read()[1]

        gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
        rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
        faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5,
                minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

        for face_coordinates in faces:
            x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
            gray_face = gray_image[y1:y2, x1:x2]
            try:
                gray_face = cv2.resize(gray_face, (emotion_target_size))
            except:
                continue

            gray_face = preprocess_input(gray_face, True)
            gray_face = np.expand_dims(gray_face, 0)
            gray_face = np.expand_dims(gray_face, -1)
            emotion_prediction = emotion_classifier.predict(gray_face)
            emotion_probability = np.max(emotion_prediction)
            emotion_label_arg = np.argmax(emotion_prediction)
            global emotion_text
            emotion_text = emotion_labels[emotion_label_arg]
            emotion_window.append(emotion_text)

            # getting the emotion text for MockInterview
            print('Your emotions ===> ', emotion_text)

            if len(emotion_window) > frame_window:
                emotion_window.pop(0)
            try:
                emotion_mode = mode(emotion_window)
            except:
                continue

            if emotion_text == 'angry':
                color = emotion_probability * np.asarray((255, 0, 0))
                emotion_list.append('angry')
            elif emotion_text == 'sad':
                color = emotion_probability * np.asarray((0, 0, 255))
                emotion_list.append('sad')
            elif emotion_text == 'happy':
                color = emotion_probability * np.asarray((255, 255, 0))
                emotion_list.append('happy')
            elif emotion_text == 'surprise':
                color = emotion_probability * np.asarray((0, 255, 255))
                emotion_list.append('surprise')
            elif emotion_text == 'fear':
                color = emotion_probability * np.asarray((0, 255, 255))
                emotion_list.append('fear')
            else:
                color = emotion_probability * np.asarray((0, 255, 0))
                emotion_list.append('neutral')

            color = color.astype(int)
            color = color.tolist()

            draw_bounding_box(face_coordinates, rgb_image, color)
            draw_text(face_coordinates, rgb_image, emotion_mode,
                    color, 0, -45, 1, 1)

        bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
        cv2.imshow('window_frame', bgr_image)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        if time.time() > start + PERIOD_OF_TIME: 
            break

    cap.release()
    print('The emotion list is ===> ', emotion_list)

    # calculate the portion of each emotion
    neutral_res = emotion_list.count('neutral')/len(emotion_list)*100
    happy_res = emotion_list.count('happy')/len(emotion_list)*100
    angry_res = emotion_list.count('angry')/len(emotion_list)*100
    fear_res = emotion_list.count('fear')/len(emotion_list)*100
    surprise_res = emotion_list.count('surprise')/len(emotion_list)*100

    # save emotion results to Result model
    account_instance = Member.objects.get(Account=account_name)
    uid = Answer.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')
    res = Result.objects.get(id=uid)
    
    res.neutral_3 = neutral_res
    res.happy_3 = happy_res
    res.angry_3 = angry_res
    res.fear_3 = fear_res
    res.surprise_3 = surprise_res
    res.save()

    cv2.destroyAllWindows()


@background(schedule=1)
def emotion4(vid_path, account_name):
    # get rid of cpu warning
    import os
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    USE_WEBCAM = False # If false, loads video file source

    # parameters for loading data and images
    emotion_model_path = './Emotion/models/emotion_model.hdf5'
    emotion_labels = get_labels('fer2013')
    # hyper-parameters for bounding boxes shape
    frame_window = 10
    emotion_offsets = (20, 40)
    # loading models
    face_cascade = cv2.CascadeClassifier('./Emotion/models/haarcascade_frontalface_default.xml')
    emotion_classifier = load_model(emotion_model_path)
    # getting input model shapes for inference
    emotion_target_size = emotion_classifier.input_shape[1:3]
    # starting lists for calculating modes
    emotion_window = []
    # starting video streaming
    cv2.namedWindow('window_frame')
    video_capture = cv2.VideoCapture(0)
    # Select video or webcam feed
    cap = None
    if (USE_WEBCAM == True):
        cap = cv2.VideoCapture(0) # Webcam source
    else:
        path = vid_path
        cap = cv2.VideoCapture(path)
        # countdown
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = frame_count / fps 
        start = time.time()
        PERIOD_OF_TIME = duration

    emotion_list = []
    while cap.isOpened(): # True:
        ret, bgr_image = cap.read()

        #bgr_image = video_capture.read()[1]

        gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
        rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
        faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5,
                minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

        for face_coordinates in faces:
            x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
            gray_face = gray_image[y1:y2, x1:x2]
            try:
                gray_face = cv2.resize(gray_face, (emotion_target_size))
            except:
                continue

            gray_face = preprocess_input(gray_face, True)
            gray_face = np.expand_dims(gray_face, 0)
            gray_face = np.expand_dims(gray_face, -1)
            emotion_prediction = emotion_classifier.predict(gray_face)
            emotion_probability = np.max(emotion_prediction)
            emotion_label_arg = np.argmax(emotion_prediction)
            global emotion_text
            emotion_text = emotion_labels[emotion_label_arg]
            emotion_window.append(emotion_text)

            # getting the emotion text for MockInterview
            print('Your emotions ===> ', emotion_text)

            if len(emotion_window) > frame_window:
                emotion_window.pop(0)
            try:
                emotion_mode = mode(emotion_window)
            except:
                continue

            if emotion_text == 'angry':
                color = emotion_probability * np.asarray((255, 0, 0))
                emotion_list.append('angry')
            elif emotion_text == 'sad':
                color = emotion_probability * np.asarray((0, 0, 255))
                emotion_list.append('sad')
            elif emotion_text == 'happy':
                color = emotion_probability * np.asarray((255, 255, 0))
                emotion_list.append('happy')
            elif emotion_text == 'surprise':
                color = emotion_probability * np.asarray((0, 255, 255))
                emotion_list.append('surprise')
            elif emotion_text == 'fear':
                color = emotion_probability * np.asarray((0, 255, 255))
                emotion_list.append('fear')
            else:
                color = emotion_probability * np.asarray((0, 255, 0))
                emotion_list.append('neutral')

            color = color.astype(int)
            color = color.tolist()

            draw_bounding_box(face_coordinates, rgb_image, color)
            draw_text(face_coordinates, rgb_image, emotion_mode,
                    color, 0, -45, 1, 1)

        bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
        cv2.imshow('window_frame', bgr_image)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        if time.time() > start + PERIOD_OF_TIME: 
            break

    cap.release()
    print('The emotion list is ===> ', emotion_list)

    # calculate the portion of each emotion
    neutral_res = emotion_list.count('neutral')/len(emotion_list)*100
    happy_res = emotion_list.count('happy')/len(emotion_list)*100
    angry_res = emotion_list.count('angry')/len(emotion_list)*100
    fear_res = emotion_list.count('fear')/len(emotion_list)*100
    surprise_res = emotion_list.count('surprise')/len(emotion_list)*100

    # save emotion results to Result model
    account_instance = Member.objects.get(Account=account_name)
    uid = Answer.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')
    res = Result.objects.get(id=uid)
    
    res.neutral_4 = neutral_res
    res.happy_4 = happy_res
    res.angry_4 = angry_res
    res.fear_4 = fear_res
    res.surprise_4 = surprise_res
    res.save()

    cv2.destroyAllWindows()



@background(schedule=1)
def emotion5(vid_path, account_name):
    # get rid of cpu warning
    import os
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    USE_WEBCAM = False # If false, loads video file source

    # parameters for loading data and images
    emotion_model_path = './Emotion/models/emotion_model.hdf5'
    emotion_labels = get_labels('fer2013')
    # hyper-parameters for bounding boxes shape
    frame_window = 10
    emotion_offsets = (20, 40)
    # loading models
    face_cascade = cv2.CascadeClassifier('./Emotion/models/haarcascade_frontalface_default.xml')
    emotion_classifier = load_model(emotion_model_path)
    # getting input model shapes for inference
    emotion_target_size = emotion_classifier.input_shape[1:3]
    # starting lists for calculating modes
    emotion_window = []
    # starting video streaming
    cv2.namedWindow('window_frame')
    video_capture = cv2.VideoCapture(0)
    # Select video or webcam feed
    cap = None
    if (USE_WEBCAM == True):
        cap = cv2.VideoCapture(0) # Webcam source
    else:
        path = vid_path
        cap = cv2.VideoCapture(path)
        # countdown
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = frame_count / fps 
        start = time.time()
        PERIOD_OF_TIME = duration

    emotion_list = []
    while cap.isOpened(): # True:
        ret, bgr_image = cap.read()

        #bgr_image = video_capture.read()[1]

        gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
        rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
        faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5,
                minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

        for face_coordinates in faces:
            x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
            gray_face = gray_image[y1:y2, x1:x2]
            try:
                gray_face = cv2.resize(gray_face, (emotion_target_size))
            except:
                continue

            gray_face = preprocess_input(gray_face, True)
            gray_face = np.expand_dims(gray_face, 0)
            gray_face = np.expand_dims(gray_face, -1)
            emotion_prediction = emotion_classifier.predict(gray_face)
            emotion_probability = np.max(emotion_prediction)
            emotion_label_arg = np.argmax(emotion_prediction)
            global emotion_text
            emotion_text = emotion_labels[emotion_label_arg]
            emotion_window.append(emotion_text)

            # getting the emotion text for MockInterview
            print('Your emotions ===> ', emotion_text)

            if len(emotion_window) > frame_window:
                emotion_window.pop(0)
            try:
                emotion_mode = mode(emotion_window)
            except:
                continue

            if emotion_text == 'angry':
                color = emotion_probability * np.asarray((255, 0, 0))
                emotion_list.append('angry')
            elif emotion_text == 'sad':
                color = emotion_probability * np.asarray((0, 0, 255))
                emotion_list.append('sad')
            elif emotion_text == 'happy':
                color = emotion_probability * np.asarray((255, 255, 0))
                emotion_list.append('happy')
            elif emotion_text == 'surprise':
                color = emotion_probability * np.asarray((0, 255, 255))
                emotion_list.append('surprise')
            elif emotion_text == 'fear':
                color = emotion_probability * np.asarray((0, 255, 255))
                emotion_list.append('fear')
            else:
                color = emotion_probability * np.asarray((0, 255, 0))
                emotion_list.append('neutral')

            color = color.astype(int)
            color = color.tolist()

            draw_bounding_box(face_coordinates, rgb_image, color)
            draw_text(face_coordinates, rgb_image, emotion_mode,
                    color, 0, -45, 1, 1)

        bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
        cv2.imshow('window_frame', bgr_image)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        if time.time() > start + PERIOD_OF_TIME: 
            break

    cap.release()
    print('The emotion list is ===> ', emotion_list)

    # calculate the portion of each emotion
    neutral_res = emotion_list.count('neutral')/len(emotion_list)*100
    happy_res = emotion_list.count('happy')/len(emotion_list)*100
    angry_res = emotion_list.count('angry')/len(emotion_list)*100
    fear_res = emotion_list.count('fear')/len(emotion_list)*100
    surprise_res = emotion_list.count('surprise')/len(emotion_list)*100

    # save emotion results to Result model
    account_instance = Member.objects.get(Account=account_name)
    uid = Answer.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')
    res = Result.objects.get(id=uid)
    
    res.neutral_5 = neutral_res
    res.happy_5 = happy_res
    res.angry_5 = angry_res
    res.fear_5 = fear_res
    res.surprise_5 = surprise_res
    res.save()

    cv2.destroyAllWindows()


@background(schedule=1)
def emotion6(vid_path, account_name):
    # get rid of cpu warning
    import os
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    USE_WEBCAM = False # If false, loads video file source

    # parameters for loading data and images
    emotion_model_path = './Emotion/models/emotion_model.hdf5'
    emotion_labels = get_labels('fer2013')
    # hyper-parameters for bounding boxes shape
    frame_window = 10
    emotion_offsets = (20, 40)
    # loading models
    face_cascade = cv2.CascadeClassifier('./Emotion/models/haarcascade_frontalface_default.xml')
    emotion_classifier = load_model(emotion_model_path)
    # getting input model shapes for inference
    emotion_target_size = emotion_classifier.input_shape[1:3]
    # starting lists for calculating modes
    emotion_window = []
    # starting video streaming
    cv2.namedWindow('window_frame')
    video_capture = cv2.VideoCapture(0)
    # Select video or webcam feed
    cap = None
    if (USE_WEBCAM == True):
        cap = cv2.VideoCapture(0) # Webcam source
    else:
        path = vid_path
        cap = cv2.VideoCapture(path)
        # countdown
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = frame_count / fps 
        start = time.time()
        PERIOD_OF_TIME = duration

    emotion_list = []
    while cap.isOpened(): # True:
        ret, bgr_image = cap.read()

        #bgr_image = video_capture.read()[1]

        gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
        rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
        faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5,
                minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

        for face_coordinates in faces:
            x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
            gray_face = gray_image[y1:y2, x1:x2]
            try:
                gray_face = cv2.resize(gray_face, (emotion_target_size))
            except:
                continue

            gray_face = preprocess_input(gray_face, True)
            gray_face = np.expand_dims(gray_face, 0)
            gray_face = np.expand_dims(gray_face, -1)
            emotion_prediction = emotion_classifier.predict(gray_face)
            emotion_probability = np.max(emotion_prediction)
            emotion_label_arg = np.argmax(emotion_prediction)
            global emotion_text
            emotion_text = emotion_labels[emotion_label_arg]
            emotion_window.append(emotion_text)

            # getting the emotion text for MockInterview
            print('Your emotions ===> ', emotion_text)

            if len(emotion_window) > frame_window:
                emotion_window.pop(0)
            try:
                emotion_mode = mode(emotion_window)
            except:
                continue

            if emotion_text == 'angry':
                color = emotion_probability * np.asarray((255, 0, 0))
                emotion_list.append('angry')
            elif emotion_text == 'sad':
                color = emotion_probability * np.asarray((0, 0, 255))
                emotion_list.append('sad')
            elif emotion_text == 'happy':
                color = emotion_probability * np.asarray((255, 255, 0))
                emotion_list.append('happy')
            elif emotion_text == 'surprise':
                color = emotion_probability * np.asarray((0, 255, 255))
                emotion_list.append('surprise')
            elif emotion_text == 'fear':
                color = emotion_probability * np.asarray((0, 255, 255))
                emotion_list.append('fear')
            else:
                color = emotion_probability * np.asarray((0, 255, 0))
                emotion_list.append('neutral')

            color = color.astype(int)
            color = color.tolist()

            draw_bounding_box(face_coordinates, rgb_image, color)
            draw_text(face_coordinates, rgb_image, emotion_mode,
                    color, 0, -45, 1, 1)

        bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
        cv2.imshow('window_frame', bgr_image)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        if time.time() > start + PERIOD_OF_TIME: 
            break

    cap.release()
    print('The emotion list is ===> ', emotion_list)

    # calculate the portion of each emotion
    neutral_res = emotion_list.count('neutral')/len(emotion_list)*100
    happy_res = emotion_list.count('happy')/len(emotion_list)*100
    angry_res = emotion_list.count('angry')/len(emotion_list)*100
    fear_res = emotion_list.count('fear')/len(emotion_list)*100
    surprise_res = emotion_list.count('surprise')/len(emotion_list)*100

    # save emotion results to Result model
    account_instance = Member.objects.get(Account=account_name)
    uid = Answer.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')
    res = Result.objects.get(id=uid)
    
    res.neutral_6 = neutral_res
    res.happy_6 = happy_res
    res.angry_6 = angry_res
    res.fear_6 = fear_res
    res.surprise_6 = surprise_res
    res.save()

    cv2.destroyAllWindows()



@background(schedule=1)
def emotion7(vid_path, account_name):
    # get rid of cpu warning
    import os
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    USE_WEBCAM = False # If false, loads video file source

    # parameters for loading data and images
    emotion_model_path = './Emotion/models/emotion_model.hdf5'
    emotion_labels = get_labels('fer2013')
    # hyper-parameters for bounding boxes shape
    frame_window = 10
    emotion_offsets = (20, 40)
    # loading models
    face_cascade = cv2.CascadeClassifier('./Emotion/models/haarcascade_frontalface_default.xml')
    emotion_classifier = load_model(emotion_model_path)
    # getting input model shapes for inference
    emotion_target_size = emotion_classifier.input_shape[1:3]
    # starting lists for calculating modes
    emotion_window = []
    # starting video streaming
    cv2.namedWindow('window_frame')
    video_capture = cv2.VideoCapture(0)
    # Select video or webcam feed
    cap = None
    if (USE_WEBCAM == True):
        cap = cv2.VideoCapture(0) # Webcam source
    else:
        path = vid_path
        cap = cv2.VideoCapture(path)
        # countdown
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = frame_count / fps 
        start = time.time()
        PERIOD_OF_TIME = duration

    emotion_list = []
    while cap.isOpened(): # True:
        ret, bgr_image = cap.read()

        #bgr_image = video_capture.read()[1]

        gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
        rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
        faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5,
                minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

        for face_coordinates in faces:
            x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
            gray_face = gray_image[y1:y2, x1:x2]
            try:
                gray_face = cv2.resize(gray_face, (emotion_target_size))
            except:
                continue

            gray_face = preprocess_input(gray_face, True)
            gray_face = np.expand_dims(gray_face, 0)
            gray_face = np.expand_dims(gray_face, -1)
            emotion_prediction = emotion_classifier.predict(gray_face)
            emotion_probability = np.max(emotion_prediction)
            emotion_label_arg = np.argmax(emotion_prediction)
            global emotion_text
            emotion_text = emotion_labels[emotion_label_arg]
            emotion_window.append(emotion_text)

            # getting the emotion text for MockInterview
            print('Your emotions ===> ', emotion_text)

            if len(emotion_window) > frame_window:
                emotion_window.pop(0)
            try:
                emotion_mode = mode(emotion_window)
            except:
                continue

            if emotion_text == 'angry':
                color = emotion_probability * np.asarray((255, 0, 0))
                emotion_list.append('angry')
            elif emotion_text == 'sad':
                color = emotion_probability * np.asarray((0, 0, 255))
                emotion_list.append('sad')
            elif emotion_text == 'happy':
                color = emotion_probability * np.asarray((255, 255, 0))
                emotion_list.append('happy')
            elif emotion_text == 'surprise':
                color = emotion_probability * np.asarray((0, 255, 255))
                emotion_list.append('surprise')
            elif emotion_text == 'fear':
                color = emotion_probability * np.asarray((0, 255, 255))
                emotion_list.append('fear')
            else:
                color = emotion_probability * np.asarray((0, 255, 0))
                emotion_list.append('neutral')

            color = color.astype(int)
            color = color.tolist()

            draw_bounding_box(face_coordinates, rgb_image, color)
            draw_text(face_coordinates, rgb_image, emotion_mode,
                    color, 0, -45, 1, 1)

        bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
        cv2.imshow('window_frame', bgr_image)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        if time.time() > start + PERIOD_OF_TIME: 
            break

    cap.release()
    print('The emotion list is ===> ', emotion_list)

    # calculate the portion of each emotion
    neutral_res = emotion_list.count('neutral')/len(emotion_list)*100
    happy_res = emotion_list.count('happy')/len(emotion_list)*100
    angry_res = emotion_list.count('angry')/len(emotion_list)*100
    fear_res = emotion_list.count('fear')/len(emotion_list)*100
    surprise_res = emotion_list.count('surprise')/len(emotion_list)*100

    # save emotion results to Result model
    account_instance = Member.objects.get(Account=account_name)
    uid = Answer.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')
    res = Result.objects.get(id=uid)
    
    res.neutral_7 = neutral_res
    res.happy_7 = happy_res
    res.angry_7 = angry_res
    res.fear_7 = fear_res
    res.surprise_7 = surprise_res
    res.save()

    cv2.destroyAllWindows()


@background(schedule=1)
def emotion8(vid_path, account_name):
    # get rid of cpu warning
    import os
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    USE_WEBCAM = False # If false, loads video file source

    # parameters for loading data and images
    emotion_model_path = './Emotion/models/emotion_model.hdf5'
    emotion_labels = get_labels('fer2013')
    # hyper-parameters for bounding boxes shape
    frame_window = 10
    emotion_offsets = (20, 40)
    # loading models
    face_cascade = cv2.CascadeClassifier('./Emotion/models/haarcascade_frontalface_default.xml')
    emotion_classifier = load_model(emotion_model_path)
    # getting input model shapes for inference
    emotion_target_size = emotion_classifier.input_shape[1:3]
    # starting lists for calculating modes
    emotion_window = []
    # starting video streaming
    cv2.namedWindow('window_frame')
    video_capture = cv2.VideoCapture(0)
    # Select video or webcam feed
    cap = None
    if (USE_WEBCAM == True):
        cap = cv2.VideoCapture(0) # Webcam source
    else:
        path = vid_path
        cap = cv2.VideoCapture(path)
        # countdown
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = frame_count / fps 
        start = time.time()
        PERIOD_OF_TIME = duration

    emotion_list = []
    while cap.isOpened(): # True:
        ret, bgr_image = cap.read()

        #bgr_image = video_capture.read()[1]

        gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
        rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
        faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5,
                minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

        for face_coordinates in faces:
            x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
            gray_face = gray_image[y1:y2, x1:x2]
            try:
                gray_face = cv2.resize(gray_face, (emotion_target_size))
            except:
                continue

            gray_face = preprocess_input(gray_face, True)
            gray_face = np.expand_dims(gray_face, 0)
            gray_face = np.expand_dims(gray_face, -1)
            emotion_prediction = emotion_classifier.predict(gray_face)
            emotion_probability = np.max(emotion_prediction)
            emotion_label_arg = np.argmax(emotion_prediction)
            global emotion_text
            emotion_text = emotion_labels[emotion_label_arg]
            emotion_window.append(emotion_text)

            # getting the emotion text for MockInterview
            print('Your emotions ===> ', emotion_text)

            if len(emotion_window) > frame_window:
                emotion_window.pop(0)
            try:
                emotion_mode = mode(emotion_window)
            except:
                continue

            if emotion_text == 'angry':
                color = emotion_probability * np.asarray((255, 0, 0))
                emotion_list.append('angry')
            elif emotion_text == 'sad':
                color = emotion_probability * np.asarray((0, 0, 255))
                emotion_list.append('sad')
            elif emotion_text == 'happy':
                color = emotion_probability * np.asarray((255, 255, 0))
                emotion_list.append('happy')
            elif emotion_text == 'surprise':
                color = emotion_probability * np.asarray((0, 255, 255))
                emotion_list.append('surprise')
            elif emotion_text == 'fear':
                color = emotion_probability * np.asarray((0, 255, 255))
                emotion_list.append('fear')
            else:
                color = emotion_probability * np.asarray((0, 255, 0))
                emotion_list.append('neutral')

            color = color.astype(int)
            color = color.tolist()

            draw_bounding_box(face_coordinates, rgb_image, color)
            draw_text(face_coordinates, rgb_image, emotion_mode,
                    color, 0, -45, 1, 1)

        bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
        cv2.imshow('window_frame', bgr_image)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        if time.time() > start + PERIOD_OF_TIME: 
            break

    cap.release()
    print('The emotion list is ===> ', emotion_list)

    # calculate the portion of each emotion
    neutral_res = emotion_list.count('neutral')/len(emotion_list)*100
    happy_res = emotion_list.count('happy')/len(emotion_list)*100
    angry_res = emotion_list.count('angry')/len(emotion_list)*100
    fear_res = emotion_list.count('fear')/len(emotion_list)*100
    surprise_res = emotion_list.count('surprise')/len(emotion_list)*100

    # save emotion results to Result model
    account_instance = Member.objects.get(Account=account_name)
    uid = Answer.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')
    res = Result.objects.get(id=uid)
    
    res.neutral_8 = neutral_res
    res.happy_8 = happy_res
    res.angry_8 = angry_res
    res.fear_8 = fear_res
    res.surprise_8 = surprise_res
    res.save()

    cv2.destroyAllWindows()



@background(schedule=1)
def emotion9(vid_path, account_name):
    # get rid of cpu warning
    import os
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    USE_WEBCAM = False # If false, loads video file source

    # parameters for loading data and images
    emotion_model_path = './Emotion/models/emotion_model.hdf5'
    emotion_labels = get_labels('fer2013')
    # hyper-parameters for bounding boxes shape
    frame_window = 10
    emotion_offsets = (20, 40)
    # loading models
    face_cascade = cv2.CascadeClassifier('./Emotion/models/haarcascade_frontalface_default.xml')
    emotion_classifier = load_model(emotion_model_path)
    # getting input model shapes for inference
    emotion_target_size = emotion_classifier.input_shape[1:3]
    # starting lists for calculating modes
    emotion_window = []
    # starting video streaming
    cv2.namedWindow('window_frame')
    video_capture = cv2.VideoCapture(0)
    # Select video or webcam feed
    cap = None
    if (USE_WEBCAM == True):
        cap = cv2.VideoCapture(0) # Webcam source
    else:
        path = vid_path
        cap = cv2.VideoCapture(path)
        # countdown
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = frame_count / fps 
        start = time.time()
        PERIOD_OF_TIME = duration

    emotion_list = []
    while cap.isOpened(): # True:
        ret, bgr_image = cap.read()

        #bgr_image = video_capture.read()[1]

        gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
        rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
        faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5,
                minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

        for face_coordinates in faces:
            x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
            gray_face = gray_image[y1:y2, x1:x2]
            try:
                gray_face = cv2.resize(gray_face, (emotion_target_size))
            except:
                continue

            gray_face = preprocess_input(gray_face, True)
            gray_face = np.expand_dims(gray_face, 0)
            gray_face = np.expand_dims(gray_face, -1)
            emotion_prediction = emotion_classifier.predict(gray_face)
            emotion_probability = np.max(emotion_prediction)
            emotion_label_arg = np.argmax(emotion_prediction)
            global emotion_text
            emotion_text = emotion_labels[emotion_label_arg]
            emotion_window.append(emotion_text)

            # getting the emotion text for MockInterview
            print('Your emotions ===> ', emotion_text)

            if len(emotion_window) > frame_window:
                emotion_window.pop(0)
            try:
                emotion_mode = mode(emotion_window)
            except:
                continue

            if emotion_text == 'angry':
                color = emotion_probability * np.asarray((255, 0, 0))
                emotion_list.append('angry')
            elif emotion_text == 'sad':
                color = emotion_probability * np.asarray((0, 0, 255))
                emotion_list.append('sad')
            elif emotion_text == 'happy':
                color = emotion_probability * np.asarray((255, 255, 0))
                emotion_list.append('happy')
            elif emotion_text == 'surprise':
                color = emotion_probability * np.asarray((0, 255, 255))
                emotion_list.append('surprise')
            elif emotion_text == 'fear':
                color = emotion_probability * np.asarray((0, 255, 255))
                emotion_list.append('fear')
            else:
                color = emotion_probability * np.asarray((0, 255, 0))
                emotion_list.append('neutral')

            color = color.astype(int)
            color = color.tolist()

            draw_bounding_box(face_coordinates, rgb_image, color)
            draw_text(face_coordinates, rgb_image, emotion_mode,
                    color, 0, -45, 1, 1)

        bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
        cv2.imshow('window_frame', bgr_image)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        if time.time() > start + PERIOD_OF_TIME: 
            break

    cap.release()
    print('The emotion list is ===> ', emotion_list)

    # calculate the portion of each emotion
    neutral_res = emotion_list.count('neutral')/len(emotion_list)*100
    happy_res = emotion_list.count('happy')/len(emotion_list)*100
    angry_res = emotion_list.count('angry')/len(emotion_list)*100
    fear_res = emotion_list.count('fear')/len(emotion_list)*100
    surprise_res = emotion_list.count('surprise')/len(emotion_list)*100

    # save emotion results to Result model
    account_instance = Member.objects.get(Account=account_name)
    uid = Answer.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')
    res = Result.objects.get(id=uid)
    
    res.neutral_9 = neutral_res
    res.happy_9 = happy_res
    res.angry_9 = angry_res
    res.fear_9 = fear_res
    res.surprise_9 = surprise_res
    res.save()

    cv2.destroyAllWindows()


@background(schedule=1)
def emotion10(vid_path, account_name):
    # get rid of cpu warning
    import os
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    USE_WEBCAM = False # If false, loads video file source

    # parameters for loading data and images
    emotion_model_path = './Emotion/models/emotion_model.hdf5'
    emotion_labels = get_labels('fer2013')
    # hyper-parameters for bounding boxes shape
    frame_window = 10
    emotion_offsets = (20, 40)
    # loading models
    face_cascade = cv2.CascadeClassifier('./Emotion/models/haarcascade_frontalface_default.xml')
    emotion_classifier = load_model(emotion_model_path)
    # getting input model shapes for inference
    emotion_target_size = emotion_classifier.input_shape[1:3]
    # starting lists for calculating modes
    emotion_window = []
    # starting video streaming
    cv2.namedWindow('window_frame')
    video_capture = cv2.VideoCapture(0)
    # Select video or webcam feed
    cap = None
    if (USE_WEBCAM == True):
        cap = cv2.VideoCapture(0) # Webcam source
    else:
        path = vid_path
        cap = cv2.VideoCapture(path)
        # countdown
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = frame_count / fps 
        start = time.time()
        PERIOD_OF_TIME = duration

    emotion_list = []
    while cap.isOpened(): # True:
        ret, bgr_image = cap.read()

        #bgr_image = video_capture.read()[1]

        gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
        rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
        faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5,
                minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

        for face_coordinates in faces:
            x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
            gray_face = gray_image[y1:y2, x1:x2]
            try:
                gray_face = cv2.resize(gray_face, (emotion_target_size))
            except:
                continue

            gray_face = preprocess_input(gray_face, True)
            gray_face = np.expand_dims(gray_face, 0)
            gray_face = np.expand_dims(gray_face, -1)
            emotion_prediction = emotion_classifier.predict(gray_face)
            emotion_probability = np.max(emotion_prediction)
            emotion_label_arg = np.argmax(emotion_prediction)
            global emotion_text
            emotion_text = emotion_labels[emotion_label_arg]
            emotion_window.append(emotion_text)

            # getting the emotion text for MockInterview
            print('Your emotions ===> ', emotion_text)

            if len(emotion_window) > frame_window:
                emotion_window.pop(0)
            try:
                emotion_mode = mode(emotion_window)
            except:
                continue

            if emotion_text == 'angry':
                color = emotion_probability * np.asarray((255, 0, 0))
                emotion_list.append('angry')
            elif emotion_text == 'sad':
                color = emotion_probability * np.asarray((0, 0, 255))
                emotion_list.append('sad')
            elif emotion_text == 'happy':
                color = emotion_probability * np.asarray((255, 255, 0))
                emotion_list.append('happy')
            elif emotion_text == 'surprise':
                color = emotion_probability * np.asarray((0, 255, 255))
                emotion_list.append('surprise')
            elif emotion_text == 'fear':
                color = emotion_probability * np.asarray((0, 255, 255))
                emotion_list.append('fear')
            else:
                color = emotion_probability * np.asarray((0, 255, 0))
                emotion_list.append('neutral')

            color = color.astype(int)
            color = color.tolist()

            draw_bounding_box(face_coordinates, rgb_image, color)
            draw_text(face_coordinates, rgb_image, emotion_mode,
                    color, 0, -45, 1, 1)

        bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
        cv2.imshow('window_frame', bgr_image)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        if time.time() > start + PERIOD_OF_TIME: 
            break

    cap.release()
    print('The emotion list is ===> ', emotion_list)

    # calculate the portion of each emotion
    neutral_res = emotion_list.count('neutral')/len(emotion_list)*100
    happy_res = emotion_list.count('happy')/len(emotion_list)*100
    angry_res = emotion_list.count('angry')/len(emotion_list)*100
    fear_res = emotion_list.count('fear')/len(emotion_list)*100
    surprise_res = emotion_list.count('surprise')/len(emotion_list)*100

    # save emotion results to Result model
    account_instance = Member.objects.get(Account=account_name)
    uid = Answer.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')
    res = Result.objects.get(id=uid)
    
    res.neutral_10 = neutral_res
    res.happy_10 = happy_res
    res.angry_10 = angry_res
    res.fear_10 = fear_res
    res.surprise_10 = surprise_res
    res.save()

    cv2.destroyAllWindows()