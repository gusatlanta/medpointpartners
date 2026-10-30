/* MedPoint Partners — Hire School Staff (hire-school-staff.html)
   The district's two-step job order: contact info, then the hiring need. It posts to data-api
   on the form — 100X's /api/public/medpoint/job-order (MEDPOINT_SCHOOL_ORDER_v1), which makes a
   draft job order — and falls back to /api/public/inquiry (the site's other forms) when that
   endpoint can't be reached, e.g. before it's deployed. */
(function () {
  var form = document.getElementById('jobOrder');
  if (!form) return;
  var API = 'https://100xrecruiting.com';
  var steps = form.querySelectorAll('.form-step');
  var tabs = document.querySelectorAll('[data-step-tab]');
  var done = form.querySelector('.alert-success');
  var role = document.getElementById('h-role');

  function show(n) {
    steps.forEach(function (s) { s.hidden = s.getAttribute('data-step') !== String(n); });
    tabs.forEach(function (t) {
      var k = +t.getAttribute('data-step-tab');
      t.classList.toggle('active', k === n);
      t.classList.toggle('done', k < n);
    });
    form.closest('.form-card').scrollIntoView({behavior: 'smooth', block: 'start'});
    var first = form.querySelector('.form-step[data-step="' + n + '"] .form-control');
    if (first) setTimeout(function () { first.focus({preventScroll: true}); }, 300);
  }
  function valid(n) {
    var fields = form.querySelectorAll('.form-step[data-step="' + n + '"] [required]');
    for (var i = 0; i < fields.length; i++) {
      if (!fields[i].checkValidity()) { fields[i].reportValidity(); return false; }
    }
    return true;
  }
  form.querySelector('[data-next]').addEventListener('click', function () { if (valid(1)) show(2); });
  form.querySelector('[data-back]').addEventListener('click', function () { show(1); });

  // ?d=slp (a role page's "Place a Job Order" button) picks the role
  var d = new URLSearchParams(location.search).get('d');
  if (d && role.querySelector('option[value="' + d + '"]')) role.value = d;

  form.addEventListener('submit', async function (e) {
    e.preventDefault();
    if (!valid(1)) { show(1); return; }
    if (!valid(2)) return;
    var f = Object.fromEntries(new FormData(form));
    if (f.hp_website) { done.style.display = 'block'; return; }   // honeypot: look finished, send nothing
    var roleName = role.options[role.selectedIndex].text;
    var name = (f.first_name + ' ' + f.last_name).trim();
    var lines = [
      ['Role', roleName + (f.count && f.count !== '1' ? ' (' + f.count + ' needed)' : '')],
      ['Delivery', f.work_setup], ['Kind of hire', f.engagement], ['Schedule', f.schedule],
      ['State', f.state], ['City / campuses', f.location], ['Grades & caseload', f.caseload],
      ['Start', f.start], ['Credentials / languages', f.credentials],
      ['Contact', name + (f.contact_title ? ', ' + f.contact_title : '') + ' · ' + f.email + (f.phone ? ' · ' + f.phone : '')]
    ].filter(function (l) { return l[1]; }).map(function (l) { return l[0] + ': ' + l[1]; });
    var jobOrder = lines.join('\n') + (f.details ? '\n\n' + f.details : '');
    var api = form.getAttribute('data-api');
    var order = {
      first_name: f.first_name, last_name: f.last_name, email: f.email, phone: f.phone, company: f.company,
      contact_title: f.contact_title, need: roleName, job_title: roleName, role_key: f.role, count: f.count,
      engagement: f.engagement, schedule: f.schedule, work_setup: f.work_setup, state: f.state,
      location: f.location, caseload: f.caseload, start: f.start, credentials: f.credentials,
      practice_area: 'K-12 schools', details: f.details, hp_website: f.hp_website
    };
    var inquiry = {
      employer_name: name, employer_email: f.email, employer_company: f.company,
      inquiry_type: 'medpoint-school-job-order',
      notes: 'Source: MedPoint Partners school job order (medpointpartners.com)\n' + jobOrder
    };
    async function post(url, body) {
      var res = await fetch(url, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body)});
      return {status: res.status, json: await res.json().catch(function () { return {}; })};
    }
    var btn = form.querySelector('button[type="submit"]'), orig = btn.textContent;
    btn.disabled = true; btn.textContent = 'Sending…';
    try {
      var out = null;
      if (api) {
        try { out = await post(api, order); } catch (e) { out = null; }   // not reachable: use the inquiry
        if (out && out.status === 400) throw new Error(out.json.error || 'Please check the form.');
        if (out && !out.json.ok) out = null;
      }
      if (!out) out = await post(API + '/api/public/inquiry', inquiry);
      if (!out.json.ok) throw new Error('');
      steps.forEach(function (s) { s.hidden = true; });
      done.style.display = 'block';
      done.scrollIntoView({behavior: 'smooth', block: 'center'});
    } catch (err) {
      btn.disabled = false; btn.textContent = orig;
      alert(err.message || 'Something went wrong — please email gus@stafffinancial.com or call 404-250-0790.');
    }
  });
})();
