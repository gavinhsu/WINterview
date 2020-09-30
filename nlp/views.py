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
import nltk
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
# nltk.download('twitter_samples')
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier

from nltk.classify import ClassifierI
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import plotly.express as px
import pandas as pd
from math import pi
from io import BytesIO
import base64
# from django.views.decorators.csrf import csrf_protect
# from django.core.context_processors import csrf
from django.views.generic import TemplateView
import GTTS.views
import warnings
import questions


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


########################################################
#BERT
torch.nn.Module.dump_patches = True
warnings.filterwarnings("ignore")

bert_file_path = os.path.join(BASE_DIR, 'bert.pickle')
bert = torch.load(bert_file_path)

# GENSIM
# tech model
tech_path = os.path.join(BASE_DIR, 'test.pickle')
tech_model = pd.read_pickle(tech_path)
# finance model
fin_path = os.path.join(BASE_DIR, 'analOthman.pkl')
fin_model = pd.read_pickle(fin_path)


class ResultView(TemplateView):
    template_name = 'result.html'

    def __init__(self, job_name=None):
        self.job_name = job_name

    def get(self, request):
        account_name = request.session['account']
        job_name = request.session['job_name']
        self.account_name = account_name
        self.job_name = job_name
        
        if job_name == "Hardware Engineer"or"Software Engineer"or"ML Engineer"or"DBA"or"Data Scientist":
            model = tech_model
        else:
            model = fin_model

        for letter in str(job_name):
            new_job = job_name.replace(' ', '_')  

        # get the entire result table 
        account_instance = Member.objects.get(Account=account_name)
        res_id = Result.objects.filter(userID=account_instance).order_by('-id')[:1].values('id') 
        res_unit = Result.objects.get(id=res_id)
        

        # NLP PROCESSING #####################################################
        job_selection = getattr(questions.models, new_job)
        answer = str(job_selection.objects.get(QuesNum='1').Ans)
        keywords = job_selection.objects.get(QuesNum='1').Keywords
        key_split = word_tokenize(keywords)
        
        # get similar keywords of CORRECT ANSWER
        a_list = []
        for w in key_split:
            word = model.wv.most_similar(w, topn=10)
            a_list.append(word)
        ans_list = []
        for i in range(len(a_list)): 
            for j in range(len(a_list[i])):
                ans_list.append(a_list[i][j][0])
        for key in key_split:
            ans_list.append(key)

        
        reply = 'It is a graphical plot to programmatically illustrate a binary classifier to see whether valid.'
        reply_tokens = word_tokenize(reply)
        reply_token = [word for word in reply_tokens if not word in stopwords.words()]
        clean_reply = remove_noise(reply_token)

        # get similar keywords of USER REPLY
        r_list = []
        for w in clean_reply:
            word = model.wv.most_similar(w, topn=10)
            r_list.append(word)
        reply_list = []
        for i in range(len(r_list)): 
            for j in range(len(r_list[i])):
                reply_list.append(r_list[i][j][0])
        for key in clean_reply:
            reply_list.append(key)

        mean = int((len(reply_list)+len(ans_list))/2)


        # run similarity between REPLY & ANSWER similar keywords
        while clean_reply:
            try:
                gensim_score = round((model.wv.n_similarity(reply_list, ans_list)) * 100, 2)
                break
            except Exception:
                print('word not found')
                break
        
        # see how many words are same between REPLY & ANSWER
        same_words = set(reply_list) & set(ans_list)
        num_of_same_words = len(same_words)

        #gensim score chart
        fig, ax = plt.subplots()
        start = 0
        key = num_of_same_words
        ax.broken_barh([(start, key)], [10, 9], facecolors=((0.3,0.1,0.4,0.6)))
        ax.set_ylim(5, 15)
        ax.set_xlim(0, mean)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_yticks([15, 25])
        ax.set_xticks([0, 25, 50, 75, mean])
        ax.set_axisbelow(True) 
        #ax.set_yticklabels(['keywords'])
        ax.grid(axis='x')
        ax.text(key+1, 15, '{:.2f}%'.format(key/mean*100), fontsize=8)

        #fig.suptitle('This is title of the chart', fontsize=16)

        #leg1 = mpatches.Patch(color='#6259D8', label='start')
        #leg2 = mpatches.Patch(color='#E53F08', label='key')
        # ax.legend(handles=[leg1, leg2], ncol=2)
        plt.tight_layout()

        #save_plot
        keywords_buffer = BytesIO()
        plt.savefig(keywords_buffer, format='png')
        keywords_buffer.seek(0)
        image_png = keywords_buffer.getvalue()
        keywords_buffer.close()

        keywords_bar = base64.b64encode(image_png)
        keywords_bar = keywords_bar.decode('utf-8')

        # BERT prediction
        bert_predict = bert.predict([(reply, answer)])
        bert_res = bert_predict[0]
        bert_score = round((bert_res/5)*100, 2)

        # FINAL SCORE
        final_score = int(round(((0.7)*bert_score + (0.3)*gensim_score + num_of_same_words), 0))

        #answer&reply similarity


        # BLINK PROCESSING #####################################################
        # total_blinks = 0
        # for x in range(10):
        #     blink = "b{0}".format(x+1)
        #     num = getattr(res_unit, blink)
        #     total_blinks += num

        # mean_blinks = total_blinks/10

        blink_dict = {}
        total_blinks = 0
        for x in range(10):
            blink = "b{0}".format(x+1)
            num = getattr(res_unit, blink)
            t = "time{0}".format(x+1)
            seconds = getattr(res_unit, t)
            minutes = int(seconds)/60
            blink_dict["bpm{0}".format(x+1)] = num/minutes
            total_blinks += blink_dict["bpm{0}".format(x+1)]
            exec(f'BPM_{x+1} = num/minutes')

        avg_blinks = round(total_blinks/10, 2)
        

        # EMOTION PROCESSING #####################################################
        # emotion_dict = {}
        # for x in range(10):
        #     n = "neutral_{0}".format(x+1)
        #     neutral = getattr(res_unit, n)
        #     emotion_dict['n{0}'.format(x+1)] = neutral
        #     h = "neutral_{0}".format(x+1)
        #     happy = getattr(res_unit, h)
        #     emotion_dict['h{0}'.format(x+1)] = happy
        #     a = "neutral_{0}".format(x+1)
        #     angry = getattr(res_unit, a)
        #     emotion_dict['a{0}'.format(x+1)] = angry
        #     f = "neutral_{0}".format(x+1)
        #     fear = getattr(res_unit, f)
        #     emotion_dict['f{0}'.format(x+1)] = fear
        #     s = "neutral_{0}".format(x+1)
        #     surprise = getattr(res_unit, s)
        #     emotion_dict['s{0}'.format(x+1)] = surprise
        
        neutral = getattr(res_unit, 'neutral_1')
        happy = getattr(res_unit, 'happy_1')
        angry = getattr(res_unit, 'angry_1')
        fear = getattr(res_unit, 'fear_1')
        surprise = getattr(res_unit, 'surprise_1')
        #emotion radar plot
        emo = {'Neutral':neutral, 'Happy':happy, 'Angry':angry, 'Fear':fear, 'Surprise':surprise}
        df = pd.DataFrame([emo],index=["emo"])
        Attributes =list(df)
        AttNo = len(Attributes)
        values = df.iloc[0].tolist()
        values += values [:1]
        angles = [n / float(AttNo) * 2 * pi for n in range(AttNo)]
        angles += angles [:1]
        ax = plt.subplot(111, polar=True)

        #Add the attribute labels to our axes
        plt.xticks(angles[:-1],Attributes)

        #Plot the line around the outside of the filled area, using the angles and values calculated before
        ax.plot(angles,values)

        #Fill in the area plotted in the last line
        ax.fill(angles, values, 'teal', alpha=0.1)

        #Give the plot a title and show it
        ax.set_title("Emotion Radar Plot")

        #save plot
        emo_buffer = BytesIO()
        plt.savefig(emo_buffer, format='png')
        emo_buffer.seek(0)
        image_png = emo_buffer.getvalue()
        emo_buffer.close()

        emo_bar = base64.b64encode(image_png)
        emo_bar = emo_bar.decode('utf-8')

        return render(request, self.template_name, locals())




