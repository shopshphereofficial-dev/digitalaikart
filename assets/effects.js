/* Digitalaikart — scroll effects engine (Apple-style reveals, 3D book, count-up) */
(function () {
  'use strict';
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  /* ---------- 1. REVEAL ON SCROLL ---------- */
  var SELECTORS = [
    '.section-title', '.section-sub', '.gold-divider',
    '.why-card', '.feature-card', '.persona', '.pricing-card',
    '.chapter-list li', '.faq-item', '.compare-row', '.assurance',
    '.spotlight', '.blog-card', '.card', '.author-box',
    '.tldr', '.product-box', '.engage', '.sources', '.summary-box',
    '.page-header', '.stats-strip', '.big-claim', '.community',
    '.final-cta', '.stats-bar', '.coming-soon', '.post-svg', '.post-title', '.post-meta'
  ].join(',');

  var els = document.querySelectorAll(SELECTORS);
  var i;
  for (i = 0; i < els.length; i++) els[i].classList.add('rv');

  /* stagger siblings inside grids so they cascade like Apple pages */
  var groups = document.querySelectorAll('.why-grid,.feature-grid,.persona-grid,.pricing-grid,.assurance-grid,.chapter-list,.compare,.stats-strip');
  for (i = 0; i < groups.length; i++) {
    var kids = groups[i].children, k;
    for (k = 0; k < kids.length; k++) {
      kids[k].style.transitionDelay = (Math.min(k, 8) * 90) + 'ms';
    }
  }

  var io = new IntersectionObserver(function (entries) {
    for (var j = 0; j < entries.length; j++) {
      if (entries[j].isIntersecting) {
        entries[j].target.classList.add('in');
        io.unobserve(entries[j].target);
      }
    }
  }, { threshold: 0.12, rootMargin: '0px 0px -50px 0px' });
  for (i = 0; i < els.length; i++) io.observe(els[i]);

  /* ---------- 2. SCROLL-LINKED 3D BOOK ROTATION ---------- */
  var book = document.querySelector('.book');
  var scene = document.querySelector('.book-scene');
  if (book && scene) {
    var glow = scene.querySelector('.book-glow');
    var ticking = false;
    var update = function () {
      ticking = false;
      var r = scene.getBoundingClientRect();
      var vh = window.innerHeight || 800;
      var p = (r.top + r.height / 2 - vh / 2) / (vh / 2 + r.height / 2);
      p = Math.max(-1, Math.min(1, p));
      var ry = -20 - p * 28;
      var rx = 6 + p * 5;
      var lift = Math.round((1 - Math.abs(p)) * 14);
      book.style.transform = 'rotateY(' + ry.toFixed(2) + 'deg) rotateX(' + rx.toFixed(2) + 'deg) translateY(' + (-lift) + 'px)';
      if (glow) glow.style.opacity = (0.35 + (1 - Math.abs(p)) * 0.45).toFixed(2);
    };
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    update();
  }

  /* ---------- 3. COUNT-UP NUMBERS ---------- */
  var counters = document.querySelectorAll('[data-count]');
  if (counters.length) {
    var cio = new IntersectionObserver(function (entries) {
      for (var j = 0; j < entries.length; j++) {
        if (!entries[j].isIntersecting) continue;
        var el = entries[j].target;
        cio.unobserve(el);
        var end = parseInt(el.getAttribute('data-count'), 10) || 0;
        var suffix = el.getAttribute('data-suffix') || '';
        var t0 = null, dur = 1500;
        var step = function (t) {
          if (t0 === null) t0 = t;
          var k = Math.min(1, (t - t0) / dur);
          k = 1 - Math.pow(1 - k, 3);
          el.textContent = Math.round(end * k) + suffix;
          if (k < 1) requestAnimationFrame(step);
        };
        requestAnimationFrame(step);
      }
    }, { threshold: 0.4 });
    for (i = 0; i < counters.length; i++) cio.observe(counters[i]);
  }

  /* ---------- 4. 3D TILT ON HOVER (cards) ---------- */
  var tilts = document.querySelectorAll('.tilt');
  for (i = 0; i < tilts.length; i++) {
    (function (el) {
      el.addEventListener('mousemove', function (ev) {
        var r = el.getBoundingClientRect();
        var x = (ev.clientX - r.left) / r.width - 0.5;
        var y = (ev.clientY - r.top) / r.height - 0.5;
        el.style.transform = 'perspective(900px) rotateY(' + (x * 7).toFixed(2) + 'deg) rotateX(' + (-y * 7).toFixed(2) + 'deg) translateY(-5px)';
      });
      el.addEventListener('mouseleave', function () { el.style.transform = ''; });
    })(tilts[i]);
  }

  /* ---------- 5. HERO PARALLAX (subtle, premium) ---------- */
  var heroContent = document.querySelector('.hero-content');
  var heroBook = document.querySelector('.hero-book');
  if (heroContent || heroBook) {
    var pticking = false;
    var pupdate = function () {
      pticking = false;
      var sy = window.pageYOffset || 0;
      if (sy > 900) return;
      if (heroContent) heroContent.style.transform = 'translateY(' + (sy * 0.16).toFixed(1) + 'px)';
      if (heroBook) heroBook.style.transform = 'translateY(' + (sy * 0.34).toFixed(1) + 'px)';
    };
    window.addEventListener('scroll', function () {
      if (!pticking) { pticking = true; requestAnimationFrame(pupdate); }
    }, { passive: true });
  }
})();