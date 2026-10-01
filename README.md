# ds-workshops

Data science workshops.

Workshop content: https://lili-lines.github.io/ds-workshops/

## Structure

```
docs/
  index.md                  home page
  <n>_<workshop>/
    slides.md               Marp slides (separated by ---)
    index.md                detailed course; [[slides]] inserts the slide viewer
    *.ipynb                 notebook
hooks/slides.py             turns slides.md into images + PDF at build time
```

To add a workshop: copy an existing folder, then add it to `nav` in `mkdocs.yml`.

## Work locally

Requirements: Python and Node.js (Marp runs through `npx`).

```bash
pip install -r requirements.txt
mkdocs serve          # http://127.0.0.1:8000, reloads on every change
```

Restart `mkdocs serve` after changing `hooks/slides.py`: hooks are not reloaded automatically.

VS Code extension to preview slides: Marp for VS Code.

The site is published to GitHub Pages on every push to `main` (`.github/workflows/pages.yml`).
