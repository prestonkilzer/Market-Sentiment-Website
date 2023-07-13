import streamlit as st
import requests
import sentiment
import json
from datetime import datetime, timedelta
from PIL import Image
import matplotlib.pyplot as plt
# Other required imports here...

# Define functions for your application

import requests
import json

def get_market_info(company):
    API_KEY = 'https://api.polygon.io/v2/aggs/ticker/'+company+'/prev?adjusted=true&apiKey=lv5IqkF2jDExuKkO9MpdSm9hHBj8hjxG'

    response = requests.get(API_KEY)
    rawdata = response.json()

    if "results" in rawdata:
        results = rawdata["results"]
        for item in results:
            if type(item) is dict and "v" in item and "o" in item and "c" in item and "h" in item and "l" in item:
                volume = item["v"]
                open_price = item['o']
                close = item['c']
                high = item['h']
                low = item['l']
    return(volume, open_price, close, high, low)

def get_private_holdings(company):
    # Implement your private holdings API calls here...
    pass

# The Streamlit application layout
st.title("Daily Market Analysis Tracker")

st.sidebar.title("Website Pages")
app_mode = st.sidebar.selectbox("Choose the section", ["Home", "Company Sentiment", "Market Info", "Private Holdings"])

if app_mode == 'Home':
    st.write("Where you can see the daily sentiment for equties and the market.")

elif app_mode == 'Company Sentiment':
    company_name = st.text_input('Enter a company ticker')
    company_name = company_name.upper()
    if st.button('Get Sentiment'):
        sentences, links, summaries = sentiment.get_news(company_name)
        sentiment_scores =  sentiment.get_sentiment(sentences)
        avgpos, avgneg, avgneu = sentiment.avgscore(sentiment_scores)
        avgpos = round(avgpos * 10 * 100, 2)
        avgneg = round(avgneg * 10 * 100, 2)
        avgneu = round(avgneu * 100, 2)# Calculate the total sum of scores
        total_score = avgpos + avgneu + avgneg

        # Calculate the percentage for each score
        positive_percentage = (avgpos / total_score)
        neutral_percentage = (avgneu / total_score)
        negative_percentage = (avgneg / total_score)

        # Apply weights to the percentages
        final_score = round((positive_percentage * 100) + (neutral_percentage * 50) + (negative_percentage * 0), 0)
            
        st.subheader("Sentiment Score between 0 and 100: " + str(final_score))
        categories = ['Positive', 'Neutral', 'Negative']
        values = [avgpos, avgneu, avgneg]
        colors = ['green', 'yellow', 'red']
        bars = plt.bar(categories, values)
        for bar, color in zip(bars, colors):
            bar.set_facecolor(color)

        # Add labels and title
        plt.xlabel('Sentiment')
        plt.ylabel('Score')
        plt.title(company_name +' Sentiment Score')
        st.pyplot(plt)

        volume, open, close, high, low = get_market_info(company_name)
        st.header('Previous Business Day ' + company_name+ ' Trading Information')
        st.write("Open: " + str(open))
        st.write("Close: " + str(close))
        st.write("High: " + str(high))
        st.write("Low: " + str(low))
        st.write("Volume: " + str(volume))

        for i in range(5):
            st.write(sentences[i])
            st.write(links[i])


elif app_mode == 'Market Info':
    st.header('Previous Business Day SPY Information')
    
    sentences, links, summaries = sentiment.get_news('SPY')
    sentiment_scores =  sentiment.get_sentiment(sentences)
    avgpos, avgneg, avgneu = sentiment.avgscore(sentiment_scores)
    avgpos = round(avgpos, 2) * 10 * 100
    avgneg = round(avgneg, 2) * 10 * 100
    avgneu = round(avgneu, 2) * 100
    total_score = avgpos + avgneu + avgneg

    # Calculate the percentage for each score
    positive_percentage = (avgpos / total_score)
    neutral_percentage = (avgneu / total_score)
    negative_percentage = (avgneg / total_score)
    # Apply weights to the percentages
    final_score = round((positive_percentage * 100) + (neutral_percentage * 50) + (negative_percentage * 0), 0)
    
    st.subheader("Sentiment Score between 0 and 100: " + str(final_score))
    categories = ['Positive', 'Neutral', 'Negative']
    values = [avgpos, avgneu, avgneg]
    colors = ['green', 'yellow', 'red']
    bars = plt.bar(categories, values)
    for bar, color in zip(bars, colors):
        bar.set_facecolor(color)

    # Add labels and title
    plt.xlabel('Sentiment')
    plt.ylabel('Score')
    plt.title('SPY Sentiment Score')
    st.pyplot(plt)

    # Display the chart

    volume, open, close, high, low = get_market_info('SPY')
    print(volume, open, close, high, low)
    st.write("Open: " + str(open))
    st.write("Close: " + str(close))
    st.write("High: " + str(high))
    st.write("Low: " + str(low))
    st.write("Volume: " + str(volume))

    for i in range(5):
        st.write(sentences[i])
        st.write(links[i])

