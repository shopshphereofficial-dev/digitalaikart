/* Digitalaikart AI — chat engine (plans, tokens, memory, custom role) */
(function () {
  'use strict';
  var D = window.DSK, $ = function (id) { return document.getElementById(id); };
  var u = null, chatSha = null, msgs = [], busy = false, guest = { used: +(localStorage.getItem('dskAI_used') || 0), hist: [] };
  var GUEST_LIMIT = 5;

  function toast(t) { var e = $('toast'); e.textContent = t; e.classList.add('on'); setTimeout(function () { e.classList.remove('on'); }, 2600); }
  function plan() { return D.PLANS[(u && u.plan) || 'free']; }
  function tokensLeft() { return u ? (plan().tokens === -1 ? Infinity : u.tokens) : Math.max(0, GUEST_LIMIT - guest.used); }

  function badge() {
    $('plan-badge').textContent = u ? plan().name + ' PLAN' : 'GUEST MODE';
    $('tok-badge').textContent = tokensLeft() === Infinity ? '∞ tokens' : tokensLeft() + ' token' + (tokensLeft() === 1 ? '' : 's') + ' left';
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
  function hist() { return u ? msgs : guest.hist; }

  function showChat() { $('auth-screen').style.display = 'none'; $('chat-screen').style.display = 'flex'; }
  function showAuth() { $('chat-screen').style.display = 'none'; $('auth-screen').style.display = 'block'; }

  function persist() {
    if (!u) return;
    var save = msgs.map(function (m) { return { r: m.r, t: m.t }; });
    D.putChat(u.id, save, chatSha).then(function (r) {
      if (r && r.content) chatSha = r.content.sha;
    }).catch(function () {});
    D.getUsers().then(function (db) {
      var me = db.users.find(function (x) { return x.id === u.id; });
      if (me) { me.tokens = u.tokens; me.plan = u.plan; me.month = u.month; me.role = u.role || ''; me.name = u.name; D.putUsers(db); }
    }).catch(function () {});
  }

  function monthlyReset() {
    var ym = D.ym();
    if (u.month !== ym) { u.month = ym; u.tokens = plan().tokens === -1 ? -1 : plan().tokens; persist(); }
  }

  function loadChat() {
    $('msgs').innerHTML = '';
    if (u) {
      D.getChat(u.id).then(function (c) {
        chatSha = c.sha; msgs = c.msgs;
        if (!msgs.length) msgs = [{ r: 'a', t: 'Welcome back' }];
        msgs.forEach(function (m) { var e = addMsg(m.r, m.t); if (m.r === 'a') linkify(e); });
        if (msgs.length <= 1) addMsg('a', 'Hello ' + (u.name || '') + '! Ask me anything — AI tools, career, study help, or business ideas.');
      });
    } else if (guest.hist.length) {
      guest.hist.forEach(function (m) { var e = addMsg(m.r, m.t); if (m.r === 'a') linkify(e); });
    }
  }

  function send(text) {
    text = (text || '').trim();
    if (!text || busy) return;
    var left = tokensLeft();
    if (left <= 0) { $('paywall').classList.add('on'); return; }
    busy = true;
    addMsg('user', text);
    $('ai-in').value = '';
    var h = hist(); h.push({ r: 'u', t: text });
    var think = addMsg('ai', 'Thinking...', 'thinking');
    var SYS = "You are Digitalaikart AI, the assistant for digitalkartai.shop — an Indian digital products store. STRICT RULES: (1) Reply in the SAME language the user writes in. (2) Be SHORT and direct: 2-6 lines by default. No greetings, no repeating the question, no filler. Longer only if clearly asked. (3) Products you know: 'GPT-6 Astra Guide' (₹149, complete 108-page GPT-6 guide, https://digitalkartai.shop/products/gpt-6-astra-guide/) and 'AI Job Hunt Kit' (₹99, 60 AI prompts for resume/interviews/LinkedIn, https://digitalkartai.shop/products/ai-job-hunt-kit/). If the question relates, recommend the matching product ONCE with its link. Never invent products or prices. (4) You help with AI/tech, career advice, study help, business ideas. Be accurate; if unsure, say so.";
    if (u && plan().pro && u.role) SYS = "Custom role set by user: " + u.role + "\n\n" + SYS;
    var p = plan();
    var contents = h.slice(-p.mem).map(function (m) {
      return { role: m.r === 'u' ? 'user' : 'model', parts: [{ text: m.t }] };
    });
    fetch('https://generativelanguage.googleapis.com/v1beta/models/' + p.model + ':generateContent?key=' + D.KEY, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ systemInstruction: { parts: [{ text: SYS }] }, contents: contents, generationConfig: { maxOutputTokens: 600, temperature: 0.7 } })
    }).then(function (r) { return r.json(); }).then(function (d) {
      think.remove();
      var c = d.candidates && d.candidates[0], txt = '';
      if (c && c.content && c.content.parts) c.content.parts.forEach(function (x) { if (x.text) txt += x.text; });
      txt = txt || ('Sorry, no answer received. ' + (d.error && d.error.message ? d.error.message : 'Please try again.'));
      var m = addMsg('ai', txt); linkify(m);
      h.push({ r: 'a', t: txt });
      if (u) { if (u.tokens > 0) u.tokens = Math.max(0, u.tokens - 1); }
      else { guest.used++; localStorage.setItem('dskAI_used', guest.used); }
      badge(); persist(); busy = false;
      if (tokensLeft() <= 0) setTimeout(function () { $('paywall').classList.add('on'); }, 900);
    }).catch(function () {
      think.remove(); addMsg('ai', 'Network error — check your internet and try again.'); busy = false;
    });
  }

  /* ---------- boot ---------- */
  function boot() {
    if (!D.ready) {
      /* backend token not configured yet — guest-only mode */
      showChat(); badge(); loadChat();
      toast('Login system is almost live — for now, enjoy ' + GUEST_LIMIT + ' free guest messages.');
      return;
    }
    var uid = localStorage.getItem('dsk_uid');
    if (!uid) { showAuth(); return; }
    D.getUsers().then(function (db) {
      u = db.users.find(function (x) { return x.id === uid; });
      if (!u) { localStorage.removeItem('dsk_uid'); showAuth(); return; }
      /* payment return: ?upgraded=plan */
      var up = new URLSearchParams(location.search).get('upgraded');
      if (up && D.PLANS[up] && up !== 'free') { u.plan = up; u.tokens = D.PLANS[up].tokens; }
      monthlyReset();
      showChat(); badge(); loadChat(); renderSettings();
      if (up && D.PLANS[up]) { toast('🎉 ' + D.PLANS[up].name + ' plan activated! Tokens refilled.'); history.replaceState(null, '', '/ai/'); persist(); }
    }).catch(function () { showAuth(); toast('Account server busy — try again.'); });
  }

  function renderSettings() {
    $('set-name').value = (u && u.name) || '';
    var ta = $('set-role');
    ta.value = (u && u.role) || '';
    if (u && plan().pro) { ta.disabled = false; ta.placeholder = 'e.g. You are my strict startup mentor. Give blunt, actionable advice.'; }
    else { ta.disabled = true; ta.placeholder = 'Custom AI role is available on Pro and Ultimate plans.'; }
    var fp = $('free-prods');
    fp.innerHTML = '';
    if (u && plan().products) {
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

  document.addEventListener('DOMContentLoaded', function () {
    $('ai-send').onclick = function () { send($('ai-in').value); };
    $('ai-in').addEventListener('keydown', function (e) { if (e.key === 'Enter') send($('ai-in').value); });
    document.querySelectorAll('.ai-suggest button').forEach(function (b) {
      b.onclick = function () { send(b.dataset.q || b.textContent); };
    });
    $('btn-later').onclick = function () { $('paywall').classList.remove('on'); };
    $('btn-logout').onclick = function () { localStorage.removeItem('dsk_uid'); location.href = '/ai/'; };
    $('btn-new').onclick = function () {
      if (u) { D.putChat(u.id, [], chatSha).catch(function () {}); }
      location.reload();
    };
    $('btn-settings').onclick = function () { renderSettings(); $('settings').classList.add('on'); };
    $('set-close').onclick = function () { $('settings').classList.remove('on'); };
    $('set-save').onclick = function () {
      if (!u) return;
      var n = $('set-name').value.trim(); if (n) u.name = n;
      if (plan().pro) u.role = $('set-role').value.trim().slice(0, 500);
      persist(); toast('Saved!'); $('settings').classList.remove('on');
    };
    boot();
  });
})();
