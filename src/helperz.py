from flask import Flask, redirect, url_for, request, render_template
from icecream import ic
import random


def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def process_text(str: str)->str:
    ic(str)
    return str

def append_record(jsonObject):
    new_record = createRandRec()
    jsonObject.append(new_record)
    return jsonObject


# List of words
nouns = ["dog", "cat", "house", "car", "tree", "book", "phone", "computer", "table", "chair"]
verbs = ["runs", "jumps", "eats", "drinks", "writes", "types", "reads", "walks", "runs", "plays"]
adjectives = ["big", "small", "happy", "sad", "old", "new", "long", "short", "fast", "slow"]
adverbs = ["quickly", "slowly", "loudly", "softly", "carefully", "recklessly", "wisely", "foolishly", "cleverly", "stupidly"]
prepositions = ["in", "on", "at", "by", "with", "from", "to", "under", "above", "beside"]

def create_sentence():

    noun = random.choice(nouns)
    verb = random.choice(verbs)
    adjective = random.choice(adjectives)
    adverb = random.choice(adverbs)
    preposition = random.choice(prepositions)

    sentence = f"The {adjective} {noun} {verb} {adverb} {preposition} the {noun}."

    return sentence



def createRandRec():

    userMes = create_sentence()
    aiMes = create_sentence()

    print(userMes)
    print(aiMes)

    message = {
        "user" : userMes,
        "ai" : aiMes 
    }

    return message 