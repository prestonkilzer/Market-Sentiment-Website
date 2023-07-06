import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
import requests
import pandas as pd
from finvizfinance.quote import finvizfinance
from finvizfinance.news import News

nltk.download('vader_lexicon')

def get_news(company):
    stock = finvizfinance(company)
    news_df = stock.ticker_news()
    sentences = list(news_df['Title'])
    links = list(news_df['Link'])

    API_KEY = 'https://api.polygon.io/v2/reference/news?ticker='+company+'&published_utc=2023-06-22&limit=100&apiKey=lv5IqkF2jDExuKkO9MpdSm9hHBj8hjxG'
    response = requests.get(API_KEY)
    rawdata = response.json()

    for item in rawdata:
        if item == "results":
            rawdata = rawdata[item]

    summaries = []
    titles = []
    for bar in rawdata:
        for category in bar:
            if category == "description":
                summaries.append(bar[category])
                summaries = list(summaries)
    return sentences, links, summaries

def get_sentiment(summaries):
    sentiment_scores = []
    sid = SentimentIntensityAnalyzer()
    for sentence in summaries:
        ss = sid.polarity_scores(sentence)
        sentiment_scores.append(ss)
    return sentiment_scores

def avgscore(scores):
    avg_positive = sum(score['pos'] for score in scores) / len(scores)
    avg_negative = sum(score['neg'] for score in scores) / len(scores)
    avg_neutral = sum(score['neu'] for score in scores) / len(scores)
    return avg_positive, avg_negative, avg_neutral

news, links, summaries = get_news('AAPL')
score = get_sentiment(news)

avg_positive, avg_negative, avg_neutral = avgscore(score)


