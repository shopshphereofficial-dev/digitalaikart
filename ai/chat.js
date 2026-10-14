/* Digitalaikart AI — chat engine.
 *
 * All model calls go to our own server function; the browser never holds an
 * upstream key and never learns which model is behind a tier. The user picks
 * an "Astryn" tier and the server decides what runs and what it costs.
 */
(function () {
  'use strict';
  var D = window.DSK, $ = function (id) { return document.getElementById(id); };
  var FN = 'https://guoxqlojsslwetlymbvj.supabase.co/functions/v1/ai';

  var u = null, msgs = [], busy = false, mode = 'chat', tier = null;
  var guest = { used: +(localStorage.getItem('dskAI_used') || 0) };
  var GUEST_LIMIT = 5;

  /* Public tier list — names and token prices only. Which model each one maps
     to is decided on the server and is never sent to the browser. */
  var TIERS = {
    chat: [
      { id: 'astryn-lite', name: 'Astryn Lite', cost: 1, blurb: 'Fast and light — everyday questions' },
      { id: 'astryn-core', name: 'Astryn Core', cost: 1, blurb: 'Balanced speed and smarts' },
      { id: 'astryn-pro',  name: 'Astryn Pro',  cost: 2, blurb: 'Sharper reasoning for tougher work' },
      { id: 'astryn-max',  name: 'Astryn Max',  cost: 5, blurb: 'Deepest thinking for complex problems' }
    ],
    image: [
      { id: 'astryn-image',       name: 'Astryn Image',       cost: 30,  blurb: 'Quick images, lowest cost' },
      { id: 'astryn-image-pro',   name: 'Astryn Image Pro',   cost: 55,  blurb: 'High quality, strong detail' },
      { id: 'astryn-image-ultra', name: 'Astryn Image Ultra', cost: 110, blurb: 'Best quality, crisp text' }
    ]
  };
  var GUEST_TIER = { chat: 'astryn-lite', image: 'astryn-image' };

  function toast(t) { var e = $('toast'); e.textContent = t; e.classList.add('on'); setTimeout(function () { e.classList.remove('on'); }, 3000); }
  function plan() { return D.PLANS[(D.profile && D.profile.plan) || 'free']; }
  function tokensLeft() { return D.profile ? D.profile.tokens : Math.max(0, GUEST_LIMIT - guest.used); }
  function tierFor(id) {
    var list = TIERS[mode] || [];
    for (var i = 0; i < list.length; i++) if (list[i].id === id) return list[i];
    return list[0];
  }
  function chosen() { return u ? (tier || TIERS[mode][0].id) : GUEST_TIER[mode]; }

  function badge() {
    var p = plan();
    $('plan-badge').textContent = D.profile ? p.name + ' PLAN' : 'GUEST MODE';
    var t = tokensLeft();
    $('tok-badge').textContent = t + ' token' + (t === 1 ? '' : 's') + ' left';
  }

  function addMsg(role, text, cls) {
    var m = document.createElement('div');
    m.className = 'msg ' + (role === 'user' ? 'user' : 'ai') + (cls ? ' ' + cls : '');
    m.textContent = text;
    $('msgs').appendChild(m);
    $('msgs').scrollTop = $('msgs').scrollHeight;
    return m;
  }
  function linkify(m) { m.innerHTML = m.textContent.replace(/(https?:\/\/[^\s)]+)/g, '<a href="$1" target="_blank" rel="noopener">$1</a>'); }

  function showChat() { $('auth-screen').style.display = 'none'; $('chat-screen').style.display = 'flex'; }
  function showAuth() { $('chat-screen').style.display = 'none'; $('auth-screen').style.display = 'block'; }

  /* ---------- mode + tier picker ---------- */
  function buildPicker() {
    var bar = document.createElement('div');
    bar.id = 'tier-bar';
    bar.style.cssText = 'display:flex;flex-wrap:wrap;gap:.4rem;align-items:center;padding:.5rem .6rem 0';

    ['chat', 'image'].forEach(function (k) {
      var b = document.createElement('button');
      b.type = 'button';
      b.dataset.mode = k;
      b.textContent = k === 'chat' ? 'Chat' : 'Image';
      b.className = 'tier-mode';
      b.onclick = function () {
        if (mode === k) return;
        mode = k; tier = null;
        $('ai-in').placeholder = k === 'chat' ? 'Type your question...' : 'Describe the image you want...';
        renderPicker();
      };
      bar.appendChild(b);
    });

    var sel = document.createElement('select');
    sel.id = 'tier-select';
    sel.style.cssText = 'margin-left:auto;background:#fff;border:1px solid #cbd5e1;border-radius:9px;padding:.4rem .5rem;font-size:.75rem;font-family:inherit;color:#0f172a';
    sel.onchange = function () { tier = sel.value; renderPicker(); };
    bar.appendChild(sel);

    var host = document.querySelector('.ai-input');
    host.parentNode.insertBefore(bar, host);

    var note = document.createElement('div');
    note.id = 'tier-note';
    note.style.cssText = 'padding:.25rem .7rem 0;font-size:.68rem;color:#64748b';
    host.parentNode.insertBefore(note, host);

    var st = document.createElement('style');
    st.textContent = '.tier-mode{background:#fff;border:1px solid #cbd5e1;color:#1d4ed8;border-radius:99px;padding:.3rem .8rem;font-size:.72rem;font-weight:700;cursor:pointer;font-family:inherit}'
      + '.tier-mode.on{background:linear-gradient(135deg,#1d4ed8,#1e40af);color:#fff;border-color:transparent}';
    document.head.appendChild(st);

    renderPicker();
  }

  function renderPicker() {
    var bar = document.getElementById('tier-bar');
    if (!bar) return;
    bar.querySelectorAll('.tier-mode').forEach(function (b) { b.classList.toggle('on', b.dataset.mode === mode); });

    var sel = document.getElementById('tier-select');
    sel.innerHTML = '';
    TIERS[mode].forEach(function (t) {
      var o = document.createElement('option');
      o.value = t.id;
      o.textContent = t.name + ' · ' + t.cost + ' token' + (t.cost === 1 ? '' : 's');
      sel.appendChild(o);
    });
    sel.value = chosen();

    var t = tierFor(chosen());
    var note = document.getElementById('tier-note');
    if (u) {
      note.textContent = t.name + ' — ' + t.blurb + ' (' + t.cost + ' token' + (t.cost === 1 ? '' : 's') + ' per ' + (mode === 'chat' ? 'message' : 'image') + ')';
      sel.disabled = false;
    } else {
      note.textContent = 'Guest mode: ' + GUEST_LIMIT + ' free messages on Astryn Lite. Log in for higher tiers.';
      sel.disabled = true;
    }
  }

  /* ---------- send ---------- */
  function send(text) {
    text = (text || '').trim();
    if (!text || busy) return;
    if (tokensLeft() <= 0) { $('paywall').classList.add('on'); return; }

    busy = true;
    addMsg('user', text);
    $('ai-in').value = '';
    msgs.push({ r: 'u', t: text });
    var think = addMsg('ai', mode === 'image' ? 'Creating your image...' : 'Thinking...', 'thinking');

    function finish(payload) {
      think.remove();
      if (payload.image) {
        var wrap = document.createElement('div');
        wrap.className = 'msg ai';
        if (payload.reply) { var cap = document.createElement('div'); cap.textContent = payload.reply; wrap.appendChild(cap); }
        var img = document.createElement('img');
        img.src = 'data:image/jpeg;base64,' + payload.image;
        img.alt = 'Image created with Digitalaikart AI';
        img.style.cssText = 'max-width:100%;border-radius:12px;margin-top:.4rem;display:block';
        wrap.appendChild(img);
        $('msgs').appendChild(wrap);
        $('msgs').scrollTop = $('msgs').scrollHeight;
        msgs.push({ r: 'a', t: payload.reply || '[image]' });
      } else {
        var m = addMsg('ai', payload.reply);
        linkify(m);
        msgs.push({ r: 'a', t: payload.reply });
      }
      if (D.profile && typeof payload.tokens === 'number') { D.profile.tokens = payload.tokens; }
      else if (!D.profile) { guest.used++; localStorage.setItem('dskAI_used', guest.used); }
      badge(); renderPicker();
      busy = false;
      if (tokensLeft() <= 0) setTimeout(function () { $('paywall').classList.add('on'); }, 900);
    }

    function fail(msg, code) {
      think.remove();
      addMsg('ai', msg);
      busy = false;
      if (code === 'not_enough_tokens' || code === 'guest_limit') {
        setTimeout(function () { $('paywall').classList.add('on'); }, 700);
      }
    }

    function call(token) {
      var headers = { 'Content-Type': 'application/json' };
      if (token) headers.Authorization = 'Bearer ' + token;
      return fetch(FN, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({ kind: mode, tier: chosen(), prompt: text })
      }).then(function (r) { return r.json().then(function (j) { return { ok: r.ok, body: j }; }); });
    }

    var p = D.client ? D.client().auth.getSession() : Promise.resolve({ data: {} });
    p.then(function (s) {
      var token = s.data && s.data.session ? s.data.session.access_token : null;
      return call(token);
    }).then(function (res) {
      var b = res.body || {};
      if (b.reply || b.image) return finish(b);
      if (b.error === 'not_enough_tokens') return fail('You are out of tokens. Upgrade to keep going — plans start at ₹199/month.', b.error);
      if (b.error === 'guest_limit') return fail('You have used your ' + GUEST_LIMIT + ' free guest messages. Create a free account to keep chatting.', b.error);
      if (b.error === 'ai_not_configured') return fail('The assistant is being set up right now — please try again shortly.', b.error);
      fail('Sorry, something went wrong. Please try again.', b.error);
    }).catch(function () {
      fail('Network error — check your internet and try again.');
    });
  }

  /* ---------- boot ---------- */
  function renderSettings() {
    var pf = D.profile;
    $('set-name').value = (pf && pf.name) || '';
    var ta = $('set-role');
    ta.value = (pf && pf.role) || '';
    if (pf && plan().role) { ta.disabled = false; ta.placeholder = 'e.g. You are my strict startup mentor. Give blunt, actionable advice.'; }
    else { ta.disabled = true; ta.placeholder = 'Custom AI role is available on Pro and Ultimate plans.'; }
    var fp = $('free-prods');
    fp.innerHTML = '';
    if (pf && plan().products.length) {
      var h = document.createElement('div');
      h.innerHTML = '<strong style="color:var(--gold)">Free products included in your plan:</strong><br>';
      fp.appendChild(h);
      plan().products.forEach(function (pr) {
        var a = document.createElement('a');
        a.href = pr[1]; a.textContent = '⬇ ' + pr[0]; a.download = ''; a.style.display = 'block'; a.style.margin = '.2rem 0';
        fp.appendChild(a);
      });
    }
  }

  function loadChat() {
    $('msgs').innerHTML = '';
    var hello = document.createElement('div');
    hello.className = 'msg ai';
    hello.textContent = 'Hi ' + ((D.profile && D.profile.name) || 'there') + '! I am Astryn, your Digitalaikart assistant. Ask me anything — or switch to Image to create a picture.';
    $('msgs').appendChild(hello);
    msgs = [];
  }

  function start() {
    u = D.user;
    if (!u) { showChat(); badge(); renderPicker(); loadChat(); return; }
    showChat(); badge(); renderPicker(); loadChat(); renderSettings();
  }
  window.DSK_START = start;

  document.addEventListener('DOMContentLoaded', function () {
    buildPicker();
    $('ai-send').onclick = function () { send($('ai-in').value); };
    $('ai-in').addEventListener('keydown', function (e) { if (e.key === 'Enter') send($('ai-in').value); });
    document.querySelectorAll('.ai-suggest button').forEach(function (b) {
      b.onclick = function () { send(b.dataset.q || b.textContent); };
    });
    $('btn-later').onclick = function () { $('paywall').classList.remove('on'); };
    $('btn-logout').onclick = function () { D.logout(); };
    $('btn-new').onclick = function () { loadChat(); };
    $('btn-settings').onclick = function () { renderSettings(); $('settings').classList.add('on'); };
    $('set-close').onclick = function () { $('settings').classList.remove('on'); };
    $('set-save').onclick = function () {
      if (!D.profile) return;
      var patch = {};
      var n = $('set-name').value.trim(); if (n) patch.name = n;
      if (plan().role) patch.role = $('set-role').value.trim().slice(0, 500);
      D.saveProfile(patch).then(function () { toast('Saved!'); $('settings').classList.remove('on'); });
    };

    D.readyCheck().then(function (user) {
      if (!window.supabase) { showChat(); badge(); return; }
      if (!user) { showAuth(); return; }
      start();
    }).catch(function () { showAuth(); });
  });
})();
