import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
import pickle
from nltk import NaiveBayesClassifier, classify
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

class wsbsentiment:
    wsb = pd.read_csv("./wsbsentiment.csv", names = ['title', 'text', 'sentiment'], encoding = "utf-8", encoding_errors = 'ignore')
    
    def wsbclassify(data = ''):
        """
        Classify a r/wallstreetbets post as positive or negative.

        Parameters
        ----------
        data : str
        A string to classify as positive or negative

        Returns
        -------
        str: either "positive" or "negative"
        """
        if data == '':
            return "noentry error."
        wsblist = wsbsentiment.wsb.drop(columns = ['text'])
        wsbtext = wsbsentiment.wsb.dropna(subset = ['text'])
        wsbtext = wsbtext.drop(columns = ['title'])
        wsblist = wsblist[wsblist['sentiment'] != 'neutral']
        wsblist = wsblist.values.tolist()
        wsbtext = wsbtext[wsbtext['sentiment'] != 'neutral']
        wsbtext = wsbtext.values.tolist()
        wsblist = wsblist + wsbtext
        all_words = set(word.lower() for post in wsblist for word in word_tokenize(post[0]))
        stopwords = nltk.corpus.stopwords.words('english')
        stopwords.append('\'s')
        stopwords.append('\'d')
        for stopword in stopwords:
            all_words.discard(stopword)
        words = []
        try:
            with open ('./words.pkl', 'rb') as fp:
                words = pickle.load(fp)
        except:
            words = [({word: (word in word_tokenize(post[0])) for word in all_words}, post[1]) for post in wsblist]
            with open ('./words.pkl', 'wb') as fp:
                pickle.dump(words, fp)
        train_data = words[:(round(len(words) * 0.8))]
        test_data = words[(round(len(words) * 0.8)):]
        classifier = NaiveBayesClassifier.train(train_data)
        custom_wsb = str(data)
        custom_tokens = word_tokenize(custom_wsb)
        return classifier.classify(dict([token, True] for token in custom_tokens))

    def wsblingo(data):
        """
        Get the sentiment of a r/wallstreetbets text.
        """
        sentiment = None
        try:
            sentiment = wsbsentiment.wsbclassify(data = data)
            return sentiment
        except Exception as e:
           return str("something went wrong. error: " + str(e) + ". got: " + str(data) + ". did you set your working directory to the root of the wsbsentiment directory when you started tendiebot? you might still be in your home directory or inside of the `flask` directory...")
