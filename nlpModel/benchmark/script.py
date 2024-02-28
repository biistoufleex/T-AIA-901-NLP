import spacy
from langdetect import detect
import sys
import time
import matplotlib.pyplot as plt
import random
from collections import Counter
from spacy.training.example import Example
from spacy.scorer import Scorer
from NER import start_model_ner
from CDT import extract_trip_info


input_data = [
"Comment atteindre Rennes depuis marseille",
"Comment atteindre le havre depuis marseille",
"depart le mans arriver le havre",
"Aller de le havre à marseille.",
"Comment aller à marseille depuis le havre ?",
"Comment atteindre marseille depuis le havre ?",
"Comment atteindre marseille en partant de le havre le plus rapidement ?",
"Comment atteindre marseille à partir de le havre ?",
"Comment me rendre de le havre à marseille ?",
"Comment me rendre à marseille depuis le havre ?",
"Comment puis-je aller à marseille en venant de le havre ?",
"Comment puis-je me rendre de le havre à marseille ?",
"Comment puis-je me rendre de le havre à marseille le plus rapidement ?",
"Comment puis-je me rendre à marseille en partant de le havre ?",
"Comment puis-je rejoindre marseille depuis le havre ?",
"Comment puis-je rejoindre marseille à partir de le havre ?",
"De le havre vers marseille.",
"De le havre à marseille.",
"Depuis le havre vers marseille.",
"Dirigez-vous vers marseille en partant de le havre.",
"Il y a-t-il des trains de le havre à marseille ?",
"Il y a-t-il des trains vers marseille depuis le havre ?",
"Indique-moi le chemin depuis le havre jusqu'à marseille.",
"Indique-moi le trajet de le havre à marseille.",
"Indique-moi le trajet le plus simple de le havre vers marseille.",
"Indique-moi le trajet le plus simple depuis le havre vers marseille.",
"J'aimerais aller à marseille en partant de le havre.",
"J'aimerais connaître le chemin pour aller de le havre à marseille.",
"J'aimerais connaître le chemin pour aller à marseille depuis le havre.",
"J'aimerais me rendre de le havre à marseille.",
"Je cherche le chemin pour aller à marseille depuis le havre.",
"Je cherche un moyen d'aller de le havre à marseille.",
"Je cherche à me déplacer de le havre à marseille. Comment procéder ?",
"Je cherche à me déplacer vers marseille depuis le havre. Comment procéder ?",
"Je cherche à me déplacer vers marseille depuis le havre. Peux-tu m'aider ?",
"Je désire aller de le havre à marseille. Comment faire ?",
"Je désire aller à marseille depuis le havre. Peux-tu aider ?",
"Je pars de le havre en direction de marseille.",
"Je pars de le havre pour aller à marseille.",
"Je pars de le havre vers marseille.",
"Je prévois un voyage de le havre à marseille.",
"Je recherche un itinéraire de le havre à marseille.",
"Je recherche un itinéraire pour aller à marseille en partant de le havre.",
"Je souhaite aller de le havre à marseille, s'il te plaît.",
"Je souhaite aller à marseille en partant de le havre. Comment faire ?",
"Je souhaite aller à marseille en partant de le havre. Comment faire ?",
"Je souhaite me déplacer vers marseille à partir de le havre.",
"Je souhaite me rendre de le havre jusqu'à marseille.",
"Je souhaiterais aller à marseille depuis le havre.",
"Je souhaiterais me déplacer de le havre à marseille, si c'est réalisable.",
"Je suis en train de planifier un déplacement de le havre à marseille.",
"Je vais de nice à marseille.",
"Je vais de le havre vers marseille.",
"Je vais à nice depuis le havre.",
"Je vais à marseille en partant de le havre.",
"Je veux aller de le havre à nice.",
"Je veux aller à nice depuis le havre.",
"Je voudrais savoir comment me rendre de le havre à rouen, s'il te plaît.",
"Je voudrais savoir comment me rendre de le havre à marseille.",
"Je voudrais savoir comment me rendre à rouen depuis le havre, s'il te plaît.",
"Je voudrais savoir comment me rendre à marseille depuis le havre.",
"Le voyage de le havre à marseille est ce que je recherche.",
"Mon trajet va de le havre à marseille.",
"Montre-moi le chemin pour aller à rouen à partir de le havre.",
"Montre-moi le chemin pour me rendre de lyon à rouen.",
"Montre-moi le chemin pour passer de lyon à marseille.",
"Montre-moi le trajet pour aller à marseille en partant de le havre.",
"Partez pour marseille en partant de le havre.",
"Peux-tu m'aider à planifier le trajet depuis le havre jusqu'à marseille ?",
"Peux-tu m'aider à trouver mon chemin de le havre à marseille ?",
"Peux-tu m'aider à trouver mon chemin de lyon à marseille ?",
"Peux-tu m'aider à trouver mon chemin vers marseille en partant de le havre ?",
"Peux-tu me diriger vers marseille depuis le havre ?",
"Peux-tu me guider de le havre jusqu'à marseille ?",
"Peux-tu me guider de le havre vers lyon ?",
"Pourrais-tu m'aider à planifier le trajet de le havre vers marseille ?",
"Pourrais-tu m'aider à rejoindre marseille depuis le havre ?",
"Pourrais-tu m'indiquer comment aller de le havre à marseille ?",
"Pourrais-tu me diriger de le havre vers marseille ?",
"Pourrais-tu me donner les indications pour aller de le havre à marseille ?",
"Pourrais-tu me donner les indications pour rejoindre marseille depuis le havre ?",
"Pourrais-tu me guider vers marseille depuis le havre ?",
"Pourrais-tu me guider vers marseille depuis le havre ?",
"Pourriez-vous m'indiquer comment aller de le havre à marseille, je vous prie ?",
"Recherche le chemin entre le havre et marseille.",
"Recherche le chemin le plus court entre le havre et marseille.",
"Recherche le trajet le plus court vers marseille à partir de le havre.",
"Rendez-vous à marseille depuis le havre.",
"Serait-il possible de me rendre de le havre à marseille, s'il vous plaît ?",
"Trouve le meilleur itinéraire de le havre à marseille.",
"Trouve un itinéraire de le havre à marseille.",
"Trouve un itinéraire pour aller de le havre à marseille.",
"Trouve un itinéraire pour aller à marseille depuis le havre.",
"Trouve un itinéraire pour aller à marseille en partant de le havre.",
"Trouve un moyen d'atteindre marseille depuis le havre.",
"Trouve-moi le chemin de le havre à marseille.",
"Trouve-moi un itinéraire de marseille vers le havre.",
"Trouve-moi un itinéraire pour aller de le havre à marseille.",
"Trouve-moi un moyen de transport de le havre jusqu'à marseille.",
"Trouve-moi un moyen de transport de le havre vers marseille.",
"Trouver un moyen d'atteindre marseille depuis le havre est mon objectif.",
"Y a-t-il un moyen d'aller de le havre à marseille ?",
"Y a-t-il un moyen d'atteindre marseille depuis le havre ?",
]

def timer(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    return result, end_time - start_time

def exec_benchmark(input_data):
    ner_times = []
    cdt_times = []
    
    for sentence in input_data:
        _, ner_time = timer(start_model_ner, sentence)
        ner_times.append(ner_time)
        
        _, cdt_time = timer(extract_trip_info, sentence)
        cdt_times.append(cdt_time)

    total_ner_time = sum(ner_times)
    total_cdt_time = sum(cdt_times)

    return ner_times, cdt_times, total_ner_time, total_cdt_time

def graph(ner_times, cdt_times):
    plt.figure(figsize=(10, 6))
    plt.plot(ner_times, label='NER Execution Time')
    plt.plot(cdt_times, label='CDT Execution Time')
    plt.xlabel('Sample Index')
    plt.ylabel('Time (seconds)')
    plt.title('Execution Time per Sample')
    plt.legend()
    plt.show()

# Assuming `start_model_ner` and `extract_trip_info` are defined and work correctly with a single sentence as input
ner_times, cdt_times, total_ner_time, total_cdt_time = exec_benchmark(input_data)

print(f"Total NER Time: {total_ner_time} seconds")
print(f"Total CDT Time: {total_cdt_time} seconds")

graph(ner_times, cdt_times)