import streamlit as st
from scrape_twitter_v2 import scrape_tweets
import requests
import pandas as pd
import json
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

from time import time, sleep


st.set_page_config(page_title="Coin price vs twitter sentiment", 
                        page_icon="💲", 
                        layout="wide", 
                        initial_sidebar_state="auto", 
                        menu_items=None)

from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=15 * 60 * 1000, key="dataframerefresh")

def fetch_crypto_price(coin = "dogecoin", interval = "m5"):
    """
    Fetch crypto price from coincap.io
    coin : str
        coin name : one of "dogecoin", "ethereum", "shiba-inu"
    interval : str

    """
    time = datetime.utcnow()
    start_time = time - timedelta(hours=1)
    start_time = datetime_to_epoch(start_time)

    end_time = time - timedelta(seconds=15)
    end_time = datetime_to_epoch(end_time)

    print(start_time, end_time)

    url = "http://api.coincap.io/v2/assets/" + coin + "/history?interval=" + interval #+ "&start=" + str(start_time) + "&end=" + str(end_time)
    payload = ""
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    
    df = pd.DataFrame(json.loads(response.text.encode('utf-8'))["data"])
    df = df[[ "date", "priceUsd"]].copy()
    #df["date"] = pd.to_datetime(df["date"])
    #df.set_index("date", inplace = True)
    #df.sort_index(inplace = True, ascending = True)
    return df

def datetime_to_epoch(d1):

    # create 1,1,1970 in same timezone as d1
    d2 = datetime(1970, 1, 1, tzinfo=d1.tzinfo)
    time_delta = d1 - d2
    ts = int(time_delta.total_seconds())
    return ts

def get_sentiment_metrics(df):
    pos = round(df["pos_score"].mean() * 100, 2)
    neu = round(df["neu_score"].mean() * 100, 2)
    neg = round(df["neg_score"].mean() * 100, 2)

    if neu > pos and neu > neg:
        buy_indicator = "Buy"   
        color = "normal"
    elif pos > neg:
        buy_indicator = "Buy"
        color = "normal"
    else:
        buy_indicator = "Sell"
        color = "inverse"
    return pos, neu, neg, buy_indicator, color


