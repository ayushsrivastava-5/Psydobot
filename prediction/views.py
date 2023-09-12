from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import joblib
import gensim
#from gensim.models import Word2Vec
#from word_mover_distance import model
#import emd2
import pandas as pd
#import sklearn as sk
import numpy as np

import nltk
nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize.toktok import ToktokTokenizer

from bs4 import BeautifulSoup
import re,string,unicodedata


import nltk
from nltk.stem import WordNetLemmatizer
import re







# Create your views here.
from django.http import HttpResponse


def login(request):
    return render(request,'login.html')


def index(request):
    return render(request,'start.html')


def signup(request):
    if(request.method=="POST"):
        if (len(request.POST['zip']) == 6):
            try:
                User.objects.get(username = request.POST['username'])
                return render (request,'login.html', {'error':'Username is already taken!'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password'])
                auth.login(request,user)
                return redirect('index')
        else:
            return render (request,'login.html', {'error':'ZIP Code is invalid!'})
    else:
        return render(request,'login.html')


def login_1(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password = request.POST['password'])
        if user is not None:
            auth.login(request,user)
            return redirect('home')
         
        else:
            return render (request,'login.html', {'error':'Username or password is incorrect!'})
    else:
        return render(request,'login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
    return redirect('index')

def home(request):
    return render(request,'home.html')

def stress(request):
    return render(request,'stress_meter.html')

def lowstress(request):
    return render(request,'low_stress.html')

def highstress(request):
    return render(request,'high_stress.html')

def moderatestress(request):
    return render(request,'moderate_stress.html')

def map(request):
    return render(request,'map.html')
    
@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        symp_1 = json.loads(request.body)
        sym = symp_1['message']

        model = joblib.load('C:\\Users\\shubham\\Downloads\\model_chatbot.pkl')
        def strip_html(text):
            soup = BeautifulSoup(text, "html.parser")
            return soup.get_text()


        def remove_urls(text):
            # Regular expression to match URLs
            url_pattern = re.compile(r'https?://\S+|www\.\S+')
            # Replace URLs with an empty string
            clean_text = url_pattern.sub('', text)
            return clean_text


        #Removing the square brackets and notations
        def remove_between_square_brackets(text):
            return re.sub('[^A-Za-z0-9/. ]', '', text)

        #Lemmatizing the text
        def simple_lemmatizer(text):
            lemmatizer = WordNetLemmatizer()
            text = ' '.join([lemmatizer.lemmatize(word) for word in text.split()])
            return text
            
        #set stopwords to english
        stop=set(stopwords.words('english'))
        #print(stop)

        #Tokenization of text
        tokenizer=ToktokTokenizer()

        #Setting English stopwords
        stopword_list=nltk.corpus.stopwords.words('english')

        #removing the stopwords
        def remove_stopwords(text, is_lower_case=False):
            tokens = tokenizer.tokenize(text)
            tokens = [token.strip() for token in tokens]
            if is_lower_case:
                filtered_tokens = [token for token in tokens if token not in stopword_list]
            else:
                filtered_tokens = [token for token in tokens if token.lower() not in stopword_list]
            filtered_text = ' '.join(filtered_tokens)    
            return filtered_text

        #Apply function on review column
        sym = remove_urls(sym)
        sym = strip_html(sym)
        sym = remove_between_square_brackets(sym)
        sym = simple_lemmatizer(sym)
        sym = remove_stopwords(sym)

        ocd = "fear of contamination, avoid germs, sanitation, compulsive behaviour, following specific order or pattern, agitation, compulsive hoarding, hypervigilance, impulsivity, meaningless repetition of own words, repetitive movements, ritualistic behaviour, social isolation, or persistent repetition of words or actions anxiety, apprehension, depression or fear food aversion,intrusive thoughts,repetitive behaviors,repeated occurrence,unpleasant, or repeatedly going over thoughts,avoids being alone,fear of losing, compulsion, right way of doing things, fear of losing loved ones"
        adhd = "aggression, excitability, fidgeting, hyperactivity, impulsivity, irritability, lack of restraint, or persistent repetition of words or actions, absent-mindedness, difficulty focusing, forgetfulness, problem paying attention, or short attention span, anger, anxiety, boredom, excitement, or mood swings, depression or learning disability,memory loss, mistakes, disorganised behaviour, misplacing things, being late, lack of concentration, procastination, distress, require extra time, slow, family history of adhd, attention deficit, restless, socially immature, difficulty in sustaining attention"
        depression = "low blood pressure, anxiety, apathy, general discontent, guilt, hopelessness, loss of interest, loss of interest or pleasure in activities, mood swings, or sadness, agitation, excessive crying, irritability, restlessness, or social isolation,panic attack early awakening, excess sleepiness, insomnia, or restless sleep excessive hunger, fatigue, or loss of appetite, lack of concentration, slowness in activity, or thoughts of suicide, weight gain or weight loss, poor appetite or repeatedly going over thoughts,headache, difficulty in staying focused, avoiding social interactions, irritable, numbness, fatigue, worthlessness, struggle"
        ptsd = "accidents, incidents, death, past, crime, horror, terror, hostility,  self-destructive behaviour, or social isolation, flashback, traumatic events, trauma, memories, fear, severe anxiety,panic attack or mistrust, loss of interest or pleasure in activities, guilt, or loneliness, nightmares, unwilling to share details, avoid meeting people, nightmares"
        # fine = "good, fine,  well, nothing, healthy, energetic, normal, happy, nothing special"
        
        disease = {}
        disease['ocd']=ocd
        disease['adhd']=adhd
        disease['depression']=depression
        disease['ptsd']=ptsd
        #disease['fine']=fine

        min=0.20
        p=''
        for i in disease.keys():
            distance = model.wmdistance(sym,disease[i])
            #print(distance)
            if(distance<min):
                min=distance
                p=i
            if 'compulsion' in i or 'specific order' in i:
                p='OCD'
            if 'disorganized' in i or 'poor attention' in i or 'ADHD' in i:
                p='ADHD'
        response = {"message":"Error"}
        if(p=='' or p=='fine'):
            response = {"message": "You dont seem to have any disorder. Try taking some less stress and be happy...."}
        else:
            response = {"message": "You might be suffering from " + p +". But it is alright. Do visit a doctor and you will get fine very soon. Stay happy!!"}

        #response = {'message': 'Hello, you said: ' + message['message']}
        return JsonResponse(response)
    else:
        return render(request,'chatbot.html')