import spacy
from langdetect import detect
import sys

def detect_language(text):

    neg = 0
    pos = 0

    try:
        language = detect(text)
        if language == 'fr':   
            return True
    except:
        try:
            test_language = spacy.load('fr_core_news_sm')
            doc = test_language(text)
            for token in doc:
                language = detect(token.text)
                if language == 'fr':
                    pos = pos + 1
                else:
                    neg = neg + 1

            if pos > neg:
                return True   
        except:
            return False

def analyze_text(text):

    nlp = spacy.load('../model/model_sur_entrainer')
    doc = nlp(text)
    
    trip_info = {"DEPART": None, "ARRIVER": None}

    for ent in doc.ents:
        if ent.label_ in trip_info:
            trip_info[ent.label_] = ent.text  

    if trip_info["DEPART"] and trip_info["ARRIVER"]:
        if trip_info["DEPART"].lower() == trip_info["ARRIVER"].lower():
            return "NO_TRIP"
        return trip_info
    else:
        return "NO_TRIP"
    

def start_model_ner(text):
    if detect_language(text):
        trip_result = analyze_text(text)
        if trip_result != "NO_TRIP" and trip_result != "identique":
            return 'OK'
        else:
            return 'NO_TRIP'
    else:
        return 'NO_TRIP'