/* Digitalaikart Admin — Part 2: products (edit/delete) & blog management */
(function () {
  'use strict';
  var A = window.__dskAdmin;
  var $ = A.$;

  /* ================= PRODUCTS ================= */
  var prodDoc = null, prodSha = null;
  $('btn-load-products').addEventListener('click', loadProducts);
  function loadProducts() {
    A.spin(true);
    A.getF('products/index.html').then(function (f) {
      prodDoc = A.parse(f.c); prodSha = f.sha;
      var grid = prodDoc.querySelector('.product-grid');
      var cards = grid ? Array.from(grid.querySelectorAll('.card')) : [];
      var box = $('prod-list'); box.innerHTML = '';
      if (!cards.length) box.innerHTML = '<p class="muted">Koi product card nahi mila.</p>';
      cards.forEach(function (card, idx) {
        var aEl = card.querySelector('a[href^="/products/"]');
        var url = aEl ? aEl.getAttribute('href') : '';
        var t = card.querySelector('.card-title'), d = card.querySelector('.card-desc');
        var pr = card.querySelector('.price'), po = card.querySelector('.price-old');
        var feats = Array.from(card.querySelectorAll('.card-features li')).map(function (li) { return li.textContent; });
        var el = document.createElement('div'); el.className = 'card';
        el.innerHTML =
          '<div class="row"><span class="pill">#' + (idx + 1) + '</span><span class="muted">' + A.esc(url) + '</span></div>' +
          '<label style="margin-top:.7rem">Naam</label><input data-k="title" value="' + A.esc(t ? t.textContent : '') + '">' +
          '<label>Description</label><textarea data-k="desc" rows="2">' + A.esc(d ? d.textContent : '') + '</textarea>' +
          '<label>Price (₹)</label><input data-k="price" inputmode="numeric" value="' + A.esc(pr ? pr.textContent.replace(/[^\d.]/g, '') : '') + '">' +
          '<label>Purana price / MRP (₹)</label><input data-k="old" inputmode="numeric" value="' + A.esc(po ? po.textContent.replace(/[^\d.]/g, '') : '') + '">' +
          '<label>Features (har line ek)</label><textarea data-k="feat" rows="4">' + A.esc(feats.join('\n')) + '</textarea>' +
          '<button class="btn btn-gold btn-save" data-i="' + idx + '">Save &rarr; Site Update</button>' +
          '<button class="btn btn-danger btn-del" data-i="' + idx + '">Delete Product</button>';
        box.appendChild(el);
      });
      A.spin(false); A.toast(cards.length + ' products load hue');
    }).catch(function (e) { A.spin(false); A.toast(e.message); });
  }

  function cardFrom(doc, i) { return doc.querySelectorAll('.product-grid .card')[i]; }

  document.addEventListener('click', function (ev) {
    if (!ev.target.closest) return;
    var b = ev.target.closest('.btn-save');
    if (b) { saveProduct(parseInt(b.dataset.i, 10), b.closest('.card')); return; }
    var d = ev.target.closest('.btn-del');
    if (d) deleteProduct(parseInt(d.dataset.i, 10));
  });

  function saveProduct(i, uiCard) {
    if (!prodDoc) return;
    var g = function (k) { var el = uiCard.querySelector('[data-k="' + k + '"]'); return el ? el.value.trim() : ''; };
    var card = cardFrom(prodDoc, i); if (!card) return;
    A.spin(true);
    var t = card.querySelector('.card-title'), d = card.querySelector('.card-desc');
    var pr = card.querySelector('.price'), po = card.querySelector('.price-old');
    var ul = card.querySelector('.card-features');
    var url = card.querySelector('a[href^="/products/"]').getAttribute('href');
    if (t) t.textContent = g('title');
    if (d) d.textContent = g('desc');
    if (pr) pr.textContent = '\u20B9' + g('price');
    if (po) { if (g('old')) po.textContent = '\u20B9' + g('old'); else po.remove(); }
    if (ul) {
      ul.innerHTML = '';
      g('feat').split('\n').map(function (s) { return s.trim(); }).filter(Boolean).forEach(function (line) {
        var li = prodDoc.createElement('li'); li.textContent = line; ul.appendChild(li);
      });
    }
    A.putF('products/index.html', A.serialize(prodDoc), 'Admin: update product card', prodSha).then(function (r) {
      prodSha = r.content.sha;
      return A.getF('products.json').then(function (f) {
        var j = JSON.parse(f.c);
        var slug = url.replace(/\/products\/|\/$/g, '');
        var hit = (j.products || []).filter(function (p) { return p.url === url || p.slug === slug; })[0];
        if (hit) {
          hit.name = g('title'); hit.tagline = g('desc'); hit.price = '\u20B9' + g('price'); hit.mrp = '\u20B9' + g('old');
          return A.putF('products.json', JSON.stringify(j, null, 2), 'Admin: sync products.json (' + slug + ')', f.sha);
        }
      });
    }).then(function () { A.spin(false); A.toast('Ho gaya! Site pe live ho jayega 1-2 min me ✅'); })
      .catch(function (e) { A.spin(false); A.toast(e.message); });
  }

  function deleteProduct(i) {
    if (!prodDoc) return;
    var card = cardFrom(prodDoc, i); if (!card) return;
    var url = card.querySelector('a[href^="/products/"]').getAttribute('href');
    if (!confirm('Ye product delete karna hai? (Page + card + sitemap — sab hata denge)')) return;
    A.spin(true);
    var slug = url.replace(/\/products\/|\/$/g, '');
    card.remove();
    A.putF('products/index.html', A.serialize(prodDoc), 'Admin: remove product card (' + slug + ')', prodSha).then(function (r) {
      prodSha = r.content.sha;
      return A.getF('products.json').then(function (f) {
        var j = JSON.parse(f.c);
        j.products = (j.products || []).filter(function (p) { return p.slug !== slug && p.url !== url; });
        return A.putF('products.json', JSON.stringify(j, null, 2), 'Admin: remove from products.json (' + slug + ')', f.sha);
      });
    }).then(function () {
      return A.getF('sitemap.xml').then(function (f) {
        var x = f.c.replace(new RegExp('[ \\t]*<url><loc>[^<]*' + slug + '[^<]*</loc>.*?</url>\\s*', ''), '');
        return A.putF('sitemap.xml', x, 'Admin: remove sitemap entry (' + slug + ')', f.sha);
      });
    }).then(function () {
      return A.getF('products/' + slug + '/index.html').then(function (f) { return A.delF('products/' + slug + '/index.html', 'Admin: delete product page (' + slug + ')', f.sha); });
    }).then(function () { A.spin(false); A.toast('Product delete ho gaya 🗑️'); loadProducts(); })
      .catch(function (e) { A.spin(false); A.toast('Delete: ' + e.message); });
  }

  /* ================= BLOG ================= */
  var blogDoc = null, blogSha = null;
  $('btn-load-blog').addEventListener('click', loadBlog);
  function loadBlog() {
    A.spin(true);
    A.getF('blog/index.html').then(function (f) {
      blogDoc = A.parse(f.c); blogSha = f.sha;
      var cards = Array.from(blogDoc.querySelectorAll('a.blog-card'));
      var box = $('blog-list'); box.innerHTML = '';
      if (!cards.length) box.innerHTML = '<p class="muted">Koi post nahi mila.</p>';
      cards.forEach(function (c) {
        var href = c.getAttribute('href') || '';
        var slug = (href.match(/\/blog\/([a-z0-9-]+)\.html/i) || [])[1] || '';
        var t = c.querySelector('h3'), d = c.querySelector('.date');
        var el = document.createElement('div'); el.className = 'list-item';
        el.innerHTML = '<div style="flex:1"><div class="t">' + (t ? A.esc(t.textContent) : href) + '</div><div class="d">' + (d ? A.esc(d.textContent) : '') + '</div><div class="views" data-slug="' + A.esc(slug) + '"></div></div><button class="del" data-href="' + A.esc(href) + '" title="Delete">\u2715</button>';
        box.appendChild(el);
        if (slug) fetch('https://abacus.jasoncameron.dev/get/digitalkartai.shop/' + slug).then(function (r) { return r.json(); }).then(function (j) {
          var el2 = box.querySelector('.views[data-slug="' + slug + '"]');
          if (el2 && typeof j.value === 'number') el2.textContent = '\uD83D\uDC41 ' + j.value + ' views';
        }).catch(function () {});
      });
      A.spin(false); A.toast(cards.length + ' posts mile');
    }).catch(function (e) { A.spin(false); A.toast(e.message); });
  }

  document.addEventListener('click', function (ev) {
    if (!ev.target.closest) return;
    var d = ev.target.closest('.list-item .del');
    if (!d) return;
    var href = d.dataset.href || d.getAttribute('data-href');
    if (!href || !confirm('Ye blog post delete karna hai? (File + card + sitemap)')) return;
    A.spin(true);
    var file = href.replace(/^\//, '');
    var card = Array.from(blogDoc.querySelectorAll('a.blog-card')).filter(function (c) { return c.getAttribute('href') === href; })[0];
    A.delF(file, 'Admin: delete blog post (' + file + ')').then(function () {
      if (card) card.remove();
      return A.putF('blog/index.html', A.serialize(blogDoc), 'Admin: remove blog card', blogSha);
    }).then(function () {
      return A.getF('sitemap.xml').then(function (f) {
        var loc = A.SITE + '/' + file;
        var x = f.c.replace(new RegExp('[ \\t]*<url><loc>' + loc.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '</loc>.*?</url>\\s*', ''), '');
        return A.putF('sitemap.xml', x, 'Admin: remove sitemap entry', f.sha);
      });
    }).then(function () { A.spin(false); A.toast('Post delete ho gaya 🗑️'); loadBlog(); })
      .catch(function (e) { A.spin(false); A.toast(e.message); });
  });
})();
