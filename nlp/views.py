from django.shortcuts import render
import re, string 
import pandas as pd   
from collections import defaultdict
from collections import Counter, namedtuple
import re
import spacy
from sklearn.manifold import TSNE #visualize high-dimensional data
'''import nltk
nltk.download('stopwords')  
from nltk.corpus import stopwords
STOPWORDS = set(stopwords.words('english'))'''
from gensim.models import Word2Vec

# Create your views here.
