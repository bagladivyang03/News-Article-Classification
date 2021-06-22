from flask import Flask, render_template, url_for, request
import pandas as pd 
import pickle
import requests 
from dotenv import load_dotenv
load_dotenv()
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
nltk.download('stopwords')
import sys
from nltk.corpus import stopwords
import logging
import json
API_KEY = os.getenv("API_KEY")
GOOGLE_NEWS_API_KEY = os.getenv("GOOGLE_NEWS_API_KEY")
app = Flask(__name__)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

def clean_text(text):
      # Lowercase and remove \r & \n
  text = text.lower().replace("\r","").replace("\n"," ").strip()
  # Remove multiple spaces
  text = re.sub(r'[^a-z\s]','',text)   # Takes care of other unwanted symbols.
  text = re.sub(' +',' ',text)
  # Remove unwanted/common words
  stop_words = set(stopwords.words('english'))
  stop_words.add('said')
  word_tokens = text.split(' ')
  filtered_sentence = [w for w in word_tokens if not w in stop_words] 
  text = " ".join(filtered_sentence)
  return text

ngrams_range = (1,2)
min_df = 0
max_df = 1.0
max_features = 250
norm = 'l2'  

tfidf = TfidfVectorizer(encoding='utf-8',
                        stop_words=None,
                        lowercase = False,
                        max_df = max_df,
                        min_df = min_df,
                        max_features = max_features,
                        norm = norm,
                        sublinear_tf = 'true')

articles =[]
all_articles = []

@app.route('/')
def home():
    url = "https://google-search3.p.rapidapi.com/api/v1/crawl/q=government+movies+technology+business&num=500"
    headers = {
        'x-rapidapi-key': GOOGLE_NEWS_API_KEY,
        'x-rapidapi-host': "google-search3.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers)
    print(response.json()['results'])
    articles_requested = response.json()['results']
    print(articles_requested)
    articles_data = response.json()['results']
    print(articles_data)
    articles = []
    for i in range(0,len(articles_requested)):
        if(articles_requested[i]['description'] != None):
            articles.append(articles_requested[i]['description'])
    articles_df = pd.DataFrame(articles,columns = ['STORY'])
    articles_df['story_parsed'] = articles_df['STORY'].apply(clean_text)
    articles_trained = tfidf.fit_transform(articles_df['story_parsed']).toarray()
    filename = 'new_article_classification.pkl'
    clf = pickle.load(open(filename, 'rb'))
    articles_predicted = clf.predict(articles_trained)
    
    for i in range(0,len(articles_predicted)):
        data = {}
        data['article_type'] = articles_predicted[i]
        data['title'] = articles_data[i]['title']
        data['description'] = articles_data[i]['description']
        data['link'] = articles_data[i]['link']
        all_articles.append(data)
    print(all_articles)
    return render_template('base.html',articles=articles)


@app.route('/newsarticle/<varible_name>/')
def article(varible_name):
    if(varible_name == 'entertainment'):
        articles= filter(lambda x: x['article_type']==2,all_articles)
    if(varible_name == 'politics'):
        articles= filter(lambda x: x['article_type']==0,all_articles)
    if(varible_name == 'technology'):
        articles= filter(lambda x: x['article_type']==1,all_articles)
    if(varible_name == 'business'):
        articles= filter(lambda x: x['article_type']==3,all_articles)
    return render_template('article.html',title=varible_name,articles=articles)


if __name__ == '__main__':
	app.run(debug=True)