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
