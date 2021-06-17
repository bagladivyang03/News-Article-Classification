from flask import Flask, render_template, url_for, request
import pandas as pd 
import pickle
import requests 
from dotenv import load_dotenv
load_dotenv()
import os
API_KEY = os.getenv("API_KEY")

app = Flask(__name__)


@app.route('/')
def home():
    query_params = {
    #   "source": "bbc-news",
    #   "sortBy": "top",
    "sources" : "bbc-news,abc-news,aftenposten,ansa,ars-technica,associated-press",
    # "language": "en",
      "apiKey": API_KEY
    }
    main_url = "https://newsapi.org/v2/top-headlines"
    res = requests.get(main_url, params=query_params)
    articles_requested = res.json()
    print(articles_requested)
    articles = []
    for i in range(0,len(articles_requested['articles'])):
        print(articles_requested['articles'][i])
        articles.append(articles_requested['articles'][i]['title'])
    print(articles)
    return render_template('base.html',articles=articles)


@app.route('/newsarticle/<varible_name>/')
def article(varible_name):
    return render_template('result.html',title=varible_name)

if __name__ == '__main__':
	app.run(debug=True)