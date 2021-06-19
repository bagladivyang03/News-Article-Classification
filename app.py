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
from nltk.corpus import stopwords
API_KEY = os.getenv("API_KEY")

app = Flask(__name__)

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
min_df = 1
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

entertainment_articles =[]
politics_articles = []
business_articles = []
technology_articles = []
all_articles = []

@app.route('/')
def home():
    query_params = {
    #   "source": "bbc-news",
    #   "sortBy": "top",
    # "sources" : "bbc-news,abc-news,aftenposten,ansa,ars-technica,associated-press",
    "language": "en",
      "apiKey": API_KEY,
    #   "country":"in"
    # "q" :"say"
    }
    main_url = "https://newsapi.org/v2/top-headlines"
    # url = "https://bing-news-search1.p.rapidapi.com/news"

    # querystring = {"textFormat":"Raw","safeSearch":"Off"}

    # headers = {
    #     'x-bingapis-sdk': "true",
    #     'x-rapidapi-key': "a44c138188msh26db5a879ce4a96p1198c1jsn239b6a0ac379",
    #     'x-rapidapi-host': "bing-news-search1.p.rapidapi.com"
    #     }

    # response = requests.request("GET", url, headers=headers, params=querystring)
    # print(len(response.json()['value']))
    # print(response.text.json())
    res = requests.get(main_url, params=query_params)
    articles_requested = res.json()
    print(articles_requested)
    articles_data = articles_requested['articles']
    print(articles_data)
    articles = []
    for i in range(0,len(articles_requested['articles'])):
        if(articles_requested['articles'][i]['content'] != None):
            articles.append(articles_requested['articles'][i]['content'])
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
        data['image'] = articles_data[i]['urlToImage']
        all_articles.append(data)
    print(all_articles)
    return render_template('base.html',articles=articles)


@app.route('/newsarticle/<varible_name>/')
def article(varible_name):
    if(varible_name == 'entertainment'):
        entertainment_articles= filter(lambda x: x['article_type']==2,all_articles)
    if(varible_name == 'politics'):
        entertainment_articles= filter(lambda x: x['article_type']==0,all_articles)
    if(varible_name == 'technology'):
        entertainment_articles= filter(lambda x: x['article_type']==1,all_articles)
    if(varible_name == 'business'):
        entertainment_articles= filter(lambda x: x['article_type']==3,all_articles)
    return render_template('article.html',title=varible_name,articles=entertainment_articles)


if __name__ == '__main__':
	app.run(debug=True)