from rasa_nlu.model import Interpreter
import json, os, requests

interpreter = Interpreter.load("./models/current/nlu")

responses = ["Mi spiace non ho trovato risutati", "il risultato è {}"] 

params = {}

def do_convert(params):
    curr_from = params.get("from", "EUR")
    curr_to = params.get("to","BTC")
    curr_am = params.get("amount", "1")

    response = requests.get("https://api.cryptonator.com/api/ticker/{0}-{1}".format(curr_from, curr_to))
    if response.status_code != 200 or "ticker" not in response.json():
        return responses[0], params
    data = response.json()["ticker"]
    #print(data)
    
    amount = str(float(data["price"]) * float(curr_am))
    stringa= "{0} {1}".format(amount, data["target"])
    return responses[1].format(stringa), params

def policy(intent, params):
    if intent == "convert":
        return do_convert(params)
    if intent == "greet":
        return "Salve!", params
    if intent == "thankyou":
        return "Non c'è di che!", params

def respond(message, params):
    processed = interpreter.parse(message)
    print(processed)
    intent = processed["intent"]["name"]
    entities = processed["entities"]
    #print(json.dumps(entities, indent=2))
    for ent in entities:
        params[ent["entity"]] = str(ent["value"])
    policy(intent,params)
    return  policy(intent,params)

for message in ["converti 30 bitcoin in euro", "invece 1000 EUR in BTC", "quanto vale 1 Ethereum in Bitcoin"]:
    response, params = respond(message, params)
    print("USER: {}".format(message))
    print("BOT: {}".format(response))

while True:
    message = input("Input message: ")
    if(message == "q" or message == "exit"):
        break
    print("USER: {}".format(message))
    response, params = respond(message, params)
    print("BOT: {}".format(response))




