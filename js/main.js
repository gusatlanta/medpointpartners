/* MedPoint Partners — Main JS (loaded on every page) */

// Mega menu tabs (called from onclick in the nav markup)
window.switchMegaTab = function (tab, btn) {
  var menu = btn.closest('.mega-menu') || document;
  menu.querySelectorAll('.mega-tab-btn').forEach(function (b) { b.classList.remove('active'); });
  menu.querySelectorAll('.mega-panel').forEach(function (p) { p.classList.remove('active'); });
  btn.classList.add('active');
  var panel = document.getElementById('mega-' + tab);
  if (panel) panel.classList.add('active');
};

(function () {
  // Scroll-aware navbar
  var navbar = document.querySelector('.navbar');
  if (navbar) {
    window.addEventListener('scroll', function () {
      navbar.classList.toggle('scrolled', window.scrollY > 10);
    }, { passive: true });
  }

  // Mobile nav toggle
  var toggle = document.querySelector('.nav-toggle');
  var menu = document.querySelector('.nav-menu');
  if (toggle && menu && navbar) {
    toggle.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      toggle.classList.toggle('open', open);
      toggle.setAttribute('aria-expanded', open);
    });
    document.addEventListener('click', function (e) {
      if (!navbar.contains(e.target)) {
        menu.classList.remove('open');
        toggle.classList.remove('open');
        toggle.setAttribute('aria-expanded', false);
      }
    });
  }

  // Highlight the current page in the nav
  var currentPath = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links > li > a').forEach(function (link) {
    var raw = link.getAttribute('href') || '';
    if (raw.indexOf('#') > -1) return;  // in-page anchors aren't pages
    if (raw === currentPath || raw === currentPath + '.html') link.classList.add('active');
  });

  // Form submit — posts to the hundredx public inquiry API
  var HUNDREDX_API = 'https://100xrecruiting.com';

  // HUMAN_CHECK_v1 (Gus 11-27, after bot talent requests full of random letters): Cloudflare's
  // "Verify you are human" box above every form's submit button, plus a hidden honeypot field
  // only bots fill. 100X checks the box's token (INQUIRY_HUMAN_CHECK_v1 in its app.py). The key
  // is 100X's public Turnstile site key; medpointpartners.com has to be on its hostname list in
  // Cloudflare, or the box shows error 110200. This page never blocks more than the server
  // does: if the box can't load, the form still sends and 100X decides.
  var TURNSTILE_SITE_KEY = '0x4AAAAAAFVLCgI7uu3nWXEb';
  var TICK_MSG = 'Please tick the "Verify you are human" box above, then send again.';
  var forms = document.querySelectorAll('form[data-form]');
  var checks = [];

  function renderChecks() {
    checks.forEach(function (c) {
      if (c.id != null || !window.turnstile) return;
      try {
        c.id = window.turnstile.render(c.box, {
          sitekey: TURNSTILE_SITE_KEY, theme: 'light', 'response-field': false,
          callback: function () { c.failed = null; c.msg.hidden = true; },
          'error-callback': function (code) { c.failed = code || 'error'; },
        });
      } catch (err) { c.failed = 'render'; }
    });
  }
  function humanToken(c) {
    try { return (c.id != null && window.turnstile && window.turnstile.getResponse(c.id)) || ''; }
    catch (err) { return ''; }
  }
  function resetCheck(c) {
    try { if (c.id != null && window.turnstile) window.turnstile.reset(c.id); } catch (err) {}
  }
  function showMsg(c, text) { c.msg.textContent = text; c.msg.hidden = false; }

  if (forms.length) {
    window.mpTurnstileReady = renderChecks;
    var ts = document.createElement('script');
    ts.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit&onload=mpTurnstileReady';
    ts.async = true;
    ts.defer = true;
    document.head.appendChild(ts);
  }

  forms.forEach(function (form) {
    var hp = document.createElement('div');
    hp.setAttribute('aria-hidden', 'true');
    hp.style.cssText = 'position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden;';
    hp.innerHTML = '<label>Leave this empty <input type="text" name="hp_website" tabindex="-1" autocomplete="off"></label>';
    form.appendChild(hp);

    var submitBtn = form.querySelector('button[type="submit"]');
    var box = document.createElement('div');
    box.className = 'human-check';
    box.style.cssText = 'margin:4px 0 14px;min-height:65px;';
    var msg = document.createElement('p');
    msg.className = 'human-check-msg';
    msg.setAttribute('role', 'alert');
    msg.hidden = true;
    msg.style.cssText = 'color:#b42318;font-size:.88rem;font-weight:500;margin:-6px 0 12px;';
    var spot = submitBtn ? submitBtn : null;
    (spot ? spot.parentNode : form).insertBefore(box, spot);
    (spot ? spot.parentNode : form).insertBefore(msg, spot);
    var check = { box: box, msg: msg, id: null, failed: null };
    checks.push(check);

    form.addEventListener('submit', async function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var token = humanToken(check);
      if (!token && check.id != null && !check.failed) { showMsg(check, TICK_MSG); return; }
      msg.hidden = true;
      var btn = form.querySelector('button[type="submit"]');
      var successEl = form.querySelector('.alert-success');
      var orig = btn ? btn.textContent : '';
      if (btn) { btn.disabled = true; btn.textContent = 'Sending…'; }

      var d = Object.fromEntries(new FormData(form));
      var name = ((d.first_name || '') + ' ' + (d.last_name || '')).trim();
      var notes = [
        'Source: MedPoint Partners (medpointpartners.com)',
        d.role_title   ? 'Role: '             + d.role_title   : '',
        d.hire_type    ? 'Type: '             + d.hire_type    : '',
        d.setting      ? 'Setting: '          + d.setting      : '',
        d.location     ? 'Location: '         + d.location     : '',
        d.timeline     ? 'Timeline: '         + d.timeline     : '',
        d.compensation ? 'Compensation: '     + d.compensation : '',
        d.your_title   ? 'Submitter title: '  + d.your_title   : '',
        d.phone        ? 'Phone: '            + d.phone        : '',
        d.topic        ? 'Topic: '            + d.topic        : '',
        d.message      ? 'Message: '          + d.message      : '',
        d.notes        ? 'Notes: '            + d.notes        : '',
      ].filter(Boolean).join('\n');

      try {
        var res = await fetch(HUNDREDX_API + '/api/public/inquiry', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            employer_name:    name || d.name || '',
            employer_email:   d.email || '',
            employer_company: d.company || '',
            inquiry_type:     form.dataset.form,
            notes:            notes,
            hp_website:       d.hp_website || '',
            cf_turnstile_response: token,
          }),
        });
        var json = await res.json().catch(function () { return {}; });
        resetCheck(check);   // a token works once; a second send needs a fresh one
        if (json.ok) {
          form.reset();
          if (successEl) successEl.style.display = 'block';
          if (btn) { btn.textContent = 'Sent ✓'; }
        } else if (json.error === 'human_check') {
          if (btn) { btn.disabled = false; btn.textContent = orig; }
          showMsg(check, check.failed
            ? 'The "Verify you are human" box didn\'t load. Please refresh the page and try again, or call 404-250-0790.'
            : (json.message || TICK_MSG));
        } else {
          throw new Error(json.error || 'server error');
        }
      } catch (err) {
        if (btn) { btn.disabled = false; btn.textContent = orig; }
        alert('Something went wrong — please call 404-250-0790.');
      }
    });
  });
  if (window.turnstile) renderChecks();
})();
