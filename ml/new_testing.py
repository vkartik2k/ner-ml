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
import csv
import re
from conlleval import evaluate


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

list1 = []

f = open("locations_only/shuffled.csv", "r")
curr = []
for x in f:
    if "Sentence #" in x:
        if curr != [] :
            list1.append(curr)
        curr = []
    else :
        # x = x[0:len(x)-1]
        y = x.strip('\n').split(',')
        if y[1]!='':
            curr.append(y)

X2 = [sent2features(s) for s in list1]
Y2 = [sent2labels2(s) for s in list1]


# print(X2)
X_train2, X_test2, Y_train2, Y_test2 = train_test_split(X2, Y2, test_size=0.25, random_state=0)

X_test = X_test2
Y_test = Y_test2


# X_test_encoded = [sent2features(X_test)]
# X_test = [sent2features(s) for s in X_test]

filename='model/crfmodel.sav'
loaded_model = pickle.load(open(filename, 'rb'))
y_pred = loaded_model.predict(X_test)
# print(y_pred) 

print(len(Y_test))
print(len(y_pred))

Y_TEST = []
for i in Y_test:
    Y_TEST += i

Y_PRED = []
for i in y_pred:
    Y_PRED += i

evaluate(Y_TEST, Y_PRED, verbose=True) 
