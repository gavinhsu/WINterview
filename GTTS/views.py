from django.shortcuts import render
from django.views.generic import TemplateView
import speech_recognition as sr
import time
from gtts import gTTS
from pygame import mixer
import tempfile


# Create your views here.
class Speech(TemplateView):
    template_name = 'speech_to_text.html'
    
    def get(self, request):
        # s = self.convert_text()
        s = "hello"
        return render(request, self.template_name, {
            "s" : s,
        })


    #def speak(self, sentence, lang, loops=1):

        #with tempfile.NamedTemporaryFile(delete = False) as fp:
            # tts = gTTS(text=sentence, lang=lang)
            # tts.save('{}.mp3'.format(fp.name))
            # # tts.save('test.mp3')
            # mixer.init()
            # mixer.music.load('{}.mp3'.format(fp.name))
            # # mixer.music.load('test.mp3')
            # mixer.music.play(loops)

    # def button_click(self, request):
    #     if(request.Get.get('speech_button')):
    #         buttonClicked = "hello"
    #         print("button clicked")                                                     
    #     return render(request, 'speech_to_text.html', {'buttonClicked':buttonClicked})


    # def convert_text(self):
    #     # obtain audio from the microphone
    #     r = sr.Recognizer()
    #     with sr.Microphone() as source:
    #         print("Please wait. Calibrating microphone...")
    #         # listen for 0.5 seconds and create the ambient noise energy level
    #         r.adjust_for_ambient_noise(source, duration=5)
    #         print("Say something!")
    #         audio = r.listen(source)

    #     # recognize speech using Google Speech Recognition
    #     try:
    #         print("Your speech is ===>")
    #         s = r.recognize_google(audio, language="en-us")
    #         print(s)
    #     except sr.UnknownValueError:
    #         print("Google Speech Recognition could not understand audio")
    #     except sr.RequestError as e:
    #         print("No response from Google Speech Recognition service: {0}".format(e))
    #     return s

    # if __name__ == '__convert_text__':
    #     convert_text()
    #     #speak(sentence=s, lang='en-us', loops=1)