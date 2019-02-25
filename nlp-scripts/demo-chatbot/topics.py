#######################################
#   Counter with bag-of-words

# Import Counter
from collections import Counter

# tokenize the article
tokens = word_tokenize(article)

# convert into lowercase: lower_tokens
lower_tokens = [t.lower() for t in tokens]

# create counter
bow_simple = Counter(lower_tokens)

# most common
print(bow_simple.most_common(10))

#######################################
#   Text preprocessing

from nltk.stem import WordNetLemmatizer

# retain alphabetic words
alpha_only = [t for t in lower_tokens if t.isalpha()]

# remove all stop words
no_stops = [t for t in alpha_only if t not in english_stops]

# instantiate WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()

# lemmatize all tokens
lemmatized = [wordnet_lemmatizer.lemmatize(t) for t in no_stops]

# create the bag-of-words
bow = Counter(lemmatized)

# most common tokens
print(bow.most_common(10))

#######################################
#   Creating and querying a corpus with gensim

from gensim.corpora.dictionary import Dictionary

# create dictionary from articles
dictionary = Dictionary(articles)

# select the id for "computer"
computer_id = dictionary.token2id.get("computerv")

# computer_id to print
print(dictionary.get(computer_id))

# create a MmCorpus: corpus
corpus = [dictionary.doc2bow(article) for article in articles]

# irst 10 word ids with frequency counts from fifth document
print(corpus[4][:10])

#######################################
#   Gensim bag-of-words

# save fifth document
doc = corpus[4]

# Sort the doc for frequency
bow_doc = sorted(doc, key=lambda w: w[1], reverse=True)

# top 5 words of the document 
for word_id, word_count in bow_doc[:5]:
    print(dictionary.get(word_id), word_count)
    
# create defaultdict: total_word_count
total_word_count = defaultdict(int)
for word_id, word_count in itertools.chain.from_iterable(corpus):
    total_word_count[word_id] += word_count

# create a sorted list from the defaultdict
sorted_word_count = sorted(total_word_count.items(), key=lambda w: w[1], reverse=True) 

# top 5 words across all documents 
for word_id, word_count in sorted_word_count[:5]:
    print(dictionary.get(word_id), word_count)

#######################################
## Tf-iDf with Wikipedia

from gensim.models.tfidfmodel import TfidfModel

# new TfidfModel using corpus
tfidf = TfidfModel(corpus)

# calculate tfidf weights of doc
tfidf_weights = tfidf[doc]

# first five weights
print(tfidf_weights[:5])

# sort weights
sorted_tfidf_weights = sorted(tfidf_weights, key=lambda w: w[1], reverse=True)

# top 5 weighted words
for term_id, weight in sorted_tfidf_weights[:5]:
    print(dictionary.get(term_id), weight)