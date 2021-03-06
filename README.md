# WSB Sentiment Analysis

## About

Using a nascent dataset collected using the Reddit API, we got a couple hundred posts from [r/wallstreetbets](https://reddit.com/r/wallstreetbets). This particular subreddit proves difficult for existing sentiment analysis models because of the rather unique language used in the subreddit.

The dataset is designed to constantly expand. The easiest way for you to contribute is by either *fixing* `wsbsentiment.csv` or by *running* `wsbsentiment.py` on your own machine. To get your Reddit API key:

1. Make a copy of `settings.ini.example` and name it `settings.ini`.
2. In your copy, add your username, password, and an API key and secret. Use the [quick start guide](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example) for the API!
3. Set your working directory to `wsbsentiment`, then run `generatetoken.py`. This will query the Reddit API and get a token, which will be valid for a couple of hours. It'll save this token to a file called `token`, which `wsbsentiment.py` will look for.

When you push your changes up, make sure you push up `wsbsentiment.csv`, which is the dataset that the sentiment analysis model is trained on. You shouldn't be able to go fast enough to time out the Reddit API. If you don't force anything, you shouldn't be able to commit or push your token or anything inside of `settings.ini.example`, but always double-check that you're not committing or updating any files that you didn't expect!

Predicably with any Internet forum, the text in the dataset may contain lewd and/or offensive words. Reader discretion is advised.

## Usage

The simplest way to use this is to use the no-code interface, named *tendiebot*. To start tendiebot, set your working directory to the repository directory on your local machine, then run `app.py`. Then, go to `127.0.0.1:5000` or the address specified in the ephemeral Flask server in your web browser.

```
git clone https://github.com/kim3-sudo/wsbsentiment
cd wsbsentiment
python3 ./flask/app.py
```

Make sure you set your working directory to `wsbsentiment`, not `flask` or your home directory.

If you *want* to do things the hard way, you could also use the Jupyter Notebooks provided. `sentiment_analysis.ipynb` leverages a naive Bayesian classifier to do sentiment analysis. If you add to `wsbsentiment.csv` and want to use the new phrases, delete `words.pkl`. It will be regenerated when you run `sentiment_analysis.ipynb`. The `words.pkl` file stores tokenized words that otherwise take a *very* long time to tokenize. After `words.pkl` is created, the rest of the notebook should run pretty quickly.

`text_generation.ipynb` uses `aitextgen` to generate text based on GPT-2. It's much more memory-efficient than stock GPT-2, but it takes a GPT-2-style tokenizing method. This takes a long time to train (~3 hours on 400 rows of text), so we'd recommend using the model, which is found in `aitextgen.tokenizer.json`. If you want to retrain the model and you get better results, feel free to contribute a new `aitextgen.tokenizer.json` with those changes.

## Hardware Requirements

A GPGPU with CUDA is *required* to run any text generation training, but you should be able to actually generate text with the pretrained model. No GPU requirement exists for the sentiment analysis portion (in fact, it doesn't even support GPU acceleration).

The models have been trained with the following hardware:

- AMD Ryzen 5 3600 @ 3.59GHz
- 64GB DDR4 RAM @ 2133 MT/s
- Nvidia Quadro M6000 with 12GB of VRAM
