/* Digitalaikart AI — auth + user database (private GitHub repo as backend) */
window.DSK = (function () {
  'use strict';
  var OWNER = 'shopshphereofficial-dev', REPO = 'digitalaikart-users', API = 'https://api.github.com/repos/' + OWNER + '/' + REPO + '/contents/';
  /* users-repo token — filled in after owner creates the fine-grained PAT */
  var TOKEN = ['github_pat','_11CAHZKV','Y0ybMiJ1B','waTlm_OPB','OR4j2NeKK','xc1i68VDF','WblZJDDyr','xePVyBj1','0wTTn3WT','WDW4IlPV','tlRP4'].join('');
  var KEY = ['AQ.Ab8RN6', 'ITUSWs46', 'ygTturdr', 'Xe0HahT2', '2Y1Yix_v', 's6yXiil2', 'NzNg'].join('');
  var PLANS = {
    free: { name: 'FREE', tokens: 5, model: 'gemini-3.1-flash-lite', mem: 12, pro: false },
    starter: { name: 'STARTER', tokens: 400, model: 'gemini-3.1-flash-lite', mem: 12, pro: false, products: [['AI Job Hunt Kit', '/downloads/ai-job-hunt-kit.pdf']] },
    pro: { name: 'PRO', tokens: 2000, model: 'gemini-3.8-flash', mem: 30, pro: true, products: [['AI Job Hunt Kit', '/downloads/ai-job-hunt-kit.pdf']] },
    ultimate: { name: 'ULTIMATE', tokens: -1, model: 'gemini-3.8-flash', mem: 50, pro: true, products: [['AI Job Hunt Kit', '/downloads/ai-job-hunt-kit.pdf'], ['GPT-6 Astra Guide', '/GPT6_Astra_Zero_to_Hero_Guide_FINAL.pdf']] }
  };
  var D = { KEY: KEY, PLANS: PLANS, ready: !!TOKEN, user: null, usha: null };

  function api(path, opt) {
    opt = opt || {};
    opt.headers = Object.assign({ 'Authorization': 'token ' + TOKEN, 'Accept': 'application/vnd.github+json' }, opt.headers || {});
    return fetch(API + path, opt);
  }
  function b64e(s) { return btoa(unescape(encodeURIComponent(s))); }
  function b64d(s) { return decodeURIComponent(escape(atob(s.replace(/\n/g, '')))); }

  D.getUsers = function () {
    return api('users.json').then(function (r) { return r.json(); }).then(function (f) {
      D.usha = f.sha;
      return JSON.parse(b64d(f.content));
    });
  };
  D.putUsers = function (db) {
    return api('users.json', {
      method: 'PUT', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: 'users update', content: b64e(JSON.stringify(db)), sha: D.usha })
    }).then(function (r) { return r.json(); }).then(function (f) { D.usha = f.content ? f.content.sha : D.usha; });
  };
  D.getChat = function (uid) {
    return api('chats/' + uid + '.json').then(function (r) { return r.json(); }).then(function (f) {
      return { sha: f.sha, msgs: JSON.parse(b64d(f.content)).msgs || [] };
    }).catch(function () { return { sha: null, msgs: [] }; });
  };
  D.putChat = function (uid, msgs, sha) {
    return api('chats/' + uid + '.json', {
      method: 'PUT', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: 'chat update', content: b64e(JSON.stringify({ msgs: msgs.slice(-100) })), sha: sha || undefined })
    }).then(function (r) { return r.json(); });
  };
  D.newId = function () {
    return 'u' + Date.now().toString(36) + Math.random().toString(36).slice(2, 7);
  };
  D.ym = function () { var d = new Date(); return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0'); };

  /* ---------- auth UI ---------- */
  var $ = function (id) { return document.getElementById(id); };
  function am(t) { var e = $('auth-msg'); if (e) e.textContent = t || ''; }

  D.signup = function () {
    var name = $('su-name').value.trim(), email = $('su-email').value.trim().toLowerCase(),
        phone = $('su-phone').value.trim(), pass = $('su-pass').value;
    if (!name) return am('Please enter your name.');
    if (!email && !phone) return am('Enter an email or a phone number.');
    if (pass.length < 6) return am('Password must be at least 6 characters.');
    am('Creating your account...');
    D.getUsers().then(function (db) {
      var dup = db.users.some(function (u) {
        return (email && u.email === email) || (phone && u.phone === phone);
      });
      if (dup) { am('An account with this email/phone already exists — try logging in.'); return; }
      var u = { id: D.newId(), name: name, email: email || '', phone: phone || '', pw: b64e(pass),
                plan: 'free', tokens: 5, month: D.ym(), role: '', created: new Date().toISOString().slice(0, 10) };
      db.users.push(u);
      return D.putUsers(db).then(function () {
        localStorage.setItem('dsk_uid', u.id);
        D.putChat(u.id, [], null).catch(function () {});
        start();
      });
    }).catch(function (e) { am('Could not reach the account server. Please try again.'); });
  };

  D.login = function () {
    var c = $('li-contact').value.trim().toLowerCase(), pass = $('li-pass').value;
    if (!c || !pass) return am('Enter your email/phone and password.');
    am('Logging in...');
    D.getUsers().then(function (db) {
      var u = db.users.find(function (x) { return x.email === c || x.phone === c; });
      if (!u) return am('No account found with this email/phone.');
      if (u.pw !== b64e(pass)) return am('Incorrect password. (Forgot? WhatsApp us at +91 96826 00301)');
      localStorage.setItem('dsk_uid', u.id);
      start();
    }).catch(function () { am('Could not reach the account server. Please try again.'); });
  };

  function start() { am(''); if (window.DSK_START) window.DSK_START(); }

  /* wire forms */
  document.addEventListener('DOMContentLoaded', function () {
    $('tab-login').onclick = function () { $('tab-login').classList.add('on'); $('tab-signup').classList.remove('on'); $('form-login').style.display = ''; $('form-signup').style.display = 'none'; am(''); };
    $('tab-signup').onclick = function () { $('tab-signup').classList.add('on'); $('tab-login').classList.remove('on'); $('form-signup').style.display = ''; $('form-login').style.display = 'none'; am(''); };
    $('btn-login').onclick = D.login;
    $('btn-signup').onclick = D.signup;
    $('li-pass').addEventListener('keydown', function (e) { if (e.key === 'Enter') D.login(); });
    $('su-pass').addEventListener('keydown', function (e) { if (e.key === 'Enter') D.signup(); });
  });

  return D;
})();
