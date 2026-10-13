/* Digitalaikart — Adsterra ads (site-wide). Loaded from /assets/effects.js.
 *
 * Adsterra *Direct Link* (Smartlink) placements.
 *
 * A Direct Link is a plain URL with no visual format of its own, so each slot
 * renders a clearly-labelled "Sponsored" card that links out to it. Nothing is
 * auto-opened or hidden — that would break Adsterra's policy. Each slot appends
 * &psid=<slot> so the Adsterra dashboard can report which placement earns.
 *
 * To run REAL visual units (Banner / Native Banner / Social Bar / Popunder):
 * create the unit in the Adsterra dashboard, copy the whole <script> block it
 * gives you, and paste it as a string into DAK_ADS.units.<slot> below. It is
 * then rendered in that slot instead of the sponsored card.
 */
(function () {
  'use strict';

  var DAK_ADS = {
    smartlink: 'https://www.profitableratecpmnetwork.com/ihsrwhnv5?key=9f5c8df66b946865982c450a0400d19f',
    units: { inline: '', mid: '', banner: '', sticky: '' }
  };
  window.DAK_ADS = DAK_ADS;

  var COPY = {
    inline: { h: 'Sponsored offer', p: 'A hand-picked deal from our ad partner.', cta: 'View offer' },
    mid: { h: 'Sponsored offer', p: 'A hand-picked deal from our ad partner.', cta: 'View offer' },
    banner: { h: "Today's sponsor", p: 'A sponsored offer from our ad partner.', cta: 'Open' },
    sticky: { h: 'Sponsored offer', p: 'From our ad partner', cta: 'View' }
  };

  var CSS = ''
    + '.dak-ad{box-sizing:border-box}'
    + '.dak-slot{position:relative;margin:1.75rem auto;max-width:760px}'
    + '.dak-label{display:block;font-size:.6rem;letter-spacing:.16em;text-transform:uppercase;font-weight:700;color:#64748b;margin-bottom:.45rem}'
    + '.dak-card{position:relative;display:flex;gap:.9rem;align-items:center;padding:.9rem 1rem;background:var(--navy-card,#0f1e36);border:1px solid var(--border,#1e3a5f);border-radius:16px;overflow:hidden;text-decoration:none;color:inherit;transition:transform .25s cubic-bezier(.16,1,.3,1),border-color .2s,box-shadow .25s}'
    + '.dak-card::before{content:"";position:absolute;top:0;left:0;right:0;height:2px;background:var(--gold-gradient,linear-gradient(135deg,#f5c542,#e8a82c))}'
    + '.dak-card:hover{border-color:rgba(245,197,66,.5);transform:translateY(-2px);box-shadow:0 14px 34px rgba(0,0,0,.35)}'
    + '.dak-thumb{flex:0 0 auto;width:62px;height:62px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:.8rem;letter-spacing:.06em;color:#0a1628;background:var(--gold-gradient,linear-gradient(135deg,#f5c542,#e8a82c))}'
    + '.dak-body{flex:1;min-width:0}'
    + '.dak-h{display:block;font-weight:700;font-size:1rem;color:var(--text-primary,#e2e8f0);line-height:1.25}'
    + '.dak-p{display:block;font-size:.82rem;color:var(--text-secondary,#94a3b8);margin-top:.2rem}'
    + '.dak-cta{flex:0 0 auto;padding:.5rem .95rem;border-radius:999px;font-weight:700;font-size:.8rem;color:#0a1628;background:var(--gold-gradient,linear-gradient(135deg,#f5c542,#e8a82c));white-space:nowrap}'
    + '.dak-banner .dak-card{background:var(--gold-gradient,linear-gradient(135deg,#f5c542,#e8a82c));border-color:transparent;color:#0a1628}'
    + '.dak-banner .dak-card::before{display:none}'
    + '.dak-banner .dak-h{color:#0a1628}'
    + '.dak-banner .dak-p{color:rgba(10,22,40,.72)}'
    + '.dak-banner .dak-thumb{background:rgba(10,22,40,.16);color:#0a1628}'
    + '.dak-banner .dak-cta{background:#0a1628;color:#f5c542}'
    + '.dak-sticky{position:fixed;left:0;right:0;bottom:0;z-index:98;padding:.55rem .8rem;background:rgba(10,22,40,.97);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);border-top:1px solid var(--border,#1e3a5f);transform:translateY(130%);transition:transform .4s cubic-bezier(.16,1,.3,1)}'
    + '.dak-sticky.on{transform:translateY(0)}'
    + '.dak-sticky-in{max-width:900px;margin:0 auto;display:flex;align-items:center;gap:.6rem}'
    + '.dak-sticky .dak-card{border:none;background:transparent;padding:0;flex:1;gap:.7rem}'
    + '.dak-sticky .dak-card::before{display:none}'
    + '.dak-sticky .dak-card:hover{transform:none;box-shadow:none}'
    + '.dak-sticky .dak-thumb{width:42px;height:42px;border-radius:10px;font-size:.7rem}'
    + '.dak-sticky .dak-h{font-size:.9rem}'
    + '.dak-sticky .dak-p{font-size:.74rem}'
    + '.dak-sticky .dak-cta{padding:.4rem .8rem;font-size:.75rem}'
    + '.dak-close{flex:0 0 auto;width:30px;height:30px;border-radius:50%;border:1px solid var(--border,#1e3a5f);background:transparent;color:var(--text-secondary,#94a3b8);font-size:1.05rem;line-height:1;cursor:pointer;display:flex;align-items:center;justify-content:center}'
    + '.dak-close:hover{color:#fff;border-color:rgba(245,197,66,.5)}'
    + 'body.dak-has-sticky{padding-bottom:74px}'
    + 'body.dak-has-sticky .whatsapp-float{bottom:92px}'
    + 'body.dak-has-sticky .hb-fab{bottom:176px}'
    + 'body.dak-has-sticky .hb-panel{bottom:236px}';

  function injectStyles() {
    if (document.getElementById('dak-ad-css')) return;
    var s = document.createElement('style');
    s.id = 'dak-ad-css';
    s.textContent = CSS;
    document.head.appendChild(s);
  }

  function linkFor(psid) {
    var u = DAK_ADS.smartlink;
    if (psid) u += (u.indexOf('?') > -1 ? '&' : '?') + 'psid=' + encodeURIComponent(psid);
    return u;
  }

  function cardEl(psid, copy) {
    var a = document.createElement('a');
    a.className = 'dak-card';
    a.href = linkFor(psid);
    a.target = '_blank';
    a.rel = 'nofollow noopener sponsored';

    var thumb = document.createElement('span');
    thumb.className = 'dak-thumb';
    thumb.textContent = 'AD';

    var body = document.createElement('span');
    body.className = 'dak-body';
    var h = document.createElement('span');
    h.className = 'dak-h';
    h.textContent = copy.h;
    var p = document.createElement('span');
    p.className = 'dak-p';
    p.textContent = copy.p;
    body.appendChild(h);
    body.appendChild(p);

    var cta = document.createElement('span');
    cta.className = 'dak-cta';
    cta.textContent = copy.cta;

    a.appendChild(thumb);
    a.appendChild(body);
    a.appendChild(cta);
    return a;
  }

  function slotEl(psid, slotKey, variant) {
    var w = document.createElement('aside');
    w.className = 'dak-ad dak-slot' + (variant ? ' dak-' + variant : '');
    w.setAttribute('aria-label', 'Advertisement');
    var raw = DAK_ADS.units[slotKey];
    if (raw && raw.trim()) {
      w.innerHTML = raw;
      return w;
    }
    var l = document.createElement('span');
    l.className = 'dak-label';
    l.textContent = 'Sponsored';
    w.appendChild(l);
    w.appendChild(cardEl(psid, COPY[slotKey] || COPY.inline));
    return w;
  }

  function stickyEl() {
    var bar = document.createElement('div');
    bar.className = 'dak-ad dak-sticky';
    bar.setAttribute('aria-label', 'Advertisement');

    var inner = document.createElement('div');
    inner.className = 'dak-sticky-in';
    var raw = DAK_ADS.units.sticky;
    if (raw && raw.trim()) inner.innerHTML = raw;
    else inner.appendChild(cardEl('sticky', COPY.sticky));

    var close = document.createElement('button');
    close.type = 'button';
    close.className = 'dak-close';
    close.setAttribute('aria-label', 'Close advertisement');
    close.textContent = '\u00D7';
    close.addEventListener('click', function () {
      bar.classList.remove('on');
      document.body.classList.remove('dak-has-sticky');
      try { localStorage.setItem('dak_ad_closed', '1'); } catch (e) {}
    });
    inner.appendChild(close);
    bar.appendChild(inner);
    return bar;
  }

  function mount() {
    try {
      /* Keep the store's checkout / thank-you page clean. */
      if (/thank-you|checkout/.test(location.pathname)) return;

      injectStyles();
      var doc = document;
      var placed = false;

      var postBody = doc.querySelector('.post-body');
      var productInfo = doc.querySelector('.product-info');

      /* 1) In-content slot. */
      if (postBody) {
        var p1 = postBody.querySelector('p');
        var inlineNode = slotEl('inline', 'inline');
        if (p1 && p1.parentNode === postBody) postBody.insertBefore(inlineNode, p1.nextSibling);
        else postBody.insertBefore(inlineNode, postBody.firstChild);
        placed = true;

        /* 2) Mid-article slot for long reads. */
        var ps = postBody.querySelectorAll('p');
        if (ps.length >= 4) {
          var midP = ps[Math.floor(ps.length / 2)];
          if (midP && midP.parentNode === postBody) postBody.insertBefore(slotEl('mid', 'mid'), midP.nextSibling);
        }
      } else if (productInfo) {
        productInfo.insertBefore(slotEl('inline', 'inline'), productInfo.firstChild);
        placed = true;
        var pg = doc.querySelector('.pricing-grid');
        if (pg && pg.parentNode) pg.parentNode.insertBefore(slotEl('mid', 'mid'), pg.nextSibling);
      } else {
        var hero = doc.querySelector('section.hero');
        if (hero && hero.parentNode) {
          hero.parentNode.insertBefore(slotEl('inline', 'inline'), hero.nextSibling);
          placed = true;
          var comm = doc.querySelector('.community');
          if (comm && comm.parentNode) comm.parentNode.insertBefore(slotEl('mid', 'mid'), comm);
        }
      }

      /* Fallback for listing pages (products / blog indexes). */
      if (!placed) {
        var grid = doc.querySelector('.product-grid') || doc.querySelector('.blog-grid');
        if (grid && grid.parentNode) {
          grid.parentNode.insertBefore(slotEl('inline', 'inline'), grid);
          placed = true;
        }
      }

      /* 3) Banner before the footer, on every page. */
      var footer = doc.querySelector('footer');
      if (footer && footer.parentNode && !doc.querySelector('.dak-banner')) {
        footer.parentNode.insertBefore(slotEl('banner', 'banner', 'banner'), footer);
      }

      /* 4) Dismissible sticky bottom bar (skip the /ai app). */
      var closed = false;
      try { closed = localStorage.getItem('dak_ad_closed') === '1'; } catch (e) {}
      if (!closed && location.pathname.indexOf('/ai') !== 0 && !doc.querySelector('.dak-sticky')) {
        var bar = stickyEl();
        doc.body.appendChild(bar);
        var shown = false;
        var onScroll = function () {
          var y = window.pageYOffset || doc.documentElement.scrollTop || 0;
          if (!shown && y > 700) {
            shown = true;
            bar.classList.add('on');
            doc.body.classList.add('dak-has-sticky');
          }
        };
        window.addEventListener('scroll', onScroll, { passive: true });
        onScroll();
      }
    } catch (e) { /* never break the page */ }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount);
  else mount();
})();
