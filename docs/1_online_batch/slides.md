---
marp: true
theme: terminal
paginate: true
size: 16:9
---

<!-- _paginate: false -->

# Online learning<br>vs Batch learning
Apprendre une fois, ou apprendre en continu ?
Cas d'usage : prédire la température d'une serre à partir de la météo.

---

## Le problème : une serre, ça change
- Les saisons passent (hiver → printemps → été)
- Les cultures changent, la serre est réaménagée
- Les capteurs vieillissent, se décalent, tombent en panne

➡️ Un modèle appris « une bonne fois pour toutes » peut devenir faux sans que personne ne s'en rende compte.

---

## C'est quoi, « apprendre » pour un modèle ?
- Un modèle = une fonction `sortie = f(entrées)` avec des paramètres réglables
- Apprendre = régler ces paramètres pour que les prédictions collent aux mesures passées
- Exemple : `T_int ≈ a × T_ext + b × humidité + c × heure + d`
  → le modèle cherche les bons `a`, `b`, `c`, `d`

Analogie : étalonner un instrument à partir de mesures de référence.

---

## 🧊 Batch learning
```
[ historique complet ] ──► entraînement ──► modèle figé ──► prédictions
```
- On apprend en une fois sur un gros paquet (batch) de données
- Le modèle est ensuite figé et déployé
- Pour le mettre à jour : on refait tout l'entraînement

Analogie : l'étalonnage en usine, fait une fois avant la livraison.

---

## 🌊 Online learning
```
mesure 1 ──► prédire ──► apprendre ──┐
mesure 2 ──► prédire ──► apprendre ──┤  le modèle évolue
mesure 3 ──► prédire ──► apprendre ──┘  en permanence
```
- Le modèle apprend à chaque nouvelle mesure, par une petite correction
- On ne garde pas l'historique : une mesure est vue, utilisée, puis oubliée
- Le modèle est toujours à jour

Analogie : un régulateur adaptatif ou un filtre récursif (type Kalman).

---

## La dérive (drift)
Les données de demain ne ressemblent pas à celles d'hier.

| Type de dérive | Exemple en serre |
|---|---|
| Progressive | les saisons |
| Soudaine | changement de culture, nouvel écran thermique |
| Récurrente | jour / nuit, semaine / week-end |
| Capteur | décalage, capteur figé, panne |

Le batch ne voit pas la dérive. L'online la suit.

---

## Évaluer honnêtement : ne jamais tricher avec le futur
- Batch : on entraîne sur le passé, on teste sur la suite (jamais de mélange aléatoire sur des séries temporelles !)
- Online : évaluation prequential = prédire d'abord, apprendre ensuite
  → au moment de prédire, le modèle n'a jamais vu la réponse

---

## Nos données
- Données de serre réelles = privées ❌
- On utilise un jeu public très proche : UCI Appliances Energy Prediction
  - capteurs de température/humidité intérieurs + station météo extérieure
  - une mesure toutes les 10 min, janvier → mai 2016 (~20 000 mesures)
- Objectif : prédire la température intérieure à partir de la météo extérieure et de l'heure

---

## L'expérience
Trois stratégies, même modèle (régression linéaire), mêmes entrées :
1. 🧊 Batch figé : entraîné sur janvier, jamais mis à jour
2. 🔁 Batch ré-entraîné chaque semaine sur tout l'historique
3. 🌊 Online : mis à jour à chaque mesure (bibliothèque `river`)

---

## Résultats : erreur moyenne en °C

| Mois | 🧊 Batch figé | 🔁 Batch hebdo | 🌊 Online |
|---|---|---|---|
| Janvier | 0,84 | – | 0,93 |
| Février | 1,43 | 1,07 | 0,16 |
| Mars | 1,72 | 0,83 | 0,14 |
| Avril | 2,81 | 0,89 | 0,14 |
| Mai | 5,07 | 1,33 | 0,18 |

Le batch figé se dégrade mois après mois. L'online reste stable.

---

## ⚠️ Mais l'online a ses pièges
- Il apprend aussi les erreurs : un capteur décalé de +10 °C pendant 3 jours → le modèle met ~5 jours à s'en remettre
- Réglage sensible : un taux d'apprentissage trop grand → le modèle diverge (comme un gain trop fort dans une boucle de régulation)
- Audit / reproductibilité : le modèle change sans cesse. Lequel a pris la décision d'hier à 14h ?
- Démarrage à froid : au début, il ne sait rien (erreur plus élevée en janvier)

---

## Quand choisir quoi ?

| Si… | Alors |
|---|---|
| Le phénomène est stable, le modèle doit être validé / certifié | 🧊 Batch |
| Ça change lentement, on a le temps de ré-entraîner | 🔁 Batch ré-entraîné |
| Ça change vite, flux continu, peu de mémoire (embarqué) | 🌊 Online |
| Dans tous les cas | 📈 surveiller l'erreur en production |

---

## À retenir
1. Un modèle n'est bon que tant que le monde ressemble à ses données d'entraînement
2. Le batch est simple et robuste, mais vieillit
3. L'online s'adapte, mais apprend tout, y compris les pannes
4. En pratique : du batch ré-entraîné ou de l'online, avec un contrôle qualité des données en amont

➡️ Place à la pratique : le notebook !
