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

    nlp = spacy.load('model/model_sur_entrainer')
    doc = nlp(text)
    
    trip_info = {"DEPART": None, "ARRIVER": None}

    for ent in doc.ents:
        if ent.label_ in trip_info:
            trip_info[ent.label_] = ent.text  

    if trip_info["DEPART"] and trip_info["ARRIVER"]:
        if trip_info["DEPART"].lower() == trip_info["ARRIVER"].lower():
            return "identique"
        return trip_info
    else:
        return "NO TRIP"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py 'Votre texte ici'")
        sys.exit(1)

    text = " ".join(sys.argv[1:])
    
    if detect_language(text):
        print("Le texte est en français.")
        trip_result = analyze_text(text)
        if trip_result != "NO TRIP" and trip_result != "identique":
            print(f"DEPART: {trip_result['DEPART']}, ARRIVER: {trip_result['ARRIVER']}")
            print(trip_result)
        else:
            if trip_result == "identique":
                print("Vous avez renseigné un départ et une arrivée identique.")
            else:
                print(trip_result)
    else:
        print("Le texte n'est pas en français.")
