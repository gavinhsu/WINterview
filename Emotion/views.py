from django.shortcuts import render
import cv2
import numpy as np
from keras.models import load_model
from statistics import mode
from Emotion.utils.datasets import get_labels
from Emotion.utils.inference import detect_faces
from Emotion.utils.inference import draw_text
from Emotion.utils.inference import draw_bounding_box
from Emotion.utils.inference import apply_offsets
from Emotion.utils.inference import load_detection_model
from Emotion.utils.preprocessor import preprocess_input


# get rid of cpu warning
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

USE_WEBCAM = False # If false, loads video file source


def emotion(vid_path):
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
                #emotion_list.append('sad')
            elif emotion_text == 'happy':
                color = emotion_probability * np.asarray((255, 255, 0))
                emotion_list.append('happy')
            elif emotion_text == 'surprise':
                color = emotion_probability * np.asarray((0, 255, 255))
                emotion_list.append('surprise')
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

    cap.release()
    print('The emotion list is ===> ', emotion_list)

    cv2.destroyAllWindows()

