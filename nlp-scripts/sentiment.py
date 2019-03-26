from rasa_nlu.components import Component
from rasa_nlu import utils
from rasa_nlu.model import Metadata
#import nltk, os
#from nltk.sentiment.vader import SentimentIntensityAnalyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

# pipeline name: "sentiment.sentiment_analyzer"
# should be added to component_classes in registry.py

class SentimentAnalyzer(Component):
    """A pre-trained sentiment component"""
    name = "sentiment.sentiment_analyzer"
    provides = ["entities"]
    requires = []
    defaults = {}
    language_list = ["en", "it"]

    def __init__(self, component_config=None):
        super(SentimentAnalyzer, self).__init__(component_config)

    def train(self, training_data, cfg, **kwargs):
        pass
		
    def convert_to_rasa(self, value, confidence):
        """Convert model output into the Rasa NLU compatible output format."""
        entity = {"value": value,
                  "confidence": confidence,
                  "entity": "sentiment",
                  "extractor": "sentiment_extractor"}
        return entity

    def process(self, message, **kwargs):
        """Retrieve the text message, translate to italian, pass it to the classifier
            and append the prediction results to the message class."""
        ita_message = TextBlob(message.text)
        if(ita_message.detect_language()=="it"):
            ita_message = ita_message.translate(from_lang="it", to='en')
        #ita_message.sentiment
        #ita_message.sentiment.polarity
        sid = SentimentIntensityAnalyzer()
        res = sid.polarity_scores(ita_message)
        key, value = max(res.items(), key=lambda x: x[1])
        entity = self.convert_to_rasa(key, value)
        message.set("entities", [entity], add_to_output=True)

    def persist(self, model_dir):
        pass
