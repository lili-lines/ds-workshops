"""Hook MkDocs : transforme chaque `slides.md` (format Marp) en images + PDF,
et remplace `[[slides]]` dans la page du même dossier par une visionneuse.

Les images sont générées dans `.cache/slides/` (hors de docs/, pour ne pas
relancer `mkdocs serve` en boucle) puis copiées dans le site à la fin du build.
"""
import logging
import os
import posixpath
import shutil
import subprocess
from pathlib import Path

log = logging.getLogger("mkdocs.hooks.slides")

MARQUEUR = "[[slides]]"
MARP = "@marp-team/marp-cli@4"
CACHE = Path(".cache/slides")
THEMES = Path("themes")
IMAGES = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}


def _dossiers_slides(docs_dir):
    for src in sorted(Path(docs_dir).rglob("slides.md")):
        yield src, src.parent.relative_to(docs_dir).as_posix()


def _marp(*args):
    npx = shutil.which("npx")
    if npx is None:
        raise RuntimeError("npx introuvable : installez Node.js pour générer les slides")
    # --no-stdin : sinon Marp attend du Markdown sur l'entrée standard et bloque
    # --allow-local-files : sinon les images du dossier de l'atelier ne sont pas rendues
    # --html : autorise les <div> utilisés pour les mises en page en colonnes
    subprocess.run([npx, "--yes", MARP, "--no-stdin", "--allow-local-files", "--html", *args, "--theme-set", str(THEMES)],
                   stdin=subprocess.DEVNULL, check=True, capture_output=True, timeout=300)


def on_pre_build(config):
    maj_themes = max((f.stat().st_mtime for f in THEMES.glob("*.css")), default=0)
    for src, rel in _dossiers_slides(config["docs_dir"]):
        out = CACHE / rel
        pdf = out / "slides.pdf"
        maj_images = max((f.stat().st_mtime for f in src.parent.rglob("*") if f.suffix.lower() in IMAGES), default=0)
        maj_sources = max(src.stat().st_mtime, maj_themes, maj_images)
        if pdf.exists() and any(out.glob("slide.*.png")) and pdf.stat().st_mtime >= maj_sources:
            continue  # déjà à jour
        log.info("Génération des slides : %s", rel)
        out.mkdir(parents=True, exist_ok=True)
        for ancien in out.iterdir():
            ancien.unlink()
        try:
            _marp(str(src), "--images", "png", "--image-scale", "1.5", "-o", str(out / "slide.png"))
            _marp(str(src), "--pdf", "-o", str(pdf))
            # Le PDF prend la date des sources au début de la génération : si slides.md
            # est modifié pendant la génération, le prochain build refera les slides.
            os.utime(pdf, (maj_sources, maj_sources))
        except (RuntimeError, subprocess.SubprocessError) as e:
            shutil.rmtree(out, ignore_errors=True)
            log.warning("Slides non générées pour %s : %s", rel, getattr(e, "stderr", e))


def _visionneuse(images, prefixe):
    grandes = "\n".join(
        f'<div class="swiper-slide"><img src="{prefixe}{img}" alt="Slide {i}" loading="lazy"></div>'
        for i, img in enumerate(images, 1))
    miniatures = "\n".join(
        f'<div class="swiper-slide"><img src="{prefixe}{img}" alt="Thumbnail {i}" loading="lazy"></div>'
        for i, img in enumerate(images, 1))
    return f"""
<div class="slides-viewer">
<div class="swiper slides-main">
<div class="swiper-wrapper">
{grandes}
</div>
<div class="swiper-button-prev"></div>
<div class="swiper-button-next"></div>
</div>
<div class="slides-toolbar">
<span class="slides-counter"></span>
<span class="slides-actions">
<a href="{prefixe}slides.pdf" download>Download PDF</a>
<button type="button" class="slides-fullscreen">Full screen</button>
</span>
</div>
<div class="swiper slides-thumbs">
<div class="swiper-wrapper">
{miniatures}
</div>
</div>
</div>
"""


def on_page_markdown(markdown, page, config, files):
    if MARQUEUR not in markdown:
        return markdown
    rel = posixpath.dirname(page.file.src_uri)
    images = sorted(p.name for p in (CACHE / rel).glob("slide.*.png"))
    if not images:
        log.warning("Aucune slide trouvée pour %s", page.file.src_uri)
        remplacement = '!!! warning "Slides unavailable"\n    The slides could not be generated (is Node.js installed?).'
    else:
        cible = posixpath.join(rel, "slides") + "/"
        prefixe = posixpath.relpath(cible, page.url or ".") + "/" if page.url else cible
        remplacement = _visionneuse(images, prefixe)
    return markdown.replace(MARQUEUR, remplacement)


def on_post_build(config):
    for _, rel in _dossiers_slides(config["docs_dir"]):
        if (CACHE / rel).exists():
            shutil.copytree(CACHE / rel, Path(config["site_dir"]) / rel / "slides", dirs_exist_ok=True)
