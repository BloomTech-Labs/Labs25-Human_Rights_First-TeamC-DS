from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import nltk
import re
import csv
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer

# %matplotlib inline
pd.set_option('display.max_colwidth', 300)

df = pd.read_csv(
    'https://raw.githubusercontent.com/Lambda-School-Labs/Labs25-Human_Rights_First-TeamC-DS/main/Data/training_data.csv', na_values=False)

df = df.drop(columns=df.columns[0])
df.head()

df['text'] = df['text'].astype(str)
df['tags_str'] = df['tags_str'].astype(str)

# clean the tags_str column


def tags_cleaner(text):
  # remove whitespaces
    text = ' '.join(text.split())
    # convert text to lowercase
    text = text.lower()

    return text


df['tags_new_clean'] = df['tags_str'].apply(lambda x: tags_cleaner(x))

df['tags_new'] = df['tags_new_clean'].apply(lambda x: x.split(', '))
df.tags_new

# now the data is in lists
tags = []

for i in df['tags_str']:
    tags.append(i)

tags = nltk.FreqDist(tags)
tags_df = pd.DataFrame(
    {'Tags': list(tags.keys()), 'Count': list(tags.values())})


g = tags_df.nlargest(columns="Count", n=50)
plt.figure(figsize=(12, 15))
ax = sns.barplot(data=g, x="Count", y="Tags")
ax.set(ylabel='Count')
plt.show()

# function for text cleaning


def clean_text(text):
    # remove backslash-apostrophe
    text = re.sub("\'", "", text)
    # remove everything alphabets
    text = re.sub("[^a-zA-Z]", " ", text)
    # remove whitespaces
    text = ' '.join(text.split())
    # convert text to lowercase
    text = text.lower()

    return text


df['new_text'] = df['text'].apply(lambda x: clean_text(x))
df[['text', 'new_text']].sample(5)


def freq_words(x, terms=30):
    all_words = ' '.join([text for text in x])
    all_words = all_words.split()

    fdist = nltk.FreqDist(all_words)
    words_df = pd.DataFrame(
        {'word': list(fdist.keys()), 'count': list(fdist.values())})

    # selecting top 20 most frequent words
    d = words_df.nlargest(columns="count", n=terms)
    plt.figure(figsize=(12, 15))
    ax = sns.barplot(data=d, x="count", y="word")
    ax.set(ylabel='Word')
    plt.show()


nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

# function to remove stopwords


def remove_stopwords(text):
    no_stopword_text = [w for w in text.split() if not w in stop_words]
    return ' '.join(no_stopword_text)


df['new_text'] = df['new_text'].apply(lambda x: remove_stopwords(x))
freq_words(df['new_text'], 100)


multilabel_binarizer = MultiLabelBinarizer()

multilabel_binarizer.fit(df['tags_new'])
print(multilabel_binarizer.classes_)
# transform target variable
y = multilabel_binarizer.transform(df['tags_new'])
print(y.shape)
