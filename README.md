# ds-workshops

Ateliers de data science.

Lien vers le contenu des ateliers : https://lili-lines.github.io/ds-workshops/**

## Organisation

```
docs/
  index.md                  page d'accueil
  <n>_<atelier>/
    slides.md               slides au format Marp (séparées par ---)
    index.md                cours détaillé ; [[slides]] y insère la visionneuse
    pratique.md             consignes + lien Colab
    *.ipynb                 notebook
hooks/slides.py             transforme slides.md en images + PDF au build
```

Pour ajouter un atelier : copier un dossier existant, puis l'ajouter dans `nav` de `mkdocs.yml`.

## Travailler en local

Prérequis : Python et Node.js (Marp est lancé via `npx`).

```bash
pip install -r requirements.txt
mkdocs serve          # http://127.0.0.1:8000, rechargé à chaque modification
```

Extension VS Code slides vizu : *Marp for VS Code*.

Le site est publié automatiquement sur GitHub Pages à chaque push sur `main` (`.github/workflows/pages.yml`).


## Idée d'autre workshop

. machine learning starter : https://mlcourse.ai/book/index.html
. online tree for agriculture case
. online another model for agriculture case
. reg lin + feature ing : montrer que les données bien préparé font casi tout le boulot
. time series
. lgbm 
. objet detection : lib facebook ou https://huggingface.co/nvidia/LocateAnything-3B for agri case
. pipeline clasique ml
. 


support/détails/ref, slides, exercices, correction
    time : 15min speak, 15min talk, 30min practice

