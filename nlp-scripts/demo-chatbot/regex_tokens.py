#######################################
##  re.split() and re.findall()

import re

# match sentence endings
sentence_endings = r"[.?!]"

# split on sentence endings
print(re.split(sentence_endings, my_string))

# find capitalized words
capitalized_words = r"[A-Z]\w+"
print(re.findall(capitalized_words, my_string))

# split on spaces
spaces = r"\s+"
print(re.split(spaces, my_string))

# all digits
digits = r"\d+"
print(re.findall(digits, my_string))

#######################################
#Word tokenization with NLTK

from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

# sentences
sentences = sent_tokenize(scene_one)

# word_tokenize to tokenize
tokenized_sent = word_tokenize(sentences[3])

# set of unique tokens
unique_tokens = set(word_tokenize(scene_one))
print(unique_tokens)

#######################################
#   regex with re.search()

# first occurrence
match = re.search("coconuts", scene_one)
# start and end indexes of match
print(match.start(), match.end())

# search for anything in square brackets
pattern1 = r"\[.*\]"

# first text in square brackets
print(re.search(pattern1, scene_one))

# Findscript notation at the beginning of the fourth sentence
pattern2 = r"[\w\s]+:"
print(re.match(pattern2, sentences[3]))

#######################################
#   Regex, NLTK tokenization

from nltk.tokenize import regexp_tokenize
from nltk.tokenize import TweetTokenizer

# find hashtags
pattern1 = r"#\w+"

# Use on the first tweet
regexp_tokenize(tweets[0], pattern1)

# matches both mentions and hashtags
pattern2 = r"([#|@]\w+)"

# on the last tweet
regexp_tokenize(tweets[-1], pattern2)

# TweetTokenizer to tokenize all tweets
tknzr = TweetTokenizer()
all_tokens = [tknzr.tokenize(t) for t in tweets]
print(all_tokens)

#######################################
#   Non-ascii tokenization

# german_text
all_words = word_tokenize(german_text)
print(all_words)

# tokenize only capital words
capital_words = r"[A-ZÜ]\w+"
print(regexp_tokenize(german_text, capital_words))

# tokenize only emoji
emoji = "['\U0001F300-\U0001F5FF'|'\U0001F600-\U0001F64F'|'\U0001F680-\U0001F6FF'|'\u2600-\u26FF\u2700-\u27BF']"
print(regexp_tokenize(german_text, emoji))

#######################################
#   Charting

# split into lines
lines = holy_grail.split('\n')

# replace all script lines
pattern = "[A-Z]{2,}(\s)?(#\d)?([A-Z]{2,})?:"
lines = [re.sub(pattern, '', l) for l in lines]

# tokenize each line
tokenized_lines = [regexp_tokenize(s, "\w+") for s in lines]

# frequency list of lengths
line_num_words = [len(t_line) for t_line in tokenized_lines]

# plot histogram of line lengths
plt.hist(line_num_words)

# Show the plot
plt.show()