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

# sentence = input('Enter sentence for NER : ').split()

sentences = open("Accidents.csv").read().split('\n')

for i in range(len(sentences)):
    sentences[i] = sentences[i].split()
# sentence = input('Enter sentence for NER :').split()

def word2features(sent, i):
    word = sent[i]
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
        word1 = sent[i-1]
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
        })
    else:
        features['BOS'] = True
    if i < len(sent)-1:
        word1 = sent[i+1]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
        })
    else:
        features['EOS'] = True
    return features

def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

# X_test = [sent2features(sentence)]
X_test = [sent2features(s) for s in sentences]

filename='crfmodel.sav'
loaded_model = pickle.load(open(filename, 'rb'))
y_pred = loaded_model.predict(X_test)
print(y_pred) 


col1 = []
col2 = []

for i in sentences:
    for j in i:
        col1.append(j)
for i in y_pred:
    for j in i:
        col2.append(j)

print(len(col1))
print(len(col2))

with open('acc_out.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for i in range(len(col1)) :
        writer.writerow([col1[i], col2[i]])