elif app_mode == 'Selected Private News':
    # Define your private holdings
    private_holdings = ["SpaceX", "Qonto", "Bytedance", "Shein", "Stripe, Inc.", "Baibu", "Fuzhou Pupu E-commerce Co., Ltd.", "Octane Lending, Inc.", "Shanghai Yinhe Industrial Co., Ltd.", "N26, Inc.", "Stash Financial, Inc.", "Taxfix AG", "Flipkart Internet Pvt. Ltd.", "Neo Financial Technologies, Inc.", "J.H. Whitney VI, L.P."]
    # Get the current date and time
    current_datetime = datetime.now()

    # Calculate the date from the past year
    past_year_date = current_datetime - timedelta(days=30)
    # Create a dropdown menu with the private holdings

    selected_holding = st.selectbox('Select a private company:', private_holdings)
    # Now add some conditional display

    if selected_holding == "SpaceX":

        url = ('https://newsapi.org/v2/everything?'
           'q='+selected_holding+'&'
           'from='+str(past_year_date)+'&'
           'sortBy=relevancy&'
           'apiKey=170eef92d9874eeab6605ba11b12cf1d')
        
        response = requests.get(url)
        data = response.json()

        articles = data.get("articles", [])
        for article in articles:
            title = article.get("title")
            link = article.get("url")
            if title and link:
                st.write("Title:", title)
                st.write("Link:", link)
                st.write()
        if not articles:
            st.write("No recent news for " + selected_holding)

    if selected_holding == "Qonto":

        url = ('https://newsapi.org/v2/everything?'
           'q='+selected_holding+'&'
           'from='+str(past_year_date)+'&'
           'sortBy=relevancy&'
           'apiKey=170eef92d9874eeab6605ba11b12cf1d')
        
        response = requests.get(url)
        data = response.json()

        articles = data.get("articles", [])
        for article in articles:
            title = article.get("title")
            link = article.get("url")
            if title and link:
                st.write("Title:", title)
                st.write("Link:", link)
                st.write()
        if not articles:
            st.write("No recent news for " + selected_holding)              


    if selected_holding == "Bytedance":

        url = ('https://newsapi.org/v2/everything?'
           'q='+selected_holding+'&'
           'from='+str(past_year_date)+'&'
           'sortBy=relevancy&'
           'apiKey=170eef92d9874eeab6605ba11b12cf1d')
        
        response = requests.get(url)
        data = response.json()

        articles = data.get("articles", [])
        for article in articles:
            title = article.get("title")
            link = article.get("url")
            if title and link:
                st.write("Title:", title)
                st.write("Link:", link)
                st.write()
        if not articles:
            st.write("No recent news for " + selected_holding)
    
    if selected_holding == "Shein":

        url = ('https://newsapi.org/v2/everything?'
           'q='+selected_holding+'&'
           'from='+str(past_year_date)+'&'
           'sortBy=relevancy&'
           'apiKey=170eef92d9874eeab6605ba11b12cf1d')
        
        response = requests.get(url)
        data = response.json()

        articles = data.get("articles", [])
        for article in articles:
            title = article.get("title")
            link = article.get("url")
            if title and link:
                st.write("Title:", title)
                st.write("Link:", link)
                st.write()
        if not articles:
            st.write("No recent news for " + selected_holding)
    
    if selected_holding == "Stripe, Inc.":

        url = ('https://newsapi.org/v2/everything?'
           'q='+selected_holding+'&'
           'from='+str(past_year_date)+'&'
           'sortBy=relevancy&'
           'apiKey=170eef92d9874eeab6605ba11b12cf1d')
        
        response = requests.get(url)
        data = response.json()

        articles = data.get("articles", [])
        for article in articles:
            title = article.get("title")
            link = article.get("url")
            if title and link:
                st.write("Title:", title)
                st.write("Link:", link)
                st.write()
        if not articles:
            st.write("No recent news for " + selected_holding)
    
    if selected_holding == "Baibu":

        url = ('https://newsapi.org/v2/everything?'
           'q='+selected_holding+'&'
           'from='+str(past_year_date)+'&'
           'sortBy=relevancy&'
           'apiKey=170eef92d9874eeab6605ba11b12cf1d')
        
        response = requests.get(url)
        data = response.json()

        articles = data.get("articles", [])
        for article in articles:
            title = article.get("title")
            link = article.get("url")
            if title and link:
                st.write("Title:", title)
                st.write("Link:", link)
                st.write()
        if not articles:
            st.write("No recent news for " + selected_holding)

    if selected_holding == "Fuzhou Pupu E-commerce Co., Ltd.":

        url = ('https://newsapi.org/v2/everything?'
           'q='+selected_holding+'&'
           'from='+str(past_year_date)+'&'
           'sortBy=relevancy&'
           'apiKey=170eef92d9874eeab6605ba11b12cf1d')
        
        response = requests.get(url)
        data = response.json()

        articles = data.get("articles", [])
        for article in articles:
            title = article.get("title")
            link = article.get("url")
            if title and link:
                st.write("Title:", title)
                st.write("Link:", link)
                st.write()
        if not articles:
            st.write("No recent news for " + selected_holding)

    if selected_holding == "Octane Lending, Inc.":

        url = ('https://newsapi.org/v2/everything?'
           'q='+selected_holding+'&'
           'from='+str(past_year_date)+'&'
           'sortBy=relevancy&'
           'apiKey=170eef92d9874eeab6605ba11b12cf1d')
        
        response = requests.get(url)
        data = response.json()

        articles = data.get("articles", [])
        for article in articles:
            title = article.get("title")
            link = article.get("url")
            if title and link:
                st.write("Title:", title)
                st.write("Link:", link)
                st.write()
        if not articles:
            st.write("No recent news for " + selected_holding)

    if selected_holding == "Shanghai Yinhe Industrial Co., Ltd.":

        url = ('https://newsapi.org/v2/everything?'
           'q='+selected_holding+'&'
           'from='+str(past_year_date)+'&'
           'sortBy=relevancy&'
           'apiKey=170eef92d9874eeab6605ba11b12cf1d')
        
        response = requests.get(url)
        data = response.json()

        articles = data.get("articles", [])
        for article in articles:
            title = article.get("title")
            link = article.get("url")
            if title and link:
                st.write("Title:", title)
                st.write("Link:", link)
                st.write()
        if not articles:
            st.write("No recent news for " + selected_holding)

    if selected_holding == "N26, Inc.":

        url = ('https://newsapi.org/v2/everything?'
           'q='+selected_holding+'&'
           'from='+str(past_year_date)+'&'
           'sortBy=relevancy&'
           'apiKey=170eef92d9874eeab6605ba11b12cf1d')
        
        response = requests.get(url)
        data = response.json()

        articles = data.get("articles", [])
        for article in articles:
            title = article.get("title")
            link = article.get("url")
            if title and link:
                st.write("Title:", title)
                st.write("Link:", link)
                st.write()
        if not articles:
            st.write("No recent news for " + selected_holding)

    if selected_holding == "Stash Financial, Inc.":

        url = ('https://newsapi.org/v2/everything?'
           'q='+selected_holding+'&'
           'from='+str(past_year_date)+'&'
           'sortBy=relevancy&'
           'apiKey=170eef92d9874eeab6605ba11b12cf1d')
        
        response = requests.get(url)
        data = response.json()

        articles = data.get("articles", [])
        for article in articles:
            title = article.get("title")
            link = article.get("url")
            if title and link:
                st.write("Title:", title)
                st.write("Link:", link)
                st.write()
        if not articles:
            st.write("No recent news for " + selected_holding)

    if selected_holding == "Taxfix AG":

        url = ('https://newsapi.org/v2/everything?'
           'q='+selected_holding+'&'
           'from='+str(past_year_date)+'&'
           'sortBy=relevancy&'
           'apiKey=170eef92d9874eeab6605ba11b12cf1d')
        
        response = requests.get(url)
        data = response.json()

        articles = data.get("articles", [])
        for article in articles:
            title = article.get("title")
            link = article.get("url")
            if title and link:
                st.write("Title:", title)
                st.write("Link:", link)
                st.write()
        if not articles:
            st.write("No recent news for " + selected_holding)

    if selected_holding == "Flipkart Internet Pvt. Ltd.":

        url = ('https://newsapi.org/v2/everything?'
           'q='+selected_holding+'&'
           'from='+str(past_year_date)+'&'
           'sortBy=relevancy&'
           'apiKey=170eef92d9874eeab6605ba11b12cf1d')
        
        response = requests.get(url)
        data = response.json()

        articles = data.get("articles", [])
        for article in articles:
            title = article.get("title")
            link = article.get("url")
            if title and link:
                st.write("Title:", title)
                st.write("Link:", link)
                st.write()
        if not articles:
            st.write("No recent news for " + selected_holding)

    if selected_holding == "Neo Financial Technologies, Inc.":

        url = ('https://newsapi.org/v2/everything?'
           'q='+selected_holding+'&'
           'from='+str(past_year_date)+'&'
           'sortBy=relevancy&'
           'apiKey=170eef92d9874eeab6605ba11b12cf1d')
        
        response = requests.get(url)
        data = response.json()

        articles = data.get("articles", [])
        for article in articles:
            title = article.get("title")
            link = article.get("url")
            if title and link:
                st.write("Title:", title)
                st.write("Link:", link)
                st.write()
        if not articles:
            st.write("No recent news for " + selected_holding)

    if selected_holding == "J.H. Whitney VI, L.P.":

        url = ('https://newsapi.org/v2/everything?'
           'q='+selected_holding+'&'
           'from='+str(past_year_date)+'&'
           'sortBy=relevancy&'
           'apiKey=170eef92d9874eeab6605ba11b12cf1d')
        
        response = requests.get(url)
        data = response.json()

        articles = data.get("articles", [])
        for article in articles:
            title = article.get("title")
            link = article.get("url")
            if title and link:
                st.write("Title:", title)
                st.write("Link:", link)
                st.write()
        if not articles:
            st.write("No recent news for " + selected_holding)

