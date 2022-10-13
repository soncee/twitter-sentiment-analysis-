from ast import keyword
from cgi import test
from email.mime import image
from turtle import title
import pandas as pd
import streamlit as st
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import numpy as np
import re
import matplotlib.pyplot as plt
from PIL import Image
from pickle import TRUE
import seaborn as sns


api_key = "WMu8MRl34VKMVxFSSntWxGBuU"
api_secret_key = "JsXbtOw8vPog6C6ENu4MvsXbaJfsOJIGLesFZPv64BDu7VSoER"
access_token = "1543097817975377920-PKftQa0U6aANGsIJNvLaitrF54LWjx"
access_token_secret_key = "riQfrSaQEiNP0CpVNYHRz4Axk6OPn9GdTIRHaAFqco7hC"

auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token,access_token_secret_key)

api = tweepy.API(auth, wait_on_rate_limit= TRUE)


st.title("Sentiment Analysis")
st.subheader("Curious about people's perception about some topics? let's find it out below (english language only)")
raw_text = st.text_area("Enter the keywords that you want to search in twitter")
Analyzer_choice = st.selectbox("Select the Activities",  ["Show Recent Tweets","Generate WordCloud" ,"Visualize the Sentiment Analysis"])
limit = st.slider('tweets counts', 0, 1000, step=1)

if st.button("run"):
    if (Analyzer_choice == "Show Recent Tweets"):
        st.success("Fetching recent Tweets")

        keywords =  api.search_tweets(q=raw_text, count = limit, lang ="en")
        df = pd.DataFrame([tweet.text for tweet in keywords], columns=['Tweets'])
        user = [tweet.user.screen_name for tweet in keywords]
        tweet_time = [tweet.created_at for tweet in keywords]
        loc = [tweet.user.location for tweet in keywords]
        df['username'] = user
        df['tweet time'] = tweet_time
        df['location'] = loc
        for tweet in keywords :
            st.write('from ', tweet.user.screen_name, 'tweets: ', tweet.text, 'tweet date',tweet.created_at)
        st.write(df)
        st.download_button("Download CSV file", df.to_csv(),file_name='tweets.csv',mime='text/csv')

    elif (Analyzer_choice =="Generate WordCloud"):
        st.success("Generating Word Cloud")

        post = api.search_tweets(q =raw_text, count = limit, lang="en")
        df = pd.DataFrame([tweet.text for tweet in post], columns=['Tweets'])
        words = ' '.join([twts for twts in df['Tweets']])
        wc = WordCloud(width=1000, height=500, random_state=21, max_font_size=110).generate(words)
        plt.imshow(wc)
        plt.axis('off')
        st.pyplot()
    else:
        st.success("Analyzing")
        def GetKeywordInfo():
            keywords =  api.search_tweets(q=raw_text, count = limit, lang="en")
            df = pd.DataFrame([tweet.text for tweet in keywords], columns=['Tweets'])

            def cleanTxt(text):
                text = re.sub('@[A-Za-z0–9]+', '', text) 
                text = re.sub('#', '', text) 
                text = re.sub('RT[\s]+', '', text) 
                text = re.sub('https?:\/\/\S+', '', text) 
                return text

            df['Tweets'] = df['Tweets'].apply(cleanTxt)

            def getSubjectivity(text):
                return TextBlob(text).sentiment.subjectivity


            def getPolarity(text):
                return  TextBlob(text).sentiment.polarity


            df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
            df['Polarity'] = df['Tweets'].apply(getPolarity)

            def getAnalysis(score):
                if score < 0:
                    return 'Negative'
                elif score == 0:
                    return 'Neutral'
                else:
                    return 'Positive'
            df['Analysis'] = df['Polarity'].apply(getAnalysis)
            return df
        df = GetKeywordInfo()
        st.write(df)
        st.download_button("Download CSV file", df.to_csv(),file_name='sentiments.csv',mime='text/csv')
        st.subheader("Shows the population")
        Neutral_count = df['Analysis'].value_counts().Neutral
        Positive_count = df['Analysis'].value_counts().Positive
        Negative_count = df['Analysis'].value_counts().Negative
        bar_names = ['Positive','Neutral','Negative']
        label = [Positive_count, Neutral_count,Negative_count]
        color = ['green','blue','red']
        fig = plt.figure(figsize=(6,6))
        ax = plt.axes()
        ax.set_title('Sentiment Percentage')
        ax.pie(label,labels=bar_names,colors=color,autopct='%1.0f%%')
        st.pyplot(fig)



       







    











    
    


    
        


       
      

	



		