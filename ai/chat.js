/* Digitalaikart AI — chat engine.
 *
 * All model calls go to our own server function; the browser never holds an
 * upstream key and never learns which model is behind a tier. The user picks
 * an "Astral" tier and the server decides what runs and what it costs.
 *
 * Chats live in Supabase, so the sidebar can list past conversations and the
 * assistant remembers the person across them.
 */
(function () {
  'use strict';
  var D = window.DSK, $ = function (id) { return document.getElementById(id); };
  var FN = 'https://guoxqlojsslwetlymbvj.supabase.co/functions/v1/ai';

  var u = null, busy = false, mode = 'chat', tier = null, convoId = null, convos = [];
  var guest = { used: +(localStorage.getItem('dskAI_used') || 0) };
  var GUEST_LIMIT = 5;

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

  function toast(t) { var e = $('toast'); e.textContent = t; e.classList.add('on'); setTimeout(function () { e.classList.remove('on'); }, 3000); }
  function plan() { return D.PLANS[(D.profile && D.profile.plan) || 'free']; }
  function creditsLeft() { return D.profile ? D.profile.tokens : Math.max(0, GUEST_LIMIT - guest.used); }
  function tierFor(id) {
    var list = TIERS[mode] || [];
    for (var i = 0; i < list.length; i++) if (list[i].id === id) return list[i];
    return list[0];
  }
  function chosen() { return u ? (tier || TIERS[mode][0].id) : GUEST_TIER[mode]; }
  function nfmt(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }

  function badge() {
    var p = plan();
    $('plan-badge').textContent = D.profile ? p.name + ' PLAN' : 'GUEST MODE';
    var c = creditsLeft();
    $('tok-badge').textContent = nfmt(c) + ' credit' + (c === 1 ? '' : 's');
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

  /* ---------- sidebar ---------- */
  function buildSidebar() {
    var st = document.createElement('style');
    st.textContent =
      '.ai-wrap{max-width:1080px}'
      + '#chat-screen{gap:.9rem;align-items:stretch}'
      + '#sb{width:236px;flex:0 0 236px;background:#ffffff;border:1px solid var(--border);border-radius:16px;padding:.7rem;display:flex;flex-direction:column;gap:.4rem;max-height:74vh}'
      + '#sb .sb-new{background:linear-gradient(135deg,#1d4ed8,#1e40af);color:#fff;border:none;border-radius:11px;padding:.6rem;font-weight:800;font-size:.82rem;cursor:pointer;font-family:inherit}'
      + '#sb .sb-h{font-size:.62rem;letter-spacing:.06em;color:#94a3b8;font-weight:700;margin:.5rem .2rem .1rem}'
      + '#sb .sb-list{flex:1;overflow-y:auto;display:flex;flex-direction:column;gap:.2rem}'
      + '#sb .sb-item{display:flex;align-items:center;gap:.35rem;padding:.45rem .5rem;border-radius:9px;cursor:pointer;font-size:.76rem;color:#334155;line-height:1.3}'
      + '#sb .sb-item:hover{background:#f1f5f9}'
      + '#sb .sb-item.on{background:#eef2ff;color:#1d4ed8;font-weight:700}'
      + '#sb .sb-item span{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}'
      + '#sb .sb-del{opacity:0;border:none;background:none;color:#94a3b8;cursor:pointer;font-size:.8rem;padding:0 .15rem}'
      + '#sb .sb-item:hover .sb-del{opacity:1}'
      + '#sb .sb-del:hover{color:#dc2626}'
      + '#sb .sb-empty{font-size:.72rem;color:#94a3b8;padding:.5rem;line-height:1.5}'
      + '#sb-toggle{display:none;background:#fff;border:1px solid var(--border);border-radius:10px;padding:.35rem .6rem;font-size:.75rem;cursor:pointer;font-family:inherit}'
      + '@media(max-width:820px){#sb{position:fixed;left:.6rem;right:.6rem;top:5.4rem;z-index:60;width:auto;flex:1 1 auto;box-shadow:0 24px 60px rgba(15,23,42,.25);display:none}#sb.on{display:flex}#sb-toggle{display:inline-block}}';
    document.head.appendChild(st);

    var sb = document.createElement('aside');
    sb.id = 'sb';
    sb.innerHTML = '<button class="sb-new" type="button">+ New chat</button>'
      + '<div class="sb-h">RECENT</div><div class="sb-list" id="sb-list"></div>';
    var host = $('chat-screen');
    host.insertBefore(sb, host.firstChild.nextSibling);
    sb.querySelector('.sb-new').onclick = newChat;

    var tb = document.createElement('button');
    tb.id = 'sb-toggle';
    tb.type = 'button';
    tb.textContent = '☰ Chats';
    tb.onclick = function () { sb.classList.toggle('on'); };
    var topbar = document.querySelector('.topbar');
    topbar.insertBefore(tb, topbar.firstChild);
  }

  function renderSidebar() {
    var box = document.getElementById('sb-list');
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
      label.textContent = c.title || 'New chat';
      var del = document.createElement('button');
      del.className = 'sb-del';
      del.type = 'button';
      del.title = 'Delete';
      del.textContent = '✕';
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
    addMsg('ai', 'Hi ' + ((D.profile && D.profile.name) || 'there') + '! I am Astral. What shall we work on?');
    renderSidebar();
    var sb = document.getElementById('sb'); if (sb) sb.classList.remove('on');
  }

  function openConvo(id) {
    convoId = id;
    var sb = document.getElementById('sb'); if (sb) sb.classList.remove('on');
    $('msgs').innerHTML = '';
    var c = convos.filter(function (x) { return x.id === id; })[0];
    if (c && c.title) $('msgs').dataset.title = c.title;
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

  /* ---------- mode + tier picker ---------- */
  function buildPicker() {
    var bar = document.createElement('div');
    bar.id = 'tier-bar';
    bar.style.cssText = 'display:flex;flex-wrap:wrap;gap:.4rem;align-items:center;padding:.5rem .6rem 0';

    ['chat', 'image'].forEach(function (k) {
      var b = document.createElement('button');
      b.type = 'button';
      b.dataset.mode = k;
      b.textContent = k === 'chat' ? 'Chat' : 'Create image';
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
      o.textContent = t.name + ' · ' + nfmt(t.cost) + ' credits';
      sel.appendChild(o);
    });
    sel.value = chosen();

    var t = tierFor(chosen());
    var note = document.getElementById('tier-note');
    if (u) {
      note.textContent = t.name + ' — ' + t.blurb + ' · ' + nfmt(t.cost) + ' credits per ' + (mode === 'chat' ? 'message' : 'image');
      sel.disabled = false;
    } else {
      note.textContent = 'Guest mode: ' + GUEST_LIMIT + ' free messages on Astral Lite. Log in to unlock higher tiers.';
      sel.disabled = true;
    }
  }

  /* ---------- send ---------- */
  function send(text) {
    text = (text || '').trim();
    if (!text || busy) return;
    var need = tierFor(chosen()).cost;
    if (u && creditsLeft() < need) { $('paywall').classList.add('on'); return; }
    if (!u && creditsLeft() <= 0) { $('paywall').classList.add('on'); return; }

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
        img.alt = 'Image created with Digitalaikart AI';
        img.style.cssText = 'max-width:100%;border-radius:12px;margin-top:.4rem;display:block';
        wrap.appendChild(img);
        $('msgs').appendChild(wrap);
        $('msgs').scrollTop = $('msgs').scrollHeight;
      } else {
        var m = addMsg('ai', payload.reply);
        linkify(m);
      }
      if (payload.conversation_id) convoId = payload.conversation_id;
      if (D.profile && typeof payload.credits === 'number') D.profile.tokens = payload.credits;
      else if (!D.profile) { guest.used++; localStorage.setItem('dskAI_used', guest.used); }
      badge(); renderPicker();
      if (u) loadConvos();
      busy = false;
      if (creditsLeft() <= 0) setTimeout(function () { $('paywall').classList.add('on'); }, 900);
    }

    function fail(msg, code) {
      think.remove();
      addMsg('ai', msg);
      busy = false;
      if (code === 'not_enough_credits' || code === 'guest_limit') {
        setTimeout(function () { $('paywall').classList.add('on'); }, 700);
      }
    }

    function call(token) {
      var headers = { 'Content-Type': 'application/json' };
      if (token) headers.Authorization = 'Bearer ' + token;
      return fetch(FN, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({ kind: mode, tier: chosen(), prompt: text, conversation_id: convoId })
      }).then(function (r) { return r.json(); });
    }

    var p = D.client ? D.client().auth.getSession() : Promise.resolve({ data: {} });
    p.then(function (s) {
      var token = s.data && s.data.session ? s.data.session.access_token : null;
      return call(token);
    }).then(function (b) {
      if (b.reply || b.image) return finish(b);
      if (b.error === 'not_enough_credits') return fail('You are out of credits. Upgrade to keep going — plans start at ₹199/month.', b.error);
      if (b.error === 'guest_limit') return fail('You have used your ' + GUEST_LIMIT + ' free guest messages. Create a free account to keep chatting.', b.error);
      if (b.error === 'ai_not_configured') return fail('The assistant is being set up right now — please try again shortly.', b.error);
      fail('Sorry, something went wrong. Please try again.', b.error);
    }).catch(function () {
      fail('Network error — check your internet and try again.');
    });
  }

  /* ---------- settings ---------- */
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

  function start() {
    u = D.user;
    if (!u) { showChat(); badge(); renderPicker(); newChat(); return; }
    showChat(); badge(); renderPicker(); renderSettings();
    loadConvos().then(function () {
      if (convos.length) openConvo(convos[0].id); else newChat();
    });
  }
  window.DSK_START = start;

  document.addEventListener('DOMContentLoaded', function () {
    buildSidebar();
    buildPicker();
    $('ai-send').onclick = function () { send($('ai-in').value); };
    $('ai-in').addEventListener('keydown', function (e) { if (e.key === 'Enter') send($('ai-in').value); });
    document.querySelectorAll('.ai-suggest button').forEach(function (b) {
      b.onclick = function () { send(b.dataset.q || b.textContent); };
    });
    $('btn-later').onclick = function () { $('paywall').classList.remove('on'); };
    $('btn-logout').onclick = function () { D.logout(); };
    $('btn-new').onclick = function () { newChat(); };
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
