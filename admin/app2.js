/* Digitalaikart Admin — Part 2: products & blog management */
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

  /* ---- add product ---- */
  $('btn-add-product').addEventListener('click', function () {
    var name = $('np-name').value.trim(), tag = $('np-tag').value.trim();
    var price = $('np-price').value.trim(), mrp = $('np-mrp').value.trim();
    var feats = $('np-feat').value.split('\n').map(function (s) { return s.trim(); }).filter(Boolean);
    var rzp = $('np-rzp').value.trim();
    if (!name || !tag || !price) { A.toast('Naam, tagline aur price zaroori hain'); return; }
    var slug = A.slugify(name);
    if (slug.length < 3) { A.toast('Naam se slug nahi ban raha — English naam try karo'); return; }
    var buy = rzp || 'https://wa.me/919682600301';
    A.spin(true);

    var off = mrp && parseInt(mrp, 10) > parseInt(price, 10) ? Math.round((1 - price / mrp) * 100) + '% OFF' : 'NEW';
    var featsCard = feats.slice(0, 5).map(function (f) { return '<li>' + A.esc(f) + '</li>'; }).join('\n');
    var page = pageTemplate(name, tag, slug, price, mrp, feats, buy, off);

    A.putF('products/' + slug + '/index.html', page, 'Admin: new product page (' + name + ')').then(function () {
      return A.getF('products/index.html').then(function (f) {
        var doc = A.parse(f.c), grid = doc.querySelector('.product-grid');
        if (!grid) throw new Error('products page me .product-grid nahi mila');
        var c = doc.createElement('div'); c.className = 'card tilt';
        c.innerHTML =
          '<div class="card-img"><span class="card-badge">' + A.esc(off) + '</span></div>' +
          '<div class="card-body"><h3 class="card-title">' + A.esc(name) + '</h3>' +
          '<p class="card-desc">' + A.esc(tag) + '</p>' +
          '<ul class="card-features">' + featsCard + '</ul>' +
          '<div class="price-row"><span class="price">\u20B9' + A.esc(price) + '</span>' + (mrp ? '<span class="price-old">\u20B9' + A.esc(mrp) + '</span>' : '') + '<span class="price-label">one-time</span></div>' +
          '<a href="/products/' + slug + '/" class="btn btn-gold">View Details &rarr;</a></div>';
        grid.insertBefore(c, grid.firstChild);
        return A.putF('products/index.html', A.serialize(doc), 'Admin: add product card (' + name + ')', f.sha);
      });
    }).then(function () {
      return A.getF('products.json').then(function (f) {
        var j = JSON.parse(f.c);
        j.products = j.products || [];
        j.products.push({ slug: slug, name: name, tagline: tag, price: '\u20B9' + price, mrp: '\u20B9' + (mrp || price), url: '/products/' + slug + '/', topics: [name.toLowerCase()].concat(feats.map(function (x) { return x.toLowerCase(); })) });
        return A.putF('products.json', JSON.stringify(j, null, 2), 'Admin: add to products.json (' + slug + ')', f.sha);
      });
    }).then(function () {
      return A.getF('sitemap.xml').then(function (f) {
        var x = f.c.replace('</urlset>', '  <url><loc>' + A.SITE + '/products/' + slug + '/</loc><lastmod>' + new Date().toISOString().slice(0, 10) + '</lastmod><priority>0.9</priority></url>\n</urlset>');
        return A.putF('sitemap.xml', x, 'Admin: add sitemap entry (' + slug + ')', f.sha);
      });
    }).then(function () {
      A.spin(false); A.toast('Naya product live! 🎉');
      ['np-name', 'np-tag', 'np-price', 'np-mrp', 'np-feat', 'np-rzp'].forEach(function (id) { $(id).value = ''; });
      loadProducts();
    }).catch(function (e) { A.spin(false); A.toast(e.message); });
  });

  function pageTemplate(name, tag, slug, price, mrp, feats, buy, off) {
    var featsLi = feats.map(function (f) { return '      <li>' + A.esc(f) + '</li>'; }).join('\n');
    var featsCards = feats.map(function (f) { return '    <div class="feature-card"><p>' + A.esc(f) + '</p></div>'; }).join('\n');
    return '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>' + A.esc(name) + ' | Digitalaikart</title>\n<meta name="description" content="' + A.esc(tag) + '">\n<link rel="canonical" href="' + A.SITE + '/products/' + slug + '/">\n<meta property="og:title" content="' + A.esc(name) + '">\n<meta property="og:description" content="' + A.esc(tag) + '">\n<meta property="og:type" content="website">\n<link rel="stylesheet" href="/assets/style.css">\n</head>\n<body>\n<nav class="nav"><div class="nav-inner"><a href="/" class="nav-logo">Digitalaikart</a><div class="nav-links"><a href="/">Home</a><a href="/products/" class="active">Products</a><a href="/blog/">Blog</a></div></div></nav>\n<section class="product-hero">\n  <div class="product-info">\n    <h1>' + A.esc(name) + '</h1>\n    <p>' + A.esc(tag) + '</p>\n    <ul class="chapter-list">\n' + featsLi + '\n    </ul>\n    <div class="pricing-grid">\n      <div class="pricing-card featured tilt">\n        <span class="pricing-badge">' + A.esc(off) + '</span>\n        <div class="price">\u20B9' + A.esc(price) + '</div>\n        <div class="price-note">' + (mrp ? '<s>\u20B9' + A.esc(mrp) + '</s> ' : '') + 'one-time payment</div>\n        <a href="' + A.esc(buy) + '" class="btn btn-gold">Buy Now</a>\n      </div>\n    </div>\n  </div>\n</section>\n<section class="section">\n  <h2 class="section-title">What\u2019s Inside</h2>\n  <div class="gold-divider"></div>\n  <div class="feature-grid">\n' + featsCards + '\n  </div>\n</section>\n<section class="section">\n  <h2 class="section-title">Order & Support</h2>\n  <div class="gold-divider"></div>\n  <p style="text-align:center;max-width:640px;margin:0 auto;color:#334155">Koi sawaal? WhatsApp karo: <a href="https://wa.me/919682600301">+91 96826 00301</a></p>\n</section>\n<footer><div class="footer-links"><a href="/">Home</a><a href="/products/">Products</a><a href="/blog/">Blog</a><a href="/privacy-policy.html">Privacy Policy</a><a href="/refund-policy.html">Refund Policy</a><a href="/terms.html">Terms & Conditions</a></div><p><strong>Digitalaikart</strong> \u2014 Premium AI Digital Products</p><p>Feedback & Inquiries: <a href="mailto:lonefaisal977@gmail.com">lonefaisal977@gmail.com</a> | WhatsApp: <a href="https://wa.me/919682600301">+91 96826 00301</a></p><p style="margin-top:0.5rem;color:#334155">&copy; 2026 Digitalaikart. All rights reserved.</p></footer>\n<script src="/assets/effects.js"><\/script>\n</body>\n</html>';
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
