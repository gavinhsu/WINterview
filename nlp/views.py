from django.shortcuts import render, redirect
from django.contrib import auth
from django.http import HttpResponse
import os, re, string
from MockInterview.settings import BASE_DIR
from questions.models import *
from users.models import *
import GTTS.views
import questions
from django.views.generic import TemplateView
import random, pickle, cloudpickle, torch, nltk, base64, warnings
import pandas as pd
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
from statistics import mode
import matplotlib.pyplot as plt
# fix main thread problem
plt.switch_backend('agg')
import matplotlib.patches as mpatches
from math import pi
from io import BytesIO
# from django.views.decorators.csrf import csrf_protect
# from django.core.context_processors import csrf
from math import pi
import numpy as np

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
        job_selection = getattr(questions.models, new_job)
        account_instance = Member.objects.get(Account=account_name)
        #res_id = Result.objects.filter(userID=account_instance).order_by('-id')[:1].values('id') 
        res_id = 333
        res_unit = Result.objects.get(id=res_id)
        ans_unit = Answer.objects.get(id=res_id)
        

        # retreive reply, questions, keywords, difficulty, time & answers
        full_reply = []
        full_ques = []
        full_ans = []
        full_key = []
        full_pn = []
        full_time = []
        full_diff = []

        for x in range(4):
            reply = "a{0}".format(x+1)
            ques = "q{0}".format(x+1)
            pn = "r{0}".format(x+1)
            time = "t{0}".format(x+1)
            get_reply = getattr(ans_unit, reply)
            get_ques = getattr(ans_unit, ques)
            get_time = getattr(ans_unit, time)
            get_pn = getattr(res_unit, pn)
            get_ans = str(job_selection.objects.get(Ques=get_ques).Ans)
            get_key = job_selection.objects.get(Ques=get_ques).Keywords
            get_diff = job_selection.objects.get(Ques=get_ques).Difficulties
            full_reply.append(get_reply)
            full_ques.append(get_ques)
            full_ans.append(get_ans)
            full_key.append(get_key)
            full_pn.append(get_pn)
            full_time.append(get_time)
            full_diff.append(get_diff)
            exec(f'reply{x+1} = full_reply[x]')
            exec(f'ques{x+1} = full_ques[x]')
            exec(f'answer{x+1} = full_ans[x]')
            exec(f'keyword{x+1} = full_key[x]')
            exec(f'time{x+1} = full_time[x]')
            exec(f'diff{x+1} = full_diff[x]')

        keyscore_list = []
        final_list = []

        # NLP PROCESSING #####################################################   
        for NUM in range(4):    
            key_split = word_tokenize(full_key[NUM])

            # solve answer keyword not in dictionary 
            word_vectors = model.wv
            
            # get similar keywords of CORRECT ANSWER
            a_list = []
            for w in key_split:
                if w in word_vectors.vocab:
                    word = model.wv.most_similar(w, topn=10)
                    a_list.append(word)
                else:
                    a_list.append(w)

            ans_list = []
            for i in range(len(a_list)): 
                for j in range(len(a_list[i])):
                    ans_list.append(a_list[i][j][0])
            # add the original words
            for key in key_split:
                ans_list.append(key)


            # Reply processing
            reply_tokens = word_tokenize(full_reply[NUM])
            reply_token = [word for word in reply_tokens if not word in stopwords.words()]
            c_reply = remove_noise(reply_token)

            # solve reply word not in dictionary 
            word_vectors = model.wv

            # get similar keywords of USER REPLY
            r_list = []
            for w in c_reply:
                if w in word_vectors.vocab:
                    word = model.wv.most_similar(w, topn=10)
                    r_list.append(word)
                else:
                    r_list.append(w)

            reply_list = []
            for r in range(len(r_list)): 
                for j in range(len(r_list[r])):
                    reply_list.append(r_list[r][j][0])
            # add the original words
            for key in c_reply:
                reply_list.append(key)

            print('---------', NUM+1, '----------------------------------------')


            # run similarity between REPLY & ANSWER similar keywords
            gensim_reply = []
            for w in reply_list:
                if w in word_vectors.vocab:
                    gensim_reply.append(w)
            
            gensim_ans = []
            for w in ans_list:
                if w in word_vectors.vocab:
                    gensim_ans.append(w)

            while c_reply:
                try:
                    gensim_score = round((model.wv.n_similarity(gensim_reply, gensim_ans)) * 100, 2)
                    break
                except Exception:
                    print('word not found')
                    break
        
            # see how many words are same between REPLY & ANSWER
            same_words = set(reply_list) & set(ans_list)
            num_of_same_words = len(same_words)


            # Calculate the proportion of same keywords
            counter = 0
            for w in key_split:
                k_list = []
                if w in word_vectors.vocab:
                    word = model.wv.most_similar(w, topn=10)
                    k_list.append(word)
                else:
                    k_list.append(w)

                key_list = []
                for i in range(len(k_list)): 
                    for j in range(len(k_list[i])):
                        key_list.append(k_list[i][j][0])
                same_num = len([i for i in reply_list if i in key_list])
                if same_num >= 1:
                    counter += 1

            keyword_score = round((counter/len(key_split))*100, 2)
            keyscore_list.append(keyword_score)
            print('KEYSCORE ===> ', keyword_score, '%')
        

            # BERT prediction
            rep = full_reply[NUM]
            answ = full_ans[NUM]
            bert_predict = bert.predict([(rep, answ)])
            bert_res = bert_predict[0]
            bert_score = round((bert_res/5)*100, 2)

            # P/N confidence prediction
            clean_pn = full_pn[NUM][1:-1].split()
            print(clean_pn)
            pn_result = clean_pn[0][1:-2]
            print(pn_result)
            pn_percent = float(clean_pn[-1])

            # FINAL SCORE
            final_score = int(round(((0.7)*bert_score + (0.3)*gensim_score), 0))
            if pn_percent == 'positive':
                final_score += pn_percent*2
            else:
                final_score -= pn_percent*2

            final_list.append(final_score)
            print('FINAL_SCORE ===> ', final_score)
            

        # calulate the average score of keywordscore & finalscore (out of 100)
        avg_key = sum(keyscore_list)/len(keyscore_list) 
        avg_final = sum(final_list)/len(final_list)

        #keyscore_list
        key1 = keyscore_list[0]
        key2 = keyscore_list[1]
        key3 = keyscore_list[2]
        key4 = keyscore_list[3]
        # key5 = keyscore_list[4]
        # key6 = keyscore_list[5]
        # key7 = keyscore_list[6]
        # key8 = keyscore_list[7]
        # key9 = keyscore_list[8]
        # key10 = keyscore_list[9]

        #semantic_list
        sem1 = final_list[0]
        sem2 = final_list[1]
        sem3 = final_list[2]
        sem4 = final_list[3]
        # sem5 = final_list[4]
        # sem6 = final_list[5]
        # sem7 = final_list[6]
        # sem8 = final_list[7]
        # sem9 = final_list[8]
        # sem10 = final_list[9]

        
        # Plot keyword accuracy
        for i in range(4):           
            key_fig, key_ax = plt.subplots()
            key_fig.set_figheight(3)
            key_fig.set_figwidth(4)
            key_start = 0
            key = keyscore_list[i]
            key_ax.broken_barh([(key_start, key)], [1,2], facecolors='#53bda5')
            key_ax.set_ylim(0, 4)
            key_ax.set_xlim(0, 100)
            key_ax.spines['left'].set_visible(False)
            key_ax.spines['bottom'].set_visible(False)
            key_ax.spines['top'].set_visible(False)
            key_ax.set_xticks([0, 100])
            key_ax.set_axisbelow(True) 
            key_ax.set_yticks([])
            key_ax.set_title('Keyword Accuracy', fontsize=14) 
            key_ax.grid(axis='x')
            key_ax.text(key+1, 2, str(keyscore_list[i])+'%', fontsize=14)

            #fig.suptitle('This is title of the chart', fontsize=16)
            #leg1 = mpatches.Patch(color='#6259D8', label='start')
            #leg2 = mpatches.Patch(color='#E53F08', label='key')
            # ax.legend(handles=[leg1, leg2], ncol=2)
            plt.tight_layout()

            #save_plot
            keywords_buffer = BytesIO()
            plt.savefig(keywords_buffer, format='png')
            keywords_buffer.seek(0)
            key_image = keywords_buffer.getvalue()
            keywords_buffer.close()

            keywords_bar = base64.b64encode(key_image)
            exec(f"keywords_bar{i+1} = keywords_bar.decode('utf-8')")



        # plot final similarity score
        for i in range(4):
            final_fig, final_ax = plt.subplots()
            final_fig.set_figheight(3)
            final_fig.set_figwidth(4)
            final_start = 0
            final = final_list[i]
            final_ax.broken_barh([(final_start, final)], [1, 2], facecolors='#53bda5')
            final_ax.set_xlim(0, 100)
            final_ax.set_ylim(0, 4)
            final_ax.spines['left'].set_visible(False)
            final_ax.spines['bottom'].set_visible(False)
            final_ax.spines['top'].set_visible(False)
            final_ax.set_xticks([0, 100])
            final_ax.set_yticks([])
            final_ax.set_axisbelow(True)
            final_ax.set_title('Answer Fitness',fontsize=14) 
            final_ax.grid(axis='x')
            final_ax.text(final+1, 2, str(final_list[i])+'%', fontsize=14)
            #fig.suptitle('This is title of the chart', fontsize=16)
            #leg1 = mpatches.Patch(color='#6259D8', label='start')
            #leg2 = mpatches.Patch(color='#E53F08', label='key')
            # ax.legend(handles=[leg1, leg2], ncol=2)
            plt.tight_layout()
            #save_plot
            final_buffer = BytesIO()
            plt.savefig(final_buffer, format='png')
            final_buffer.seek(0)
            final_image = final_buffer.getvalue()
            final_buffer.close()

            final_bar = base64.b64encode(final_image)
            exec(f"final_bar{i+1} = final_bar.decode('utf-8')")



        # BLINK PROCESSING #####################################################

        blink_dict = {}
        total_blinks = 0
        blink_score_list = []
        
        for x in range(10):
            blink = "b{0}".format(x+1)
            num = getattr(res_unit, blink)
            t = "time{0}".format(x+1)
            seconds = getattr(res_unit, t)
            minutes = int(seconds)/60
            blink_dict["bpm{0}".format(x+1)] = num/minutes
            #print(blink_dict["bpm{0}".format(x+1)])
            total_blinks += blink_dict["bpm{0}".format(x+1)]

            # set comments according to how nervous u r
            normal_comment = "You were not nervous at all! Great job and keep it up!"
            little_nervous_comment = "You seemed a little bit nervous. Try to relax a bit!"
            very_nervous_comment = "You were too nervous! Please try to relax before construct your answer."

            if blink_dict["bpm{0}".format(x+1)] <= 40:
                blink_score_list.append(10)
                exec(f'BlinkComment_{x+1} = normal_comment')
            elif 40 < blink_dict["bpm{0}".format(x+1)] <= 60:
                blink_score_list.append(8)
                exec(f'BlinkComment_{x+1} = little_nervous_comment')
            else:
                blink_score_list.append(6)
                exec(f'BlinkComment_{x+1} = very_nervous_comment')

            exec(f'BPM_{x+1} = num/minutes')

        final_blink_score = sum(blink_score_list)

      

        ##EMOTION PROCESSING #####################################################
        emotion_dict = {}
        n_sum = 0
        h_sum = 0
        a_sum = 0
        f_sum = 0
        s_sum = 0
        for x in range(3):
            n = "neutral_{0}".format(x+1)
            neutral = getattr(res_unit, n)
            emotion_dict['n{0}'.format(x+1)] = neutral
            h = "happy_{0}".format(x+1)
            happy = getattr(res_unit, h)
            emotion_dict['h{0}'.format(x+1)] = happy
            a = "angry_{0}".format(x+1)
            angry = getattr(res_unit, a)
            emotion_dict['a{0}'.format(x+1)] = angry
            f = "fear_{0}".format(x+1)
            fear = getattr(res_unit, f)
            emotion_dict['f{0}'.format(x+1)] = fear
            s = "surprise_{0}".format(x+1)
            surprise = getattr(res_unit, s)
            emotion_dict['s{0}'.format(x+1)] = surprise
  
            neutral = emotion_dict["n{0}".format(x+1)]
            happy = emotion_dict["h{0}".format(x+1)]
            angry = emotion_dict["a{0}".format(x+1)]
            fear = emotion_dict["f{0}".format(x+1)]
            surprise = emotion_dict["s{0}".format(x+1)]
            # sum up each emotion's percentage
            n_sum += neutral
            h_sum += happy
            a_sum += angry
            f_sum += fear
            s_sum += surprise

            print('---------EMOTION', x+1, '----------------------------------------')
            print(neutral, happy, angry, fear, surprise)

            #emotion radar plot
            emo = {'Neutral':neutral, 'Happy':happy, 'Angry':angry, 'Fear':fear, 'Surprise':surprise}
            df = pd.DataFrame([emo],index=["emo"])
            Attributes = list(df)
            AttNo = len(Attributes)
            values = df.iloc[0].tolist()
            values += values [:1]
            angles = [n / float(AttNo) * 2 * pi for n in range(AttNo)]
            angles += angles [:1]
            ax = plt.subplot(111, polar=True)

            #Add the attribute labels to our axes
            plt.xticks(angles[:-1], Attributes)

            #Plot the line around the outside of the filled area, using the angles and values calculated before
            ax.plot(angles, values)

            #Fill in the area plotted in the last line
            ax.fill(angles, values, 'teal', alpha=0.1)

            #Give the plot a title and show it
            ax.set_title("Emotion Radar Plot")

            plt.tight_layout()
            #save plot
            emo_buffer = BytesIO()
            plt.savefig(emo_buffer, format='png')
            emo_buffer.seek(0)
            image_png = emo_buffer.getvalue()
            emo_buffer.close()

            emo_bar = base64.b64encode(image_png)
            #emo_bar = emo_bar.decode('utf-8')
            exec(f"emo_bar{x+1} = emo_bar.decode('utf-8')")
        
        # calculate average emotion score
        avg_neutral = n_sum/3
        avg_happy = h_sum/3
        avg_angry = a_sum/3
        avg_fear = f_sum/3
        avg_surprise = s_sum/3
        emo_score = avg_neutral + avg_happy - 0.2*avg_angry - 0.1*avg_fear - 0.1*avg_surprise

        if emo_score >= 80:
            final_emo_score = 100
        elif 80 > emo_score >= 60:
            final_emo_score = 80
        elif 60 > emo_score >= 40:
            final_emo_score = 60
        else:
            final_emo_score = 50

        # GET ENTIRE OVERALL SCORE!!!
        overall_score = 0.35*keyword_score + 0.35*final_score + 0.18*final_blink_score + 0.12*final_emo_score
        print('KEYWORD SCORE ====> ', keyword_score)
        print('CORRECTNESS SCORE ====> ', final_score)
        print('BLINK SCORE ====> ', final_blink_score)
        print('EMOTION SCORE ====> ', final_emo_score)
        print('OVERALL SCORE ====> ', overall_score)
        
        if overall_score >= 80:
            fuel_degree = 87.5
        elif 80 > overall_score >= 60:
            fuel_degree = 62.5
        elif 60 > overall_score >= 40:
            fuel_degree = 37.5
        else:
            fuel_degree = 12.5
        
        
        n1 = round(emotion_dict['n1'],2)
        h1 = round(emotion_dict['h1'],2)
        a1 = round(emotion_dict['a1'],2)
        f1 = round(emotion_dict['f1'],2)
        s1 = round(emotion_dict['s1'],2)
        n2 = round(emotion_dict['n2'],2)
        h2 = round(emotion_dict['h2'],2)
        a2 = round(emotion_dict['a2'],2)
        f2 = round(emotion_dict['f2'],2)
        s2 = round(emotion_dict['s2'],2)
        n3 = round(emotion_dict['n3'],2)
        h3 = round(emotion_dict['h3'],2)
        a3 = round(emotion_dict['a3'],2)
        f3 = round(emotion_dict['f3'],2)
        s3 = round(emotion_dict['s3'],2)
        n4 = round(emotion_dict['n4'],2)
        h4 = round(emotion_dict['h4'],2)
        a4 = round(emotion_dict['a4'],2)
        f4 = round(emotion_dict['f4'],2)
        s4 = round(emotion_dict['s4'],2)
        print(n4,h4,a4,s4,f4)




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

all_words_path = os.path.join(BASE_DIR,'all_words.txt')
f = open(all_words_path, "r")
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

 
