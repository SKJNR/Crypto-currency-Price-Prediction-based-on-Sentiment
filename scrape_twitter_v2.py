from datetime import datetime, timedelta
import requests
import json
import pandas as pd
import nltk
nltk.download("vader_lexicon", "nltk_data")
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sid = SentimentIntensityAnalyzer()

# Get datetime for now and 7 days ago, correctly formatted for Twitter API
dtformat = '%Y-%m-%dT%H:%M:%SZ'

# time = datetime.now() gives you the local time whereas time = datetime.utcnow()
# gives the local time in UTC. Hence now() may be ahead or behind which gives the
# error

time = datetime.utcnow()
start_time = time - timedelta(hours=1)

# Subtracting 15 seconds because api needs end_time must be a minimum of 10
# seconds prior to the request time
end_time = time - timedelta(seconds=15)

# convert to strings
start_time, end_time = start_time.strftime(
    dtformat),  end_time.strftime(dtformat)

# Function to get sentiment of a text


def get_sentiment(text):
    d = sid.polarity_scores(text)

    # Method 1:
    d.pop('compound')
    return d["pos"], d["neg"], d["neu"], max(d, key=d.get)


def get_seniment_of_tweets(df):
  df['pos_score'], df['neg_score'], df['neu_score'], df['sentiment'] = zip(
      *df['text'].map(get_sentiment))

  return df


def scrape_tweets(coin):
  _query = coin
  max_results = str(100)

  url = "https://api.twitter.com/2/tweets/search/recent?query=" + _query + "&start_time=" + start_time + \
      "&end_time=" + end_time + "&max_results=" + \
      max_results + "&tweet.fields=id,text,created_at,lang"
  print(url)

  payload = ""
  headers = {
      'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAP2lawEAAAAA56AM1v9m%2B%2FJHcn1TtnaELFoJB10%3DZ1KKfrINgjvadccGnBcnDaWyeR3z2vG5OYUSZ96FuzXhucQRmN',
      'Cookie': 'guest_id=v1%3A164858392161650785; guest_id_ads=v1%3A164858392161650785; guest_id_marketing=v1%3A164858392161650785; personalization_id="v1_iSN/fsfFJ6mIo42uRQX+uw=="'
  }

  response = requests.request("GET", url, headers=headers, data=payload)
  if response.status_code == 200:
    df = json.loads(response.text)["data"]
    df = pd.DataFrame(df)
    df["created_at"] = pd.to_datetime(df["created_at"])
    df = get_seniment_of_tweets(df)

    return df
  else:
    print("Error: " + str(response.status_code))
