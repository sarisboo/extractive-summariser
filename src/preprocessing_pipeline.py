import numpy as np 
import pandas as pd
import re
import nltk 
nltk.download('punkt')
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
nltk.download('stopwords')
from string import punctuation
from nltk.stem.porter import PorterStemmer

#Read the data
train = pd.read_csv('./data/cleaned/train_cleaned.csv')
train_copy = train.copy()
print(train_copy.head())

# Preprocessing

## Sentence Segmentation
'''
Sentence Segmentation -> Not always segments properly for example Dr. or Mrs., Mr. might be considered end of a sentence 
We use nltk for smarter segmentation on the article column

For the highlights there is a problem because there is a space before full stop column 
Might consider further splitting the column according to simple rules using regex

FUTURE: Be careful with the items with len = 1, they are usually punctuation or empty strings
'''

# Splitting the article  column into sentences -> Mostly acceptable splits in this case
train_copy.article = train_copy.article.apply(lambda x: sent_tokenize(x))

print(train_copy.article.iloc[0])
print(train_copy.highlights.iloc[0])

# Function that custom splits the highlights column when it hasn't been split properly

def highlights_splitter(text):
    sentence_list = re.split(r"\s+\.\s*", text)
    return sentence_list

# Spiltting with custom split
train_copy.highlights = train_copy.highlights.apply(lambda x: highlights_splitter(x))

print(train_copy.highlights.iloc[0])


## Word Tokenization
'''
def tokenize_words(sent_list):
    word_list = []
    for sent in sent_list:
        words = word_tokenize(sent)
        word_list.append(words)
    return word_list
'''
# Tokenizing, removing stop words, punctuation and non-alphabetic characters
def preprocess_corpus(texts):
    mystopwords = set(stopwords.words("english"))
    def remove_stops_digits(tokens):
        return [token.lower() for token in tokens if token not in mystopwords and not token.isdigit() and token not in punctuation]
    return [remove_stops_digits(word_tokenize(text)) for text in texts]

train_copy.highlights = train_copy.highlights.apply(lambda x: preprocess_corpus(x))
print(train_copy.highlights.iloc[0])

'''
Stemming and Lemmatization
Lemmatization -> Gives a more linguistaically correct from than Stemming 
Also, we don't remove tokens or lowercase before doing lemmatization because we have to know the part of speech of the word to get its lemma
Stemming -> Faster than lemmatization
We typically lowercase the text before stemming
'''

def stem_tokens(token_lists):
    stemmer = PorterStemmer()
    def stem_word(tokens):
        return [stemmer.stem(token) for token in tokens]
    return [stem_word(token_list) for token_list in token_lists]

train_copy.highlights = train_copy.highlights.apply(lambda x: stem_tokens(x))
print(train_copy.highlights.iloc[0])