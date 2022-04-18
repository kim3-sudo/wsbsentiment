import pandas as pd
import numpy as np
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
import nltk
from nltk.tokenize import word_tokenize
import pickle
from nltk import classify
from nltk import NaiveBayesClassifier
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from gensim.models.phrases import Phrases
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

import flask

class wsbsentiment:
    def __init__(self, wsb = None):
        self.wsb = pd.read_csv("./wsbsentiment.csv", names = ['title', 'text', 'sentiment'], encoding = "utf-8", encoding_errors = 'ignore')
    
    def wsblingo(data):
        """
        Get the sentiment of a r/wallstreetbets text.
        """
        sentiment = None
        try:
            classobj = wsbsentiment()
            sentiment = wsbsentiment.wsbclassify(classobj, data = data)
            return sentiment
        except Exception as e:
            return str("something went wrong. error: " + str(e) + ". got: " + str(data) + ". did you set your working directory to the root of the wsbsentiment directory when you started tendiebot? you might still be in your home directory or inside of the `flask` directory...")

    def wsbclassify(self, data = ''):
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
        wsblist = self.wsb.drop(columns = ['text'])
        wsbtext = self.wsb.dropna(subset = ['text'])
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
        
    def wsbgenerate(self):
        """
        Generate a r/wallstreetbets post text

        Parameters
        ----------
        None

        Returns
        -------
        str: a post or an error message

        """
        try:
            wsbstrlist = []
            for index, row in wsb.iterrows():
                wsbstrlist.append(str(row['title']))
                wsbstrlist.append(str(row['text']))
            # Split documents into tokens
            tokenizer = RegexpTokenizer(r"[A-Za-z0-9']+\b")
            for index in range(len(wsbstrlist)):
                wsbstrlist[index] = str(wsbstrlist[index]).lower()
                wsbstrlist[index] = tokenizer.tokenize(wsbstrlist[index])
            # Remove words that are only one character
            wsbstrlist = [[token for token in post if len(token) > 1] for post in wsbstrlist]
            # Remove nans
            wsbstrlist = [[token for token in post if token != 'nan'] for post in wsbstrlist]
            lemmatizer = WordNetLemmatizer()
            wsbstrlist = [[lemmatizer.lemmatize(token) for token in post] for post in wsbstrlist]
            while [] in wsbstrlist:
                wsbstrlist.remove([])
            ngram = Phrases(wsbstrlist, min_count = 20)
            for index in range(len(wsbstrlist)):
                for token in ngram[wsbstrlist[index]]:
                    if '_' in token:
                        wsbstrlist[index].append(token)
            wsbstrlist = [item for subitem in wsbstrlist for item in subitem]
            chars = sorted(list(set(wsbstrlist)))
            char_to_num = dict((c, i) for i, c in enumerate(chars))
            seq_length = 100
            x_data = []
            y_data = []
            input_len = len(wsbstrlist)
            vocab_len = len(chars)
            for i in range(0, input_len - seq_length, 1):
                # Define input and output sequences
                # Input is the current character plus desired sequence length
                in_seq = wsbstrlist[i:i + seq_length]

                # Out sequence is the initial character plus total sequence length
                out_seq = wsbstrlist[i + seq_length]

                # We now convert list of characters to integers based on
                # previously and add the values to our lists
                x_data.append([char_to_num[char] for char in in_seq])
                y_data.append(char_to_num[out_seq])
            n_patterns = len(x_data)
            X = np.reshape(x_data, (n_patterns, seq_length, 1))
            X = X/float(vocab_len)
            y = np_utils.to_categorical(y_data)
            model = Sequential()
            model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
            model.add(Dropout(0.2))
            model.add(LSTM(256, return_sequences=True))
            model.add(Dropout(0.2))
            model.add(LSTM(128))
            model.add(Dropout(0.2))
            model.add(Dense(38, activation='softmax')) #y.shape[1]
            filename = "model_weights_saved.hdf5"
            model.load_weights(filename)
            model.compile(loss='categorical_crossentropy', optimizer='adam')
            num_to_char = dict((i, c) for i, c in enumerate(chars))
            start = np.random.randint(0, len(x_data) - 1)
            pattern = x_data[start]
            resultstr = []
            for i in range(1000):
                x = np.reshape(pattern, (1, len(pattern), 1))
                x = x / float(vocab_len)
                prediction = model.predict(x, verbose=0)
                index = np.argmax(prediction)
                result = num_to_char[index]

                resultstr += result

                pattern.append(index)
                pattern = pattern[1:len(pattern)]
        except Exception as e:
            return str("something went wrong. error: " + str(e) + ". did you set your working directory to the root of the wsbsentiment directory when you started tendiebot? you might still be in your home directory or inside of the `flask` directory. also check whether you have the `.hdf5` weights file downloaded...")

    def wsbgetadvice():
        """
        Generate a r/wallstreetbets post with positive sentiment.

        Parameters
        ----------
        None

        Returns
        -------
        str: a post text with positive sentiment
        """
        classobj = wsbsentiment()
        generated = wsbsentiment.wsbgenerate(classobj)
        sentiment = wsbsentiment.wsbclassify(classobj, data = generated)
        while sentiment == 'negative':
            generated = wsbsentiment.wsbgenerate(classobj)
            sentiment = wsbsentiment.wsbclassify(classobj, data = generated)
        return generated