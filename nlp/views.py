from django.shortcuts import render, redirect
from django.contrib import auth
from django.http import HttpResponse
import os, re, string
from MockInterview.settings import BASE_DIR
from questions.models import *
from users.models import *
import random
import pickle
import pandas as pd
import cloudpickle
import torch
# for nltk model building ######################################
import nltk
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
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
from sre_parse import Tokenizer



# Create your views here.
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


def predict(n):
    uid = Answer.objects.all().order_by('-id')[0].id

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


        

# GENSIM
file_path = os.path.join(BASE_DIR, 'test.pickle')
w2v_model = pd.read_pickle(file_path)

# import nltk
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize

# reply = 'python is a great way to program'
# answer = 'python is a good programming language'
# reply_tokens = word_tokenize(reply)
# #ans_tokens = word_tokenize(answer)

# clean_reply = [word for word in reply_tokens if not word in stopwords.words()]
#clean_ans = [word for word in ans_tokens if not word in stopwords.words()]

# similarity = w2v_model.wv.n_similarity(reply_tokens, ans_tokens)
# print(similarity)


#######################################################################
#BERT
#torch.nn.Module.dump_patches = True

#bert_file_path = os.path.join(BASE_DIR, 'bert.pickle')
#bert = torch.load(bert_file_path)
s1 = "python is a good programming language"
s2 = "python is really great to program"

#predict = bert.predict([(s1, s2)])
#predict = float(predict)
#score = (predict/5)*100
#print('BERT ===> ', score, '%')



class ResultView(TemplateView):
    template_name = 'result.html'

    def __init__(self, job_name=None):
        self.job_name = job_name

    def get(self, request):
        job_name = request.session['job_name']
        self.job_name = job_name
        
        keywords = Data_Scientist.objects.get(QuesNum='1').Keywords
        key_split = word_tokenize(keywords)

        # get similar keywords of correct answer
        a_list = []
        for w in key_split:
            word = w2v_model.wv.most_similar(w, topn=10)
            a_list.append(word)
        ans_list = []
        for i in range(len(a_list)): 
            for j in range(len(a_list[i])):
                ans_list.append(a_list[i][j][0])
        for key in key_split:
            ans_list.append(key)
        print('\n', 'ANSWER ==== ', ans_list)

        
        ans = 'It is a graphical plot to programmatically illustrate a binary classifier to see whether valid.'
        ans_tokens = word_tokenize(ans)
        reply_token = [word for word in ans_tokens if not word in stopwords.words()]
        clean_reply = remove_noise(reply_token)

        # get similar keywords of user reply
        r_list = []
        for w in clean_reply:
            word = w2v_model.wv.most_similar(w, topn=10)
            r_list.append(word)
        reply_list = []
        for i in range(len(r_list)): 
            for j in range(len(r_list[i])):
                reply_list.append(r_list[i][j][0])
        for key in clean_reply:
            reply_list.append(key)
        print('\n', 'REPLY ==== ', reply_list)

        mean = int((len(reply_list)+len(ans_list))/2)

        # run similarity between reply & answer similar keywords
        while clean_reply:
            try:
                similarity = round((w2v_model.wv.n_similarity(reply_list, ans_list)) * 100, 2)
                print(similarity)
                break
            except Exception:
                print('word not found')
                break
        
        # see how many words are same between reply & answer
        same_words = set(reply_list) & set(ans_list)
        num_of_same_words = len(same_words)
        same_percentage = round(num_of_same_words/mean, 4) * 100


        return render(request, self.template_name, locals())
