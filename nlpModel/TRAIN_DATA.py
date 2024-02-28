TRAIN_DATA = [
    (
        "Je voudrais aller de Paris à Marseille",
        {"entities": [(21, 26, "DEPART"), (29, 38, "ARRIVER")]},
    ),
    (
        "Je veux prendre un train de Lyon à Bordeaux",
        {"entities": [(28, 32, "DEPART"), (35, 43, "ARRIVER")]},
    ),
    (
        "Comment puis-je me rendre de Toulouse à Lille ?",
        {"entities": [(29, 37, "DEPART"), (40, 45, "ARRIVER")]},
    ),
    (
        "Il y a-t-il des trains de Nice à Strasbourg ?",
        {"entities": [(26, 30, "DEPART"), (33, 43, "ARRIVER")]},
    ),
    (
        "Pouvez-vous m'indiquer le trajet de Nantes à Bordeaux ?",
        {"entities": [(36, 42, "DEPART"), (45, 53, "ARRIVER")]},
    ),
    (
        "Je souhaite voyager de Lyon à Paris",
        {"entities": [(23, 27, "DEPART"), (30, 35, "ARRIVER")]},
    ),
    (
        "Y a-t-il un moyen de se rendre de Marseille à Toulouse ?",
        {"entities": [(34, 43, "DEPART"), (46, 54, "ARRIVER")]},
    ),
    (
        "Je veux aller voir ma famille à Bordeaux en partant de Paris",
        {"entities": [(32, 40, "ARRIVER"), (55, 60, "DEPART")]},
    ),
    (
        "Pouvez-vous me dire comment aller de Toulouse à Lille ?",
        {"entities": [(37, 45, "DEPART"), (48, 53, "ARRIVER")]},
    ),
    (
        "Je veux aller passer mes vacances à Lille en partant de Paris",
        {"entities": [(36, 41, "ARRIVER"), (56, 61, "DEPART")]},
    ),
    (
        "Pouvez-vous me dire comment aller de Paris à Nice ?",
        {"entities": [(37, 42, "DEPART"), (45, 49, "ARRIVER")]},
    ),
    (
        "Il y a-t-il des trains de Toulouse à Bordeaux ?",
        {"entities": [(26, 34, "DEPART"), (37, 45, "ARRIVER")]},
    ),
    (
        "Je souhaite voyager de Marseille à Lyon",
        {"entities": [(23, 32, "DEPART"), (35, 39, "ARRIVER")]},
    ),
    (
        "Y a-t-il un moyen de se rendre de Bordeaux à Nice ?",
        {"entities": [(34, 42, "DEPART"), (45, 49, "ARRIVER")]},
    ),
    (
        "Je veux aller voir ma famille à Paris en partant de Lyon",
        {"entities": [(32, 37, "ARRIVER"), (52, 56, "DEPART")]},
    ),
    (
        "Pouvez-vous me dire comment aller de Lille à Toulouse ?",
        {"entities": [(37, 42, "ARRIVER"), (45, 53, "DEPART")]},
    ),
    (
        "Il y a-t-il des trains de Lyon à Strasbourg ?",
        {"entities": [(26, 30, "DEPART"), (33, 43, "ARRIVER")]},
    ),
    (
        "Je veux aller passer mes vacances à Bordeaux en partant de Marseille",
        {"entities": [(36, 44, "ARRIVER"), (59, 68, "DEPART")]},
    ),
    (
        "Pouvez-vous me dire comment aller de Paris à Lille ?",
        {"entities": [(37, 42, "DEPART"), (45, 50, "ARRIVER")]},
    ),
    (
        "Il y a-t-il des trains de Toulouse à Lyon ?",
        {"entities": [(26, 34, "DEPART"), (37, 41, "ARRIVER")]},
    ),
    (
        "Je souhaite voyager de Marseille à Nice",
        {"entities": [(23, 32, "DEPART"), (35, 39, "ARRIVER")]},
    ),
    (
        "Y a-t-il un moyen de se rendre de Bordeaux à Toulouse ?",
        {"entities": [(45, 53, "DEPART"), (34, 42, "ARRIVER")]},
    ),
    (
        "Pouvez-vous me dire comment aller de Lille à Marseille ?",
        {"entities": [(37, 42, "DEPART"), (45, 54, "ARRIVER")]},
    ),
    (
        "Il y a-t-il des trains de Strasbourg à Lyon ?",
        {"entities": [(26, 36, "DEPART"), (39, 43, "ARRIVER")]},
    ),
    (
        "Je veux aller passer mes vacances à Paris en partant de Lille",
        {"entities": [(56, 64, "DEPART"), (36, 41, "ARRIVER")]},
    ),
    (
        "Pouvez-vous me dire comment aller de Bordeaux à Lyon ?",
        {"entities": [(37, 45, "DEPART"), (48, 52, "ARRIVER")]},
    ),
    (
        "Il y a-t-il des trains de Nice à Toulouse ?",
        {"entities": [(26, 30, "DEPART"), (33, 43, "ARRIVER")]},
    ),
    (
        "Je souhaite voyager de Marseille à Paris",
        {"entities": [(23, 32, "DEPART"), (35, 40, "ARRIVER")]},
    ),
    (
        "Y a-t-il un moyen de se rendre de Toulouse à Bordeaux ?",
        {"entities": [(34, 42, "DEPART"), (45, 53, "ARRIVER")]},
    ),
    (
        "Je veux aller voir ma famille à Lyon en partant de Paris",
        {"entities": [(51, 56, "DEPART"), (32, 36, "ARRIVER")]},
    ),
    (
        "Je veux aller voir mon ami Albert à Tours en partant de Bordeaux",
        {"entities": [(56, 64, "DEPART"), (36, 41, "ARRIVER")]},
    ),
    (
        "mon ami Albert est a Lyon, je voudrais partir le voir, je suis a Lille",
        {"entities": [(65, 70, "DEPART"), (21, 25, "ARRIVER")]},
    ),
    (
        "Comment me rendre à Port-Boulet depuis la gare de Tours ?",
        {"entities": [(50, 55, "DEPART"), (20, 31, "ARRIVER")]},
    ),
    (
        "J'aimerais me barrer de Paris pour aller sur Marseille",
        {"entities": [(24, 29, "DEPART"), (45, 54, "ARRIVER")]},
    ),
    (
        "Comment je fais pour zapper de Lyon à Bordeaux ?",
        {"entities": [(31, 35, "DEPART"), (38, 46, "ARRIVER")]},
    ),
    (
        "C'est quoi le plus rapide pour bouger de Toulouse à Lille ?",
        {"entities": [(41, 49, "DEPART"), (52, 57, "ARRIVER")]},
    ),
    (
        "Y'a des trains qui font Nice-Strasbourg ?",
        {"entities": [(24, 28, "DEPART"), (29, 39, "ARRIVER")]},
    ),
    (
        "Je kiffe aller de Nantes à Bordeaux, tu sais comment ?",
        {"entities": [(18, 24, "DEPART"), (27, 35, "ARRIVER")]},
    ),
    (
        "Je planifie de Lyon à Paris, des idées ?",
        {"entities": [(15, 19, "DEPART"), (22, 27, "ARRIVER")]},
    ),
    (
        "On peut partir de Marseille à Toulouse ou bien ?",
        {"entities": [(18, 27, "DEPART"), (30, 38, "ARRIVER")]},
    ),
    (
        "Je veux voir ma famille à Bordeaux, je décolle de Paris",
        {"entities": [(26, 34, "ARRIVER"), (50, 55, "DEPART")]},
    ),
    (
        "Chui à Toulouse et je veux aller à Lille, ça se fait facile ?",
        {"entities": [(7, 15, "DEPART"), (35, 40, "ARRIVER")]},
    ),
    (
        "Je pars de Paris pour les vacs à Lille, tu connais le trajet ?",
        {"entities": [(11, 16, "DEPART"), (33, 38, "ARRIVER")]},
    ),
    (
        "Faut que je me casse de Paris pour Nice, t'as un plan ?",
        {"entities": [(24, 29, "DEPART"), (35, 39, "ARRIVER")]},
    ),
    (
        "Des idées pour aller de Toulouse à Bordeaux sans se ruiner ?",
        {"entities": [(24, 32, "DEPART"), (35, 43, "ARRIVER")]},
    ),
    (
        "Je cherche un moyen sympa de Marseille à Lyon, une suggestion ?",
        {"entities": [(29, 38, "DEPART"), (41, 45, "ARRIVER")]},
    ),
    (
        "Je dois rallier Bordeaux à Nice, le plus vite possible, des astuces ?",
        {"entities": [(16, 24, "DEPART"), (27, 31, "ARRIVER")]},
    ),
    (
        "Je démarre de Lyon pour voir la famille à Paris, c'est long ?",
        {"entities": [(14, 18, "DEPART"), (42, 47, "ARRIVER")]},
    ),
    (
        "Je veux me taper le trajet Lille-Toulouse, c'est jouable en train ?",
        {"entities": [(27, 32, "ARRIVER"), (33, 41, "DEPART")]},
    ),
    (
        "C'est galère de faire Strasbourg-Lyon en bagnole ?",
        {"entities": [(22, 32, "DEPART"), (33, 37, "ARRIVER")]},
    ),
    (
        "Je me fais un trip de Marseille à Bordeaux, tu m'accompagnes ?",
        {"entities": [(22, 31, "DEPART"), (34, 42, "ARRIVER")]},
    ),
    (
        "On se fait un Paris-Lille ce weekend ?",
        {"entities": [(14, 19, "DEPART"), (20, 25, "ARRIVER")]},
    ),
    (
        "Je bounce de Toulouse pour Lyon, c'est direct ?",
        {"entities": [(13, 21, "DEPART"), (27, 31, "ARRIVER")]},
    ),
    (
        "Je m'envole de Marseille pour Paris, c'est combien de temps ?",
        {"entities": [(15, 24, "DEPART"), (30, 35, "ARRIVER")]},
    ),
    (
        "J'peux partir de Bordeaux pour Toulouse sans galérer ?",
        {"entities": [(17, 25, "DEPART"), (31, 39, "ARRIVER")]},
    ),
    (
        "On se tape un road trip de Lille à Marseille, t'en dis quoi ?",
        {"entities": [(27, 32, "DEPART"), (35, 44, "ARRIVER")]},
    ),
    (
        "Y'a moyen de skipper de Strasbourg à Lyon sans se prendre la tête ?",
        {"entities": [(24, 34, "DEPART"), (37, 41, "ARRIVER")]},
    ),
    (
        "Je vais squatter chez des potes à Paris, je pars de Lille, easy ?",
        {"entities": [(52, 57, "DEPART"), (34, 39, "ARRIVER")]},
    ),
    (
        "On bouge de Bordeaux pour Lyon ce soir, c'est ok pour toi ?",
        {"entities": [(12, 20, "DEPART"), (26, 30, "ARRIVER")]},
    ),
    # phrase ajouté
    (
        "bonjour, je veux partir a paris depuis marseille",
        {"entities": [(26, 31, "ARRIVER"), (39, 48, "DEPART")]},
    ),
    (
        "j'aimerais partir pour le havre depuis amiens",
        {"entities": [(23, 31, "ARRIVER"), (39, 45, "DEPART")]},
    ),
    (
        "j'aimerais venir a caen en partant de nice",
        {"entities": [(19, 23, "ARRIVER"), (38, 42, "DEPART")]},
    ),
    (
        "Je veux un billet de train pour paris lyon",
        {"entities": [(38, 42, "ARRIVER"), (32, 37, "DEPART")]},
    ),
    (
        "On me demande d'arriver a grenoble depuis tours",
        {"entities": [(26, 34, "ARRIVER"), (42, 47, "DEPART")]},
    ),
    (
        "Strasbourg paris", 
        {"entities": [(11, 16, "ARRIVER"), (0, 10, "DEPART")]}),
    (
        "Rennes Lyon", 
        {"entities": [(7, 11, "ARRIVER"), (0, 6, "DEPART")]}
    ),
    (
        "reims annecy", 
        {"entities": [(6, 12, "ARRIVER"), (0, 5, "DEPART")]}
    ),
    (
        "départ de châteauroux vers nantes",
        {"entities": [(27, 33, "ARRIVER"), (10, 21, "DEPART")]},
    ),
    (
        "Je veux faire strasbourg toulon comment puis-je faire ?",
        {"entities": [(25, 31, "ARRIVER"), (14, 24, "DEPART")]},
    ),
    (
        "De mulhouse vers la rochelle",
        {"entities": [(17, 28, "ARRIVER"), (3, 11, "DEPART")]},
    ),
    (
        "Je veux un billet poitiers Niort",
        {"entities": [(27, 32, "ARRIVER"), (18, 26, "DEPART")]},
    ),
    (
        "Je veux un billet niort, Bourges",
        {"entities": [(25, 32, "ARRIVER"), (18, 23, "DEPART")]},
    ),
    (
        "Je veux prendre un train de lyon à Bordeaux",
        {"entities": [(35, 43, "ARRIVER"), (28, 32, "DEPART")]},
    ),
    (
        "Recherche le chemin entre colmar et bordeaux.",
        {"entities": [(36, 44, "ARRIVER"), (26, 32, "DEPART")]},
    ),
    (
        "Rendez-vous à dax depuis biaritz.",
        {"entities": [(14, 17, "ARRIVER"), (25, 32, "DEPART")]},
    ),
    (
        "Trouve-moi un itinéraire pour aller de montpellier à pau.",
        {"entities": [(53, 56, "ARRIVER"), (39, 50, "DEPART")]},
    ),
    (
        "Trouve-moi un moyen de transport de nimes jusqu'à nevers.",
        {"entities": [(50, 56, "ARRIVER"), (36, 41, "DEPART")]},
    ),
    (
        "Y a-t-il un moyen d'atteindre clermont depuis Lille ?",
        {"entities": [(30, 38, "ARRIVER"), (46, 51, "DEPART")]},
    ),
    (
        "Y a-t-il un moyen d'atteindre nantes depuis nevers ?",
        {"entities": [(30, 36, "ARRIVER"), (44, 50, "DEPART")]},
    ),
]

