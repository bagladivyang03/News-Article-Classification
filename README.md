# News-Article-Classification
This web application is developed to help classify news articles into 4 categories - 
a] Entertainment  
b] Politics  
c] Technology  
d] Business
The application uses NLP techniques and machine learning models to classify the articles into their respective categories. This application deals with text data(news articles) hence the preprocessing of data is slightly different than usual.  
You can check out the app [here](https://news-article-classification.herokuapp.com/)



## Steps followed:

### Data Preprocessing 
1. Clean the text 
2. Tokenize the text
3. Apply Lemmatization(WordNet)
4. Remove stopwords

### Feature Engineering
1. Apply TF-IDF vectorization

### Model Building
1. Split the processed data into train and test sets. 
2. Apply ML Algorithms like Random Forest and Logistic Regression.

### Model Evalution
1. Compare the results of the two applied algorithms and choose the best one(in this case Logistic Regression).
2. Save the model into pickle file.

### Build Web Application
1. Use the flask web framework.
2. Use the Google Search API to fetch the news.
3. Use the saved model to classify the fetched news. 

### Deploy the web app
1. Deploy the web application using Heroku platform.



## Architecture of Application

![Architecture Diagram](/images/Architecture.png)


## Screenshots

![Architecture Diagram](/images/homepage.JPG)

![Architecture Diagram](/images/entertainment.JPG)
