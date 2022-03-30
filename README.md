# Fetching tweets

- "scrape_tweets" function from scrape_twitter_v2.py file fetched latest 100 tweets for a particular coin.
- It uses twitter developer V2 recent search API with time window as last 1 hour. So, it fetches 100 recent tweets within last 1 hour.
- I am fetching below tweet fields:
  - id : id of tweet
  - text : text of tweet
  - created_at : The timestamp at which the tweet posted
  - lang : Language of the tweet
- The JSON data returned by twitter API converted to dataframe and "created_at" column converted to datetime format using pandas.
- Then sentiment extracted from "text" field using "Vader lexicon" from NLTK. I used this model since it is used widely and works very well for sentiment analysis.
- "Vader lexicon" gives "positive", "negative" and "neutral" sentiment scores.
- I have added 3 new columns to the twitter df namely pos_score, neg_score and neu_score.
- Whoever has max score out of pos, neg, neu then that becomes the sentiment classification for the tweet and stored as "sentiment" column.

# Fetching Crypto Prices

- I fetched crypto prices information using coincap API. This is a free API.
- I fetched crypto data with frequency of 5 minutes .i.e each price is from every five minutes.
- To get sentiment metric shown at top of the web app:
  - For each of the crypto:
    - Get average pos, neg, neu scores.
    - Now comapre these average scores.
    - If for a crypto the avg. neg score is more than avg. pos score, then the final sentiment for that tweet is "Negative" and it will be suggested to "SELL" this crypto.
    - If for a crypto the avg pos or avg neu is more than the avg neg score, then final sentiment is positive.
    - Now a final sentiment score is calculated, by the formula (avg pos score)/(avg neg score).
    - The higher his score, more positive sentiment, so it is suggested as BUY.
    -
