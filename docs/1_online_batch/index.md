# Online learning vs Batch learning

[[slides]]

Découvrir une approche machine learning.
Cet atelier compare deux façons d'apprendre sur des données réelles de capteurs. Capteurs de temperature dans une serre à partir de l'historique et de la météo.
. leur fonctionnement des modèles
. et voir pq dans le cas des capteurs en agriculture c'est + pertinant de online

todo:
. les capteurs, changement, usure
. Les modèles de machine learning le permettent, mais une question est souvent oubliée : que se passe-t-il quand le système change ?
. voc : model, feature, target, training, drift


## 1. Les datas, provenance, explication sur le type de données
Une serre est un bon exemple. Le climat intérieur dépend de la météo extérieure, mais cette relation change au fil de l'année : en hiver le chauffage domine, au printemps c'est le soleil et l'aération. Un modèle appris en hiver « croit » que le monde est toujours en hiver.

Controle de qualité des données

## 2. Choix des modèles

## 3. Apprentissage, batch vs online
[dessin bébé dans river, ou barage]

On rassemble un historique de données, on entraîne le modèle en une seule fois sur tout ce paquet, puis on l'utilise tel quel. C'est l'approche « classique » enseignée dans la plupart des cours de data science, avec des outils comme `scikit-learn` (`model.fit(X, y)` puis `model.predict(X)`).


BATCH

avantage +
stable, robuste aux données aberrantes

inconvenient -
modèle vieillit
pour le mettre à jour, il faut tout ré-entraîner, ce qui demande de conserver l'historique et de la puissance de calcul

batch + re train regulier
En pratique, on ré-entraîne souvent le modèle à intervalle régulier (chaque nuit, chaque semaine, chaque mois). C'est un bon compromis, très utilisé en industrie : le modèle suit les changements, avec un retard qui dépend de la fréquence de ré-entraînement.

ONLINE
Le modèle traite les données une par une, dans l'ordre où elles arrivent. Pour chaque nouvelle mesure :

1. il prédit la valeur,
2. il reçoit la vraie valeur,
3. il corrige légèrement ses paramètres dans la direction qui aurait réduit l'erreur.

Il n'a pas besoin de garder l'historique : chaque mesure est utilisée puis oubliée. Pour les ingénieurs, l'idée est proche d'un régulateur adaptatif, d'un filtre récursif ou de l'algorithme LMS en traitement du signal.
Audit : le modèle change à chaque mesure, il faut journaliser ses états pour pouvoir expliquer une décision passée.
controle de qualité des capteurs


Avantages +
- S'adapte en continu aux dérives.
- Très léger : mémoire constante, calcul minime par mesure. Il est adapté à l'embarqué et aux flux de données en temps réel.
- Pas de cycle de ré-entraînement à organiser.

Limites -
- il apprend en continur, y compris les erreurs : un capteur en panne « contamine » le modèle, qui doit ensuite désapprendre.
- Réglage délicat : un taux d'apprentissage trop grand fait diverger le modèle, et un taux trop petit le rend lent à réagir.
- démarrage à froid : au début, le modèle ne sait rien, necessite un temps d'adaptation



## 4. Netoyage, Création de feature, visualisation de l'information dans les données

## 5. Choix de l'implémentation

[`river`](https://riverml.xyz)[^1]


## 6. Evaluation
. métrique
. batch, train = periode t, test = periode t+1, par de mélange de données
. online = on pred avant de train


## 7. Résultats 
Données : UCI Appliances Energy Prediction[^2], de janvier à mai 2016, une mesure toutes les 10 minutes. Cible : température intérieure moyenne. Entrées : température et humidité extérieures, vent, heure de la journée.

| Mois | Batch figé (entraîné sur janvier) | Batch ré-entraîné chaque semaine | Online |
|---|---|---|---|
| Janvier | 0,84 °C | – | 0,93 °C |
| Février | 1,43 °C | 1,07 °C | 0,16 °C |
| Mars | 1,72 °C | 0,83 °C | 0,14 °C |
| Avril | 2,81 °C | 0,89 °C | 0,14 °C |
| Mai | 5,07 °C | 1,33 °C | 0,18 °C |

Lecture :
- Le batch figé se dégrade régulièrement. En mai, il se trompe de 5 °C en moyenne, car il n'a jamais vu de printemps.
- Le batch ré-entraîné limite les dégâts, mais reste en retard sur les changements rapides (début mai, quand il fait soudain plus chaud).
- L'online est un peu moins bon en janvier (démarrage à froid), puis reste très précis. Il faut relativiser : son avantage vient en grande partie du fait qu'il « colle » en permanence à l'état récent de la serre. Avec des mesures toutes les 10 minutes, la température varie peu d'une mesure à l'autre, ce qui l'aide beaucoup.

Les pièges, démontrés :
- Capteur en panne : un décalage de +10 °C pendant 3 jours fait grimper l'erreur du modèle online, qui met environ 5 jours à revenir à la normale après la panne.
- Taux d'apprentissage : à 0,01 le modèle fonctionne, à 0,05 il diverge complètement.

Et dans tous les cas : surveillez l'erreur de votre modèle en production. C'est le seul moyen de détecter qu'il ne colle plus à la réalité.


## Pour aller plus loin
Autres jeux publics de capteurs pour tester l'approche :

- UCI Occupancy Detection (température, humidité, lumière, CO₂) : https://archive.ics.uci.edu/dataset/357/occupancy+detection
- Intel Berkeley Lab (54 capteurs, dérive due aux batteries) : http://db.csail.mit.edu/labdata/labdata.html
 

[^1]: Documentation de `river` : https://riverml.xyz
[^2]: Jeu de données UCI Appliances Energy Prediction : https://archive.ics.uci.edu/dataset/374/appliances+energy+prediction
