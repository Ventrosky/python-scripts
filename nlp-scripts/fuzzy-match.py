from nltk import stem, tokenize
from nltk.metrics import edit_distance

stemmer = stem.PorterStemmer()
 
def normalize(s):
    words = tokenize.wordpunct_tokenize(s.lower().strip())
    return ' '.join([stemmer.stem(w) for w in words])
 
def fuzzy_match(s1, s2, max_dist=3):
    return edit_distance(normalize(s1), normalize(s2)) <= max_dist
