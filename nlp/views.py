from django.shortcuts import render, redirect
from django.contrib import auth
from django.http import HttpResponse
import random
import pandas as pd
import re, string
# for nltk model building ######################################
import nltk
# nltk.download('twitter_samples') # 5000 neg & 5000 pos $ 20000 none
# nltk.download('stopwords') # such as 'is, the'
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
# nltk.download('punkt') # pre-trained model
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag # tag 詞彙的型態
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier # for model building
# from django.views.decorators.csrf import csrf_protect
# from django.core.context_processors import csrf

from django.views.generic import TemplateView
from questions.models import Answer
# Create your views here.
a=12
print(a)
answer = Answer.objects.filter(userID='A123456789一二三').values('a1')
print(answer)

def predict(request):
    answer = Answer.objects.filter(userID='26').value_list('a1')
    print(answer)
    pdb.set_trace()
    print(aaa)

    # def remove_noise(tweet_tokens, stop_words = ()):
    #     cleaned_tokens = []

    #     # REMOVING NOISE (IRRELEVANT LETTERS, HYPERLINKS, OR PUNCTUATION MARKS)
    #     for token, tag in pos_tag(tweet_tokens):
    #         # use re to search and replace the links that start with 'http://' with empty string''
    #         token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'    
    #                     '(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', token)
    #         #replace @ followed by [special characters] with ''
    #         token = re.sub("(@[A-Za-z0-9_]+)", '', token)

    #         if tag.startswith("NN"):
    #             pos = 'n'
    #             pos = 'v'
    #         else:
    #             pos = 'a'

    #         lemmatizer = WordNetLemmatizer() # NORMALIZATION (turn different tenses of words into only one)
    #         token = lemmatizer.lemmatize(token, pos)

    #         if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
    #             cleaned_tokens.append(token.lower())
    #     return cleaned_tokens

   

    # # unpickle
    # model = pd.read_pickle('model.pickle')
    # custom_tokens = remove_noise(word_tokenize(sentence))
    # results = model.classify(dict([token, True] for token in custom_tokens))

    return HttpResponse(results)
    #print('The result is: ', results)

def nlp_test_view(request):
    # answer = Answer.objects.filter(userID_id='26').values('a1')
    return render(request, 'nlp_test.html',{'answer':answer})


