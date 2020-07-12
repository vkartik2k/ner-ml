#######################################################
#   Written by : Kartik Verma and Shobit Sinha 2020   #
#######################################################

import pandas as pd
import numpy as np
import pickle
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import Perceptron
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
import sklearn_crfsuite
from sklearn_crfsuite import CRF,scorers
from sklearn_crfsuite import metrics
from collections import Counter

############################################################################################
#                        Converting data to features defination                            #
############################################################################################

def word2features(sent, i):
    word = sent[i][0]
    features = {
        'bias': 1.0, 
        'word.lower()': word.lower(), 
        'word[-3:]': word[-3:],
        'word[-2:]': word[-2:],
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),
    }
    if i > 0:
        word1 = sent[i-1][0]
        # postag1 = sent[i-1][1]
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
        })
    else:
        features['BOS'] = True
    if i < len(sent)-1:
        word1 = sent[i+1][0]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
        })
    else:
        features['EOS'] = True
    return features

def word2features2(sent, i):
    word = sent[i][0]
    features = {
        'bias': 1.0, 
        'word.lower()': word.lower(), 
        'word[-3:]': word[-3:],
        'word[-2:]': word[-2:],
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),
    }
    if i > 0:
        word1 = sent[i-1][0]
        # postag1 = sent[i-1][1]
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
        })
    else:
        features['BOS'] = True
    if i < len(sent)-1:
        word1 = sent[i+1][0]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
        })
    else:
        features['EOS'] = True
    return [features]

def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]
def sent2labels(sent):
    return [label for token, postag, label in sent]
def sent2tokens(sent):
    return [token for token, postag, label in sent]


def sent2labels2(sent):
    return [xe[1] for xe in sent]

############################################################################################
#                                    Loading main_dataset                                  #
############################################################################################

df = pd.read_csv('Dataset/main_dataset.csv', encoding = "ISO-8859-1")
df = df[:100000]
df.head()
df.isnull().sum()
df = df.fillna(method='ffill')

df['Sentence #'].nunique(), df.Word.nunique(), df.Tag.nunique()
df1=df.groupby('Tag').size().reset_index(name='counts')

class SentenceGetter(object):
    def __init__(self, data):
        self.n_sent = 1
        self.data = data
        self.empty = False
        agg_func = lambda s: [(w, p, t) for w, p, t in zip(s['Word'].values.tolist(), 
                                                           s['POS'].values.tolist(), 
                                                           s['Tag'].values.tolist())]
        self.grouped = self.data.groupby('Sentence #').apply(agg_func)
        self.sentences = [s for s in self.grouped]

    def get_next(self):
        try: 
            s = self.grouped['Sentence: {}'.format(self.n_sent)]
            self.n_sent += 1
            return s 
        except:
            return None

getter = SentenceGetter(df)
sentences = getter.sentences

X1 = [sent2features(s) for s in sentences]
Y1 = [sent2labels(s) for s in sentences]

print("Status : main_dataset loaded successfully!")

############################################################################################
#                                    Loading covid_dataset                                 #
############################################################################################

list1 = []

f = open("Dataset/shuffled.csv", "r")
curr = []
for x in f:
    if "Sentence #" in x:
        if curr != [] :
            list1.append(curr)
        curr = []
    else :
        # x = x[0:len(x)-1]
        y = x.strip('\n').split(',')
        curr.append(y)

X2 = [sent2features(s) for s in list1]
Y2 = [sent2labels2(s) for s in list1]

print("Status : Annotated Data loaded successfully!")


############################################################################################
#                                 Defining and training Model                              #
############################################################################################

crf = sklearn_crfsuite.CRF(
    algorithm='lbfgs',
    c1=0.1,
    c2=0.1,
    max_iterations=250,
    all_possible_transitions=True
)

X_train2, X_test2, Y_train2, Y_test2 = train_test_split(X2, Y2, test_size=0.3, random_state=0)

X_train = X1 + X_train2
Y_train = Y1 + Y_train2
X_test = X_test2
Y_test = Y_test2

print("Status : Training and Testing Data ready!")
print("Size of training data " , len(X_train))
print("Size of testing data " , len(X_test))

crf.fit(X_train, Y_train)

pickle.dump(crf, open('model/crfmodel.sav', 'wb'))

print("Status : Training Successful!")

Y_pred = crf.predict(X_test)
print(metrics.flat_classification_report(Y_test, Y_pred, labels = None))