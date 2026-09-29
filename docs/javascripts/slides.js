// Visionneuse de slides : grande slide + bande de miniatures (Swiper).
// `document$` est fourni par MkDocs Material et se déclenche à chaque changement de page.
document$.subscribe(function () {
  document.querySelectorAll(".slides-viewer").forEach(function (viewer) {
    var counter = viewer.querySelector(".slides-counter");

    var thumbs = new Swiper(viewer.querySelector(".slides-thumbs"), {
      slidesPerView: "auto",
      spaceBetween: 8,
      freeMode: true,
      watchSlidesProgress: true,
    });

    var main = new Swiper(viewer.querySelector(".slides-main"), {
      grabCursor: true,
      keyboard: { enabled: true, onlyInViewport: true },
      navigation: {
        nextEl: viewer.querySelector(".swiper-button-next"),
        prevEl: viewer.querySelector(".swiper-button-prev"),
      },
      thumbs: { swiper: thumbs },
      on: {
        init: function (s) { counter.textContent = "Slide " + (s.activeIndex + 1) + " / " + s.slides.length; },
        slideChange: function (s) { counter.textContent = "Slide " + (s.activeIndex + 1) + " / " + s.slides.length; },
      },
    });

    // Un clic sur la slide passe à la suivante
    viewer.querySelector(".slides-main").addEventListener("click", function (e) {
      if (!e.target.closest(".swiper-button-prev, .swiper-button-next") && main.allowClick) main.slideNext();
    });

    viewer.querySelector(".slides-fullscreen").addEventListener("click", function () {
      if (document.fullscreenElement) document.exitFullscreen();
      else viewer.requestFullscreen();
    });
  });
});
