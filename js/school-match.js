/* MedPoint Partners — school match page (school-match.html)
   A district pastes or picks a job description; we score it against the blinded
   candidate spotlights from 100xrecruiting.com (the same feed the school tickers
   scroll) and show the best match. Spotlights carry no name, employer or school.
   window.MP_SCHOOL (the 23 roles, their words, sample JDs) is written by tools/build_pages.py.
   A spotlight's profile page plays the candidate's video intro first when they've filmed one;
   once the feed marks those spotlights (video: true), the card links straight to it. */
(function () {
  var S = window.MP_SCHOOL;
  var out = document.getElementById('matchOut');
  if (!S || !out) return;
  var jd = document.getElementById('jd');
  var sample = document.getElementById('jd-sample');
  var deptSel = document.getElementById('dept');
  var go = document.getElementById('matchGo');
  var topic = document.getElementById('s-topic');
  var notes = document.getElementById('s-notes');
  var role = document.getElementById('s-role');
  var asked = document.getElementById('matchAsked');
  var params = new URLSearchParams(location.search);
  var via = params.get('src') === 'qr' ? 'QR scan' : 'website';
  var feed = null, shown = [], copiedJd = '', copiedRole = '';

  var STATES = {AL: 'alabama', AK: 'alaska', AZ: 'arizona', AR: 'arkansas', CA: 'california', CO: 'colorado',
    CT: 'connecticut', DE: 'delaware', FL: 'florida', GA: 'georgia', HI: 'hawaii', ID: 'idaho', IL: 'illinois',
    IN: 'indiana', IA: 'iowa', KS: 'kansas', KY: 'kentucky', LA: 'louisiana', ME: 'maine', MD: 'maryland',
    MA: 'massachusetts', MI: 'michigan', MN: 'minnesota', MS: 'mississippi', MO: 'missouri', MT: 'montana',
    NE: 'nebraska', NV: 'nevada', NH: 'new hampshire', NJ: 'new jersey', NM: 'new mexico', NY: 'new york',
    NC: 'north carolina', ND: 'north dakota', OH: 'ohio', OK: 'oklahoma', OR: 'oregon', PA: 'pennsylvania',
    RI: 'rhode island', SC: 'south carolina', SD: 'south dakota', TN: 'tennessee', TX: 'texas', UT: 'utah',
    VT: 'vermont', VA: 'virginia', WA: 'washington', WV: 'west virginia', WI: 'wisconsin', WY: 'wyoming'};
  // Common words that would make every job description "match" every candidate
  var STOP = /^(about|their|there|which|would|could|should|students?|schools?|district|required|requires|including|experience|years?|position|support|services?|within|other|across|these|those|ability|skills|preferred|candidate|responsibilities|qualifications)$/;

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c];
    });
  }
  // Short words (rn, ot, rbt, aba…) only count as whole words
  function compile(words) {
    return words.map(function (w) {
      var e = w.replace(/[.*+?^${}()|[\]\\\/]/g, '\\$&');
      return new RegExp(w.length <= 4 ? '\\b' + e + '\\b' : e, 'i');
    });
  }
  function hits(res, text) {
    var n = 0;
    res.forEach(function (r) { if (r.test(text)) n++; });
    return n;
  }
  S.depts.forEach(function (d) { d.res = compile(d.words); });
  var terms = S.terms.map(function (t) { return {t: t, re: compile([t])[0]}; });

  function byKey(k) {
    for (var i = 0; i < S.depts.length; i++) if (S.depts[i].key === k) return S.depts[i];
    return null;
  }
  function deptOf(text) {
    var best = null, top = 0;
    S.depts.forEach(function (d) { var n = hits(d.res, text); if (n > top) { top = n; best = d; } });
    return best;
  }
  function spotText(p) {
    return [p.title, p.eyebrow, p.big, p.big_label, p.highlight, p.area].concat(p.chips || [], p.creds || []).join(' ');
  }
  // Same rule as each department's ticker (data-only): the first department with a word anywhere
  // in the spotlight's title or eyebrow. Never from its skills (an accountant with a "Speech"
  // chip isn't an SLP), and a hospital RN isn't offered as a school nurse.
  function spotDept(p) {
    var t = ((p.title || '') + ' ' + (p.eyebrow || '')).toLowerCase();
    for (var i = 0; i < S.depts.length; i++) {
      if (S.depts[i].only.some(function (w) { return t.indexOf(w) >= 0; })) return S.depts[i];
    }
    return null;
  }
  function places(area) {
    var w = [];
    String(area || '').split(/[^A-Za-z]+/).forEach(function (x) {
      if (STATES[x]) w.push(x, STATES[x]);
      else if (x.length >= 4 && !/^(area|metro|open|remote|hybrid|onsite|relocate)$/i.test(x)) w.push(x.toLowerCase());
    });
    return w;
  }
  function inJd(word, raw) {
    // State abbreviations match as capitals ("GA"), everything else in any case
    return word.length === 2 ? new RegExp('\\b' + word + '\\b').test(raw)
                             : new RegExp('\\b' + word + '\\b', 'i').test(raw);
  }
  function score(p, raw) {
    var text = spotText(p), lower = text.toLowerCase(), why = [], s = 0, seen = {};
    terms.forEach(function (t) { if (raw && t.re.test(raw) && t.re.test(text)) { s += 10; why.push(t.t); } });
    places(p.area).some(function (w) {
      if (raw && inJd(w, raw)) { s += 8; why.unshift(p.area); return true; }
      return false;
    });
    var shared = 0;
    (raw.toLowerCase().match(/[a-z][a-z-]{4,}/g) || []).forEach(function (w) {
      if (seen[w] || STOP.test(w)) return;
      seen[w] = 1;
      if (new RegExp('\\b' + w.replace(/-/g, '\\-') + '\\b').test(lower)) shared++;
    });
    return {p: p, s: s + Math.min(shared, 10), why: why};
  }

  function load(cb) {
    if (feed) return cb(feed);
    out.innerHTML = '<div class="match-empty"><p>Checking the candidates we\'re representing now…</p></div>';
    fetch(S.feed).then(function (r) { return r.json(); }).then(function (j) {
      var seen = {};
      feed = ((j && j.spotlights) || []).filter(function (p) {
        var k = [p.title, p.area, p.big].join('|').toLowerCase();
        if (seen[k]) return false;
        seen[k] = 1;
        return true;
      });
      cb(feed);
    }).catch(function () { feed = []; cb(feed); });
  }

  function card(r, i, best) {
    var p = r.p;
    var creds = (p.creds || []).map(function (c) { return '<span class="mpc-badge gold">&#10003; ' + esc(c) + '</span>'; }).join('');
    var why = best && r.why.length
      ? '<div class="match-why-label">Matches your job description</div><div class="mpc-badges">'
        + r.why.slice(0, 6).map(function (w) { return '<span class="mpc-badge green">' + esc(w) + '</span>'; }).join('') + '</div>'
      : '';
    var link = /^https:\/\//.test(p.link || '') ? p.link : '';
    return '<div class="match-card' + (best ? ' match-card--best' : '') + '">'
      + '<div class="match-eyebrow">' + esc(p.eyebrow || p.title || r.d.one) + '</div>'
      + (p.big ? '<div class="match-big">' + esc(p.big) + '</div>' : '')
      + (p.big_label ? '<div class="match-label">' + esc(p.big_label) + '</div>' : '')
      + (creds ? '<div class="mpc-badges">' + creds + '</div>' : '')
      + '<div class="match-who">' + esc(p.title) + '<small>' + esc(p.area || '') + ' &middot; available now &middot; name on request</small></div>'
      + why
      + '<div class="match-actions"><button type="button" class="btn btn-primary" data-ask="' + i + '">Ask About This Candidate</button>'
      + (link && p.video ? '<a class="btn btn-outline-dark" href="' + esc(link.replace(/#.*$/, '') + '#share-video') + '" target="_blank" rel="noopener">&#9654; Watch Their Video Intro</a>'
         : link ? '<a class="btn btn-outline-dark" href="' + esc(link) + '" target="_blank" rel="noopener">See Their Profile &#8599;</a>' : '')
      + '</div></div>';
  }

  function none(d, text) {
    var who = d ? d.one : 'school candidate';
    out.innerHTML = '<div class="match-empty"><div class="feature-icon"><svg class="ico" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg></div>'
      + '<h3>We\'re screening ' + esc(d ? d.name : 'school candidates') + ' now</h3>'
      + (text ? '<p>No ' + esc(who) + ' in our live spotlights fits this job description yet. Send it to us and we\'ll come back with a blinded shortlist in 48–72 hours.</p>'
              : '<p>No ' + esc(who) + ' is in our live spotlights yet. Paste your job description and send it to us — we\'ll come back with a blinded shortlist in 48–72 hours.</p>')
      + '<a href="#send" class="btn btn-primary" data-send="1">Send My Job Description &rarr;</a></div>';
  }

  function prefill(d, text) {
    if (text && (!notes.value || notes.value === copiedJd)) { notes.value = text; copiedJd = text; }
    if (d && (!role.value || role.value === copiedRole)) { role.value = d.one; copiedRole = d.one; }
    topic.value = 'School match (' + via + ')' + (d ? ' — ' + d.name : '');
  }

  function run(auto) {
    var text = jd.value.trim();
    var d = byKey(deptSel.value) || (text ? deptOf(text) : null);
    if (!d && !text) {
      if (!auto) { jd.focus(); jd.placeholder = 'Paste a job description, or pick a role above.'; }
      return;
    }
    prefill(d, text);
    load(function (items) {
      var ranked = items.map(function (p) { return {p: p, d: spotDept(p)}; })
        .filter(function (x) { return x.d && (!d || x.d === d); })
        .map(function (x) { var r = score(x.p, text); r.d = x.d; return r; })
        .sort(function (a, b) { return b.s - a.s; });
      shown = ranked.slice(0, 3);
      if (!shown.length) return none(d, text);
      out.innerHTML = '<div class="match-head"><h3>' + (text ? 'Your best match' : 'Top ' + esc(d ? d.name : 'school') + ' candidate') + '</h3>'
        + '<span class="live-pill">Live spotlights</span></div>'
        + card(shown[0], 0, true)
        + (shown.length > 1 ? '<div class="match-also">' + shown.slice(1).map(function (r, i) { return card(r, i + 1, false); }).join('') + '</div>' : '')
        + '<p class="form-note" style="text-align:left;">' + (text ? 'Matched on department, credentials, setting, and location.' : 'Paste your job description to sharpen the match.')
        + ' A recruiter confirms every match before an introduction.</p>';
    });
  }

  function toForm() {
    document.getElementById('send').scrollIntoView({behavior: 'smooth'});
    setTimeout(function () { document.getElementById('s-first').focus({preventScroll: true}); }, 500);
  }

  out.addEventListener('click', function (e) {
    var ask = e.target.closest('[data-ask]'), send = e.target.closest('[data-send]');
    if (send) { e.preventDefault(); prefill(null, jd.value.trim()); toForm(); return; }
    if (!ask) return;
    var r = shown[+ask.getAttribute('data-ask')];
    if (!r) return;
    var p = r.p, who = p.title + (p.area ? ', ' + p.area : '');
    prefill(r.d, jd.value.trim());
    topic.value = 'School match (' + via + ') — asked about spotlight ' + p.id + ': ' + who;
    asked.textContent = 'You\'re asking about: ' + who + ' (spotlight ' + p.id + ')';
    asked.hidden = false;
    toForm();
  });
  go.addEventListener('click', function () { run(false); });
  sample.addEventListener('change', function () {
    var d = byKey(sample.value);
    if (!d) return;
    jd.value = d.jd;
    deptSel.value = d.key;
    run(false);
  });
  deptSel.addEventListener('change', function () {
    if (sample.value && sample.value !== deptSel.value) sample.value = '';
    run(true);
  });

  // From a QR code or a role page: ?d=slp picks the role and shows its top candidate
  var start = byKey(params.get('d') || '');
  topic.value = 'School match (' + via + ')';
  if (start) {
    deptSel.value = start.key;
    run(true);
  }
})();
