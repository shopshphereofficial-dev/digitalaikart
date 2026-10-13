/* Digitalaikart — Adsterra ads (site-wide). Loaded from /assets/effects.js.
 *
 * Balanced setup, all above-the-fold / in-content (footer gets almost no views
 * and can return near-zero CPM). Deliberately NOT overloading the page:
 *
 *   Popunder (1 only)      pl31810111 ...  — Adsterra: max one popunder per page
 *   Native Banner          pl31810114 ...  — high-CPM, above the fold
 *   Banner 728x90 / 320x50 298e... / 6a5a... — one leaderboard, desktop/mobile split
 *   Banner 300x250         4a26...         — in-content medium rectangle
 *   Direct Link            zd5auhku...     — small in-content link
 *
 * Units 468x60, 160x300, 160x600 and the 2nd popunder are intentionally left
 * out (they were clutter / footer placements that hurt CPM).
 *
 * Banners load from /ads/banner.html and the native from /ads/native.html, each
 * in its own iframe (Adsterra banners share one global `atOptions`, and their
 * scripts use document.write which needs to be parsed, not injected late).
 * Open /ads/test.html to check every unit on its own.
 */
(function () {
  'use strict';

  var B = {
    desk: { w: 728, h: 90, key: '298e7bf30c810c17b5244b482f4ab868' },   // leaderboard
    mob: { w: 320, h: 50, key: '6a5ac0d7d109349c0d63b93eae37a827' },    // mobile banner
    mid: { w: 300, h: 250, key: '4a261336349315e3cf9d439e10636666' }    // medium rectangle
  };

  var POPUNDER = 'https://pl31810111.profitableratecpmnetwork.com/4f/19/76/4f1976c51ca5a0bb0e2a98a3b3cbdaef.js';
  var DIRECT_LINK = 'https://www.profitableratecpmnetwork.com/zd5auhku?key=ee60637529c45d25ec412af6a3feb679';

  var CSS = ''
    + '.dak-unit{margin:1.6rem auto;max-width:100%;overflow-x:auto;overflow-y:hidden}'
    + '.dak-unit iframe{display:block;margin:0 auto;border:0;background:transparent}'
    + '.dak-desk{display:none}'
    + '@media (min-width:768px){.dak-desk{display:block}.dak-mob{display:none}}'
    + '.dak-dl{display:block;width:max-content;max-width:100%;margin:1.2rem auto;font-size:.78rem;letter-spacing:.04em;color:#8fa0b8;text-decoration:none}'
    + '.dak-dl:hover{color:#f5c542;text-decoration:underline}';

  function injectStyles() {
    if (document.getElementById('dak-ad-css')) return;
    var s = document.createElement('style');
    s.id = 'dak-ad-css';
    s.textContent = CSS;
    document.head.appendChild(s);
  }

  /* Hide a slot that rendered nothing, so no big empty gap is left behind. */
  function watchEmpty(wrap, frame) {
    frame.addEventListener('load', function () {
      setTimeout(function () {
        try {
          var d = frame.contentDocument;
          if (d && !d.querySelector('iframe, ins, img, video, object, embed, [id^="container-"] > *')) {
            wrap.style.display = 'none';
          }
        } catch (e) {}
      }, 4500);
    });
  }

  function frameNode(src, w, h, extraClass) {
    var wrap = document.createElement('div');
    wrap.className = 'dak-unit' + (extraClass ? ' ' + extraClass : '');

    var f = document.createElement('iframe');
    f.width = w;
    f.height = h;
    f.setAttribute('scrolling', 'no');
    f.setAttribute('frameborder', '0');
    f.title = 'Advertisement';
    f.style.width = w + 'px';
    f.style.height = h + 'px';
    f.src = src;

    watchEmpty(wrap, f);
    wrap.appendChild(f);
    return wrap;
  }

  function bannerNode(unit, extraClass) {
    var wrap = frameNode('/ads/banner.html?k=' + encodeURIComponent(unit.key) + '&w=' + unit.w + '&h=' + unit.h, unit.w, unit.h, extraClass);
    wrap.setAttribute('data-dak', unit.w + 'x' + unit.h);
    return wrap;
  }

  function nativeNode() {
    var wrap = frameNode('/ads/native.html', 300, 250);
    wrap.setAttribute('data-dak', 'native');
    var f = wrap.querySelector('iframe');
    if (f) {
      f.style.width = '100%';
      f.removeAttribute('width');
      var fit = function () {
        try {
          var d = f.contentDocument;
          if (!d) return;
          var hh = Math.max((d.body && d.body.scrollHeight) || 0, (d.documentElement && d.documentElement.scrollHeight) || 0);
          if (hh > 30) { f.style.height = hh + 'px'; f.setAttribute('height', hh); }
        } catch (e) {}
      };
      f.addEventListener('load', function () { setTimeout(fit, 1500); setTimeout(fit, 4500); });
    }
    return wrap;
  }

  function linkNode() {
    var a = document.createElement('a');
    a.className = 'dak-dl';
    a.href = DIRECT_LINK;
    a.target = '_blank';
    a.rel = 'nofollow noopener sponsored';
    a.textContent = 'Sponsored link';
    return a;
  }

  function after(ref, nodes) {
    if (!ref || !ref.parentNode) return false;
    var parent = ref.parentNode;
    var anchor = ref.nextSibling;
    for (var i = 0; i < nodes.length; i++) parent.insertBefore(nodes[i], anchor);
    return true;
  }

  function before(ref, nodes) {
    if (!ref || !ref.parentNode) return false;
    var parent = ref.parentNode;
    for (var i = 0; i < nodes.length; i++) parent.insertBefore(nodes[i], ref);
    return true;
  }

  function mount() {
    try {
      /* Keep the checkout / thank-you page clean. */
      if (/thank-you|checkout/.test(location.pathname)) return;

      injectStyles();
      var doc = document;

      /* Single Popunder — site-wide, sits on the top page to catch clicks. */
      var ps = doc.createElement('script');
      ps.src = POPUNDER;
      doc.body.appendChild(ps);

      var postBody = doc.querySelector('.post-body');
      var productInfo = doc.querySelector('.product-info');
      var hero = doc.querySelector('section.hero');
      var grid = doc.querySelector('.product-grid') || doc.querySelector('.blog-grid');
      var nav = doc.querySelector('.nav') || doc.querySelector('nav');

      var topRef = null, midRef = null, topBefore = false;

      if (postBody) {
        var ps1 = postBody.querySelectorAll('p');
        topRef = ps1[0] || postBody;
        midRef = ps1.length >= 4 ? ps1[Math.floor(ps1.length / 2)] : null;
      } else if (productInfo) {
        topRef = productInfo;
        midRef = doc.querySelector('.pricing-grid') || null;
      } else if (hero) {
        topRef = hero;
        midRef = doc.querySelector('.community') || null;
      } else if (grid) {
        topRef = grid;
        topBefore = true;
      } else if (nav) {
        topRef = nav;
      }

      var topNodes = [
        bannerNode(B.desk, 'dak-desk'),
        bannerNode(B.mob, 'dak-mob'),
        nativeNode()
      ];

      if (topRef) {
        if (topBefore) before(topRef, topNodes);
        else after(topRef, topNodes);
      } else {
        var footer = doc.querySelector('footer');
        if (footer && footer.parentNode) before(footer, topNodes);
      }

      var midAnchor = (midRef && midRef.parentNode) ? midRef : topNodes[topNodes.length - 1];
      after(midAnchor, [bannerNode(B.mid), linkNode()]);
    } catch (e) { /* never break the page */ }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount);
  else mount();
})();
