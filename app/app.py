from flask import Flask, render_template, jsonify
from flask import *
import json
from flask_cors import CORS
import sounddevice
import speech_recognition as sr
from werkzeug.exceptions import HTTPException
from spellchecker import SpellChecker
from langdetect import detect

import sys
sys.path.append("../nlpModel/")
sys.path.append("../pathfinding/")

from train.v1.nlp_Test_1 import extract_trip_info
from pathfinder import PathFinder


recognizer = sr.Recognizer()
# french = SpellChecker(language='fr')

app = Flask(__name__)
CORS(app)


"""
Catch Erreur Exception
"""


@app.errorhandler(Exception)
def handle_exception(e):
    # gerer erreur exception with cors
    if isinstance(e, HTTPException):
        response = e.get_response()
        response.status_code = e.code
        response.data = jsonify(error=str(e))
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response
    # other exception
    response = jsonify(error=str(e))
    response.status_code = 400
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


""" 
Correcteur orthographe en francais
"""


def correct_spelling(text):
    # dict fr
    spell = SpellChecker(language="fr")
    words = text.split()
    # corriger orthopgraphe
    corrected_text = []
    for word in words:
        corrected_word = spell.correction(word)
        corrected_text.append(corrected_word)
    # concatene phrase corrigé
    corrected_text = " ".join(corrected_text)
    return corrected_text


"""
Detect language etranger
"""


def is_not_french(text):
    detected_language = detect(text)
    print("LANGUE DETECT : ", detected_language)
    return detected_language != "fr"


"""
Homepage
"""


@app.route("/")
def home():
    return render_template("home.html")


"""
Cette route permettra de traiter la recherche par text
"""


@app.route("/searchText", methods=["GET", "POST"])
def search_txt():
    data = request.get_json()
    if request.method == "POST":
        if data and "trajet" in data:
            userText = request.get_json().get("trajet").strip()
            print(userText)
            # verif is not french
            if is_not_french(userText):
                print("NOT FRENCH")
                return jsonify(data={"error": "Veuillez écrire votre demande en francais."}), 400
            # test correcteur d'orthographe
            # corrected_text = correct_spelling(userText)
            # print("Phrase corigé: ", corrected_text)
            print("NOT FRENCH")
            
            # si ok envoi au nlp
            response = process_nlp(userText)
            return response
            
            # return jsonify({"data": userText})
        else:
            return (
                jsonify(error="la clé 'trajet' est manquante dans les données JSON"),
                400,
            )
    else:
        return jsonify(error="Request de type POST attendu"), 400


"""
Cette route permettra de traiter la recherche par voix
"""


@app.route("/voiceRecognize", methods=["GET", "POST"])
def search_voice_recognize():
    text = ""
    print(request.get_json())
    if request.method == "POST":
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                print("Debut de l'audio...")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio, language="fr-FR", key=None)
            # verif is not french
            if is_not_french(text):
                print("NOT FRENCH")
                return jsonify(error="Veuillez écrire votre demande en francais."), 400
            # call le process NLP
            print("Text reconnu : " + text.strip())
            # return jsonify(data=text.strip()), 200
            response = process_nlp(text.strip())
            return response
            # return jsonify({"data": process_nlp(text.strip())}), 200 
        except sr.WaitTimeoutError:
            # Gérer l'erreur "listening timed out while waiting for phrase to start" ici
            return (
                jsonify(error="Le délai d'écoute a expiré. Veuillez recommencer."),
                400,
            )
        except sr.UnknownValueError:
            return (
                jsonify(
                    error="Impossible de reconnaître la parole en français. Veuillez recommencer."
                ),
                400,
            )
        except Exception as e:
            return jsonify(error="Une erreur s'est produite : " + str(e)), 500


"""
Cette route permettra de traiter la recherche par file voix
"""


@app.route("/voiceRecognizeFile", methods=["GET", "POST"])
def search_voice_recognize_file():

    if "file" in request.files:

        file = request.files["file"]
        # return jsonify(error = "Erreur inattendue: "), 400

        if file.filename == "":
            return json.dumps({"error": "Le fichier envoyé est invalide."})
        # verifier si c est un fichier supporté. FORMAT : [.waw, .aif, .aiff, .aifc]
        if not file.filename.endswith((".wav", ".aif", ".aiff", ".aifc")):
            return (
                (
                    jsonify(
                        error="Le fichier audio doit etre au format .wav, .aif, .aiff ou .flac."
                    ),
                    400,
                ),
            )
        recognizer = sr.Recognizer()

        # audio object
        audio = sr.AudioFile(file)
        # read audio object and transcribe
        try:
            with audio as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.record(source)
            result = recognizer.recognize_google(audio, language="fr-FR", key=None)
            # verif is not french
            if is_not_french(result):
                return jsonify(error="Veuillez écrire votre demande en francais."), 400
            # process_nlp
            response = process_nlp(result)
            # response["phrase"].append(result)
            
            return response
            # return jsonify({"data": process_nlp(result)}), 200 
        except sr.UnknownValueError:
            raise ValueError(
                "Impossible de reconnaître la parole en français, veuillez recommencer !"
            )
        except sr.RequestError as e:
            return jsonify(error=str(e)), 400
        except ValueError as e:
            return jsonify(error=str(e)), 400

        except Exception as e:
            return jsonify(error="Erreur inattendue: " + str(e)), 400
    else:
        return jsonify(error="Aucun fichier reçu"), 400


def process_nlp(sentence):

    print("PROCESS NLP EN COURS")
    print(sentence)
    try:
        # call function nlp extract_trip_info
        nlp_result = extract_trip_info(sentence)
        
        if "NOT_FRENCH" in nlp_result:
            print("ERRRROOOOOR")
            return jsonify(error="Veuillez écrire votre demande en francais.")
        
        if "NOT_TRIP" in nlp_result:
            print("ERRRROOOOOR")
            return jsonify(data={"error":"Impossible de détecter les informations de votre trajet. Veuillez recommencer."}),400
        #  check if departure and arrivals
        if len(nlp_result) != 2 or len(set(nlp_result)) != 2:
            print("ERRRROOOOOR")
            return jsonify(data={"error":"Nous ne parvenons pas a traiter votre demande. Veuillez reformuler."}),400
        
        # si ok call pathfinding
        print("PROCESS PATHFINDING EN COURS")
        print(nlp_result)

        # return shortest paths
        return process_pathfinding(nlp_result, sentence)
   
    
    except Exception as e:
        return jsonify(error=str(e))

    
    
    

def process_pathfinding(array_villes, sentence):
    try:

        print("START generate_graph")
        
        PathFinder.generate_graph()
        print("START generate_station_city_csv")
        
        PathFinder.generate_station_city_csv()
        print("START shortest_paths")
        
        shortest_paths = PathFinder.get_shortest_path_between_cities(array_villes)
        
        formatted_response = PathFinder.format_response_nlp(shortest_paths)
        formatted_response["phrase"] = sentence
        
        print(formatted_response)
        # if 'error' in formatted_response:
        #     status_code = 400
        # else:
        #     status_code = 200
            
        # print("STATUS CODE === ", status_code)
        # if formatted_response.
        return jsonify({"data": formatted_response}), 400 
    except Exception as e:
        print(str(e))
        return jsonify(error=str(e))


# if __name__ == "__main__":
#     app.run(debug=True, port=5002)
