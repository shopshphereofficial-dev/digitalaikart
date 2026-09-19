/* Digitalaikart Admin — Part 1: helpers, GitHub API, auth, tabs, settings */
(function () {
  'use strict';
  var API = 'https://api.github.com/repos/shopshphereofficial-dev/digitalaikart';
  var SITE = 'https://digitalkartai.shop';
  var LS_TOK = 'dskA_token', LS_PIN = 'dskA_pin', SS_OK = 'dskA_unlocked';
  var TOKEN = localStorage.getItem(LS_TOK) || '';
  function setTok(t) { TOKEN = t; localStorage.setItem(LS_TOK, t); }
  var $ = function (id) { return document.getElementById(id); };

  /* ---- helpers ---- */
  function toast(m) { var t = $('toast'); t.textContent = m; t.style.display = 'block'; setTimeout(function () { t.style.display = 'none'; }, 3500); }
  function spin(on) { $('spin').style.display = on ? 'flex' : 'none'; }
  function b64e(s) { var b = new TextEncoder().encode(s), o = ''; for (var i = 0; i < b.length; i++) o += String.fromCharCode(b[i]); return btoa(o); }
  function b64d(s) { var b = atob(String(s).replace(/\s/g, '')), a = new Uint8Array(b.length); for (var i = 0; i < b.length; i++) a[i] = b.charCodeAt(i); return new TextDecoder().decode(a); }
  function sha256(s) { return crypto.subtle.digest('SHA-256', new TextEncoder().encode(s)).then(function (b) { return Array.from(new Uint8Array(b)).map(function (x) { return x.toString(16).padStart(2, '0'); }).join(''); }); }
  function esc(s) { var d = document.createElement('div'); d.textContent = s == null ? '' : String(s); return d.innerHTML; }
  function slugify(s) { return String(s).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 60); }
  function parse(html) { return new DOMParser().parseFromString(html, 'text/html'); }
  function serialize(doc) { return '<!DOCTYPE html>\n' + doc.documentElement.outerHTML; }

  /* ---- GitHub API ---- */
  function gh(method, path, body) {
    return fetch(API + path, {
      method: method,
      headers: { 'Authorization': 'Bearer ' + TOKEN, 'Accept': 'application/vnd.github+json', 'Content-Type': 'application/json' },
      body: body ? JSON.stringify(body) : undefined
    }).then(function (r) {
      if (r.status === 401) throw new Error('Token galat/expired — Settings me naya token daalo');
      if (r.status === 204 || (r.status === 404 && method === 'DELETE')) return null;
      if (!r.ok) return r.text().then(function (t) { throw new Error('GitHub ' + r.status + ': ' + t.slice(0, 160)); });
      return r.json();
    });
  }
  function getF(path) {
    return gh('GET', '/contents/' + path + '?ref=main&t=' + Date.now()).then(function (j) { return { c: b64d(j.content), sha: j.sha }; });
  }
  function putF(path, content, msg, sha) {
    var b = { message: msg, content: b64e(content), branch: 'main' };
    if (sha) b.sha = sha;
    return gh('PUT', '/contents/' + path, b);
  }
  function delF(path, msg, sha) {
    if (sha) return gh('DELETE', '/contents/' + path, { message: msg, sha: sha, branch: 'main' });
    return getF(path).then(function (f) { return gh('DELETE', '/contents/' + path, { message: msg, sha: f.sha, branch: 'main' }); });
  }

  /* ---- screens ---- */
  function show(which) {
    ['scr-setup', 'scr-lock', 'scr-app'].forEach(function (id) { $(id).classList.add('hide'); });
    $(which).classList.remove('hide');
    $('tabs').classList.toggle('hide', which !== 'scr-app');
  }
  function boot() {
    if (!TOKEN || !localStorage.getItem(LS_PIN)) { show('scr-setup'); return; }
    if (sessionStorage.getItem(SS_OK) === '1') { show('scr-app'); return; }
    show('scr-lock'); setTimeout(function () { $('in-pin').focus(); }, 80);
  }

  /* ---- setup ---- */
  $('btn-setup').addEventListener('click', function () {
    var t = $('in-token').value.trim(), p1 = $('in-pin1').value.trim(), p2 = $('in-pin2').value.trim();
    if (!t || t.length < 20) { toast('Pehle token paste karo'); return; }
    if (!/^\d{4,8}$/.test(p1)) { toast('PIN 4 se 8 digit ka hona chahiye'); return; }
    if (p1 !== p2) { toast('PIN match nahi kar rahe'); return; }
    spin(true);
    var oldTok = TOKEN; TOKEN = t;
    gh('GET', '/contents/products.json?ref=main').then(function () {
      return sha256(p1);
    }).then(function (h) {
      localStorage.setItem(LS_PIN, h); setTok(t); sessionStorage.setItem(SS_OK, '1');
      spin(false); boot(); toast('Setup complete! Welcome boss 😎');
    }).catch(function (e) { TOKEN = oldTok; spin(false); toast(e.message); });
  });

  /* ---- lock/unlock ---- */
  $('in-pin').addEventListener('input', function () {
    var v = this.value;
    renderDots(v.length);
    if (v.length < 4) return;
    sha256(v).then(function (h) {
      if (h === localStorage.getItem(LS_PIN)) { sessionStorage.setItem(SS_OK, '1'); $('in-pin').value = ''; renderDots(0); boot(); }
      else { $('in-pin').value = ''; renderDots(0); toast('Galat PIN 🚫'); }
    });
  });
  function renderDots(n) {
    var el = $('pin-dots'); el.innerHTML = '';
    for (var i = 0; i < 6; i++) {
      var d = document.createElement('span');
      d.style.cssText = 'width:12px;height:12px;border-radius:50%;border:2px solid ' + (i < n ? '#f5c542' : 'rgba(255,255,255,.18)') + ';background:' + (i < n ? '#f5c542' : 'none');
      el.appendChild(d);
    }
  }
  renderDots(0);

  function wipe() {
    if (!confirm('Pakka? Token + PIN sab delete ho jayega. (Site pe koi asar nahi)')) return;
    localStorage.removeItem(LS_TOK); localStorage.removeItem(LS_PIN); sessionStorage.removeItem(SS_OK); location.reload();
  }
  $('btn-wipe').addEventListener('click', wipe);
  $('btn-logout-full').addEventListener('click', wipe);
  $('btn-lock').addEventListener('click', function () { sessionStorage.removeItem(SS_OK); location.reload(); });
  $('btn-retoken').addEventListener('click', function () {
    var t = prompt('Naya token paste karo (github_pat_...)');
    if (!t) return;
    var oldTok = TOKEN; TOKEN = t.trim();
    spin(true);
    gh('GET', '/contents/products.json?ref=main').then(function () {
      setTok(TOKEN); spin(false); toast('Naya token save ho gaya ✅');
    }).catch(function (e) { TOKEN = oldTok; spin(false); toast(e.message); });
  });

  /* ---- tabs ---- */
  document.querySelectorAll('.tabs button').forEach(function (b) {
    b.addEventListener('click', function () {
      document.querySelectorAll('.tabs button').forEach(function (x) { x.classList.remove('on'); });
      b.classList.add('on');
      ['view-products', 'view-blog', 'view-settings'].forEach(function (id) { $(id).classList.add('hide'); });
      $('view-' + b.dataset.v).classList.remove('hide');
    });
  });

  $('tok-status').textContent = TOKEN ? ('Saved • ' + TOKEN.slice(0, 7) + '…' + TOKEN.slice(-4)) : 'Koi token nahi';

  /* ---- expose for part 2 ---- */
  window.__dskAdmin = {
    $: $, toast: toast, spin: spin, esc: esc, slugify: slugify, parse: parse, serialize: serialize,
    gh: gh, getF: getF, putF: putF, delF: delF, SITE: SITE, boot: boot
  };

  boot();
})();
