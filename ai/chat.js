/* Digitalaikart AI — Astral chat engine.
 *
 * Model calls go to our own server function; the browser never holds an
 * upstream key and never learns which model is behind a tier.
 *
 * The chat itself stays clean: no credit counters, no per-message price. The
 * user's balance and everything else lives in Settings. Upgrade prompts appear
 * once before the first free message, and whenever the credits run out.
 */
(function () {
  'use strict';
  var D = window.DSK, $ = function (id) { return document.getElementById(id); };
  var FN = 'https://guoxqlojsslwetlymbvj.supabase.co/functions/v1/ai';

  var u = null, busy = false, mode = 'chat', tier = null, convoId = null, convos = [];
  var guest = { used: +(localStorage.getItem('dskAI_used') || 0) };
  var GUEST_LIMIT = 5;
  var askedUpgrade = localStorage.getItem('dskAI_upgrade_seen') === '1';

  /* Public tier list — names and credit prices only. Which model each one maps
     to is decided on the server and is never sent to the browser. */
  var TIERS = {
    chat: [
      { id: 'astryn-lite', name: 'Astral Lite', cost: 10, blurb: 'Fast and light — everyday questions' },
      { id: 'astryn-core', name: 'Astral Core', cost: 10, blurb: 'Balanced speed and smarts' },
      { id: 'astryn-pro',  name: 'Astral Pro',  cost: 20, blurb: 'Sharper reasoning for tougher work' },
      { id: 'astryn-max',  name: 'Astral Max',  cost: 50, blurb: 'Deepest thinking for complex problems' }
    ],
    image: [
      { id: 'astryn-image',       name: 'Astral Image',       cost: 300,  blurb: 'Quick images, lowest cost' },
      { id: 'astryn-image-pro',   name: 'Astral Image Pro',   cost: 550,  blurb: 'High quality, strong detail' },
      { id: 'astryn-image-ultra', name: 'Astral Image Ultra', cost: 1100, blurb: 'Best quality, crisp text' }
    ]
  };
  var GUEST_TIER = { chat: 'astryn-lite', image: 'astryn-image' };

  function toast(t) { var e = $('toast'); if (!e) return; e.textContent = t; e.classList.add('on'); setTimeout(function () { e.classList.remove('on'); }, 3000); }
  function plan() { return D.PLANS[(D.profile && D.profile.plan) || 'free']; }
  function creditsLeft() { return D.profile ? D.profile.tokens : Math.max(0, GUEST_LIMIT - guest.used); }
  function tierFor(id) {
    var list = TIERS[mode] || [];
    for (var i = 0; i < list.length; i++) if (list[i].id === id) return list[i];
    return list[0];
  }
  function chosen() { return u ? (tier || TIERS[mode][0].id) : GUEST_TIER[mode]; }
  function nfmt(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }
  function initial(n) { return ((n || 'A').trim().charAt(0) || 'A').toUpperCase(); }

  function showApp() { $('auth-screen').style.display = 'none'; $('app-screen').style.display = 'flex'; }
  function showAuth() { $('app-screen').style.display = 'none'; $('auth-screen').style.display = 'block'; }

  /* ---------- theme ---------- */
  function applyTheme(t) {
    document.documentElement.setAttribute('data-theme', t);
    localStorage.setItem('dskAI_theme', t);
    var b = $('theme-btn'); if (b) b.innerHTML = t === 'dark' ? '&#9790;' : '&#9788;';
    var s = $('set-theme'); if (s) s.textContent = t === 'dark' ? 'Dark' : 'Light';
  }
  function toggleTheme() {
    var t = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    applyTheme(t);
  }

  /* ---------- model picker ---------- */
  function openModelMenu() {
    var old = document.getElementById('model-menu');
    if (old) { old.remove(); return; }
    var btn = $('model-btn');
    var menu = document.createElement('div');
    menu.id = 'model-menu';
    menu.style.cssText = 'position:absolute;z-index:130;background:#fff;border:1px solid var(--border);border-radius:14px;box-shadow:0 18px 45px rgba(15,23,42,.18);padding:.4rem;min-width:250px';
    var r = btn.getBoundingClientRect();
    menu.style.top = (r.bottom + 6) + 'px';
    menu.style.left = Math.max(8, r.left) + 'px';

    ['chat', 'image'].forEach(function (k) {
      var h = document.createElement('div');
      h.style.cssText = 'font-size:.6rem;letter-spacing:.08em;color:#94a3b8;font-weight:800;padding:.45rem .6rem .2rem';
      h.textContent = k === 'chat' ? 'CHAT' : 'CREATE IMAGE';
      menu.appendChild(h);
      TIERS[k].forEach(function (t) {
        var b = document.createElement('button');
        b.type = 'button';
        b.style.cssText = 'display:flex;flex-direction:column;align-items:flex-start;gap:.1rem;width:100%;text-align:left;background:' +
          (mode === k && chosen() === t.id ? '#eef2ff' : 'none') + ';border:none;border-radius:10px;padding:.5rem .6rem;cursor:pointer;font-family:inherit';
        b.innerHTML = '<b style="font-size:.82rem;color:#0f172a">' + t.name + '</b>' +
          '<small style="font-size:.68rem;color:#64748b">' + t.blurb + '</small>';
        b.onclick = function () { mode = k; tier = t.id; closeModelMenu(); updateModelLabel(); };
        menu.appendChild(b);
      });
    });
    document.body.appendChild(menu);
    setTimeout(function () { document.addEventListener('click', closeModelMenu, { once: true }); }, 10);
  }
  function closeModelMenu() { var m = document.getElementById('model-menu'); if (m) m.remove(); }
  function updateModelLabel() {
    $('model-name').textContent = tierFor(chosen()).name;
    $('ai-in').placeholder = mode === 'image' ? 'Describe the image you want...' : 'Ask Astral anything...';
  }

  /* ---------- upgrade popup ---------- */
  function showUpgrade(kind) {
    var t = $('up-title'), x = $('up-text'), b = $('up-badge');
    if (kind === 'out') {
      b.innerHTML = '&#9888;';
      t.textContent = 'You are out of credits';
      x.textContent = D.profile
        ? 'Your credits for this month are used up. Upgrade for thousands more every month.'
        : 'You have used your ' + GUEST_LIMIT + ' free messages. Create a free account for 50 credits a month, or pick a plan.';
    } else {
      b.innerHTML = '&#9733;';
      t.textContent = 'Unlock more of Astral';
      x.textContent = D.profile
        ? 'You have ' + nfmt(creditsLeft()) + ' credits on the ' + plan().name + ' plan. Upgrade for thousands every month.'
        : 'You have ' + GUEST_LIMIT + ' free messages to try Astral. Free accounts get 50 credits a month; paid plans get thousands.';
    }
    $('upgrade').classList.add('on');
  }

  /* ---------- sidebar ---------- */
  function renderSidebar() {
    var box = $('sb-list');
    if (!box) return;
    box.innerHTML = '';
    if (!u) {
      box.innerHTML = '<div class="sb-empty">Log in to keep your chats and find them here later.</div>';
      return;
    }
    if (!convos.length) {
      box.innerHTML = '<div class="sb-empty">No chats yet. Ask something to start one.</div>';
      return;
    }
    convos.forEach(function (c) {
      var row = document.createElement('div');
      row.className = 'sb-item' + (c.id === convoId ? ' on' : '');
      var label = document.createElement('span');
      label.className = 't';
      label.textContent = c.title || 'New chat';
      var del = document.createElement('button');
      del.className = 'sb-del'; del.type = 'button'; del.title = 'Delete'; del.textContent = '\u2715';
      del.onclick = function (e) { e.stopPropagation(); deleteConvo(c.id); };
      row.appendChild(label); row.appendChild(del);
      row.onclick = function () { openConvo(c.id); };
      box.appendChild(row);
    });
  }

  function loadConvos() {
    if (!u) { convos = []; renderSidebar(); return Promise.resolve(); }
    return D.client().from('conversations')
      .select('id,title,updated_at').order('updated_at', { ascending: false }).limit(60)
      .then(function (r) { convos = r.data || []; renderSidebar(); });
  }

  function newChat() {
    convoId = null;
    $('msgs').innerHTML = '';
    greet();
    renderSidebar();
    var sb = $('sb'); if (sb) sb.classList.remove('on');
  }

  function greet() {
    var name = (D.profile && D.profile.name) || '';
    var m = document.createElement('div');
    m.className = 'msg ai';
    m.textContent = name
      ? 'Hi ' + name + '! I am Astral. What shall we work on?'
      : 'Hi! I am Astral, Digitalaikart\'s assistant. What shall we work on?';
    $('msgs').appendChild(m);
  }

  function openConvo(id) {
    convoId = id;
    var sb = $('sb'); if (sb) sb.classList.remove('on');
    $('msgs').innerHTML = '';
    D.client().from('conversations').select('msgs').eq('id', id).maybeSingle().then(function (r) {
      var msgs = (r.data && r.data.msgs) || [];
      if (!msgs.length) return newChat();
      msgs.forEach(function (m) {
        var e = addMsg(m.r === 'u' ? 'user' : 'ai', m.t);
        if (m.r !== 'u') linkify(e);
      });
    });
    renderSidebar();
  }

  function deleteConvo(id) {
    D.client().from('conversations').delete().eq('id', id).then(function () {
      if (id === convoId) newChat();
      loadConvos();
      toast('Chat deleted.');
    });
  }

  /* ---------- messages ---------- */
  function addMsg(role, text, cls) {
    var m = document.createElement('div');
    m.className = 'msg ' + (role === 'user' ? 'user' : 'ai') + (cls ? ' ' + cls : '');
    m.textContent = text;
    $('msgs').appendChild(m);
    $('msgs').scrollTop = $('msgs').scrollHeight;
    return m;
  }
  function linkify(m) { m.innerHTML = m.textContent.replace(/(https?:\/\/[^\s)]+)/g, '<a href="$1" target="_blank" rel="noopener">$1</a>'); }

  /* ---------- send ---------- */
  function send(text) {
    text = (text || '').trim();
    if (!text || busy) return;

    var need = tierFor(chosen()).cost;
    if (creditsLeft() < need) { showUpgrade('out'); return; }
    if (!askedUpgrade) {
      askedUpgrade = true;
      localStorage.setItem('dskAI_upgrade_seen', '1');
      showUpgrade('first');
    }

    busy = true;
    addMsg('user', text);
    $('ai-in').value = '';
    var think = addMsg('ai', mode === 'image' ? 'Creating your image...' : 'Thinking...', 'thinking');

    function finish(payload) {
      think.remove();
      if (payload.image) {
        var wrap = document.createElement('div');
        wrap.className = 'msg ai';
        if (payload.reply) { var cap = document.createElement('div'); cap.textContent = payload.reply; wrap.appendChild(cap); }
        var img = document.createElement('img');
        img.src = 'data:image/jpeg;base64,' + payload.image;
        img.alt = 'Image created with Astral AI';
        img.style.cssText = 'max-width:100%;border-radius:12px;margin-top:.4rem;display:block';
        wrap.appendChild(img);
        $('msgs').appendChild(wrap);
        $('msgs').scrollTop = $('msgs').scrollHeight;
      } else {
        linkify(addMsg('ai', payload.reply));
      }
      if (payload.conversation_id) convoId = payload.conversation_id;
      if (D.profile && typeof payload.credits === 'number') D.profile.tokens = payload.credits;
      else if (!D.profile) { guest.used++; localStorage.setItem('dskAI_used', guest.used); }
      refreshPlanRow();
      if (u) loadConvos();
      busy = false;
      if (creditsLeft() < tierFor(chosen()).cost) setTimeout(function () { showUpgrade('out'); }, 800);
    }

    function fail(msg, code) {
      think.remove();
      addMsg('ai', msg);
      busy = false;
      if (code === 'not_enough_credits' || code === 'guest_limit') setTimeout(function () { showUpgrade('out'); }, 600);
    }

    var p = D.client ? D.client().auth.getSession() : Promise.resolve({ data: {} });
    p.then(function (s) {
      var token = s.data && s.data.session ? s.data.session.access_token : null;
      var headers = { 'Content-Type': 'application/json' };
      if (token) headers.Authorization = 'Bearer ' + token;
      return fetch(FN, {
        method: 'POST', headers: headers,
        body: JSON.stringify({ kind: mode, tier: chosen(), prompt: text, conversation_id: convoId })
      }).then(function (r) { return r.json(); });
    }).then(function (b) {
      if (b.reply || b.image) return finish(b);
      if (b.error === 'not_enough_credits') return fail('You are out of credits for this month.', b.error);
      if (b.error === 'guest_limit') return fail('You have used your free guest messages. Create an account to keep going.', b.error);
      if (b.error === 'ai_not_configured') return fail('Astral is being set up right now — please try again shortly.', b.error);
      fail('Sorry, something went wrong. Please try again.', b.error);
    }).catch(function () {
      fail('Network error — check your internet and try again.');
    });
  }

  /* ---------- settings ---------- */
  function refreshPlanRow() {
    var pf = D.profile;
    var pname = pf ? plan().name : 'Guest';
    var left = creditsLeft();
    $('set-plan-name').textContent = pf ? pname + ' plan' : 'Guest';
    $('set-plan-credits').textContent = pf
      ? nfmt(left) + ' credits left this month'
      : GUEST_LIMIT + ' free messages (used ' + guest.used + ')';
    $('sb-plan').textContent = pf ? pname : 'Guest';
    $('sb-name').textContent = (pf && pf.name) || (u ? 'You' : 'Guest');
    $('sb-av').textContent = initial(pf && pf.name);
    var av = $('set-account').querySelector('.sb-av'); if (av) av.textContent = initial(pf && pf.name);
    $('set-acct-name').textContent = (pf && pf.name) || 'You';
    $('set-acct-mail').textContent = (u && u.email) || 'not signed in';
  }

  function renderProducts() {
    var box = $('set-products');
    box.innerHTML = '';
    if (!D.profile) { box.innerHTML = '<div class="set-hint">Log in to see the products included in your plan.</div>'; return; }
    var p = plan();
    if (!p.products.length) {
      box.innerHTML = '<div class="set-hint">No products included on the ' + p.name + ' plan. Starter, Pro and Ultimate include free products.</div>';
      return;
    }
    p.products.forEach(function (pr) {
      var a = document.createElement('a');
      a.href = pr[1]; a.textContent = '\u2913 ' + pr[0]; a.setAttribute('download', '');
      box.appendChild(a);
    });
  }

  function renderSettings() {
    var pf = D.profile;
    $('set-name').value = (pf && pf.name) || '';
    var ta = $('set-role');
    ta.value = (pf && pf.role) || '';
    var canRole = pf && plan().role;
    ta.disabled = !canRole;
    $('set-role-hint').textContent = canRole
      ? 'Astral will follow this in every chat.'
      : 'Custom instructions are available on Pro and Ultimate.';
    renderProducts();
    refreshPlanRow();
  }

  /* ---------- plans sheet ---------- */
  var USD_INR = 95.17;   // one rate, everything else derives from it
  var PLANS_DATA = {
    monthly: [
      { id:'starter',    name:'Starter',    usd:2.99,   daily:130,   tagline:'For everyday questions' },
      { id:'pro',        name:'Pro',        usd:5.99,   daily:350,   tagline:'Most popular', popular:true },
      { id:'creator',    name:'Creator',    usd:11.99,  daily:800,   tagline:'Built for images & video' },
      { id:'ultra',      name:'Ultra',      usd:24.99,  daily:1800,  tagline:'For heavy daily use' },
      { id:'business',   name:'Business',   usd:59.99,  daily:5000,  tagline:'For teams & agencies' },
      { id:'enterprise', name:'Enterprise', usd:150,    daily:30000, tagline:'Our top plan — maximum everything' }
    ],
    yearly: [
      { id:'starter-yearly', name:'Starter (Yearly)', usd:28.99,   daily:130,  tagline:'Save 20%' },
      { id:'pro-yearly',     name:'Pro (Yearly)',     usd:57.99,   daily:350,  tagline:'Best value', popular:true },
      { id:'creator-yearly', name:'Creator (Yearly)', usd:114.99,  daily:800,  tagline:'For image & video makers' },
      { id:'ultra-yearly',   name:'Ultra (Yearly)',   usd:239.99,  daily:1800, tagline:'For heavy daily use' }
    ],
    packs: [
      { id:'pack-small', name:'1,800 credits',  usd:1.49,  credits:1800,  tagline:'One-time, no subscription' },
      { id:'pack-mid',   name:'5,400 credits',  usd:3.99,  credits:5400,  tagline:'One-time, no subscription' },
      { id:'pack-large', name:'18,000 credits', usd:12.99, credits:18000, tagline:'One-time, no subscription' },
      { id:'pack-max',   name:'54,000 credits', usd:38.99, credits:54000, tagline:'One-time, no subscription' }
    ]
  };
  var planGroup = 'monthly', currency = localStorage.getItem('dskAI_cur') || 'INR';

  function money(usd) {
    if (currency === 'USD') return '$' + usd;
    /* rupees are derived from the dollar price with one rate */
    var inr = Math.round(usd * USD_INR / 10) * 10;
    return '\u20b9' + nfmt(inr);
  }

  function renderPlans() {
    var groups = [['monthly', 'Monthly'], ['yearly', 'Yearly'], ['packs', 'Credit packs']];
    var tabs = $('pl-tabs');
    tabs.innerHTML = '';
    groups.forEach(function (g) {
      var b = document.createElement('button');
      b.type = 'button'; b.textContent = g[1];
      b.className = planGroup === g[0] ? 'on' : '';
      b.onclick = function () { planGroup = g[0]; renderPlans(); };
      tabs.appendChild(b);
    });

    var cur = document.createElement('button');
    cur.type = 'button';
    cur.style.cssText = 'margin-left:auto;font-size:.72rem;padding:.45rem .7rem';
    cur.textContent = currency === 'INR' ? '\u20b9 INR' : '$ USD';
    cur.onclick = function () {
      currency = currency === 'INR' ? 'USD' : 'INR';
      localStorage.setItem('dskAI_cur', currency);
      renderPlans();
    };
    tabs.appendChild(cur);

    var list = PLANS_DATA[planGroup];
    var box = $('pl-panel');
    box.style.padding = '0';
    box.style.border = '0';
    box.innerHTML = '';

    list.forEach(function (p) {
      var mine = D.profile && D.profile.plan === p.id;
      var isPack = planGroup === 'packs';
      var el = document.createElement('div');
      el.style.cssText = 'border:1px solid var(--border);border-radius:14px;padding:1rem;margin-bottom:.7rem'
        + (p.popular ? ';border-color:#1d4ed8' : '');
      var per = isPack
        ? '<div class="plp-tag">' + p.tagline + '</div>'
        : '<div class="plp-tag">' + p.tagline + ' \u00b7 ' + nfmt(p.daily) + ' credits every day</div>';
      var price = isPack
        ? money(p.usd) + '<span> one-time</span>'
        : money(p.usd) + '<span>/' + (planGroup === 'yearly' ? 'year' : 'month') + '</span>';
      var cta;
      if (mine) {
        cta = '<span class="btn-primary" style="display:block;text-align:center;opacity:.6">Your current plan</span>';
      } else if (!D.profile) {
        cta = '<button class="btn-primary buy-btn" style="width:100%" data-plan="' + p.id + '">Sign in to buy</button>';
      } else if (p.usd > 100) {
        cta = '<a class="btn-primary" style="display:block;text-align:center;text-decoration:none" href="https://wa.me/919682600301">Talk to us</a>';
      } else {
        cta = '<button class="btn-primary buy-btn" style="width:100%" data-plan="' + p.id + '">Buy ' + p.name + '</button>';
      }
      el.innerHTML = '<h3 style="margin:0 0 .2rem;font-size:1.05rem">' + p.name + '</h3>'
        + '<div class="plp-price" style="font-size:1.5rem;font-weight:800">' + price + '</div>'
        + per + cta;
      box.appendChild(el);
    });

    var note = document.createElement('div');
    note.className = 'set-hint';
    note.style.marginTop = '.6rem';
    note.textContent = 'Prices in ' + (currency === 'USD' ? 'US dollars' : 'Indian rupees')
      + '. Subscriptions give you a fresh allowance every day. Credit packs never expire for 12 months.';
    box.appendChild(note);
  }


  /* ---------- buy ---------- */
  function buy(planId, btn) {
    if (!D.profile) {
      toast('Please sign in first.');
      $('plans-sheet').classList.remove('on');
      $('settings').classList.remove('on');
      return;
    }
    var was = btn.textContent;
    btn.textContent = 'Opening Razorpay...';
    btn.disabled = true;
    D.client().auth.getSession().then(function (r) {
      var tok = r.data && r.data.session ? r.data.session.access_token : null;
      return fetch(FN.replace('/ai', '/create-order'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + tok },
        body: JSON.stringify({ plan_id: planId, currency: currency })
      });
    }).then(function (r) { return r.json(); }).then(function (d) {
      if (d.url) { window.location.href = d.url; return; }
      btn.textContent = was; btn.disabled = false;
      if (d.error === 'payments_not_configured') toast('Payments are being set up — please try again soon.');
      else toast('Could not start the payment. Please try again.');
    }).catch(function () {
      btn.textContent = was; btn.disabled = false;
      toast('Network error — please try again.');
    });
  }


  /* ---------- thank you ---------- */
  function thankYou() {
    var wrap = document.createElement('div');
    wrap.id = 'thanks';
    wrap.style.cssText = 'position:fixed;inset:0;z-index:200;display:flex;align-items:center;justify-content:center;padding:1.2rem;background:rgba(15,23,42,.55);backdrop-filter:blur(4px)';
    wrap.innerHTML = '<div style="background:var(--navy-card);border:1px solid var(--border);border-radius:20px;max-width:420px;width:100%;padding:2rem 1.5rem;text-align:center">'
      + '<div style="width:64px;height:64px;margin:0 auto .9rem;border-radius:50%;background:linear-gradient(135deg,#16a34a,#15803d);display:flex;align-items:center;justify-content:center;font-size:1.9rem;color:#fff">&#10003;</div>'
      + '<h2 style="margin:0 0 .5rem;font-size:1.3rem">Payment successful</h2>'
      + '<p id="thanks-body" style="font-size:.88rem;color:var(--text-secondary);line-height:1.6;margin:0 0 1.3rem">Thank you! Your credits are being added — they will show in Settings in a few seconds.</p>'
      + '<button class="btn-primary" id="thanks-ok" style="width:100%">Start using Astral</button>'
      + '<p style="font-size:.7rem;color:var(--text-muted);margin:.9rem 0 0">A receipt has been emailed to you by Razorpay.</p>'
      + '</div>';
    document.body.appendChild(wrap);

    document.getElementById('thanks-ok').onclick = function () {
      wrap.remove();
      D.loadProfile().then(function () { refreshPlanRow(); renderProducts(); });
    };

    /* pull the balance in a couple of times — the webhook can lag a moment */
    var tries = 0;
    var t = setInterval(function () {
      tries++;
      D.loadProfile().then(function () {
        refreshPlanRow();
        var b = document.getElementById('thanks-body');
        if (b) b.textContent = 'Thank you! You now have ' + nfmt(creditsLeft()) + ' credits. Your plan is ' + plan().name + '.';
      });
      if (tries >= 4) clearInterval(t);
    }, 3000);
  }

  /* ---------- boot ---------- */
  function start() {
    u = D.user;
    showApp();
    updateModelLabel();
    refreshPlanRow();
    if (!u) { newChat(); return; }
    renderSettings();
    loadConvos().then(function () {
      if (convos.length) openConvo(convos[0].id); else newChat();
    });
  }
  window.DSK_START = start;

  document.addEventListener('DOMContentLoaded', function () {
    applyTheme(localStorage.getItem('dskAI_theme') || 'light');

    $('theme-btn').onclick = toggleTheme;
    $('model-btn').onclick = openModelMenu;
    $('sb-new').onclick = newChat;
    $('sb-settings').onclick = function () { renderSettings(); $('settings').classList.add('on'); };
    $('avatar-btn').onclick = function () { renderSettings(); $('settings').classList.add('on'); };
    $('sb-toggle').onclick = function () { $('sb').classList.toggle('on'); };

    $('ai-send').onclick = function () { send($('ai-in').value); };
    $('ai-in').addEventListener('keydown', function (e) { if (e.key === 'Enter') send($('ai-in').value); });
    document.querySelectorAll('#suggest button').forEach(function (b) {
      b.onclick = function () { send(b.dataset.q || b.textContent); };
    });

    $('set-close').onclick = function () { $('settings').classList.remove('on'); };
    $('set-theme').onclick = toggleTheme;
    $('set-upgrade').onclick = function () { $('settings').classList.remove('on'); renderPlans(); $('plans-sheet').classList.add('on'); };
    $('set-allplans').onclick = function () { $('settings').classList.remove('on'); renderPlans(); $('plans-sheet').classList.add('on'); };
    $('set-logout').onclick = function () { D.logout(); };
    $('set-save').onclick = function () {
      if (!D.profile) { toast('Create an account to save your settings.'); return; }
      var patch = {};
      var n = $('set-name').value.trim(); if (n) patch.name = n;
      if (plan().role) patch.role = $('set-role').value.trim().slice(0, 500);
      D.saveProfile(patch).then(function () { refreshPlanRow(); toast('Saved!'); $('settings').classList.remove('on'); });
    };

    $('plans-close').onclick = function () { $('plans-sheet').classList.remove('on'); };
    $('pl-panel').addEventListener('click', function (e) {
      var b = e.target.closest('.buy-btn');
      if (b) buy(b.dataset.plan, b);
    });
    $('up-later').onclick = function () { $('upgrade').classList.remove('on'); };
    $('up-cta').onclick = function () { $('upgrade').classList.remove('on'); renderPlans(); $('plans-sheet').classList.add('on'); };

    D.readyCheck().then(function (user) {
      if (!window.supabase) { showApp(); refreshPlanRow(); newChat(); return; }
      if (!user) { showAuth(); return; }
      start();
      if (new URLSearchParams(location.search).get('paid')) {
        history.replaceState(null, '', '/ai/');
        thankYou();
      }
    }).catch(function () { showAuth(); });
  });
})();
