/* Digitalaikart — Adsterra ad units (site-wide). Loaded from /assets/effects.js.
 *
 * Real Adsterra units:
 *   1  Popunder        pl31810111.profitableratecpmnetwork.com/4f/19/76/4f1976c51ca5a0bb0e2a98a3b3cbdaef.js
 *   2  Direct Link     profitableratecpmnetwork.com/zd5auhku?key=ee60637529c45d25ec412af6a3feb679
 *   3  Popunder        pl31810113.profitableratecpmnetwork.com/10/4a/5a/104a5aa61b7d6d6c2983ef084e26ff66.js
 *   4  Native Banner   pl31810114 .../053571799d1106953a29e2998e432268/invoke.js
 *   5  Banner 468x60   c99fb39843b0d8e5632d8f8dc1bafb62
 *   6  Banner 160x300  4341abd10c412f912763624df30b6519
 *   7  Banner 320x50   6a5ac0d7d109349c0d63b93eae37a827
 *   8  Banner 300x250  4a261336349315e3cf9d439e10636666
 *   9  Banner 728x90   298e7bf30c810c17b5244b482f4ab868
 *   10 Banner 160x600  746c278ef43e13710ad2510ecef2a164
 *
 * Banners load from /ads/banner.html and the native unit from /ads/native.html,
 * each inside its own iframe. That matters for two reasons:
 *   - Adsterra banners read a single global `atOptions`, so two banners in one
 *     document would overwrite each other;
 *   - Adsterra scripts use document.write, which only works when the script is
 *     part of the document it is parsed in (not injected after page load).
 * Open /ads/test.html to check each unit on its own.
 */
(function () {
  'use strict';

  var BANNERS = {
    b728x90: { w: 728, h: 90, key: '298e7bf30c810c17b5244b482f4ab868' },
    b468x60: { w: 468, h: 60, key: 'c99fb39843b0d8e5632d8f8dc1bafb62' },
    b300x250: { w: 300, h: 250, key: '4a261336349315e3cf9d439e10636666' },
    b320x50: { w: 320, h: 50, key: '6a5ac0d7d109349c0d63b93eae37a827' },
    b160x600: { w: 160, h: 600, key: '746c278ef43e13710ad2510ecef2a164' },
    b160x300: { w: 160, h: 300, key: '4341abd10c412f912763624df30b6519' }
  };

  var POPUNDERS = [
    'https://pl31810111.profitableratecpmnetwork.com/4f/19/76/4f1976c51ca5a0bb0e2a98a3b3cbdaef.js',
    'https://pl31810113.profitableratecpmnetwork.com/10/4a/5a/104a5aa61b7d6d6c2983ef084e26ff66.js'
  ];

  var DIRECT_LINK = 'https://www.profitableratecpmnetwork.com/zd5auhku?key=ee60637529c45d25ec412af6a3feb679';

  var CSS = ''
    + '.dak-unit{margin:1.6rem auto;max-width:100%;overflow-x:auto;overflow-y:hidden}'
    + '.dak-unit iframe{display:block;margin:0 auto;border:0;background:transparent}'
    + '.dak-dl{display:block;width:max-content;max-width:100%;margin:1.2rem auto;font-size:.78rem;letter-spacing:.04em;color:#8fa0b8;text-decoration:none}'
    + '.dak-dl:hover{color:#f5c542;text-decoration:underline}';

  function injectStyles() {
    if (document.getElementById('dak-ad-css')) return;
    var s = document.createElement('style');
    s.id = 'dak-ad-css';
    s.textContent = CSS;
    document.head.appendChild(s);
  }

  /* Collapse the wrapper if the unit rendered nothing, so we never leave a big
     empty gap on the page. Same-origin iframe, so we can inspect it. */
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

  function frameNode(src, w, h) {
    var wrap = document.createElement('div');
    wrap.className = 'dak-unit';

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

  function bannerNode(unit) {
    var wrap = frameNode('/ads/banner.html?k=' + encodeURIComponent(unit.key) + '&w=' + unit.w + '&h=' + unit.h, unit.w, unit.h);
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

  function groupAfter(ref, nodes) {
    if (!ref || !ref.parentNode) return false;
    var parent = ref.parentNode;
    var anchor = ref.nextSibling;
    for (var i = 0; i < nodes.length; i++) parent.insertBefore(nodes[i], anchor);
    return true;
  }

  function groupBefore(ref, nodes) {
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

      /* Popunders — site-wide (must sit on the top page to catch clicks). */
      for (var p = 0; p < POPUNDERS.length; p++) {
        var ps = doc.createElement('script');
        ps.src = POPUNDERS[p];
        doc.body.appendChild(ps);
      }

      var footer = doc.querySelector('footer');
      var postBody = doc.querySelector('.post-body');
      var productInfo = doc.querySelector('.product-info');
      var hero = doc.querySelector('section.hero');

      var topRef = null, midRef = null;

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
      }

      if (topRef) {
        var topNodes = [bannerNode(BANNERS.b728x90), bannerNode(BANNERS.b320x50)];
        groupAfter(topRef, topNodes);

        var midAnchor = (midRef && midRef.parentNode) ? midRef : topNodes[topNodes.length - 1];
        groupAfter(midAnchor, [bannerNode(BANNERS.b300x250), bannerNode(BANNERS.b160x600)]);

        if (footer && footer.parentNode) {
          groupBefore(footer, [bannerNode(BANNERS.b468x60), bannerNode(BANNERS.b160x300), nativeNode()]);
        }
      } else if (footer && footer.parentNode) {
        groupBefore(footer, [bannerNode(BANNERS.b728x90), bannerNode(BANNERS.b300x250), nativeNode()]);
      }

      if (footer && footer.parentNode) groupBefore(footer, [linkNode()]);
    } catch (e) { /* never break the page */ }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount);
  else mount();
})();
