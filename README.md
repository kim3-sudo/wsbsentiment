# WSB Sentiment Analysis

Using a nascent dataset collected using the Reddit API, we got a couple hundred posts from [r/wallstreetbets](https://reddit.com/r/wallstreetbets). This particular subreddit proves difficult for existing sentiment analysis models because of the rather unique language used in the subreddit.

The dataset is designed to constantly expand. The easiest way for you to contribute is by either *fixing* `wsbsentiment.csv` or by *running* `wsbsentiment.py` on your own machine (given a Reddit API key) - use the [quick start guide](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example) for the API! When you push your changes up, make sure you push up `wsbsentiment.csv`, which is the dataset that the sentiment analysis model is trained on. You shouldn't be able to go fast enough to time out the Reddit API.
