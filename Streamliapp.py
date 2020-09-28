import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


st.title("Sentiment analysis of tweets about US airlines")
st.markdown("This application is a streamlit dashboard to analysis the sentiments of tweets ")

st.sidebar.title("Sentiment analysis of tweets about US airlines")
st.sidebar.markdown("This application is a streamlit dashboard to analysis the sentiments of tweets ")

DATA_URL = ("/home/rhyme/Desktop/Project/Tweets.csv")
@st.cache(persist = True)
def load_data():
    data = pd.read_csv(DATA_URL)
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data

data = load_data()
st.sidebar.subheader("SHow Random Tweet")
random_tweet = st.sidebar.radio("Sentiment", ('positive','neutral', 'negative'))

st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[["text"]].sample(n=1).iat[0,0])

#data visualization using plotly

st.sidebar.markdown("### Number of tweets by sentiments")
select = st.sidebar.selectbox("Visualization type", ["Histogram", "Pie Chart"],key = 1)

##Making dataframe for plotting

sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({"Sentiment":sentiment_count.index, "Tweets": sentiment_count.values})

## Functionality of selectbox options

if not st.sidebar.checkbox("Hide", True): ##If user checks the checkbox, none of the option is checked, to hide  plots by default
    st.markdown("### Number of tweets by sentiment")
    if select == "Histogram":
        fig = px.bar(sentiment_count, x = "Sentiment", y = "Tweets", color = "Tweets", height = 500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values = "Tweets", names = "Sentiment")
        st.plotly_chart(fig)


# Plotting map data, need to have longitude and latitude in our data, and no missing values

st.sidebar.subheader("When and where are users twitting from")
hour = st.sidebar.slider("Hour of the day", 0, 23)

modified_data = data[data['tweet_created'].dt.hour ==hour]


if not st.sidebar.checkbox("Close",True, key = '1'): #If check box is not selected, which by default is selected because we have entered True
    st.markdown("### Tweets Location based on the time of day")
    st.markdown("%i tweets between %i:00 and %i:00" %(len(modified_data), hour, (hour+1)%24))
    st.map(modified_data)
    #showing data for selected Hour
    if st.sidebar.checkbox("Show raw data", False): #if checks the box, raw data is showed, by default false, meaning not showing the raw data
        st.write(modified_data)


#Breakdown airline tweets by sentiments
st.sidebar.subheader("Breakdown airline tweets by sentiments")
choice = st.sidebar.multiselect("Pick airlines",("US Airways",'United','American','Southwest', "Delta","Virgin America"),key = '0')
##Functinality of multiselect widget

if len(choice) > 0:
    choice_data = data[data.airline.isin(choice)] #data of selected airlines only
    fig_choice = px.histogram(choice_data, x = 'airline', y = 'airline_sentiment',histfunc = 'count', color = 'airline_sentiment',
    facet_col = 'airline_sentiment', labels = {'airlines_sentiment':'tweets'}, height =600, width = 800)
    st.plotly_chart(fig_choice)

#Word CLoud
st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio("Display word cloud for what sentiment?", ('positive','neutral','negative'))

if not st.sidebar.checkbox("CLose",True, key = '3'):
    st.subheader("Word Cloud for %s sentiment"%(word_sentiment))
    df = data[data['airline_sentiment']==word_sentiment]
    words = ' '.join(df['text'])
    processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word!='RT'])
    wordcloud = WordCloud(stopwords = STOPWORDS, background_color = 'white', height = 640, width = 800).generate(processed_words)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])#Removing xticks and y ticks
    st.pyplot() #showing matplot in streamlit
