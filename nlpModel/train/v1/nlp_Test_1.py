# import spacy and fr language

import spacy
from spacy import displacy
from langdetect import detect
import pandas as pd

from unidecode import unidecode

nlp = spacy.load('fr_core_news_lg')

# Liste des mots pour reconnaître la destination en première
destination_keywords = [
    "à",
    "vers",
    "jusqu'à",
    "pour",
    "en direction de",
    "jusqu'à",
    # ... (ajoutez d'autres expressions si nécessaire)
    "atteindre",
    "jusque",
    "à destination de",
    "se rendant à",
    "allant vers",
    "pour se rendre à",
    "jusqu'à la destination",
    "atteignant",
    "arrivant à",
    "aboutissant à",
    "finissant à",
    "se terminant à",
    "débouchant à",
    "parvenant à",
    "se trouvant à",
    "atteignant son terme à",
    "aboutissant à destination à",
    "terminant son voyage à",
    "se concluant à"
] 

# Liste des mots pour reconnaître la departure en première
departure_keywords = [
    "depuis",
    "de",
    "au départ de",
    "en partant de",
    "depuis",
    "au depart de",
    # ... (ajoutez d'autres expressions si nécessaire)
    "au départ",
    "de chez",
    "à partir de",
    "partant de",
    "quittant",
    "partant depuis",
    "partant de",
    "démarrant de",
    "émanant de",
    "sortant de",
    "commençant de",
    "débutant de",
    "en provenance de",
    "en partance de",
    "éloignant de",
    "quittant depuis",
    "sortant depuis",
    "prenant son départ de",
    "débutant sa route de",
    "se mettant en route de",
    "entamant sa route de",
    "amorçant sa route de"
]
# Liste des mots a exclure
exclude_words = [
    "gare",
    "Gare",
]

"""
Build array [départ, arrivé]
"""
def extract_first_departure_and_destination(data):
    first_departure = None
    first_destination = None

    for item in data:
        if 'DEPARTURE' in item:
            first_departure = item['DEPARTURE']
            break

    for item in data:
        if 'DESTINATION' in item:
            first_destination = item['DESTINATION']
            break

    return [first_departure, first_destination]

# remove accents symbols
def remove_accents_and_symbols(text):
    clean_text = unidecode(text)
    return clean_text

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
    clean_destination_keywords = [remove_accents_and_symbols(keyword) for keyword in destination_keywords]
    
    clean_departure_keywords = [remove_accents_and_symbols(keyword) for keyword in departure_keywords]
    
    for i, token in enumerate(doc):
        if token.text in destination_keywords or token.text in clean_destination_keywords and i > 0:
            destination = doc[i].text
            # print(destination)
            if doc[i + 1].text in locs:
                # print(doc[i + 1].text)
                result.append({"DESTINATION" : doc[i+1].text})   

    for i, token in enumerate(doc):
        if token.text in departure_keywords or token.text in clean_departure_keywords  and i < len(doc) - 1:
            departure = doc[i].text
            if doc[i + 1].text in locs:
                result.append({"DEPARTURE" : doc[i+1].text})

    return extract_first_departure_and_destination(result)

# print(extract_trip_info("Je voulais aller de marseille a Paris pour"))
 
        