def main(): 
        # set config


    # set title
    st.title("The effect of crypto coin twitter sentiment on coin price.")
    st.text("This app auto updates every 15 minutes. I have taken 15 minutes interval in accordance with twitter api rules.")
    st.markdown(""" --- """)
    ## TODO: Remove read_csv lines.
    # Fetch twitter data and sentiments
    eth_tweets = scrape_tweets("ethereum")
    #eth_tweets = pd.read_csv("eth_tweets.csv")
    doge_tweets = scrape_tweets("dogecoin")
    #doge_tweets = pd.read_csv("doge_tweets.csv")
    shiba_tweets = scrape_tweets("shibainu")
    #shiba_tweets = pd.read_csv("shiba_tweets.csv")

    ## TODO : Remove read_csv lines.
    # Get price data of coins
    eth_price = fetch_crypto_price(coin = "ethereum", interval = "m5")
    #eth_price = pd.read_csv("eth_price.csv")
    doge_price = fetch_crypto_price(coin = "dogecoin", interval = "m5")
    #doge_price = pd.read_csv("doge_price.csv")
    shiba_price = fetch_crypto_price(coin = "shiba-inu", interval = "m5")
    #shiba_price = pd.read_csv("shiba_price.csv")

    # Sentiment metrics
    eth_pos, eth_neu, eth_neg, eth_buy_indicator, eth_color = get_sentiment_metrics(eth_tweets)
    doge_pos, doge_neu, doge_neg, doge_buy_indicator, doge_color = get_sentiment_metrics(doge_tweets)
    shiba_pos, shiba_neu, shiba_neg, shiba_buy_indicator, shiba_color = get_sentiment_metrics(shiba_tweets)

    st.markdown("These metrics shows the final twitter sentiment score for the crypto coins. The final twitter sentiment score calculated as (total_no_of_positive_sentiments/total_no_of_negative_sentiment_tweets.). The positive, negative, neutral twitter sentiment scores are used to determine the buy/sell/hold indicator.")

    col1, col2, col3 = st.columns(3)

    # ------------------ "Ethereum" -------------------------


    col1.metric(label = "Ethereum", 
                value = eth_buy_indicator , 
                delta = str(round((eth_pos / eth_neg), 2)) + "%", 
                delta_color = eth_color)

    col1.markdown(""" --- """)

    # Show price charts
    fig = px.area(eth_price, x="date", y="priceUsd", title="Ethereum price", )
    fig.update_layout(yaxis=dict(showgrid = False), xaxis = dict(showgrid = False))
    col1.plotly_chart(fig, use_container_width=True)

    # Show sentiments
    col1.markdown(""" Ethereum sentiment score plots: """)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=eth_tweets["created_at"], y=eth_tweets["neg_score"],
                    mode='lines+markers',
                    name='negative score'))
    fig.add_trace(go.Scatter(x=eth_tweets["created_at"], y=eth_tweets["neu_score"],
                    mode='lines+markers',
                    name='neutral score'))
    fig.add_trace(go.Scatter(x=eth_tweets["created_at"], y=eth_tweets["pos_score"],
                    mode='lines+markers', name='positive score'))
    fig.update_layout(yaxis=dict(showgrid = False), xaxis = dict(showgrid = False))
    col1.plotly_chart(fig, use_container_width=True, )
    col1.markdown(""" --- """)

    # ------------------ "Dogecoin" -------------------------

    col2.metric(label = "Dogecoin", 
                value = doge_buy_indicator, 
                delta = str(round((doge_pos / doge_neg), 2)) + "%", 
                delta_color = doge_color)
    col2.markdown(""" --- """)

    fig = px.area(doge_price, x="date", y="priceUsd", title="Dogecoin price", )
    fig.update_layout(yaxis=dict(showgrid = False), xaxis = dict(showgrid = False))
    col2.plotly_chart(fig, use_container_width=True)

    col2.markdown(""" Doge sentiment score plots: """)
    # Show sentiments
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=doge_tweets["created_at"], y=doge_tweets["neu_score"],
                    mode='lines+markers',
                    name='neutral score'))
    fig.add_trace(go.Scatter(x=doge_tweets["created_at"], y=doge_tweets["neg_score"],
                    mode='lines+markers',
                    name='negative score'))
    fig.add_trace(go.Scatter(x=doge_tweets["created_at"], y=doge_tweets["pos_score"],
                    mode='lines+markers', name='positive score'))
    fig.update_layout(yaxis=dict(showgrid = False), xaxis = dict(showgrid = False))
    col2.plotly_chart(fig, use_container_width=True)
    col2.markdown(""" --- """)

    # ------------------ "Shiba-Inu" -------------------------
    col3.metric(label = "Shiba-Inu", 
                value = shiba_buy_indicator, 
                delta = str(round((shiba_pos / shiba_neg), 2)) + "%", 
                delta_color = shiba_color)

    col3.markdown(""" --- """)

    fig = px.area(shiba_price, x="date", y="priceUsd", title="Shiba-Inu price", color_discrete_sequence = ["#1f77b4", "#ff7f0e", "#2ca02c"])
    fig.update_layout(yaxis=dict(showgrid = False), xaxis = dict(showgrid = False))
    col3.plotly_chart(fig, use_container_width=True)

    col3.markdown(""" Shiba Inu sentiment score plots: """)
    # Show sentiments
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=shiba_tweets["created_at"], y=shiba_tweets["neu_score"],
                    mode='lines+markers',
                    name='neutral score'))
    fig.add_trace(go.Scatter(x=shiba_tweets["created_at"], y=shiba_tweets["neg_score"],
                    mode='lines+markers',   
                    name='negative score'))
    fig.add_trace(go.Scatter(x=shiba_tweets["created_at"], y=shiba_tweets["pos_score"],
                    mode='lines+markers', name='positive score'))
    fig.update_layout(yaxis=dict(showgrid = False), xaxis = dict(showgrid = False))
    col3.plotly_chart(fig, use_container_width=True)
    col3.markdown(""" --- """)

    # Show raw data
    st.subheader("Ethereum tweets data with sentiment : ")
    st.write(eth_tweets.drop(["lang"], axis = 1))

    st.subheader("Doge tweets data with sentiment : ")
    st.write(doge_tweets.drop(["lang"], axis = 1))

    st.subheader("Shiba tweets data with sentiment : ")
    st.write(shiba_tweets.drop(["lang"], axis = 1))
    




if __name__ == "__main__":
    main()
        
