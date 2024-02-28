

import spacy
from spacy import displacy
from spacy.training.example import Example
from spacy.training.example import offsets_to_biluo_tags
from langdetect import detect
from spacy.util import minibatch, compounding
from unidecode import unidecode

# VARIABLE


nlp = spacy.load("fr_core_news_lg")

# Liste des mots pour reconnaître la destination en première
destination_keywords = [
    "à",
    "vers",
    "jusqu'à",
    "pour",
    "en direction de",
    "jusqu'à chez",
] 
# Liste des mots pour reconnaître la departure en première
departure_keywords = [
    "depuis",
    "de",
    "au départ de",
    "en partant de",
    "depuis",
    "au départ de chez",
]
# Liste des mots pour reconnaître les passage
passage_keywords = [
    "passant par",
    "via",
    "par le chemin de",
    "par la route de",
    "par la voie de",
    "en faisant un détour par",
    "par l'intermédiaire de",
    "en incluant",
    "avec un arrêt à",
    "parmi les étapes à",
    "en traversant",
    "en faisant escale à",
    "tout en visitant",
    "parmi les destinations à",
    "et en découvrant",
    "tout en passant par",
    "tout en explorant",
    "avec un passage à",
    "en chemin vers",
    "en voyage vers"
]
# Liste des mots a exclure
exclude_words = [
    "gare",
    "Gare",
]

# Ajout des fonction necessaire au script
# Fonction pour détecter la langue de la phrase
def detect_language(text):
    try:
        language = detect(text)
        if language != 'fr':   
            return True  # Vérifie si la langue détectée n'est pas le français
    except:
        return False

def extract_trip_info(text):

    for mot in exclude_words:
        text = text.replace(mot, '')

    doc = nlp(text)

    locs = []
    result = []
    
    is_not_french = detect_language(text)
    if is_not_french:
        return "NO_TRIP"
 
    for token in doc:
        if token.ent_type_ == "LOC":
            locs.append(token.text)
   
    if not locs:  # Si la liste est vide
            return 'NO_TRIP'

    # Normalisation des mots-clés des destination
    destination_keywords_normalized = [unidecode(keyword) for keyword in destination_keywords]

    # Normalisation des mots-clés des depart
    departure_keywords_normalized = [unidecode(keyword) for keyword in departure_keywords]

   # Normalisation des mots-clés des passage
    passage_keywords_normalized = [unidecode(keyword) for keyword in passage_keywords]


    departure = None
    destination = None
    passage = None
    departure_count = 0
    destination_count = 0
    passage_count = 0


    # FOR permettant de trouver la ville de depart 
    for i, token in enumerate(doc):
        # use unicode for text
        text_unicode = token.text
        if token.text in departure_keywords or text_unicode in departure_keywords or token.text in departure_keywords_normalized or text_unicode in departure_keywords_normalized and i < len(doc) - 1:
            if doc[i + 1].text in locs:
                departure = doc[i+1].text
                destination_count += 1  

    # FOR permettant de trouver la ville de destination   
    for i, token in enumerate(doc):
        # use unicode for text
        text_unicode = unidecode(token.text)
        if token.text in destination_keywords or text_unicode in destination_keywords or token.text in destination_keywords_normalized or text_unicode in destination_keywords_normalized and i > 0:
            if doc[i + 1].text in locs:
                destination = doc[i+1].text
                departure_count += 1  

    # FOR permettant de trouver la ville par la qu'elle on veut passer pour arriver a destination
    for keyword in passage_keywords:
        keyword_words = keyword.split()  
        keyword_length = len(keyword_words)
        for i in range(len(doc) - keyword_length + 1):
            window = [token.text for token in doc[i:i+keyword_length]]
            if window == keyword_words:
                passage_start = i + keyword_length
                passage_end = passage_start + 1
                if doc[passage_start:passage_end].text in locs:
                    passage = doc[passage_start:passage_end].text
                    passage_count += 1 
                    break

    if departure and destination and departure_count == 1 and destination_count == 1 and passage_count == 0 :
        return 'OK'
    elif departure and destination and passage and departure_count == 1 and destination_count == 1 and passage_count == 1:
        return 'OK'
    if (departure_count > 1) or (destination_count > 1):
        return 'NO_TRIP'
        