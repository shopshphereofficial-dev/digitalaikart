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


  /* ---------- 0c. SITE SEARCH (all pages, auto-injected) ---------- */
  (function () {
    if (window.__dskSearch) return; window.__dskSearch = true;
    var css = ''
      + '.dsk-search-btn{background:none;border:none;color:#e8eef7;font-size:1.25rem;cursor:pointer;padding:0 .45rem;line-height:1;opacity:.85;vertical-align:middle}'
      + '.dsk-search-btn:hover{color:#f5c542;opacity:1}'
      + '.dsk-overlay{position:fixed;inset:0;background:rgba(6,12,24,.78);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);z-index:9999;display:none;align-items:flex-start;justify-content:center;padding:9vh 1rem 2rem}'
      + '.dsk-overlay.on{display:flex}'
      + '.dsk-modal{width:100%;max-width:640px;background:#0d1f38;border:1px solid rgba(245,197,66,.28);border-radius:18px;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.55)}'
      + '.dsk-input-wrap{display:flex;align-items:center;gap:.7rem;padding:1rem 1.1rem;border-bottom:1px solid rgba(255,255,255,.08)}'
      + '.dsk-input-wrap input{flex:1;background:none;border:none;outline:none;color:#eef4fb;font-size:1.05rem;font-family:inherit}'
      + '.dsk-input-wrap input::placeholder{color:#7c8aa0}'
      + '.dsk-close{background:none;border:none;color:#8fa0b8;cursor:pointer;font-size:1rem;padding:.2rem .4rem}'
      + '.dsk-close:hover{color:#fff}'
      + '.dsk-results{max-height:52vh;overflow-y:auto}'
      + '.dsk-res{display:block;padding:.8rem 1.1rem;text-decoration:none;border-bottom:1px solid rgba(255,255,255,.05)}'
      + '.dsk-res:hover{background:rgba(245,197,66,.08)}'
      + '.dsk-badge{display:inline-block;font-size:.6rem;letter-spacing:.08em;text-transform:uppercase;font-weight:700;padding:.16rem .55rem;border-radius:99px;width:max-content;margin-bottom:.3rem}'
      + '.dsk-b{background:rgba(90,140,255,.16);color:#9db9ff}'
      + '.dsk-p{background:rgba(245,197,66,.16);color:#f5c542}'
      + '.dsk-rt{color:#eef4fb;font-weight:600;font-size:.95rem;display:block}'
      + '.dsk-rd{color:#8fa0b8;font-size:.8rem;display:block;margin-top:.15rem}'
      + '.dsk-empty,.dsk-loading{padding:1.4rem;color:#8fa0b8;font-size:.9rem;text-align:center}'
      + '.dsk-hint{padding:.55rem 1.1rem;color:#5d6c84;font-size:.68rem;border-top:1px solid rgba(255,255,255,.05)}';
    var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

    var navLinks = document.querySelector('.nav-links');
    if (!navLinks) return;
    var btn = document.createElement('button');
    btn.className = 'dsk-search-btn';
    btn.setAttribute('aria-label', 'Search products and blogs');
    btn.type = 'button';
    btn.textContent = '\uD83D\uDD0D';
    btn.addEventListener('click', open);
    navLinks.appendChild(btn);

    var overlay = null, input = null, results = null, idx = null, loading = false;

    function buildOverlay() {
      if (overlay) return;
      overlay = document.createElement('div');
      overlay.className = 'dsk-overlay';
      var modal = document.createElement('div');
      modal.className = 'dsk-modal';
      modal.innerHTML = '<div class="dsk-input-wrap"><span>\uD83D\uDD0D</span><input type="text" placeholder="Search products and blogs&hellip;" /><button class="dsk-close" type="button">\u2715</button></div><div class="dsk-results"></div><div class="dsk-hint">Searches all products and blog posts &middot; press Esc to close</div>';
      overlay.appendChild(modal);
      document.body.appendChild(overlay);
      input = modal.querySelector('input');
      results = modal.querySelector('.dsk-results');
      overlay.addEventListener('click', function (e) { if (e.target === overlay) close(); });
      modal.querySelector('.dsk-close').addEventListener('click', close);
      input.addEventListener('input', function () { render(input.value); });
      input.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
          var f = results.querySelector('a.dsk-res');
          if (f) location.href = f.getAttribute('href');
        } else if (e.key === 'Escape') { close(); }
      });
    }
    function open() {
      buildOverlay();
      overlay.classList.add('on');
      document.body.style.overflow = 'hidden';
      loadIndex();
      setTimeout(function () { input.focus(); }, 60);
    }
    function close() {
      if (!overlay) return;
      overlay.classList.remove('on');
      document.body.style.overflow = '';
    }
    document.addEventListener('keydown', function (e) {
      var tag = (document.activeElement && document.activeElement.tagName) || '';
      if (e.key === '/' && tag !== 'INPUT' && tag !== 'TEXTAREA') { e.preventDefault(); open(); }
      if (e.key === 'Escape') close();
    });

    function loadIndex() {
      if (idx || loading) return;
      loading = true;
      idx = [];
      results.innerHTML = '<div class="dsk-loading">Loading search index&hellip;</div>';
      fetch('/blog/?v=' + Date.now()).then(function (r) { return r.text(); }).then(function (t) {
        var d = new DOMParser().parseFromString(t, 'text/html');
        d.querySelectorAll('a.blog-card').forEach(function (c) {
          var h = c.querySelector('h3');
          var p = c.querySelector('.blog-card-body p');
          idx.push({ t: 'Blog', title: h ? h.textContent : '', desc: p ? p.textContent : '', href: c.getAttribute('href') || '' });
        });
        render(input.value);
      }).catch(function () { loading = false; });
      fetch('/products/?v=' + Date.now()).then(function (r) { return r.text(); }).then(function (t) {
        var d = new DOMParser().parseFromString(t, 'text/html');
        d.querySelectorAll('.card').forEach(function (c) {
          var a = c.querySelector('a[href^="/products/"]');
          if (!a) return;
          var h = c.querySelector('.card-title');
          var p = c.querySelector('.card-desc');
          idx.push({ t: 'Product', title: h ? h.textContent : '', desc: p ? p.textContent : '', href: a.getAttribute('href') || '' });
        });
        render(input.value);
      }).catch(function () { loading = false; });
    }

    function score(item, q) {
      var title = item.title.toLowerCase(), desc = item.desc.toLowerCase(), s = 0;
      for (var i = 0; i < q.length; i++) {
        if (title.indexOf(q[i]) > -1) s += 2;
        else if (desc.indexOf(q[i]) > -1) s += 1;
        else return -1;
      }
      if (title.indexOf(q.join(' ')) > -1) s += 3;
      return s;
    }
    function render(v) {
      if (!results) return;
      var q = (v || '').trim().toLowerCase().split(/\s+/).filter(Boolean);
      if (!q.length) { results.innerHTML = ''; return; }
      if (!idx) { results.innerHTML = '<div class="dsk-loading">Loading search index&hellip;</div>'; return; }
      var out = [];
      for (var i = 0; i < idx.length; i++) {
        var s = score(idx[i], q);
        if (s > 0) out.push([s, idx[i]]);
      }
      out.sort(function (a, b) { return b[0] - a[0]; });
      results.innerHTML = '';
      if (!out.length) {
        results.innerHTML = '<div class="dsk-empty">No results &mdash; try &ldquo;GPT&rdquo;, &ldquo;jobs&rdquo;, &ldquo;prompts&rdquo;&hellip;</div>';
        return;
      }
      out.slice(0, 8).forEach(function (r) {
        var it = r[1];
        var a = document.createElement('a');
        a.className = 'dsk-res';
        a.setAttribute('href', it.href);
        var badge = document.createElement('span');
        badge.className = 'dsk-badge ' + (it.t === 'Blog' ? 'dsk-b' : 'dsk-p');
        badge.textContent = it.t;
        var t = document.createElement('span');
        t.className = 'dsk-rt';
        t.textContent = it.title;
        var d = document.createElement('span');
        d.className = 'dsk-rd';
        d.textContent = it.desc.slice(0, 110) + '\u2026';
        a.appendChild(badge); a.appendChild(t); a.appendChild(d);
        results.appendChild(a);
      });
    }
  })();


  /* ---------- 0d. NAV: AI CHAT LINK (all pages) ---------- */
  (function () {
    var nl = document.querySelector('.nav-links');
    if (!nl || nl.querySelector('a[href="/ai/"]')) return;
    var a = document.createElement('a');
    a.href = '/ai/';
    a.textContent = '\u2728 AI';
    a.style.cssText = 'color:#f5c542;font-weight:700';
    nl.appendChild(a);
  })();

  /* ---------- 0e. SITE HELP BOT (all pages except /ai) ---------- */
  (function () {
    if (location.pathname.indexOf('/ai') === 0) return;
    var s = document.createElement('script');
    s.src = '/assets/helpbot.js?v=1';
    document.head.appendChild(s);
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