#######################################
#   NER with NLTK

# Tokenize into sentences
sentences = nltk.sent_tokenize(article)

# Tokenize into words
token_sentences = [nltk.word_tokenize(sent) for sent in sentences]

# parts of speech
pos_sentences = [nltk.pos_tag(sent) for sent in token_sentences] 

# named entity chunks
chunked_sentences = nltk.ne_chunk_sents(pos_sentences, binary=True)

# stems of the tree with 'NE' tags
for sent in chunked_sentences:
    for chunk in sent:
        if hasattr(chunk, "label") and chunk.label() == "NE":
            print(chunk)

#######################################
#   Charting practice

# defaultdict
ner_categories = defaultdict(int)

# nested for loop
for sent in chunked_sentences:
    for chunk in sent:
        if hasattr(chunk, 'label'):
            ner_categories[chunk.label()] += 1
            
# list from dictionary for the chart labels
labels = list(ner_categories.keys())

# list of values
values = [ner_categories.get(l) for l in labels]

# pie chart
plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
plt.show()

#######################################
#   Comparing NLTK with spaCy NER

import spacy

# English model
nlp = spacy.load('en', tagger=False, parser=False, matcher=False)

# new document
doc = nlp(article)

# found entities and labels
for ent in doc.ents:
    print(ent.label_, ent.text)

#######################################
#   French NER with polyglot I

# Polyglot's Text class
txt = Text(article)

# entities found
for ent in txt.entities:
    print(ent)
    
# type of each
print(type(ent))

#######################################
#French NER with polyglot II

# list of tuples
entities = [(ent.tag, ' '.join(ent)) for ent in txt.entities]
print(entities)

#######################################
#   Spanish NER with polyglot

count = 0

for ent in txt.entities:
    if "Márquez" in ent or "Gabo" in ent:
        count += 1
print(count)

# percentage of entities that refer to "Gabo"
percentage = count * 1.0 / len(txt.entities)
print(percentage)

#######################################
#   NER via ensemble model

# set of spaCy entities text
spacy_ents = {e.text for e in doc.ents} 

# set of intersection between spacy and polyglot entities
ensemble_ents = spacy_ents.intersection(poly_ents)

# common entities
print(ensemble_ents)

# number of entities not included
num_left_out = len(spacy_ents.union(poly_ents)) - len(ensemble_ents)
print(num_left_out)