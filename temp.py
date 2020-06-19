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

df = pd.read_csv('set.csv', encoding = "ISO-8859-1")
df.head()
df.isnull().sum()
df = df.fillna(method='ffill')

l1 = df.values.tolist()

print(l1)