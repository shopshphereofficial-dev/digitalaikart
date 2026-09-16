/* Digitalaikart — scroll effects engine (Apple-style reveals, 3D book, count-up) + analytics + view counter */
(function () {
  'use strict';

  /* ---------- 0a. GOOGLE ANALYTICS 4 (site-wide) ---------- */
  (function () {
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=G-WWDP6KR3EC';
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', 'G-WWDP6KR3EC');
  })();

  /* ---------- 0b. BLOG VIEW COUNTER (eye icon) ---------- */
  (function () {
    var BASE = 'https://abacus.jasoncameron.dev';
    var NS = 'digitalkartai.shop';
    function slugOf(u) {
      var m = (u || '').match(/\/blog\/([A-Za-z0-9_-]{3,64})\.html/i);
      return m ? m[1] : null;
    }
    function fmt(n) { return n >= 1000 ? (n / 1000).toFixed(1).replace(/\.0$/, '') + 'k' : String(n); }
    var post = slugOf(location.pathname);
    if (post) {
      fetch(BASE + '/hit/' + NS + '/' + post).then(function (r) { return r.json(); }).then(function (d) {
        var meta = document.querySelector('.post-meta');
        if (meta && typeof d.value === 'number') {
          var s = document.createElement('span');
          s.style.cssText = 'margin-left:0.4rem;color:var(--gold,#f5c542);font-weight:600';
          s.textContent = '\uD83D\uDC41 ' + fmt(d.value);
          meta.appendChild(s);
        }
      }).catch(function () {});
      return;
    }
    var cards = document.querySelectorAll('.blog-card');
    for (var c = 0; c < cards.length && c < 25; c++) {
      (function (card) {
        var sl = slugOf(card.getAttribute('href'));
        if (!sl) return;
        fetch(BASE + '/get/' + NS + '/' + sl).then(function (r) { return r.json(); }).then(function (d) {
          var dEl = card.querySelector('.date');
          if (dEl && typeof d.value === 'number' && d.value > 0) {
            var b = document.createElement('span');
            b.style.cssText = 'margin-left:0.5rem;color:var(--gold,#f5c542);font-weight:600';
            b.textContent = '\uD83D\uDC41 ' + fmt(d.value);
            dEl.appendChild(b);
          }
        }).catch(function () {});
      })(cards[c]);
    }
  })();

  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  /* ---------- 1. REVEAL ON SCROLL ---------- */
  var SELECTORS = [
    '.section-title', '.section-sub', '.gold-divider',
    '.why-card', '.feature-card', '.persona', '.pricing-card',
    '.chapter-list li', '.faq-item', '.compare-row', '.assurance',
    '.spotlight', '.blog-card', '.card', '.author-box',
    '.tldr', '.product-box', '.engage', '.sources', '.summary-box',
    '.page-header', '.stats-strip', '.big-claim', '.community',
    '.final-cta', '.stats-bar', '.coming-soon', '.post-svg', '.post-title', '.post-meta',
    '.legal h2', '.legal .updated', '.blog-header', '.ship-form', '.community-box'
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
        var start = parseInt(el.textContent, 10) || 0;
        var end = parseInt(el.getAttribute('data-count'), 10) || 0;
        if (start === end) continue;
        var suffix = el.getAttribute('data-suffix') || '';
        var t0 = null, dur = 1500;
        var step = function (t) {
          if (t0 === null) t0 = t;
          var k = Math.min(1, (t - t0) / dur);
          k = 1 - Math.pow(1 - k, 3);
          el.textContent = Math.round(start + (end - start) * k) + suffix;
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