/* Digitalaikart Admin — Part 3: add product with image, video & PDF uploads */
(function () {
  'use strict';
  var A = window.__dskAdmin;
  var $ = A.$;

  function putF64(path, b64, msg) {
    return A.gh('PUT', '/contents/' + path, { message: msg, content: b64, branch: 'main' });
  }
  function fileToB64(file) {
    return new Promise(function (res, rej) {
      var fr = new FileReader();
      fr.onload = function () { res(String(fr.result).split(',')[1]); };
      fr.onerror = function () { rej(new Error('File read fail')); };
      fr.readAsDataURL(file);
    });
  }
  function imgToJpgB64(file, maxW) {
    return new Promise(function (res, rej) {
      var fr = new FileReader();
      fr.onload = function () {
        var img = new Image();
        img.onload = function () {
          var sc = Math.min(1, maxW / img.width);
          var cv = document.createElement('canvas');
          cv.width = Math.round(img.width * sc);
          cv.height = Math.round(img.height * sc);
          cv.getContext('2d').drawImage(img, 0, 0, cv.width, cv.height);
          res(cv.toDataURL('image/jpeg', 0.82).split(',')[1]);
        };
        img.onerror = function () { rej(new Error('Image nahi padhi')); };
        img.src = fr.result;
      };
      fr.onerror = function () { rej(new Error('File read fail')); };
      fr.readAsDataURL(file);
    });
  }
  function ytId(u) {
    var m = String(u || '').match(/(?:youtu\.be\/|youtube\.com\/(?:watch\?v=|embed\/|shorts\/))([A-Za-z0-9_-]{6,})/);
    return m ? m[1] : null;
  }

  $('btn-add-product').addEventListener('click', function () {
    var name = $('np-name').value.trim(), tag = $('np-tag').value.trim();
    var price = $('np-price').value.trim(), mrp = $('np-mrp').value.trim();
    var feats = $('np-feat').value.split('\n').map(function (s) { return s.trim(); }).filter(Boolean);
    var rzp = $('np-rzp').value.trim();
    var yt = $('np-yt').value.trim();
    var imgF = ($('np-img').files || [])[0] || null;
    var pdfF = ($('np-pdf').files || [])[0] || null;
    if (!name || !tag || !price) { A.toast('Naam, tagline aur price zaroori hain'); return; }
    var slug = A.slugify(name);
    if (slug.length < 3) { A.toast('Naam se slug nahi ban raha — English naam try karo'); return; }
    if (imgF && imgF.size > 8 * 1024 * 1024) { A.toast('Photo 8MB se chhoti lo (compress ho jayegi)'); return; }
    if (pdfF && pdfF.size > 20 * 1024 * 1024) { A.toast('PDF 20MB se chhoti honi chahiye'); return; }
    var buy = rzp || 'https://wa.me/919682600301';
    A.spin(true);

    var off = mrp && parseInt(mrp, 10) > parseInt(price, 10) ? Math.round((1 - price / mrp) * 100) + '% OFF' : 'NEW';
    var featsCard = feats.slice(0, 5).map(function (f) { return '<li>' + A.esc(f) + '</li>'; }).join('\n');
    var ytCode = yt ? ytId(yt) : null;
    if (yt && !ytCode) { A.spin(false); A.toast('YouTube link samajh nahi aaya — poora link paste karo'); return; }
    var imgB64 = null, pdfB64 = null;

    Promise.resolve()
      .then(function () { return imgF ? imgToJpgB64(imgF, 900).then(function (b) { imgB64 = b; }) : null; })
      .then(function () { return pdfF ? fileToB64(pdfF).then(function (b) { pdfB64 = b; }) : null; })
      .then(function () { return imgB64 ? putF64('assets/img/' + slug + '.jpg', imgB64, 'Admin: product image (' + slug + ')') : null; })
      .then(function () { return pdfB64 ? putF64('downloads/' + slug + '.pdf', pdfB64, 'Admin: product PDF (' + slug + ')') : null; })
      .then(function () {
        var page = pageTemplate(name, tag, slug, price, mrp, feats, buy, off, imgB64 ? ('/assets/img/' + slug + '.jpg') : null, ytCode);
        return A.putF('products/' + slug + '/index.html', page, 'Admin: new product page (' + name + ')');
      })
      .then(function () {
        return A.getF('products/index.html').then(function (f) {
          var doc = A.parse(f.c), grid = doc.querySelector('.product-grid');
          if (!grid) throw new Error('products page me .product-grid nahi mila');
          var c = doc.createElement('div'); c.className = 'card tilt';
          c.innerHTML =
            '<div class="card-img">' + (imgB64 ? '<img src="/assets/img/' + slug + '.jpg" alt="' + A.esc(name) + '" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">' : '') + '<span class="card-badge">' + A.esc(off) + '</span></div>' +
            '<div class="card-body"><h3 class="card-title">' + A.esc(name) + '</h3>' +
            '<p class="card-desc">' + A.esc(tag) + '</p>' +
            '<ul class="card-features">' + featsCard + '</ul>' +
            '<div class="price-row"><span class="price">\u20B9' + A.esc(price) + '</span>' + (mrp ? '<span class="price-old">\u20B9' + A.esc(mrp) + '</span>' : '') + '<span class="price-label">one-time</span></div>' +
            '<a href="/products/' + slug + '/" class="btn btn-gold">View Details &rarr;</a></div>';
          grid.insertBefore(c, grid.firstChild);
          return A.putF('products/index.html', A.serialize(doc), 'Admin: add product card (' + name + ')', f.sha);
        });
      })
      .then(function () {
        return A.getF('products.json').then(function (f) {
          var j = JSON.parse(f.c);
          j.products = j.products || [];
          j.products.push({ slug: slug, name: name, tagline: tag, price: '\u20B9' + price, mrp: '\u20B9' + (mrp || price), url: '/products/' + slug + '/', topics: [name.toLowerCase()].concat(feats.map(function (x) { return x.toLowerCase(); })) });
          return A.putF('products.json', JSON.stringify(j, null, 2), 'Admin: add to products.json (' + slug + ')', f.sha);
        });
      })
      .then(function () {
        return A.getF('sitemap.xml').then(function (f) {
          var x = f.c.replace('</urlset>', '  <url><loc>' + A.SITE + '/products/' + slug + '/</loc><lastmod>' + new Date().toISOString().slice(0, 10) + '</lastmod><priority>0.9</priority></url>\n</urlset>');
          return A.putF('sitemap.xml', x, 'Admin: add sitemap entry (' + slug + ')', f.sha);
        });
      })
      .then(function () {
        A.spin(false); A.toast('Naya product live! 🎉');
        if (pdfB64) setTimeout(function () { A.toast('PDF ka payment-link redirect: thank-you.html?product=' + slug + ' hona chahiye'); }, 4000);
        ['np-name', 'np-tag', 'np-price', 'np-mrp', 'np-feat', 'np-rzp', 'np-yt'].forEach(function (id) { $(id).value = ''; });
        ['np-img', 'np-pdf'].forEach(function (id) { $(id).value = ''; });
        var btn = document.getElementById('btn-load-products'); if (btn) btn.click();
      })
      .catch(function (e) { A.spin(false); A.toast(e.message); });
  });

  function pageTemplate(name, tag, slug, price, mrp, feats, buy, off, imgUrl, ytCode) {
    var featsLi = feats.map(function (f) { return '      <li>' + A.esc(f) + '</li>'; }).join('\n');
    var featsCards = feats.map(function (f) { return '    <div class="feature-card"><p>' + A.esc(f) + '</p></div>'; }).join('\n');
    var heroMedia = imgUrl
      ? '\n  <div><img src="' + imgUrl + '" alt="' + A.esc(name) + '" style="width:100%;border-radius:16px;box-shadow:0 24px 60px rgba(0,0,0,.5)"></div>'
      : '';
    var videoSec = ytCode
      ? '\n<section class="section">\n  <h2 class="section-title">Video Demo</h2>\n  <div class="gold-divider"></div>\n  <div style="max-width:720px;margin:0 auto">\n    <div style="position:relative;padding-top:56.25%;border-radius:14px;overflow:hidden">\n      <iframe src="https://www.youtube.com/embed/' + ytCode + '" style="position:absolute;inset:0;width:100%;height:100%;border:0" allowfullscreen title="Video"></iframe>\n    </div>\n  </div>\n</section>\n'
      : '';
    return '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>' + A.esc(name) + ' | Digitalaikart</title>\n<meta name="description" content="' + A.esc(tag) + '">\n<link rel="canonical" href="' + A.SITE + '/products/' + slug + '/">\n<meta property="og:title" content="' + A.esc(name) + '">\n<meta property="og:description" content="' + A.esc(tag) + '">\n<meta property="og:type" content="website">' + (imgUrl ? '\n<meta property="og:image" content="' + A.SITE + imgUrl + '">' : '') + '\n<link rel="stylesheet" href="/assets/style.css">\n</head>\n<body>\n<nav class="nav"><div class="nav-inner"><a href="/" class="nav-logo">Digitalaikart</a><div class="nav-links"><a href="/">Home</a><a href="/products/" class="active">Products</a><a href="/blog/">Blog</a></div></div></nav>\n<section class="product-hero">\n  <div class="product-info">\n    <h1>' + A.esc(name) + '</h1>\n    <p>' + A.esc(tag) + '</p>\n    <ul class="chapter-list">\n' + featsLi + '\n    </ul>\n    <div class="pricing-grid">\n      <div class="pricing-card featured tilt">\n        <span class="pricing-badge">' + A.esc(off) + '</span>\n        <div class="price">\u20B9' + A.esc(price) + '</div>\n        <div class="price-note">' + (mrp ? '<s>\u20B9' + A.esc(mrp) + '</s> ' : '') + 'one-time payment</div>\n        <a href="' + A.esc(buy) + '" class="btn btn-gold">Buy Now</a>\n      </div>\n    </div>\n  </div>' + heroMedia + '\n</section>\n<section class="section">\n  <h2 class="section-title">What\u2019s Inside</h2>\n  <div class="gold-divider"></div>\n  <div class="feature-grid">\n' + featsCards + '\n  </div>\n</section>' + videoSec + '\n<section class="section">\n  <h2 class="section-title">Order & Support</h2>\n  <div class="gold-divider"></div>\n  <p style="text-align:center;max-width:640px;margin:0 auto;color:#334155">Koi sawaal? WhatsApp karo: <a href="https://wa.me/919682600301">+91 96826 00301</a></p>\n</section>\n<footer><div class="footer-links"><a href="/">Home</a><a href="/products/">Products</a><a href="/blog/">Blog</a><a href="/privacy-policy.html">Privacy Policy</a><a href="/refund-policy.html">Refund Policy</a><a href="/terms.html">Terms & Conditions</a></div><p><strong>Digitalaikart</strong> \u2014 Premium AI Digital Products</p><p>Feedback & Inquiries: <a href="mailto:lonefaisal977@gmail.com">lonefaisal977@gmail.com</a> | WhatsApp: <a href="https://wa.me/919682600301">+91 96826 00301</a></p><p style="margin-top:0.5rem;color:#334155">&copy; 2026 Digitalaikart. All rights reserved.</p></footer>\n<script src="/assets/effects.js"><\/script>\n</body>\n</html>';
  }
})();
