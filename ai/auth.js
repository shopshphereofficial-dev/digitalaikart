/* Digitalaikart AI — accounts and profiles, backed by Supabase.
 *
 * This file contains NO secrets. The project URL and the anon key are public
 * by design — they are meant to be visible in the browser, and every real
 * permission decision is made by row-level security on the database (the
 * browser can read its own profile and nothing else; tokens are written only
 * by the server).
 */
window.DSK = (function () {
  'use strict';

  var SB_URL = 'https://guoxqlojsslwetlymbvj.supabase.co';
  var SB_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd1b3hxbG9qc3Nsd2V0bHltYnZqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTE5NzQyMDQsImV4cCI6MjEwNzU1MDIwNH0.iSDgjCsyEjKaawt6RKdYPpivqnVCCvwQcR45KCBgsqU';

  /* What each plan gets. The server enforces the real numbers; this is only
     for showing the user where they stand. */
  var PLANS = {
    free:     { name: 'FREE',     tokens: 5,    mem: 12, role: false, products: [] },
    starter:  { name: 'STARTER',  tokens: 400,  mem: 12, role: false, products: [['AI Job Hunt Kit', '/downloads/ai-job-hunt-kit.pdf']] },
    pro:      { name: 'PRO',      tokens: 700,  mem: 30, role: true,  products: [['AI Job Hunt Kit', '/downloads/ai-job-hunt-kit.pdf']] },
    ultimate: { name: 'ULTIMATE', tokens: 1600, mem: 50, role: true,  products: [['AI Job Hunt Kit', '/downloads/ai-job-hunt-kit.pdf'], ['GPT-6 Astra Guide', '/GPT6_Astra_Zero_to_Hero_Guide_FINAL.pdf']] }
  };

  var D = { PLANS: PLANS, ready: false, user: null, profile: null, sb: null };

  function client() {
    /* exposed below as D.client so chat.js can reuse the same session */
    if (!D.sb) {
      D.sb = window.supabase.createClient(SB_URL, SB_KEY, {
        auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true }
      });
    }
    return D.sb;
  }

  function ym() { var d = new Date(); return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0'); }
  D.ym = ym;

  D.loadProfile = function () {
    return client().from('profiles').select('id,name,email,phone,plan,tokens,tokens_month,role').eq('id', D.user.id).maybeSingle()
      .then(function (r) { D.profile = r.data || null; return D.profile; });
  };

  D.saveProfile = function (patch) {
    if (!D.profile) return Promise.resolve();
    return client().from('profiles').update(patch).eq('id', D.user.id).then(function () {
      Object.assign(D.profile, patch);
    });
  };

  /* ---------- auth UI ---------- */
  var $ = function (id) { return document.getElementById(id); };
  function am(t) { var e = $('auth-msg'); if (e) e.textContent = t || ''; }

  function afterAuth() { am(''); if (window.DSK_START) window.DSK_START(); }

  D.signup = function () {
    var name = $('su-name').value.trim(),
        email = $('su-email').value.trim().toLowerCase(),
        phone = $('su-phone').value.trim(),
        pass = $('su-pass').value;
    if (!name) return am('Please enter your name.');
    if (!email) return am('Please enter your email — it is how you log in.');
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return am('That email does not look right.');
    if (pass.length < 6) return am('Password must be at least 6 characters.');
    am('Creating your account...');
    client().auth.signUp({
      email: email,
      password: pass,
      options: { data: { name: name, phone: phone } }
    }).then(function (r) {
      if (r.error) {
        var m = r.error.message || '';
        if (/already|registered|exists/i.test(m)) return am('An account with this email already exists — try logging in.');
        return am(m || 'Could not create the account. Please try again.');
      }
      if (!r.data.session) {
        am('Almost done — we sent a confirmation link to ' + email + '. Click it, then log in here.');
        return;
      }
      D.user = r.data.user;
      return D.loadProfile().then(afterAuth);
    }).catch(function () { am('Could not reach the account server. Please try again.'); });
  };

  D.login = function () {
    var email = $('li-contact').value.trim().toLowerCase(), pass = $('li-pass').value;
    if (!email || !pass) return am('Enter your email and password.');
    am('Logging in...');
    client().auth.signInWithPassword({ email: email, password: pass }).then(function (r) {
      if (r.error) {
        var m = r.error.message || '';
        if (/invalid|credentials/i.test(m)) return am('Wrong email or password. (Forgot? WhatsApp us at +91 96826 00301)');
        if (/confirm/i.test(m)) return am('Please confirm your email first — check your inbox.');
        return am(m || 'Could not log in.');
      }
      D.user = r.data.user;
      return D.loadProfile().then(afterAuth);
    }).catch(function () { am('Could not reach the account server. Please try again.'); });
  };

  D.logout = function () {
    return client().auth.signOut().then(function () { location.href = '/ai/'; });
  };

  /* Google sign-in. Supabase runs the whole OAuth handshake, so no Google
     credential ever touches this page — the user just picks their account. */
  D.google = function () {
    am('Opening Google...');
    client().auth.signInWithOAuth({
      provider: 'google',
      options: { redirectTo: 'https://digitalkartai.shop/ai/' }
    }).then(function (r) {
      if (r.error) am('Google sign-in is not available yet. Please use email for now.');
    }).catch(function () { am('Could not reach Google. Please try again.'); });
  };

  D.readyCheck = function () {
    D.ready = !!(window.supabase);
    if (!D.ready) return Promise.resolve(null);
    return client().auth.getSession().then(function (r) {
      D.user = r.data && r.data.session ? r.data.session.user : null;
      if (!D.user) return null;
      return D.loadProfile().then(function () { return D.user; });
    });
  };

  document.addEventListener('DOMContentLoaded', function () {
    $('tab-login').onclick = function () { $('tab-login').classList.add('on'); $('tab-signup').classList.remove('on'); $('form-login').style.display = ''; $('form-signup').style.display = 'none'; am(''); };
    $('tab-signup').onclick = function () { $('tab-signup').classList.add('on'); $('tab-login').classList.remove('on'); $('form-signup').style.display = ''; $('form-login').style.display = 'none'; am(''); };
    $('btn-login').onclick = D.login;
    $('btn-signup').onclick = D.signup;
    $('btn-google').onclick = D.google;
    $('li-pass').addEventListener('keydown', function (e) { if (e.key === 'Enter') D.login(); });
    $('su-pass').addEventListener('keydown', function (e) { if (e.key === 'Enter') D.signup(); });
  });

  D.client = client;
  return D;
})();
