#!/usr/bin/env python
# -*- coding: utf-8 -*-

#######################################
#   word vectors with spaCy
import os, csv

dirname = os.path.dirname(__file__) 
filename = os.path.realpath("{0}/data/atis/atis_intents.csv".format(dirname))

with open(filename, 'r') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    labels = []
    sentences = []
    for row in readCSV:
        label = row[0]
        sentence = row[1]
        labels.append(label)
        sentences.append(sentence)

#######################################
import spacy
import numpy as np

# Load the spacy model: nlp
nlp = spacy.load('en_vectors_web_lg')

# Calculate the length of sentences
n_sentences = len(sentences)

print(n_sentences)

# Calculate the dimensionality of nlp
embedding_dim = nlp.vocab.vectors_length

print(embedding_dim)

# Initialize the array with zeros: X
X = np.zeros((n_sentences, embedding_dim))

# Iterate over the sentences
for idx, sentence in enumerate(sentences):
    # Pass each each sentence to the nlp object to create a document
    doc = nlp(sentence)
    # Save the document's .vector attribute to the corresponding row in X
    X[idx, :] = doc.vector

