/* Digitalaikart — Google Analytics 4 (site-wide)
 * Loaded by /assets/effects.js so every page that has the site effects also has
 * analytics. Property "kidsafemirror" / web stream "Digital Kart" -> digitalkartai.shop
 */
(function () {
  if (window.__dakGA) return;
  window.__dakGA = true;

  var ID = 'G-WWDP6KR3EC';
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;

  gtag('js', new Date());
  gtag('config', ID, { anonymize_ip: true, send_page_view: true });

  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + ID;
  document.head.appendChild(s);

  function text(el) { return (el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 80); }

  /* product page view */
  if (location.pathname.indexOf('/products/') === 0) {
    gtag('event', 'view_item', {
      item_id: location.pathname,
      item_name: (document.querySelector('.product-info h1') || {}).textContent || document.title
    });
  }

  /* clicks: checkout / contact / product selection / outbound */
  document.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('a,button') : null;
    if (!a) return;
    var label = text(a);
    var href = a.getAttribute('href') || '';
    if (/buy|checkout|cart|pay now|get your copy|order/i.test(label + ' ' + href)) {
      gtag('event', 'begin_checkout', { link_text: label, link_url: href, item_id: location.pathname });
    } else if (/wa\.me|whatsapp/i.test(href)) {
      gtag('event', 'contact_whatsapp', { link_url: href });
    } else if (href.indexOf('/products/') === 0) {
      gtag('event', 'select_content', { content_type: 'product', item_id: href });
    }
    if (/^https?:\/\//i.test(href) && href.indexOf(location.hostname) === -1) {
      gtag('event', 'click_outbound', { link_url: href });
    }
  }, true);

  /* newsletter / contact form submits, if any are added later */
  document.addEventListener('submit', function (e) {
    var f = e.target;
    if (!f || !f.querySelector) return;
    gtag('event', 'form_submit', { form_id: f.id || f.name || location.pathname });
  }, true);
})();
