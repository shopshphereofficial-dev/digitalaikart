/* Digitalaikart — free website help bot (site/product/blog questions).
   Backed by LIVE, full-site knowledge: loads /site-knowledge.json (regenerated
   on every deploy) plus the live /products.json, so it always knows the current
   products, blog articles, downloads, pages and policies.
   Answers render site links as tappable buttons, not plain text. */
(function () {
  'use strict';
  var FN = 'https://guoxqlojsslwetlymbvj.supabase.co/functions/v1/ai';
  var hist = [], busy = false, open = false;
  var KB = null;            // { site, products[], blogs[], downloads[], pages[] }
  var INDEX = [];           // flat searchable items
  var LABELS = {};          // url -> friendly label
  var CATALOG = '';         // compact always-on product list
  var STOP = { the:1, and:1, for:1, you:1, your:1, are:1, can:1, how:1, what:1, does:1, with:1, this:1,
    that:1, have:1, from:1, about:1, any:1, all:1, get:1, its:1, into:1, not:1, but:1, out:1,
    which:1, when:1, where:1, who:1, why:1, will:1, there:1, their:1, our:1, was:1, were:1, is:1, do:1, i:1, a:1, an:1, of:1, to:1, in:1, on:1, me:1, my:1, we:1, it:1 };

  /* robot help-desk mark (drawn, not an emoji) */
  function icon(size) {
    return '<svg width="' + size + '" height="' + size + '" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
      + '<path d="M16 6.4V3.6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>'
      + '<circle cx="16" cy="2.6" r="1.9" fill="currentColor"/>'
      + '<rect x="4.5" y="6.6" width="23" height="16.4" rx="5.6" fill="currentColor" opacity=".18"/>'
      + '<rect x="4.5" y="6.6" width="23" height="16.4" rx="5.6" stroke="currentColor" stroke-width="2"/>'
      + '<circle cx="11.6" cy="14.4" r="2.3" fill="currentColor"/>'
      + '<circle cx="20.4" cy="14.4" r="2.3" fill="currentColor"/>'
      + '<path d="M12.2 19.3c1.6 1.5 6 1.5 7.6 0" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"/>'
      + '<path d="M4.5 13.4H2.2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>'
      + '<path d="M27.5 13.4h2.3" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>'
      + '</svg>';
  }

  var css = ''
    + '.hb-fab{position:fixed;right:22px;bottom:104px;z-index:900;width:58px;height:58px;border-radius:50%;border:none;color:#ffffff;background:linear-gradient(140deg,#2563eb,#1e3a8a);cursor:pointer;box-shadow:0 12px 28px rgba(29,78,216,.42),0 0 0 1px rgba(255,255,255,.18) inset;display:flex;align-items:center;justify-content:center;transition:transform .18s,box-shadow .18s;animation:hbPulse 2.6s ease-in-out infinite}'
    + '.hb-fab:hover{transform:translateY(-3px) scale(1.04);box-shadow:0 18px 38px rgba(29,78,216,.55);animation:none}'
    + '@keyframes hbPulse{0%,100%{box-shadow:0 12px 28px rgba(29,78,216,.42),0 0 0 0 rgba(37,99,235,.45)}50%{box-shadow:0 12px 28px rgba(29,78,216,.42),0 0 0 12px rgba(37,99,235,0)}}'
    + '.hb-panel{position:fixed;right:22px;bottom:164px;z-index:901;width:334px;max-width:calc(100vw - 44px);height:440px;max-height:62vh;background:#ffffff;border:1px solid #e2e8f0;border-radius:16px;display:none;flex-direction:column;overflow:hidden;box-shadow:0 24px 60px rgba(15,23,42,.18)}'
    + '.hb-panel.on{display:flex}'
    + '.hb-hd{padding:.75rem 1rem;border-bottom:1px solid #e2e8f0;display:flex;align-items:center;gap:.6rem;background:#f8fafc}'
    + '.hb-hi{display:flex;align-items:center;flex:0 0 auto;color:#1d4ed8}'
    + '.hb-t{flex:1;min-width:0}'
    + '.hb-hd b{color:#0f172a;font-size:.85rem}'
    + '.hb-hd small{display:block;color:#64748b;font-size:.62rem;font-weight:400}'
    + '.hb-x{background:none;border:none;color:#94a3b8;cursor:pointer;font-size:1rem;flex:0 0 auto}'
    + '.hb-msgs{flex:1;overflow-y:auto;padding:.8rem;display:flex;flex-direction:column;gap:.55rem;background:#ffffff}'
    + '.hb-m{max-width:88%;padding:.55rem .75rem;border-radius:11px;font-size:.8rem;line-height:1.5;white-space:pre-wrap}'
    + '.hb-m.u{align-self:flex-end;background:linear-gradient(135deg,#1d4ed8,#1e40af);color:#ffffff;font-weight:500}'
    + '.hb-m.a{align-self:flex-start;background:#f1f5f9;border:1px solid #e2e8f0;color:#0f172a}'
    + '.hb-m.a a{color:#1d4ed8}'
    + '.hb-links{display:flex;flex-wrap:wrap;gap:.35rem;margin-top:.55rem}'
    + '.hb-btn{display:inline-flex;align-items:center;gap:.3rem;background:linear-gradient(135deg,#1d4ed8,#1e40af);color:#ffffff !important;font-weight:700;font-size:.72rem;line-height:1.1;padding:.4rem .65rem;border-radius:8px;text-decoration:none;white-space:nowrap}'
    + '.hb-btn:hover{filter:brightness(1.06)}'
    + '.hb-btn svg{width:12px;height:12px}'
    + '.hb-chips{display:flex;gap:.4rem;flex-wrap:wrap;padding:0 .8rem .5rem}'
    + '.hb-chips button{background:#ffffff;border:1px solid #cbd5e1;color:#1d4ed8;border-radius:99px;padding:.24rem .65rem;font-size:.66rem;cursor:pointer;font-family:inherit}'
    + '.hb-chips button:hover{background:#f1f5f9}'
    + '.hb-in{display:flex;gap:.45rem;padding:.65rem;border-top:1px solid #e2e8f0}'
    + '.hb-in input{flex:1;background:#ffffff;border:1px solid #cbd5e1;border-radius:9px;padding:.55rem .7rem;color:#0f172a;font-size:.8rem;outline:none;font-family:inherit}'
    + '.hb-in input:focus{border-color:#1d4ed8}'
    + '.hb-in button{background:linear-gradient(135deg,#1d4ed8,#1e40af);border:none;border-radius:9px;padding:0 .9rem;color:#ffffff;font-weight:800;cursor:pointer;font-size:.8rem;font-family:inherit}';

  function el(t, c, txt) { var e = document.createElement(t); if (c) e.className = c; if (txt !== undefined) e.textContent = txt; return e; }

  function init() {
    var st = el('style'); st.textContent = css; document.head.appendChild(st);
    var fab = el('button', 'hb-fab');
    fab.innerHTML = icon(24);
    fab.setAttribute('aria-label', 'Open website help assistant');
    fab.onclick = toggle;
    var panel = el('div', 'hb-panel');
    panel.innerHTML = '<div class="hb-hd"><span class="hb-hi">' + icon(18) + '</span><div class="hb-t"><b>Digitalaikart Help</b><small>Products, blog &amp; site questions</small></div><button class="hb-x" aria-label="Close">\u2715</button></div><div class="hb-msgs"><div class="hb-m a"><div>Hi! I know this whole website — every product, price, blog article, download and policy. Ask me anything about Digitalaikart.</div></div></div><div class="hb-chips"><button>What products do you sell?</button><button>What are the latest blog posts?</button><button>How do I download my purchase?</button><button>What apps do you have?</button><button>What is Digitalaikart AI?</button></div><div class="hb-in"><input placeholder="Ask about this site..." /><button>Send</button></div>';
    document.body.appendChild(fab); document.body.appendChild(panel);
    panel.querySelector('.hb-x').onclick = toggle;
    var inp = panel.querySelector('.hb-in input');
    panel.querySelector('.hb-in button').onclick = function () { send(inp.value); };
    inp.addEventListener('keydown', function (e) { if (e.key === 'Enter') send(inp.value); });
    panel.querySelectorAll('.hb-chips button').forEach(function (b) {
      b.onclick = function () { send(b.textContent); };
    });
    loadKnowledge();
  }

  function toggle() {
    var p = document.querySelector('.hb-panel');
    open = !open;
    p.classList.toggle('on', open);
    if (open) setTimeout(function () { p.querySelector('.hb-in input').focus(); }, 80);
  }

  /* ---------- knowledge loading (live) ---------- */
  function loadKnowledge() {
    var t = Date.now();
    var jobs = [
      fetch('/products.json?v=' + t).then(function (r) { return r.json(); }).catch(function () { return null; }),
      fetch('/site-knowledge.json?v=' + t).then(function (r) { return r.json(); }).catch(function () { return null; })
    ];
    Promise.all(jobs).then(function (res) {
      var liveProducts = res[0] && res[0].products ? res[0].products : null;
      var kb = res[1] || {};
      KB = {
        site: kb.site || {},
        products: (liveProducts || kb.products || []).map(function (p) {
          return { name: p.name || p.slug, price: p.price || '', url: p.url || ('/products/' + (p.slug || '') + '/'),
                   tagline: p.tagline || p.summary || '', topics: p.topics || [] };
        }),
        blogs: kb.blogs || [],
        downloads: kb.downloads || [],
        pages: kb.pages || [],
        apps: kb.apps || []
      };
      buildIndex();
    }).catch(function () { KB = { site: {}, products: [], blogs: [], downloads: [], pages: [], apps: [] }; buildIndex(); });
  }

  function remember(url, label) {
    if (!url) return;
    LABELS[url] = label;
    if (url.length > 1 && url.charAt(url.length - 1) === '/') LABELS[url.slice(0, -1)] = label;
  }

  function buildIndex() {
    INDEX = []; CATALOG = ''; LABELS = {};
    KB.products.forEach(function (p) {
      CATALOG += '- ' + p.name + (p.price ? ' — ' + p.price : '') + ' — ' + p.url + '\n';
      remember(p.url, p.name);
      INDEX.push({ kind: 'PRODUCT', title: p.name, text: (p.name + ' ' + p.tagline + ' ' + (p.topics || []).join(' ')).toLowerCase(),
        line: '[PRODUCT] ' + p.name + (p.price ? ' (' + p.price + ')' : '') + ' — ' + p.url + (p.tagline ? ' — ' + p.tagline : '') });
    });
    KB.blogs.forEach(function (b) {
      remember(b.url, b.title);
      INDEX.push({ kind: 'BLOG', title: b.title || '', date: b.date || '', text: ((b.title || '') + ' ' + (b.summary || '') + ' ' + (b.section || '') + ' ' + ((b.tags || []).join(' '))).toLowerCase(),
        line: '[BLOG] ' + (b.title || '') + (b.date ? ' (' + b.date + ')' : '') + ' — ' + b.url + (b.summary ? ' — ' + b.summary : '') });
    });
    KB.downloads.forEach(function (d) {
      remember(d.url, d.title);
      INDEX.push({ kind: 'DOWNLOAD', title: d.title || '', text: ((d.title || '') + ' downloadable pdf playbook ebook').toLowerCase(),
        line: '[DOWNLOAD] ' + (d.title || '') + ' — ' + d.url });
    });
    KB.pages.forEach(function (pg) {
      remember(pg.url, pg.title);
      INDEX.push({ kind: 'PAGE', title: pg.title || '', text: ((pg.title || '') + ' ' + (pg.summary || '')).toLowerCase(),
        line: '[PAGE] ' + (pg.title || '') + ' — ' + pg.url + (pg.summary ? ' — ' + pg.summary : '') });
    });
    (KB.apps || []).forEach(function (a) {
      remember(a.url, a.name + ' (app)');
      INDEX.push({ kind: 'APP', title: a.name || '', text: ((a.name || '') + ' ' + (a.tagline || '') + ' ' + (a.category || '') + ' ' + ((a.tags || []).join(' ')) + ' android app').toLowerCase(),
        line: '[APP] ' + (a.name || '') + ' (' + (a.price || 'Free') + ') — ' + a.url + (a.tagline ? ' — ' + a.tagline : '') });
    });
  }

  function tokens(q) {
    return (q.toLowerCase().match(/[a-z0-9\u0900-\u097F]+/g) || []).filter(function (w) { return w.length >= 3 && !STOP[w]; });
  }

  function retrieve(q) {
    var tk = tokens(q);
    var wantLatest = /latest|newest|recent|new |today|this week|news|blog|article|post/i.test(q);
    var scored = [];
    INDEX.forEach(function (it) {
      var s = 0, t = it.title.toLowerCase();
      tk.forEach(function (w) { if (t.indexOf(w) > -1) s += 3; else if (it.text.indexOf(w) > -1) s += 1; });
      if (s > 0) scored.push({ s: s, it: it });
    });
    scored.sort(function (a, b) { return b.s - a.s; });
    var picks = scored.slice(0, 6).map(function (x) { return x.it; });
    if (wantLatest) {
      KB.blogs.slice(0, 5).forEach(function (b) {
        var it = INDEX.find(function (x) { return x.kind === 'BLOG' && x.title === b.title; });
        if (it && picks.indexOf(it) < 0) picks.unshift(it);
      });
    }
    var seen = {}, out = [];
    picks.forEach(function (it) { if (!seen[it.line]) { seen[it.line] = 1; out.push(it.line); } });
    return out.slice(0, 8).join('\n');
  }

  function factsBlock() {
    var s = KB.site || {}, L = [];
    if (s.what) L.push('About: ' + s.what);
    if (s.contact) L.push('Contact: WhatsApp ' + s.contact.whatsapp + ', email ' + s.contact.email);
    if (s.how_to_buy) L.push('How to buy: ' + s.how_to_buy);
    if (s.how_to_download) L.push('Downloads: ' + s.how_to_download);
    if (s.refund) L.push('Refunds: ' + s.refund);
    if (s.shipping) L.push('Shipping: ' + s.shipping);
    if (s.payment) L.push('Payment: ' + s.payment);
    if (s.paid_ai) L.push('Digitalaikart AI: ' + s.paid_ai.desc + ' (' + s.paid_ai.url + ', plans at ' + s.paid_ai.plans_url + ')');
    if (s.apps) L.push('Apps: ' + s.apps);
    return L.join('\n');
  }

  function addM(role, text) {
    var box = document.querySelector('.hb-msgs');
    var m = el('div', 'hb-m ' + (role === 'user' ? 'u' : 'a'), text);
    box.appendChild(m); box.scrollTop = box.scrollHeight;
    return m;
  }

  /* ---------- turn a reply into text + tappable link buttons ---------- */
  var URL_RE = /(https?:\/\/[^\s<>()"']+|\/(?:products|blog|downloads)\/[^\s<>()"']*|\/ai\/[^\s<>()"']*|\/[A-Za-z0-9._-]+\.html)/g;

  function prettify(url) {
    var seg = url.split('#')[0].split('?')[0].replace(/\/+$/, '').split('/').pop() || 'Open';
    seg = seg.replace(/\.[a-z0-9]+$/i, '').replace(/[-_]+/g, ' ');
    return seg.replace(/\b\w/g, function (c) { return c.toUpperCase(); });
  }
  function labelFor(url) {
    var u = url.split('#')[0].split('?')[0];
    return LABELS[u] || LABELS[u.replace(/\/+$/, '')] || prettify(url);
  }
  function arrow() {
    return '<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M5 12h13M13 6l6 6-6 6" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  }

  function renderAnswer(m, txt) {
    var links = [];
    txt = (txt || '')
      .replace(/\[([^\]]+)\]\(\s*(https?:\/\/[^\s)]+|\/[^\s)]+)\s*\)/g, function (_, label, url) {
        links.push({ label: label.trim(), url: url }); return '';
      })
      .replace(URL_RE, function (u) { links.push({ label: '', url: u }); return ' '; });
    txt = txt.replace(/[ \t]{2,}/g, ' ').replace(/[ \t]+\n/g, '\n').replace(/\n{3,}/g, '\n\n')
             .replace(/\(\s*\)/g, '').replace(/\s+([.,;:!?])/g, '$1').replace(/^[\s:,-]+/, '').trim();

    if (txt) m.appendChild(el('div', 'hb-txt', txt));

    var seen = {}, uniq = [];
    links.forEach(function (l) {
      var u = l.url.replace(/[.,;:!?)\]]+$/, '');
      if (!u || seen[u]) return;
      seen[u] = 1; uniq.push({ label: l.label, url: u });
    });
    if (!uniq.length) return;

    var box = el('div', 'hb-links');
    uniq.slice(0, 5).forEach(function (l) {
      var a = document.createElement('a');
      a.className = 'hb-btn';
      a.href = l.url;
      if (l.url.indexOf('http') === 0) { a.target = '_blank'; a.rel = 'noopener'; }
      if (l.url.indexOf('/downloads/') === 0) a.setAttribute('download', '');
      a.innerHTML = '<span>' + (l.label || labelFor(l.url)) + '</span>' + arrow();
      box.appendChild(a);
    });
    m.appendChild(box);
  }

  function send(text) {
    text = (text || '').trim();
    if (!text || busy) return;
    busy = true;
    var inp = document.querySelector('.hb-in input');
    addM('user', text); inp.value = '';

    /* Everything the bot is allowed to know about the site travels with the
       question. The persona and the model live on our server, so nothing here
       can be read out of the page. */
    var retrieved = retrieve(text);
    var prompt =
      "=== SITE FACTS ===\n" + factsBlock()
      + "\n\n=== PRODUCT CATALOG (name — price — link) ===\n" + (CATALOG || '(catalog loading)')
      + (retrieved ? "\n\n=== RELEVANT SITE CONTENT FOR THIS QUESTION ===\n" + retrieved : "")
      + "\n\n=== USER QUESTION ===\n" + text;

    fetch(FN, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ kind: 'help', prompt: prompt })
    }).then(function (r) { return r.json(); }).then(function (d) {
      var txt;
      if (d.reply) txt = d.reply;
      else if (d.error === 'guest_limit') txt = "You have reached today's free limit for site help. For unlimited questions, try Digitalaikart AI at https://digitalkartai.shop/ai/";
      else if (d.error === 'ai_not_configured') txt = "The assistant is being set up right now — please try again shortly.";
      else txt = "Sorry, something went wrong. Please try again.";
      var m = addM('a', '');
      renderAnswer(m, txt);
      busy = false;
      var box = document.querySelector('.hb-msgs'); box.scrollTop = box.scrollHeight;
    }).catch(function () { addM('a', 'Network error — please try again.'); busy = false; });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
