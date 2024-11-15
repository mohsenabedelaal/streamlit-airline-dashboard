import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud , STOPWORDS
import matplotlib.pyplot as plt

st.title("Sentiment Analysis of Tweets about US Airlines")
st.sidebar.title("Sentiment Analysis of Tweets about US Airlines")

st.markdown("This application is a Streamlit dashboard to analyze the sentiment of Tweets 🐦")
st.sidebar.markdown("This application is a Streamlit dashboard to analyze the sentiment of Tweets 🐦")


DATA_URL = ("./Tweets.csv")

@st.cache_data
def load_data():
    data = pd.read_csv(DATA_URL)
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data

data = load_data()


st.sidebar.subheader("Show random tweet")
random_tweet = st.sidebar.radio('Sentiment',('positive','neutral','negative'))
st.sidebar.markdown(data.query("airline_sentiment == @random_tweet")[['text']].sample(n=1).iat[0,0])


st.sidebar.markdown("### Number of tweets by sentiment")
select = st.sidebar.selectbox('Visualization Type',["Histogram","Pie Chart"],key='1')

sentiment_count = data['airline_sentiment'].value_counts()

sentiment_count = pd.DataFrame({"Sentiment":sentiment_count.index,'Tweets':sentiment_count.values})


if not st.sidebar.checkbox("Hide",True):
    st.markdown("### Number of tweets by sentiment")
    if select == "Histogram":
        histogram_fig = px.bar(sentiment_count,x="Sentiment",y="Tweets",color="Tweets",height=500)
        st.plotly_chart(histogram_fig)
    if select == "Pie Chart":
        pie_chart_fig = px.pie(sentiment_count,values='Tweets',names='Sentiment')
        st.plotly_chart(pie_chart_fig)


# st.map(data)
st.sidebar.subheader("When and Where are users tweeting from ?")
hour = st.sidebar.slider("Hour of day ",0,23)
# hour = st.sidebar.number_input("Hour of day ",min_value=0,max_value=23)
modify_data_depending_on_time = data[data['tweet_created'].dt.hour == hour]

if not st.sidebar.checkbox("Close",True,key=2):
    st.markdown("### Tweets Location based on the time of day")
    st.markdown("%i tweets between %i:00 and %i:00" % (len(modify_data_depending_on_time),hour,(hour+1)%24))
    st.map(modify_data_depending_on_time)
    if st.sidebar.checkbox("Show raw data",False):
        st.write(modify_data_depending_on_time)


st.sidebar.subheader("Breakdown airline tweets by sentiment")
choice_airlines = st.sidebar.multiselect('Pick airlines',('US Airways','United','American','Southwest','Delta','Virgin America'),key='3')

if len(choice_airlines) > 0:
    choice_airline_data = data[data['airline'].isin(choice_airlines)]
    airline_histogram_fig = px.histogram(choice_airline_data,x='airline',y='airline_sentiment',histfunc='count',color='airline_sentiment',
                                         facet_col='airline_sentiment',labels={'airline_sentiment':'tweets'},
                                         height=600,width=800)
    st.plotly_chart(airline_histogram_fig)



st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio('Display word cloud for what sentiment ?',('positive','neutral','negative'))

if not st.sidebar.checkbox("Hide Word Cloud",True):
    st.header("Word Cloud for %s sentiment" % (word_sentiment))
    df = data[data['airline_sentiment'] == word_sentiment]
    words = ' '.join(df['text'])
    processed_word = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith("@") and word != 'RT'])
    wordcloud = WordCloud(stopwords=STOPWORDS,background_color="white",height=640,width=800).generate(processed_word)
    wordcloud_fig = plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()