from django.shortcuts import render, redirect
from django.contrib import auth
from django.http import HttpResponse
import os, re, string
from MockInterview.settings import BASE_DIR
import random
import pandas as pd
# for nltk model building ######################################
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier
# from django.views.decorators.csrf import csrf_protect
# from django.core.context_processors import csrf
from django.views.generic import TemplateView
from questions.models import *
import GTTS.views
#from GTTS.views import QuesView2 
# Create your views here.


def predict(n):

    def remove_noise(tweet_tokens, stop_words = ()):
        cleaned_tokens = []

        # REMOVING NOISE (IRRELEVANT LETTERS, HYPERLINKS, OR PUNCTUATION MARKS)
        for token, tag in pos_tag(tweet_tokens):
            # use re to search and replace the links that start with 'http://' with empty string''
            token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'    
                        '(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', token)
            #replace @ followed by [special characters] with ''
            token = re.sub("(@[A-Za-z0-9_]+)", '', token)

            if tag.startswith("NN"):
                pos = 'n'
                pos = 'v'
            else:
                pos = 'a'

            lemmatizer = WordNetLemmatizer() # NORMALIZATION (turn different tenses of words into only one)
            token = lemmatizer.lemmatize(token, pos)

            if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
                cleaned_tokens.append(token.lower())
        return cleaned_tokens


    # ques_view = GTTS.views.QuesView2
    # uid = ques_view.uid
    uid = Answer.objects.all().order_by('-id')[0].id
    # str_n = str(n)
    # answer1 = str(Answer.objects.filter(id=uid).values(str_n))
    # for res in answer1:
    #     res = res[str_n]
    #     return res
    answer = Answer.objects.filter(id=uid).values(n)
    def res():
        for res in answer:
            res = res[n]
            return res
        

    # unpickle
    file_path = os.path.join(BASE_DIR, 'model.pickle')
    model = pd.read_pickle(file_path)
    custom_tokens = remove_noise(word_tokenize(str(res())))
    result = model.classify(dict([token, True] for token in custom_tokens))
    
    return result



def nlp_test_view(request):
    answer = Answer.objects.get(id='26').a1
    return render(request, 'nlp_test.html',{'answer':answer})



