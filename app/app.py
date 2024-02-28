from flask import Flask, render_template, jsonify
from flask import *
import json
from flask_cors import CORS
import sounddevice
import speech_recognition as sr
from werkzeug.exceptions import HTTPException
from spellchecker import SpellChecker
from langdetect import detect


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
            # verif is not french
            if is_not_french(userText):
                return jsonify(error="Veuillez écrire votre demande en francais."), 400
            # test correcteur d'orthographe
            corrected_text = correct_spelling(userText)
            print("Phrase corigé: ", corrected_text)
            return jsonify({"data": userText})
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
                audio = recognizer.listen(source, timeout=1)
            text = recognizer.recognize_google(audio, language="fr-FR", key=None)
            # verif is not french
            if is_not_french(text):
                return jsonify(error="Veuillez écrire votre demande en francais."), 400
            # call le process NLP
            print("Text reconnu : " + text.strip())
            # return jsonify(data=text.strip()), 200
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
            return jsonify({"data": result})
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
    pass


def process_pathfinding(sentence):
    pass


# if __name__ == "__main__":
#     app.run(debug=True, port=5002)