########################################################
## new nlp model with percentage #######################
positive_tweets = twitter_samples.strings('positive_tweets.json')
negative_tweets = twitter_samples.strings('negative_tweets.json')

all_words = []
documents = []

stop_words = list(set(stopwords.words('english')))

#allowed_word_types = ["J","R","V"]
allowed_word_types = ["J"]

for p in  positive_tweets:
    documents.append( (p, "pos") )
         
for p in negative_tweets:
    documents.append( (p, "neg") )

f = open('.\\all_words.txt', "r")
content = f.readlines()
for word in content:
    tmp = word.replace('\n', '')
    all_words.append(tmp)

all_words = nltk.FreqDist(all_words)
word_features = list(all_words.keys())[:5000]

def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features

classifier_path = os.path.join(BASE_DIR, 'classifier_model.pickle')
classifier = pd.read_pickle(classifier_path)
ensemble_path = os.path.join(BASE_DIR, 'confidence_model.pickle')
ensemble_clf = pd.read_pickle(ensemble_path)

def sentiment(n, account_name):
    account_instance = Member.objects.get(Account=account_name)
    uid = Answer.objects.filter(userID=account_instance).order_by('-id')[:1].values('id') 
    ans_unit = Answer.objects.get(id=uid)
    a = "a{0}".format(n)
    answer = getattr(ans_unit, a)
    print(answer)

    feats = find_features(answer)
    print(classifier.classify(feats))
    print(ensemble_clf.confidence(feats))

    return classifier.classify(feats), ensemble_clf.confidence(feats)

 
