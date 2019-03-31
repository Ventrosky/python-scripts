#######################################
# Rasa data format
from rasa_nlu.converters import load_data
import json

training_data = load_data("./training_data.json") 

print(json.dumps(data.training_examples[22], indent=2)) 
# Out: {  "text": "i'm looking for a place in the north of town",  "intent": "restaurant_search",  "entities": [    {      "start": 31,      "end": 36,      "value": "north",      "entity": "location"    }  ] 

# interpreters
message = "I want to book a flight to London" 
interpreter.parse(message)) 

# Creating a model
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Trainer

config = RasaNLUConfig(cmdline_args={"pipeline": "spacy_sklearn"})
trainer = Trainer(config)
interpreter = trainer.train(training_data)

# Rasa pipelines
spacy_sklearn_pipeline = [  "nlp_spacy",  "ner_crf",  "ner_synonyms",   "intent_featurizer_spacy",  "intent_classifier_sklearn"  ] 
# These two statements are identical:
RasaNLUConfig( cmdline_args={"pipeline": spacy_sklearn_pipeline} ) # RasaNLUConfig( cmdline_args={"pipeline": "spacy_sklearn"} )

# handling typo
pipeline = [ "nlp_spacy", "intent_featurizer_spacy", "intent_featurizer_ngrams", "intent_classifier_sklearn" ]

#######################################
# Import necessary modules
from rasa_nlu.converters import load_data
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Trainer

# Create args dictionary
args = {"pipeline": "spacy_sklearn"}

# Create a configuration and trainer
config = RasaNLUConfig(cmdline_args = args)
trainer = Trainer(config)

# Load the training data
training_data = load_data("./training_data.json")

# Create an interpreter by training the model
interpreter = trainer.train(training_data)

# Try it out
print(interpreter.parse("I'm looking for a Mexican restaurant in the North of town"))

#######################################
# Data-efficient entity recognition

# Import necessary modules
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Trainer

pipeline = [
    "nlp_spacy",
    "tokenizer_spacy",
    "ner_crf"
]

# Create a config that uses this pipeline
config = RasaNLUConfig(cmdline_args = {"pipeline": pipeline})

# Create a trainer that uses this config
trainer = Trainer(config)

# Create an interpreter by training the model
interpreter =  trainer.train(training_data)

# Parse some messages
print(interpreter.parse("show me Chinese food in the centre of town"))
print(interpreter.parse("I want an Indian restaurant in the west"))
print(interpreter.parse("are there any good pizza places in the center?"))