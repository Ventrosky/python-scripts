#######################################
#Pre-built Named Entity Recognition
import spacy

nlp = spacy.load('en')
doc = nlp("my friend Mary has worked at Google since 2009") 
for ent in doc.ents:
    print(ent.text, ent.label_) 

#roles    
pattern_1 = re.compile('.* from (.*) to (.*)') 
pattern_2 = re.compile('.* to (.*) from (.*)')

#dependency parsing
doc = nlp('a flight to Shanghai from Singapore') 
shanghai, singapore = doc[3], doc[5] 
list(shanghai.ancestors)
list(singapore.ancestors) 

#shopping example
doc = nlp("let's see that jacket in red and some blue jeans")
items = [doc[4], doc[10]]  # [jacket, jeans] 
colors = [doc[6], doc[9]]  # [red, blue] 
for color in colors:
    for tok in color.ancestors:
        if tok in items:
            print("color {} belongs to item {}".format(color, tok))
            break

#######################################
# Define included entities
include_entities = ['DATE', 'ORG', 'PERSON']

# Define extract_entities()
def extract_entities(message):
    # Create a dict to hold the entities
    ents = dict.fromkeys(include_entities)
    # Create a spacy document
    doc = nlp(message)
    for ent in doc.ents:
        if ent.label_ in include_entities:
            # Save interesting entities
            ents[ent.label_] = ent.text
    return ents

print(extract_entities('friends called Mary who have worked at Google since 2010'))
print(extract_entities('people who graduated from MIT in 1999'))

#######################################
# Create the document
doc = nlp("let's see that jacket in red and some blue jeans")

# Iterate over parents in parse tree until an item entity is found
def find_parent_item(word):
    # Iterate over the word's ancestors
    for parent in word.ancestors:
        # Check for an \"item\" entity
        if entity_type(parent) == "item":
            return parent.text
    return None

# For all color entities, find their parent item
def assign_colors(doc):
    # Iterate over the document
    for word in doc:
        # Check for "color" entities
        if entity_type(word) == "color":
            # Find the parent
            item = find_parent_item(word)
            print("item: {0} has color : {1}".format(item, word))

# Assign the colors
assign_colors(doc)