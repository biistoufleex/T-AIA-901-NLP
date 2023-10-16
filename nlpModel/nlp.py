# import spacy and fr language

import spacy
from spacy import displacy
from langdetect import detect
import pandas as pd

nlp = spacy.load('fr_core_news_lg')

# Liste des mots pour reconnaître la destination en première
destination_keywords = [
    "à",
    "vers",
    "jusqu'à",
    "pour",
    "en direction de",
    "jusqu'à chez",
    # ... (ajoutez d'autres expressions si nécessaire)
] 

# Liste des mots pour reconnaître la departure en première
departure_keywords = [
    "depuis",
    "de",
    "au départ de",
    "en partant de",
    "depuis",
    "au départ de chez",
    # ... (ajoutez d'autres expressions si nécessaire)
]
# Liste des mots a exclure
exclude_words = [
    "gare",
    "Gare",
]

# Fonction pour détecter la langue de la phrase
def detect_language(text):
    try:
        language = detect(text)
        if language != 'fr':   
            return True  # Vérifie si la langue détectée n'est pas le français
    except:
        return False
    
# Fonction pour extraire les informations pertinentes
def extract_trip_info(text):

    for mot in exclude_words:
        text = text.replace(mot, '')

    doc = nlp(text)

    locs = []
    result = []
    
    is_not_french = detect_language(text)
    if is_not_french:
        locs.append("NOT_FRENCH")
        return locs

    for token in doc:
        if token.ent_type_ == "LOC":
            locs.append(token.text)
    
    if not locs:  # Si la liste est vide
            result.append('NOT_TRIP')
    
    for i, token in enumerate(doc):
        if token.text in destination_keywords and i > 0:
            destination = doc[i].text
            # print(destination)
            if doc[i + 1].text in locs:
                # print(doc[i + 1].text)
                result.append({"DESTINATION" : doc[i+1].text})   

    for i, token in enumerate(doc):
        if token.text in departure_keywords and i < len(doc) - 1:
            departure = doc[i].text
            if doc[i + 1].text in locs:
                result.append({"DEPARTURE" : doc[i+1].text})

    return result

print(extract_trip_info("Je voulais aller de bordeaux a paris"))
 
        