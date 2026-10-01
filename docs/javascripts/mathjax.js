// MathJax pour les équations ($$…$$ et $…$, via l'extension pymdownx.arithmatex).
// MathJax ignore déjà les blocs de code (pre, code) par défaut.
// Rendu SVG : insensible à la police unique imposée par le thème. Équations alignées à gauche.
window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true,
  },
  svg: { displayAlign: "left" },
};

// Material recharge les pages sans recharger le navigateur : on relance MathJax à chaque page
document$.subscribe(function () {
  if (window.MathJax && MathJax.typesetPromise) {
    if (MathJax.startup.output.clearCache) MathJax.startup.output.clearCache();  // n'existe pas en rendu SVG
    MathJax.typesetClear();
    MathJax.texReset();
    MathJax.typesetPromise();
  }
});
