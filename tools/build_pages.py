"""Build every MedPoint Partners page from this one file.

The pages share one menu and footer, so edit the copy here and rebuild
instead of editing the .html files by hand (a rebuild overwrites them):

    python tools/build_pages.py            # writes into the site folder
    python tools/build_pages.py <folder>   # writes somewhere else (for a test)
"""
import json
import re
import sys
from pathlib import Path

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
SITE = "https://www.medpointpartners.com"
JOB_BOARD = "https://host.pcrecruiter.net/pcrbin/jobboard.aspx?uid=Staff%20Financial.npsg"
EMAIL = "gus@stafffinancial.com"
UNS = "https://images.unsplash.com/"

ICONS = {
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "award": '<path d="m15.477 12.89 1.515 8.526a.5.5 0 0 1-.81.47l-3.58-2.687a1 1 0 0 0-1.197 0l-3.586 2.686a.5.5 0 0 1-.81-.469l1.514-8.526"/><circle cx="12" cy="8" r="6"/>',
    "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "briefcase": '<path d="M16 20V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/><rect width="20" height="14" x="2" y="6" rx="2"/>',
    "receipt": '<path d="M4 2v20l2-1 2 1 2-1 2 1 2-1 2 1 2-1 2 1V2l-2 1-2-1-2 1-2-1-2 1-2-1-2 1Z"/><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"/><path d="M12 17.5v-11"/>',
    "zap": '<path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/>',
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    "clipboard": '<rect width="8" height="4" x="8" y="2" rx="1" ry="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="M12 11h4"/><path d="M12 16h4"/><path d="M8 11h.01"/><path d="M8 16h.01"/>',
    "refresh": '<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/>',
    "pin": '<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
    "check": '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
    "pulse": '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/><path d="M3.22 12H9.5l.5-1 2 4.5 2-7 1.5 3.5h5.27"/>',
    "heart": '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>',
    "hospital": '<path d="M12 6v4"/><path d="M14 14h-4"/><path d="M14 18h-4"/><path d="M14 8h-4"/><path d="M18 12h2a2 2 0 0 1 2 2v6a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-9a2 2 0 0 1 2-2h2"/><path d="M18 22V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v18"/>',
    "stethoscope": '<path d="M11 2v2"/><path d="M5 2v2"/><path d="M5 3H4a2 2 0 0 0-2 2v4a6 6 0 0 0 12 0V5a2 2 0 0 0-2-2h-1"/><path d="M8 15a6 6 0 0 0 12 0v-3"/><circle cx="20" cy="10" r="2"/>',
    "bone": '<path d="M17 10c.7-.7 1.69 0 2.5 0a2.5 2.5 0 1 0 0-5 .5.5 0 0 1-.5-.5 2.5 2.5 0 1 0-5 0c0 .81.7 1.8 0 2.5l-7 7c-.7.7-1.69 0-2.5 0a2.5 2.5 0 0 0 0 5c.28 0 .5.22.5.5a2.5 2.5 0 1 0 5 0c0-.81-.7-1.8 0-2.5Z"/>',
    "activity": '<path d="M22 12h-2.48a2 2 0 0 0-1.93 1.46l-2.35 8.36a.25.25 0 0 1-.48 0L9.24 2.18a.25.25 0 0 0-.48 0l-2.35 8.36A2 2 0 0 1 4.49 12H2"/>',
    "home": '<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>',
    "building": '<path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/><path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2"/><path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2"/><path d="M10 6h4"/><path d="M10 10h4"/><path d="M10 14h4"/><path d="M10 18h4"/>',
    "flask": '<path d="M10 2v7.527a2 2 0 0 1-.211.896L4.72 20.55a1 1 0 0 0 .9 1.45h12.76a1 1 0 0 0 .9-1.45l-5.069-10.127A2 2 0 0 1 14 9.527V2"/><path d="M8.5 2h7"/><path d="M7 16h10"/>',
    "file": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>',
    "trending": '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>',
    "landmark": '<line x1="3" x2="21" y1="22" y2="22"/><line x1="6" x2="6" y1="18" y2="11"/><line x1="10" x2="10" y1="18" y2="11"/><line x1="14" x2="14" y1="18" y2="11"/><line x1="18" x2="18" y1="18" y2="11"/><polygon points="12 2 20 7 4 7"/>',
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "video": '<path d="m16 13 5.223 3.482a.5.5 0 0 0 .777-.416V7.87a.5.5 0 0 0-.752-.432L16 10.5"/><rect x="2" y="6" width="14" height="12" rx="2"/>',
    "handshake": '<path d="m11 17 2 2a1 1 0 1 0 3-3"/><path d="m14 14 2.5 2.5a1 1 0 1 0 3-3l-3.88-3.88a3 3 0 0 0-4.24 0l-.88.88a1 1 0 1 1-3-3l2.81-2.81a5.79 5.79 0 0 1 7.06-.87l.47.28a2 2 0 0 0 1.42.25L21 4"/><path d="m21 3 1 11h-2"/><path d="M3 3 2 14l6.5 6.5a1 1 0 1 0 3-3"/><path d="M3 4h8"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "laptop": '<path d="M20 16V7a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v9m16 0H4m16 0 1.28 2.55a1 1 0 0 1-.9 1.45H3.62a1 1 0 0 1-.9-1.45L4 16"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "lock": '<rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "dumbbell": '<path d="M14.4 14.4 9.6 9.6"/><path d="M18.657 21.485a2 2 0 1 1-2.829-2.828l-1.767 1.768a2 2 0 1 1-2.829-2.829l6.364-6.364a2 2 0 1 1 2.829 2.829l-1.768 1.767a2 2 0 1 1 2.828 2.829z"/><path d="m21.5 21.5-1.4-1.4"/><path d="M3.9 3.9 2.5 2.5"/><path d="M6.404 12.768a2 2 0 1 1-2.829-2.829l1.768-1.767a2 2 0 1 1-2.828-2.829l2.828-2.828a2 2 0 1 1 2.829 2.828l1.767-1.768a2 2 0 1 1 2.829 2.829z"/>',
}


def ico(name):
    return ('<svg class="ico" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" '
            'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" >' + ICONS[name] + '</svg>')


def fill(html):
    """Swap [[ico:name]] tokens and site constants into a template string."""
    html = re.sub(r"\[\[ico:([a-z]+)\]\]", lambda m: ico(m.group(1)), html)
    return (html.replace("{{JOB_BOARD}}", JOB_BOARD).replace("{{EMAIL}}", EMAIL)
            .replace("{{SITE}}", SITE).replace("{{UNS}}", UNS))


BRAND = '<img src="img/medpoint-logo.png" alt="MedPoint Partners — powered by NorthPoint" class="brand-logo" width="170" height="58">'

NAV = '''
<!-- ── Navigation ───────────────────────────── -->
<nav class="navbar" id="navbar">
  <div class="container nav-inner">
    <a href="index.html" class="brand" aria-label="MedPoint Partners — home">
      ''' + BRAND + '''
    </a>
    <div class="nav-menu" id="navMenu">
      <ul class="nav-links" id="navLinks">
        <li><a href="services.html">Services</a></li>
        <li class="has-mega">
          <a href="services.html#titles">Specialties <span class="chevron">▾</span></a>
          <div class="mega-menu">
            <div class="mega-sidebar">
              <button class="mega-tab-btn active" onclick="switchMegaTab('direct',this)">Direct Hire</button>
              <button class="mega-tab-btn" onclick="switchMegaTab('staffing',this)">Temp &amp; Temp-to-Perm</button>
            </div>
            <div class="mega-panel active" id="mega-direct">
              <a href="services.html#retained" style="font-weight:600;color:var(--ink);">[[ico:award]] Retained Search</a>
              <a href="services.html#rpo" style="font-weight:600;color:var(--ink);">[[ico:wrench]] RPO &amp; Project Staffing</a>
              <a href="services.html#audience" style="font-weight:600;color:var(--ink);">[[ico:users]] Perfect Candidate Audience</a>
              <a href="services.html#titles">Nurses &amp; Nurse Leaders</a>
              <a href="services.html#titles">Nurse Practitioners &amp; PAs</a>
              <a href="services.html#titles">Physicians &amp; Medical Directors</a>
              <a href="services.html#titles">Allied Health &amp; Imaging</a>
              <a href="services.html#titles">Therapy &amp; Rehab</a>
              <a href="services.html#titles">Medical Assistants &amp; Front Office</a>
              <a href="services.html#titles">Practice Administrators &amp; Leadership</a>
              <a href="services.html#titles">Revenue Cycle &amp; Coding</a>
              <a href="services.html#titles">Healthcare Finance</a>
              <a class="mega-all" href="services.html#titles">All Direct Hire Specialties →</a>
            </div>
            <div class="mega-panel" id="mega-staffing">
              <a href="temp-staffing.html">Nursing Temps (RN, LPN, CNA)</a>
              <a href="temp-staffing.html">Medical Assistant Temps</a>
              <a href="temp-staffing.html">Front Desk &amp; Scheduling Temps</a>
              <a href="temp-staffing.html">Imaging &amp; Surgical Tech Temps</a>
              <a href="temp-staffing.html">Coding &amp; Billing Backlogs</a>
              <a href="temp-staffing.html">Interim Practice Administrator</a>
              <a href="temp-staffing.html">Interim Nurse Manager</a>
              <a href="temp-staffing.html">Interim Revenue Cycle &amp; Finance</a>
              <a href="services.html#temp-to-perm">Temp-to-Perm</a>
              <a href="temp-staffing.html">Payrolling (Employer of Record)</a>
              <a class="mega-all" href="temp-staffing.html">Healthcare Temps →</a>
            </div>
            <div class="mega-featured">
              <div class="mega-featured-placeholder">[[ico:stethoscope]]</div>
              <h4>We Payroll Your Healthcare Temps</h4>
              <a href="temp-staffing.html" class="learn">Learn More →</a>
            </div>
          </div>
        </li>
        <li class="has-mega">
          <a href="about.html#settings">Care Settings <span class="chevron">▾</span></a>
          <div class="dropdown-menu">
            <a href="about.html#settings">Hospitals &amp; Health Systems</a>
            <a href="about.html#settings">Physician Groups &amp; Specialty Practices</a>
            <a href="about.html#settings">Orthopedic &amp; Spine Practices</a>
            <a href="about.html#settings">Ambulatory Surgery Centers</a>
            <a href="about.html#settings">Urgent Care &amp; Primary Care</a>
            <a href="about.html#settings">Home Health &amp; Hospice</a>
            <a href="about.html#settings">Senior Living &amp; Post-Acute</a>
            <a href="about.html#settings">All Care Settings</a>
          </div>
        </li>
        <li><a href="temp-staffing.html">Temp Staffing</a></li>
        <li><a href="about.html">About</a></li>
        <li><a href="partners.html">Partner Program</a></li>
      </ul>
      <div class="nav-ctas">
        <a href="{{JOB_BOARD}}" target="_blank" rel="noopener" class="btn btn-outline-dark">Job Board</a>
        <a href="request-talent.html" class="btn btn-primary">Hire Top Talent</a>
      </div>
    </div>
    <button class="nav-toggle" id="navToggle" aria-label="Open menu" aria-expanded="false" aria-controls="navMenu"><span></span><span></span><span></span></button>
  </div>
</nav>
'''

FOOTER = '''
<!-- ── Footer ─────────────────────────────────── -->
<footer>
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="index.html" class="brand-chip" aria-label="MedPoint Partners — home">
          ''' + BRAND + '''
        </a>
        <p>Healthcare recruiting and staffing for hospitals, physician practices, and healthcare organizations — clinical and non-clinical — backed by NorthPoint's 20+ years of recruiting.</p>
      </div>
      <div class="footer-col">
        <h4>Explore</h4>
        <ul>
          <li><a href="about.html">About Us</a></li>
          <li><a href="services.html">Our Services</a></li>
          <li><a href="temp-staffing.html">Temp Staffing</a></li>
          <li><a href="services.html#titles">Specialties</a></li>
          <li><a href="about.html#settings">Care Settings</a></li>
          <li><a href="partners.html">Partner Program</a></li>
          <li><a href="{{JOB_BOARD}}" target="_blank" rel="noopener">Job Board ↗</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Contact</h4>
        <ul>
          <li><a href="mailto:{{EMAIL}}">{{EMAIL}}</a></li>
          <li><a href="tel:+14042500790">404-250-0790</a></li>
          <li><a href="tel:+16787775627">678-777-5627</a></li>
          <li><a href="contact.html">Send a Message</a></li>
          <li><a href="request-talent.html">Request Talent</a></li>
          <li><span>Atlanta, GA · Serving the Southeast &amp; nationwide</span></li>
        </ul>
      </div>
    </div>
    <hr class="footer-divider">
    <div class="footer-bottom">
      <span>&copy; 2026 MedPoint Partners. Powered by NorthPoint. All rights reserved.</span>
      <a href="contact.html">Privacy &amp; Terms</a>
    </div>
  </div>
</footer>

<script src="js/main.js"></script>
</body>
</html>
'''

ORG = {
    "@type": "Organization",
    "@id": SITE + "/#organization",
    "name": "MedPoint Partners",
    "alternateName": ["Medpoint Partners", "MedPoint"],
    "url": SITE,
    "logo": {"@type": "ImageObject", "url": SITE + "/img/medpoint-logo.png"},
    "description": "Healthcare recruiting and staffing firm in Atlanta, GA. We place clinical and non-clinical healthcare professionals — nurses, nurse practitioners, physician assistants, physicians, allied health and therapy, medical assistants and front office, coding, billing and revenue cycle, finance, and leadership — as temp, temp-to-perm, and direct hire, with payrolling as Employer of Record.",
    "address": {"@type": "PostalAddress", "addressLocality": "Atlanta", "addressRegion": "GA", "addressCountry": "US"},
    "telephone": ["+1-404-250-0790", "+1-678-777-5627"],
    "email": EMAIL,
    "areaServed": ["Atlanta, GA", "Georgia", "Southeast United States", "United States"],
    "sameAs": [],
}


def head(file, title, desc, extra_schema=None, extra_head=""):
    url = SITE + "/" + ("" if file == "index.html" else file)
    graph = [ORG] + (extra_schema or [])
    schema = json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2, ensure_ascii=False)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="icon" type="image/png" sizes="32x32" href="img/favicon-32.png">
  <link rel="apple-touch-icon" href="img/favicon-180.png">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">
  <meta name="robots" content="index, follow">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="MedPoint Partners">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/img/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:locale" content="en_US">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{SITE}/img/og-image.png">
  <meta name="theme-color" content="#0b1f3d">
  <script type="application/ld+json">
{schema}
  </script>
  <link rel="stylesheet" href="css/styles.css">{extra_head}
</head>
<body>
'''


def page_hero(crumb, h1, sub, photo, pos="center"):
    return f'''
<!-- ── Page Hero ──────────────────────────────── -->
<section class="page-hero" style="background-image:url('{UNS}{photo}?auto=format&fit=crop&w=1600&q=80');background-position:{pos};">
  <div class="container">
    <div class="breadcrumb"><a href="index.html">Home</a><span>/</span>{crumb}</div>
    <h1>{h1}</h1>
    <p>{sub}</p>
  </div>
</section>
'''


CTA = '''
<!-- ── CTA band ───────────────────────────────── -->
<div class="cta-band">
  <div class="container">
    <h2>{h2}</h2>
    <p>{p}</p>
    <div class="cta-actions">
      <a href="request-talent.html" class="btn btn-white btn-lg">Request Talent Now</a>
      <a href="{{JOB_BOARD}}" target="_blank" rel="noopener" class="btn btn-outline-white btn-lg">Browse Open Jobs ↗</a>
    </div>
  </div>
</div>
'''


def cta(h2="Ready to Find Your Next<br>Healthcare Hire?",
        p="Tell us about your open role and we'll deliver a shortlist — guaranteed."):
    return CTA.replace("{h2}", h2).replace("{p}", p)


SPECIALTIES = ["Registered Nurses (RN)", "LPNs &amp; CNAs", "Nurse Practitioners (NP)", "Physician Assistants (PA-C)",
               "Physicians (MD / DO)", "Medical Assistants", "Imaging &amp; Surgical Techs", "Therapy &amp; Rehab",
               "Front Desk &amp; Patient Access", "Coding, Billing &amp; Revenue Cycle", "Healthcare Finance",
               "Practice Administrators &amp; Leadership"]


def specialty_grid():
    return "\n".join(f'          <div class="specialty-item"><span class="specialty-dot"></span>{s}</div>' for s in SPECIALTIES)


SETTINGS = [("hospital", "Hospitals &amp; Health Systems"), ("stethoscope", "Physician Groups &amp; Specialty Practices"),
            ("bone", "Orthopedic &amp; Spine Practices"), ("activity", "Ambulatory Surgery Centers"),
            ("pulse", "Urgent Care &amp; Primary Care"), ("home", "Home Health &amp; Hospice"),
            ("heart", "Behavioral Health"), ("building", "Senior Living &amp; Post-Acute"),
            ("flask", "Labs, Imaging &amp; Diagnostics"), ("dumbbell", "Physical Therapy &amp; Rehab Clinics"),
            ("trending", "PE-Backed Platforms &amp; MSOs"), ("landmark", "Community Health Centers &amp; FQHCs")]


def settings_grid():
    return "\n".join(f'      <div class="industry-chip"><span class="industry-icon">[[ico:{i}]]</span>{t}</div>' for i, t in SETTINGS)


EOR = '''
<!-- ── EOR band ───────────────────────────────── -->
<div class="eor-band">
  <div class="container">
    <div class="eor-grid">
      <div>
        <span class="section-kicker">Payrolling · Employer of Record</span>
        <h2 class="section-title" style="color:var(--white);">You Get the Talent.<br>We Handle the Rest.</h2>
        <p style="color:rgba(255,255,255,.75);line-height:1.75;margin-bottom:28px;">MedPoint Partners — powered by NorthPoint — acts as the Employer of Record for every temp placement. One simple bill rate. Zero HR overhead on your end.</p>
        <div style="display:flex;gap:12px;flex-wrap:wrap;">
          <a href="temp-staffing.html" class="btn btn-white btn-lg">Healthcare Temps</a>
          <a href="request-talent.html" class="btn btn-outline-white btn-lg">Request Talent</a>
        </div>
      </div>
      <div class="eor-features">
        <div class="eor-feature">
          <div class="eor-icon-wrap">[[ico:receipt]]</div>
          <div>
            <h4>Weekly Payroll</h4>
            <p>We payroll your temps every week and send one clean invoice at your agreed bill rate.</p>
          </div>
        </div>
        <div class="eor-feature">
          <div class="eor-icon-wrap">[[ico:shield]]</div>
          <div>
            <h4>Workers' Comp</h4>
            <p>Workers' compensation is covered under our policy.</p>
          </div>
        </div>
        <div class="eor-feature">
          <div class="eor-icon-wrap">[[ico:clipboard]]</div>
          <div>
            <h4>Taxes &amp; Compliance</h4>
            <p>All federal, state, and FICA withholdings handled. W-2 issued at year-end.</p>
          </div>
        </div>
        <div class="eor-feature">
          <div class="eor-icon-wrap">[[ico:refresh]]</div>
          <div>
            <h4>Easy Temp-to-Perm</h4>
            <p>Love the temp? Move them to your payroll anytime with a simple conversion agreement.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
'''

EXAMPLE = '''
    <div class="example-callout"{style}>
      <div class="example-icon">[[ico:clipboard]]</div>
      <div>
        <span class="section-kicker">Sample: Screening Questionnaire</span>
        <h4>Orthopedic Physician Assistant (PA-C) — your questions, answered before the first call</h4>
        <p>We build every questionnaire with your input. For an ortho PA, it might look like this — and every résumé arrives with the candidate's answers.</p>
        <ul class="sample-q">
          <li>Which orthopedic areas have you worked in — spine, joints, sports medicine, hand, trauma?</li>
          <li>Do you first-assist in the OR? About how many cases a week?</li>
          <li>How many patients a day do you see in clinic on your own?</li>
          <li>Is your state license active, and do you hold a DEA registration?</li>
        </ul>
      </div>
    </div>'''


def example(style=""):
    return EXAMPLE.replace("{style}", f' style="{style}"' if style else "")


def profiles_section(kicker, h2, sub):
    """Blinded candidate cards from tools/profiles.json (no names, employers, or schools).
    Each card links to the request form with its code; tools/candidate_key.local.json
    (never published) says who each code is."""
    import html as _h
    path = Path(__file__).resolve().parent / "profiles.json"
    items = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    if not items:
        return ""
    e = lambda s: _h.escape(str(s), quote=True)
    cards = []
    for p in items:
        words = re.sub(r"[^A-Za-z ]", " ", p["title"]).split()
        initials = "".join(w[0] for w in words[:2]).upper()
        badges = [f'<span class="mpc-badge gold">{e(c)}</span>' for c in p.get("creds", [])[:2]]
        if p.get("years"):
            badges.append(f'<span class="mpc-badge">{e(p["years"])}+ yrs</span>')
        if p.get("work_mode"):
            badges.append(f'<span class="mpc-badge green">{e(p["work_mode"])}</span>')
        badges += [f'<span class="mpc-badge">{e(s)}</span>' for s in p.get("specialties", [])[:2]]
        win = (f'<div class="mpc-card-win"><span class="mpc-win-label">Track record</span>'
               f'<span class="mpc-win-text">{e(p["highlight"])}</span></div>') if p.get("highlight") else ""
        cards.append(f'<a class="mpc-card" href="request-talent.html?candidate={e(p["code"])}">'
                     f'<div class="mpc-card-head"><div class="mpc-avatar">{e(initials)}</div>'
                     f'<div><div class="mpc-card-title">{e(p["title"])}</div>'
                     f'<div class="mpc-card-loc">[[ico:pin]] {e(p.get("location") or "")}</div></div></div>'
                     f'<div class="mpc-badges">{"".join(badges)}</div>{win}'
                     f'<span class="mpc-card-cta">Ask about {e(p["code"])} →</span></a>')
    dup = "".join(cards).replace('<a class="mpc-card"', '<a class="mpc-card" aria-hidden="true" tabindex="-1"')
    return f'''
<!-- ── Candidates we're representing (blinded) ── -->
<section class="section" id="talent" style="padding-bottom:16px;">
  <div class="container section-head">
    <div>
      <span class="section-kicker">{kicker}</span>
      <h2 class="section-title">{h2}</h2>
      <p class="section-sub">{sub}</p>
    </div>
    <a href="request-talent.html" class="btn btn-outline-dark" style="flex-shrink:0;">Tell Us What You Need →</a>
  </div>
  <div class="mpc-marquee" aria-label="Candidates we are representing">
    <div class="mpc-track" style="animation-duration:{max(60, len(cards) * 5)}s">{"".join(cards)}{dup}</div>
  </div>
</section>
'''


PROFILES = profiles_section('Healthcare Talent Available Now', "Healthcare Pros We're <em>Representing</em> Right Now", "Screened medical coders and healthcare professionals who completed our candidate questionnaire. Names are hidden to protect confidentiality — ask about anyone and we'll make the introduction.")

AUDIENCE_STEPS = '''<li><strong>We build your list</strong> — the exact people you want to hire.</li>
        <li><strong>Our AI recruiting assistant writes the letter with you</strong> — then reaches out and invites them to apply for your job.</li>
        <li><strong>Candidates apply and film a video introduction.</strong></li>
        <li><strong>Our AI matches and scores every candidate for you.</strong></li>
        <li><strong>You reach out directly</strong> — or we do it all for you.</li>'''

# ───────────────────────────── Home ─────────────────────────────
FAQ = [
    ("What healthcare roles does MedPoint Partners place?",
     "Clinical and non-clinical roles at every level: registered nurses, LPNs, CNAs, and nurse leaders; nurse practitioners, physician assistants, CRNAs, and physicians; radiology, imaging, surgical, lab, and respiratory techs; physical, occupational, and speech therapists; medical assistants, front desk, scheduling, and patient access staff; medical coders, billers, and revenue cycle teams; and healthcare leaders, from practice administrators to CEOs, CNOs, and CFOs."),
    ("How quickly will I receive a shortlist of candidates?",
     "We deliver a blinded shortlist of pre-vetted candidates within 48 to 72 hours of receiving your talent request. Our active network and direct sourcing let us move faster than generalist staffing firms."),
    ("Do you offer temp healthcare staffing?",
     "Yes. We place healthcare temps, temp-to-perm, and direct hire — from nursing and medical assistant coverage to front desk, coding, and billing temps and interim leaders. We act as the Employer of Record, so payroll, taxes, workers' comp, and W-2s are handled on our end."),
    ("Do you check licenses and certifications?",
     "Yes. We confirm that a candidate's license or certification — RN, LPN, NP, PA-C, ARRT, CPC, and others — is active before we send them to you. Your screening questionnaire can ask about anything else you need."),
    ("What does \"blinded shortlist\" mean?",
     "A blinded profile shows a candidate's skills, experience, title, and location — but no name, employer name, or contact information. This protects candidate privacy during the screening phase. Once you express interest, we facilitate the introduction."),
    ("Where does MedPoint Partners place candidates?",
     "We are headquartered in Atlanta, GA, and serve hospitals, physician practices, and healthcare organizations throughout the Southeast. Remote roles, like coding and billing, we fill nationwide."),
]


def faq_schema():
    strip = lambda s: s.replace("&amp;", "&")
    return [{"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in FAQ]}]


def faq_html():
    items = []
    for q, a in FAQ:
        items.append(f'''      <details itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
        <summary itemprop="name">{q}</summary>
        <div class="faq-a" itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer"><span itemprop="text">{a}</span></div>
      </details>''')
    return "\n".join(items)


# Job titles that count as healthcare for the hero card. Broad words like "health",
# "billing" or "practice manager" are left out: they also match the accounting,
# legal and construction jobs in the same feed.
HOME_HEAD = '''
  <script>
  /* Healthcare openings from the 100X jobs feed: fills the hero card and adds Google Jobs schema. */
  window.MP_HEALTH = /(nurs(e|ing)|\\b(rn|lpn|lvn|cna|crna|np|aprn|pa-c)\\b|physician|medical|clinical|clinic\\b|patient|hospital\\b|healthcare|health system|home health|behavioral health|hospice|surg(ical|ery)|ortho|radiolog|x-ray|\\bmri\\b|sonograph|ultrasound|phlebotom|pharmac(y|ist)|respiratory|physical therap|occupational therap|speech.language|dental|dentist|hygienist|sterile processing|coding|coder|\\bcdi\\b|revenue cycle|\\brcm\\b|reimburse|cost report|credential|precert|prior auth)/i;
  </script>'''

HOME = '''
<!-- ── Hero ─────────────────────────────────── -->
<section class="hero">
  <div class="container hero-grid">
    <div class="hero-inner">
      <span class="hero-kicker">Healthcare Recruiting &amp; Staffing · Atlanta, GA</span>
      <h1>Specialized <em>Healthcare</em><br>Recruiting &amp; Staffing</h1>
      <p class="hero-lede">Clinical and non-clinical — from the front desk to the operating room to the C&#8209;suite.</p>
      <p class="hero-service-line">Temp &nbsp;·&nbsp; Temp-to-Perm &nbsp;·&nbsp; Direct Hire</p>

      <form class="hero-search-form" action="https://host.pcrecruiter.net/pcrbin/jobboard.aspx" method="get" target="_blank">
        <input type="hidden" name="uid" value="Staff Financial.npsg">
        <div class="hero-search-bar">
          <input type="text" name="keyword" placeholder="Keyword — e.g. RN, PA-C, Medical Coder…" aria-label="Keyword">
          <select name="specialty" aria-label="Specialty">
            <option value="">Select Specialty</option>
            <option value="Registered Nurse">Registered Nurse (RN)</option>
            <option value="LPN">LPN / CNA</option>
            <option value="Nurse Practitioner">Nurse Practitioner</option>
            <option value="Physician Assistant">Physician Assistant (PA-C)</option>
            <option value="Physician">Physician</option>
            <option value="Medical Assistant">Medical Assistant</option>
            <option value="Radiology">Radiology / Imaging Tech</option>
            <option value="Surgical Tech">Surgical Tech</option>
            <option value="Therapist">Physical / Occupational Therapist</option>
            <option value="Front Desk">Front Desk / Patient Access</option>
            <option value="Medical Coder">Medical Coder / Biller</option>
            <option value="Revenue Cycle">Revenue Cycle</option>
            <option value="Practice Administrator">Practice Administrator</option>
            <option value="Healthcare Finance">Healthcare Finance</option>
          </select>
          <button type="submit">[[ico:search]] Search Jobs</button>
        </div>
      </form>
      <div class="hero-search-sub">
        <a href="request-talent.html" class="btn-hero-pill btn-hero-pill--filled">Ready to Hire? →</a>
        <a href="temp-staffing.html" class="btn-hero-pill">Healthcare Temps →</a>
        <a href="tel:+14042500790" class="btn-hero-pill">[[ico:phone]] 404-250-0790</a>
      </div>
    </div>
    <aside class="hero-card" aria-label="Healthcare roles we're filling now">
      <div class="hero-card-head">
        <div>
          <span class="hero-card-kicker">Now Placing</span>
          <h2>Healthcare roles we're filling now</h2>
        </div>
        <span class="live-pill">Hiring now</span>
      </div>
      <div id="heroJobs"><div class="np-empty">Loading positions…</div></div>
      <a class="hero-card-go" href="request-talent.html">Hiring? Get a Shortlist in 48–72 Hrs &rarr;</a>
      <p class="hero-card-fine">Live from our job board. <a href="{{JOB_BOARD}}" target="_blank" rel="noopener" style="color:var(--blue);font-weight:600;">See every opening ↗</a></p>
    </aside>
  </div>
</section>
<script>
(function(){
  var box=document.getElementById('heroJobs');
  function esc(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
  function none(){box.innerHTML='<div class="np-empty">New searches open every week. <a href="request-talent.html">Tell us what you need →</a></div>';}
  fetch('https://100xrecruiting.com/api/public/jobs?limit=50').then(function(r){return r.json();}).then(function(d){
    var seen={}, jobs=((d&&d.jobs)||[]).filter(function(j){
      var t=(j.title||'').trim(); if(!window.MP_HEALTH.test(t)||seen[t.toLowerCase()]) return false; seen[t.toLowerCase()]=1; return true;
    }).slice(0,5);
    if(!jobs.length){none();return;}
    box.innerHTML=jobs.map(function(j){
      var meta=[j.location,j.salary].filter(Boolean).join(' · ');
      var url=/^https:\\/\\//.test(j.job_url||'')?j.job_url:'{{JOB_BOARD}}';
      return '<a class="np-job" href="'+esc(url)+'" target="_blank" rel="noopener"><span class="np-job-dot"></span><span>'
        +'<span class="np-job-title">'+esc(j.title)+'</span>'+(meta?'<span class="np-job-meta">'+esc(meta)+'</span>':'')+'</span></a>';
    }).join('');
    /* Google Jobs schema for the healthcare roles shown */
    var el=document.createElement('script'); el.type='application/ld+json';
    el.text=JSON.stringify({"@context":"https://schema.org","@graph":jobs.map(function(j){
      var loc=(j.location||'Atlanta, GA').split(',');
      return {"@type":"JobPosting","title":j.title,
        "datePosted":j.date_posted||new Date().toISOString().slice(0,10),
        "validThrough":new Date(Date.now()+60*24*60*60*1000).toISOString().slice(0,10),
        "employmentType":"FULL_TIME",
        "hiringOrganization":{"@type":"Organization","name":"MedPoint Partners","sameAs":"{{SITE}}","logo":"{{SITE}}/img/medpoint-logo.png"},
        "jobLocation":{"@type":"Place","address":{"@type":"PostalAddress","addressLocality":(loc[0]||'Atlanta').trim(),"addressRegion":(loc[1]||'GA').trim(),"addressCountry":"US"}},
        "description":"Healthcare role placed by MedPoint Partners, Atlanta. Contact us to learn more.",
        "url":/^https:\\/\\//.test(j.job_url||'')?j.job_url:'{{JOB_BOARD}}'};
    })});
    document.head.appendChild(el);
  }).catch(none);
})();
</script>

<!-- Candidate spotlights (blinded: no name, employer or school), fed from 100xrecruiting.com.
     data-only keeps healthcare candidates only (each word is matched anywhere in the title, so
     short or broad words like "rn", "health" and "hospital" are left out); the strip stays hidden when none match. -->
<div id="hx-spotlights" style="background:#f4f8fd;"></div>
<script src="https://100xrecruiting.com/static/spotlight_ticker.js?v=2" data-target="hx-spotlights" data-theme="light"
        data-only="nurse,nursing,lpn,crna,physician,pa-c,medical,clinical,patient,surgical,radiolog,sonograph,phlebotom,pharmacist,pharmacy,respiratory,physical therap,occupational therap,dentist,dental hygien,dental assist,coding,coder,revenue cycle,reimburse,credentialing,precert,prior auth"
        data-fallback="{{SITE}}/contact.html" defer></script>
''' + PROFILES + '''
<!-- ── Stats strip ───────────────────────────── -->
<div class="hero-stats">
  <div class="container">
    <div class="stats-section-title">A History of Success</div>
    <div class="stats-box">
      <div class="stat-item">
        <div class="stat-num">105+</div>
        <div class="stat-label">Years Combined Recruiting Experience</div>
      </div>
      <div class="stat-item">
        <div class="stat-num">20+</div>
        <div class="stat-label">Years Recruiting &amp; Staffing</div>
      </div>
      <div class="stat-item">
        <div class="stat-num">1,000+</div>
        <div class="stat-label">Candidate Video Intros Filmed</div>
      </div>
      <div class="stat-item">
        <div class="stat-num">48–72 hrs</div>
        <div class="stat-label">Average Shortlist Delivery</div>
      </div>
    </div>
  </div>
</div>

<!-- ── Service photo cards ───────────────────── -->
<section class="section" style="padding-top:0;">
  <div class="container">
    <div class="service-cards">

      <a class="svc-card" href="services.html#retained">
        <div class="svc-card-bg" style="background-image:url('{{UNS}}photo-1586773860418-d37222d8fce3?auto=format&fit=crop&w=800&q=80');"></div>
        <div class="svc-card-overlay"></div>
        <div class="svc-card-body">
          <h3>Executive Search</h3>
          <p>CEOs, CNOs, CFOs, administrators, and medical directors who lead through change.</p>
          <span class="svc-card-link">Learn More →</span>
        </div>
      </a>

      <a class="svc-card" href="services.html#direct">
        <div class="svc-card-bg" style="background-image:url('{{UNS}}photo-1581056771107-24ca5f033842?auto=format&fit=crop&w=800&q=80');"></div>
        <div class="svc-card-overlay"></div>
        <div class="svc-card-body">
          <h3>Direct Hire</h3>
          <p>Nurses, APPs, techs, office staff, and revenue cycle pros placed for the long term.</p>
          <span class="svc-card-link">Learn More →</span>
        </div>
      </a>

      <a class="svc-card" href="temp-staffing.html">
        <div class="svc-card-bg" style="background-image:url('{{UNS}}photo-1631217868264-e5b90bb7e133?auto=format&fit=crop&w=800&q=80');"></div>
        <div class="svc-card-overlay"></div>
        <div class="svc-card-body">
          <h3>Temp Staffing</h3>
          <p>Temps for leaves, vacancies, and busy seasons — we payroll them, you get one invoice.</p>
          <span class="svc-card-link">See Healthcare Temps →</span>
        </div>
      </a>

      <a class="svc-card" href="services.html#retained">
        <div class="svc-card-bg" style="background-image:url('{{UNS}}photo-1542744173-8e7e53415bb0?auto=format&fit=crop&w=800&q=80');background-position:center top;"></div>
        <div class="svc-card-overlay"></div>
        <div class="svc-card-body">
          <h3>Retained Search</h3>
          <p>Exclusive, dedicated engagement for critical hires — we go deeper, move faster, and guarantee results.</p>
          <span class="svc-card-link">Learn More →</span>
        </div>
      </a>

      <a class="svc-card" href="services.html#rpo">
        <div class="svc-card-bg" style="background-image:url('{{UNS}}photo-1666214280391-8ff5bd3c0bf0?auto=format&fit=crop&w=800&q=80');"></div>
        <div class="svc-card-overlay"></div>
        <div class="svc-card-body">
          <h3>RPO &amp; Project Staffing</h3>
          <p>New clinics, new units, high-volume hiring — we become your recruiting department.</p>
          <span class="svc-card-link">Learn More →</span>
        </div>
      </a>

    </div>
  </div>
</section>

<!-- ── Build the Perfect Candidate Audience ───── -->
<section class="section section-alt" id="candidate-audience">
  <div class="container split" style="align-items:start;">
    <div>
      <span class="section-kicker">Build the Perfect Candidate Audience</span>
      <h2 class="section-title">The Exact People You Want to Hire — <em>Invited to Apply</em></h2>
      <div class="section-divider"></div>
      <div class="pay-when-hire">[[ico:check]] <span>No upfront cost — you only pay when we're successful: when you hire. <span class="pwh-2">And we can payroll them for you.</span></span></div>
      <p class="section-sub" style="margin-bottom:16px;">We build a list for your HR or recruiting team with the exact people you want to hire — the nurses, PAs, techs, and office staff already doing the job somewhere else. Our AI recruiting assistant writes the letter with you and invites them to apply — then our AI matches and scores every candidate for you.</p>
      <p class="section-sub" style="margin-bottom:28px;">It proactively builds a talent bench for every position on your org chart. You just build out the org chart.</p>
      <div style="display:flex;gap:12px;flex-wrap:wrap;">
        <a href="services.html#audience" class="btn btn-primary">See How It Works →</a>
        <a href="request-talent.html" class="btn btn-outline-dark">Tell Us How We Can Help</a>
      </div>
    </div>
    <div class="panel" style="padding:28px 28px 22px;">
      <ol class="num-steps">
        ''' + AUDIENCE_STEPS + '''
      </ol>
      <div class="audience-extras"><strong class="fee-line">When you hire, pick how you pay: we payroll them for one bill rate — or one flat fee, quoted up front.</strong><br>We can payroll your people as Employer of Record · 401(k) for every hire · Benefits available<br>We help you the entire time — live office hours for any questions · Membership includes our <a href="https://www.skool.com/100xrecruiting" target="_blank" rel="noopener">100X Recruiting community on Skool</a><br><strong>Our AI recruiting assistant comes with a 100% satisfaction guarantee.</strong></div>
    </div>
  </div>
</section>

<!-- ── Temps band ──────────────────────────── -->
<section class="section section-dark">
  <div class="container split">
    <div>
      <span class="section-kicker">Temp &amp; Temp-to-Perm</span>
      <h2 class="section-title">Healthcare Temps<br>When You Need Them — <em>Fast</em></h2>
      <p>A nurse goes on leave. Flu season fills the waiting room. A new clinic opens before the team is hired. We send pre-screened temps — and as Employer of Record, we handle payroll, taxes, and workers' comp.</p>
      <a href="temp-staffing.html" class="btn btn-white btn-lg">Healthcare Temps →</a>
    </div>
    <div class="feature-list">
      <div class="feature">
        <div class="feature-icon">[[ico:stethoscope]]</div>
        <div>
          <h4>Clinical Coverage</h4>
          <p>RNs, LPNs, CNAs, medical assistants, and techs for leaves, vacancies, and volume spikes.</p>
        </div>
      </div>
      <div class="feature">
        <div class="feature-icon">[[ico:file]]</div>
        <div>
          <h4>Office, Coding &amp; Billing Teams</h4>
          <p>Front desk, scheduling, coding, and billing temps for new openings and backlogs.</p>
        </div>
      </div>
      <div class="feature">
        <div class="feature-icon">[[ico:receipt]]</div>
        <div>
          <h4>We Payroll Them for You</h4>
          <p>We act as Employer of Record — payroll, taxes, workers' comp, and W-2 all covered. You get one simple invoice.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ── How it works ──────────────────────────── -->
<section class="section section-alt">
  <div class="container">
    <span class="section-kicker">Our Process</span>
    <h2 class="section-title">From Intake to Day One</h2>
    <div class="section-divider"></div>
    <p class="section-sub">A focused, four-step process that gets the right candidate in front of you — fast.</p>
    <div class="steps-row">
      <div class="step">
        <div class="step-num">1</div>
        <h4>Discovery Call</h4>
        <p>We learn the role, schedule, setting, team, and timeline in depth — not just the job description.</p>
      </div>
      <div class="step">
        <div class="step-num">2</div>
        <h4>Targeted Search</h4>
        <p>We cast a wide net — targeted advertising plus direct sourcing — and reach passive candidates who aren't browsing job boards.</p>
      </div>
      <div class="step">
        <div class="step-num">3</div>
        <h4>Shortlist Delivered</h4>
        <p>We check licenses and certifications, build a screening questionnaire with your input, and send every résumé with the candidate's answers.</p>
      </div>
      <div class="step">
        <div class="step-num">4</div>
        <h4>Placed &amp; Guaranteed</h4>
        <p>We manage offers, support onboarding, and back every direct hire with our replacement guarantee.</p>
      </div>
    </div>
''' + example("margin-top:28px;") + '''
  </div>
</section>

<!-- ── Specialties ───────────────────────────── -->
<section class="section">
  <div class="container">
    <div class="two-col">
      <div>
        <span class="section-kicker">Specialties</span>
        <h2 class="section-title">From the Front Desk<br><span class="accent">to the Operating Room</span></h2>
        <div class="section-divider"></div>
        <p class="section-sub">We place clinical and non-clinical healthcare professionals at every level — from medical assistants and CNAs to physicians, nurse leaders, and hospital CFOs.</p>
        <div style="margin-top:28px;">
          <a href="services.html#titles" class="btn btn-primary">All Specialties →</a>
        </div>
      </div>
      <div>
        <div class="specialty-grid">
''' + specialty_grid() + '''
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ── Care settings ─────────────────────────── -->
<section class="section section-alt">
  <div class="container">
    <div class="centered">
      <span class="section-kicker">Care Settings We Serve</span>
      <h2 class="section-title">Healthcare Talent for Every Care Setting</h2>
      <div class="section-divider"></div>
      <p class="section-sub">From health systems to single-specialty practices — we know how each one runs.</p>
    </div>
    <div class="industry-grid">
''' + settings_grid() + '''
    </div>
  </div>
</section>
''' + EOR + '''
<!-- ── FAQ ────────────────────────────────────── -->
<section class="section section-alt" aria-label="Frequently asked questions">
  <div class="container">
    <div class="centered">
      <span class="section-kicker">Common Questions</span>
      <h2 class="section-title">Everything You Need to Know</h2>
    </div>
    <div class="faq" itemscope itemtype="https://schema.org/FAQPage">
''' + faq_html() + '''
    </div>
  </div>
</section>
''' + cta()

# ───────────────────────────── Services ─────────────────────────────
def svc_block(id_, tag, h3, p, items, btn, aside_icon, aside_title, aside_items, fee_label, fee_text, dark=False):
    lis = "\n".join(f"          <li>{i}</li>" for i in items)
    alis = "\n".join(f"          <li>{i}</li>" for i in aside_items)
    cls = "svc-block" + (" svc-block--dark" if dark else "")
    btn_cls = "btn btn-white" if dark else "btn btn-primary"
    return f'''
    <div class="{cls}" id="{id_}">
      <div>
        <span class="pill-tag">{tag}</span>
        <h3>{h3}</h3>
        <p>{p}</p>
        <ul class="checklist">
{lis}
        </ul>
        <a href="request-talent.html" class="{btn_cls}">{btn}</a>
      </div>
      <div class="svc-aside">
        <div class="aside-ico">[[ico:{aside_icon}]]</div>
        <h4>{aside_title}</h4>
        <ul>
{alis}
        </ul>
        <div class="fee">
          <div class="fee-label">{fee_label}</div>
          <div class="fee-text">{fee_text}</div>
        </div>
      </div>
    </div>'''


TITLE_GROUPS = [
    ("Nursing", ["Registered Nurse (RN)", "Licensed Practical Nurse (LPN)", "Certified Nursing Assistant (CNA)",
                 "Charge Nurse &amp; Nurse Manager", "Director of Nursing (DON)", "Chief Nursing Officer (CNO)"]),
    ("Physicians &amp; Advanced Practice", ["Physician (MD / DO)", "Medical Director", "Nurse Practitioner (NP)",
                                            "Physician Assistant (PA-C)", "CRNA", "Hospitalist &amp; Specialist"]),
    ("Allied Health &amp; Therapy", ["Radiologic, CT &amp; MRI Technologist", "Sonographer", "Surgical Technologist",
                                     "Medical Lab &amp; Phlebotomy", "Respiratory Therapist",
                                     "Physical, Occupational &amp; Speech Therapist"]),
    ("Medical Office &amp; Patient Access", ["Medical Assistant (MA / CMA)", "Front Desk &amp; Receptionist",
                                             "Scheduler &amp; Patient Access", "Referral Coordinator",
                                             "Precertification &amp; Prior Auth", "Credentialing &amp; Payer Enrollment"]),
    ("Revenue Cycle, Coding &amp; Finance", ["CFO &amp; Controller", "Director of Revenue Cycle",
                                             "Medical Coder (CPC / CCS)", "CDI Specialist",
                                             "Billing, A/R &amp; Collections", "Reimbursement &amp; Cost Report Analyst"]),
    ("Healthcare Leadership", ["CEO, COO &amp; Hospital Administrator", "Practice Administrator",
                               "Practice &amp; Clinic Manager", "Director of Operations",
                               "Quality &amp; Compliance Manager", "Healthcare HR Manager"]),
]


def title_groups():
    out = []
    for g, titles in TITLE_GROUPS:
        items = "\n".join(f'          <div class="specialty-item"><span class="specialty-dot"></span>{t}</div>' for t in titles)
        out.append(f'''      <div>
        <h3 style="font-size:1.1rem;margin-bottom:14px;">{g}</h3>
        <div class="specialty-grid" style="grid-template-columns:1fr;">
{items}
        </div>
      </div>''')
    return "\n".join(out)


SERVICES = page_hero("Services", "Our Recruiting Services",
                     "Flexible hiring for hospitals, physician practices, and healthcare organizations — clinical and non-clinical, temp or direct hire.",
                     "photo-1538108149393-fbbd81895907") + '''
<!-- ── Services ───────────────────────────────── -->
<section class="section">
  <div class="container">
    <span class="section-kicker">What We Offer</span>
    <h2 class="section-title">Six Ways We Help You Hire</h2>
    <div class="svc-blocks">''' + svc_block(
    "direct", "Direct Hire", "Direct Hire Placement",
    "When you need the right person in a seat for the long haul, our direct hire model delivers a curated shortlist of qualified, motivated healthcare candidates — fast.",
    ["Deep intake call — role, schedule, setting, and team", "Active and passive candidate sourcing",
     "License and certification checks", "Behavioral and skills pre-screening",
     "Reference and background coordination", "Offer negotiation and onboarding support", "Replacement guarantee included"],
    "Start a Direct Hire Search", "stethoscope", "Best For",
    ["Registered nurses and nurse leaders", "Nurse practitioners, PAs, and physicians", "Allied health and imaging techs",
     "Medical assistants and front office staff", "Practice administrators, revenue cycle, and finance"],
    "Fee Structure", "Contingency — fee applies only upon successful placement") + svc_block(
    "temp", "Temp", "Healthcare Temp Staffing",
    "Need coverage for a leave, a vacancy, flu season, or a new clinic opening? Our healthcare temps step in quickly — screened and ready to work from day one.",
    ["Rapid deployment — often within 48–72 hours", "Assignments from a few days to 12+ months",
     "We handle payroll, taxes, and workers' comp", "Clinical, front office, and coding and billing temps",
     "Interim practice administrators, nurse managers, and finance leaders"],
    "Request a Temp", "clock", "Best For",
    ["Leave and vacancy coverage", "Flu season and volume surges", "New clinic and unit openings",
     "Coding and billing backlogs", "EHR conversions and go-lives"],
    "Fee Structure", "Bill rate per hour — no placement fee") + svc_block(
    "retained", "Retained Search", "Exclusive. Dedicated. Guaranteed.",
    "For your most critical hires — CEOs, CNOs, CFOs, administrators, medical directors, and confidential replacements — our retained model gives you an exclusive partnership, a dedicated search team, and a structured process built around your organization.",
    ["Exclusive engagement — we work for you alone on this search", "Dedicated search team with a structured weekly cadence",
     "Deep market mapping — active and passive candidates", "Confidential searches handled with full discretion",
     "Full replacement guarantee"],
    "Start a Retained Search", "award", "Best For",
    ["CEO, COO, CNO, and CFO searches", "Medical directors and physician leaders", "Confidential or backfill searches",
     "Succession planning", "PE-backed platforms and multi-site groups"],
    "Fee Structure", "Retainer paid in installments — a portion upfront, balance upon placement. Full replacement guarantee included.",
    dark=True) + svc_block(
    "temp-to-perm", "Temp-to-Perm", "Temp-to-Perm",
    "Start someone as a temp and move them to your payroll when you're sure of the fit. It lowers the risk for both sides — and works well while headcount approval is in progress.",
    ["Typical temp period of 90–180 days", "They work on your team from day one", "Conversion fee agreed upfront",
     "Ideal when headcount approval is in progress", "They learn your clinic, systems, and patients before converting"],
    "Explore Temp-to-Perm", "refresh", "Best For",
    ["Roles where team fit is critical", "New positions with evolving scope", "Front office and patient access teams",
     "Clinics under a hiring freeze", "High-volume medical assistant and nursing teams"],
    "Fee Structure", "Bill rate as a temp; reduced conversion fee when you hire them") + '''

    <div class="svc-block svc-block--top" id="rpo">
      <div>
        <span class="pill-tag">RPO &amp; Project Staffing</span>
        <h3>We Become Your Recruiting Department</h3>
        <p>Opening a new clinic, staffing a new unit, or hiring after an acquisition? Our Recruitment Process Outsourcing (RPO) solution gives you a dedicated recruiting partner — with processes built around your organization's exact needs.</p>
        <ul class="checklist">
          <li>Scalable — ramp up or down as hiring needs change</li>
          <li>We integrate with your ATS, culture, and hiring process</li>
          <li>Full project staffing from intake to offer</li>
          <li>Dedicated account manager and weekly reporting</li>
          <li>Works alongside your existing HR team</li>
        </ul>
        <a href="request-talent.html" class="btn btn-primary">Tell Us About Your Project</a>
      </div>
      <div class="tool-cards">
        <div class="tool-card">
          <div class="tool-ico">[[ico:clipboard]]</div>
          <div>
            <h4>Customized Screening Questionnaires</h4>
            <p>We build role-specific screening questions with your input, then send the candidate's answers with every résumé — licenses, specialties, schedule, and fit answered up front.</p>
          </div>
        </div>
        <div class="tool-card">
          <div class="tool-ico">[[ico:video]]</div>
          <div>
            <h4>Optional Video Introductions</h4>
            <p>We invite every candidate to film a short video introduction. You see how they communicate before the first call — not just a PDF.</p>
            <div style="margin-top:14px;"><div class="mini-stat-num">1,000+</div><div class="mini-stat-label">Candidate Video Intros Filmed</div></div>
          </div>
        </div>
        <div class="tool-card">
          <div class="tool-ico">[[ico:wrench]]</div>
          <div>
            <h4>Fully Customized Recruiting &amp; Staffing Solutions</h4>
            <p>No two healthcare organizations hire the same way. We build a recruiting program around your timeline, budget, and team structure — from single hires to full department builds.</p>
          </div>
        </div>
      </div>
    </div>
''' + example() + '''

    <div class="svc-block svc-block--dark svc-block--top" id="audience">
      <div class="on-dark">
        <span class="pill-tag">Perfect Candidate Audience</span>
        <h3>Build the Perfect Candidate Audience</h3>
        <div class="pay-when-hire pay-when-hire--dark">[[ico:check]] <span>No upfront cost — you only pay when we're successful: when you hire. <span class="pwh-2">And we can payroll them for you.</span></span></div>
        <p>We build a list for your HR or recruiting team with the exact people you want to hire — then invite them to apply.</p>
        <ol class="num-steps">
        ''' + AUDIENCE_STEPS + '''
        </ol>
        <p style="font-size:.92rem;margin:-8px 0 0;">When you hire, pick how you pay: we payroll them for one bill rate — or one flat fee, quoted up front.</p>
        <a href="request-talent.html" class="btn btn-white">Build My Candidate Audience</a>
      </div>
      <div class="svc-aside">
        <div class="aside-ico">[[ico:users]]</div>
        <h4>We Can Handle the Rest</h4>
        <ul class="checklist">
          <li>We payroll your people — our back office is the Employer of Record</li>
          <li>Every hire gets our 401(k) program</li>
          <li>We can even provide benefits</li>
        </ul>
        <div class="fee">
          <div class="fee-label">We Help You the Entire Time</div>
          <div class="fee-text"><strong style="color:var(--white);">And you only pay when we're successful.</strong> We even have live office hours to help you with any questions — plus membership gets you access to our <a href="https://www.skool.com/100xrecruiting" target="_blank" rel="noopener">100X Recruiting community on Skool</a>. Our AI recruiting assistant comes with a 100% satisfaction guarantee.</div>
        </div>
      </div>
    </div>
    </div>
  </div>
</section>

<!-- ── Titles ─────────────────────────────────── -->
<section class="section section-alt" id="titles" style="scroll-margin-top:calc(var(--nav-h) + 8px);">
  <div class="container">
    <div class="centered">
      <span class="section-kicker">Specialties</span>
      <h2 class="section-title">Healthcare Titles We Fill</h2>
      <div class="section-divider"></div>
      <p class="section-sub">Clinical and non-clinical — at hospitals, practices, and every setting in between.</p>
    </div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:28px;margin-top:40px;">
''' + title_groups() + '''
    </div>
  </div>
</section>

<!-- ── Candidates ─────────────────────────────── -->
<section class="section section-dark">
  <div class="container split">
    <div>
      <span class="section-kicker">For Candidates</span>
      <h2 class="section-title">Your Next Healthcare<br>Career Move <em>Starts Here</em></h2>
      <p>Nurses, providers, techs, office staff, and revenue cycle pros: we represent you confidentially and introduce you to organizations that are hiring now — many of them before the role is ever posted.</p>
      <div style="display:flex;gap:12px;flex-wrap:wrap;">
        <a href="{{JOB_BOARD}}" target="_blank" rel="noopener" class="btn btn-white btn-lg">Browse Open Jobs ↗</a>
        <a href="contact.html" class="btn btn-outline-white btn-lg">Talk to a Recruiter</a>
      </div>
    </div>
    <div class="feature-list">
      <div class="feature">
        <div class="feature-icon">[[ico:lock]]</div>
        <div><h4>Confidential Representation</h4><p>Your name and employer stay hidden until you say yes to an introduction.</p></div>
      </div>
      <div class="feature">
        <div class="feature-icon">[[ico:video]]</div>
        <div><h4>Stand Out With a Video Intro</h4><p>Film a short introduction so hiring managers meet you before the first call.</p></div>
      </div>
      <div class="feature">
        <div class="feature-icon">[[ico:target]]</div>
        <div><h4>Roles That Fit Your Specialty</h4><p>Bedside, clinic, front desk, or business office — we only call when it's a real match.</p></div>
      </div>
    </div>
  </div>
</section>
''' + cta(h2="Ready to Fill a Critical Role?", p="Tell us about your open role and we'll deliver a shortlist in 48–72 hours.")

# ───────────────────────────── About ─────────────────────────────
def diff(icon, h4, p):
    return f'''      <div class="diff-item">
        <div class="diff-icon">[[ico:{icon}]]</div>
        <div>
          <h4>{h4}</h4>
          <p>{p}</p>
        </div>
      </div>'''


ABOUT = page_hero("About Us", "About MedPoint Partners",
                  "Healthcare recruiting and staffing — clinical and non-clinical — powered by NorthPoint and headquartered in Atlanta.",
                  "photo-1587351021759-3e566b6af7cc") + '''
<!-- ── Our Story ──────────────────────────────── -->
<section class="section">
  <div class="container">
    <div class="two-col">
      <div>
        <span class="section-kicker">Our Story</span>
        <h2 class="section-title">Everyone Wins When Clinicians Can Focus on Patients</h2>
        <div class="section-divider"></div>
        <p style="color:var(--text-muted);line-height:1.85;margin-bottom:18px;">We help hospitals, physician practices, and healthcare organizations find and hire the people they need — so they can focus on their patients, and that makes everyone win.</p>
        <p style="color:var(--text-muted);line-height:1.85;margin-bottom:18px;">We recruit for every seat on a healthcare team: nurses and nurse leaders, physicians and advanced practice providers, allied health and therapy, medical assistants and the front office, coding, billing and revenue cycle, finance, and leadership. When you call us, you're speaking with someone who knows the difference between an ortho PA who first-assists and one who only works in clinic — and which candidates belong in each seat.</p>
        <p style="color:var(--text-muted);line-height:1.85;margin-bottom:32px;">We cast a wide net with targeted advertising and direct sourcing — then narrow it to the few people who fit your role, your schedule, and your team.</p>
        <div class="mini-stats">
          <div><div class="mini-stat-num">105+</div><div class="mini-stat-label">Years Combined Experience</div></div>
          <div><div class="mini-stat-num">1,000+</div><div class="mini-stat-label">Candidate Video Intros</div></div>
          <div><div class="mini-stat-num">48–72h</div><div class="mini-stat-label">Average Shortlist Delivery</div></div>
        </div>
      </div>
      <div>
        <img class="img-frame" src="{{UNS}}photo-1666214280557-f1b5022eb634?auto=format&fit=crop&w=800&q=80" alt="Healthcare team reviewing results together" loading="lazy">
      </div>
    </div>
  </div>
</section>

<!-- ── Why Choose Us ─────────────────────────── -->
<section class="section section-alt">
  <div class="container">
    <div class="centered">
      <span class="section-kicker">Why MedPoint Partners</span>
      <h2 class="section-title">Healthcare Recruiting Done Differently</h2>
      <div class="section-divider"></div>
      <p class="section-sub">Healthcare is our specialty — clinical and non-clinical — and that focus changes everything.</p>
    </div>
    <div class="diff-grid">
''' + "\n".join([
    diff("stethoscope", "Healthcare Specialists", "We understand the licenses, certifications, schedules, settings, and pay norms behind every healthcare role — the things generalist firms guess at."),
    diff("target", "Wide Net, Precise Shortlist", "Targeted advertising and direct sourcing reach people who aren't on job boards — then we narrow it to the handful of candidates who actually fit."),
    diff("zap", "Fast Shortlists", "We don't let searches sit. Expect a blinded shortlist of pre-screened candidates within 48–72 hours of your request."),
    diff("clipboard", "Custom Screening Questionnaires", "For every search we build a questionnaire with your input. Every résumé arrives with the candidate's answers — specialty, schedule, license, EHR — so your questions are answered up front."),
    diff("video", "Video Introductions", "Candidates can film a short video introduction, so you see how they communicate before the first call."),
    diff("shield", "Guaranteed &amp; Fully Back-Officed", "Every direct hire is backed by our replacement guarantee, and every temp runs through our Employer of Record back office."),
]) + '''
    </div>
''' + example("margin-top:28px;") + '''
  </div>
</section>

<!-- ── Values ─────────────────────────────────── -->
<section class="section">
  <div class="container split">
    <div>
      <span class="section-kicker">Our Values</span>
      <h2 class="section-title">What Guides Every Search</h2>
      <div class="section-divider"></div>
      <p class="section-sub">The right hire protects patient care, your team, and your margins.</p>
    </div>
    <ul class="checklist">
      <li><strong>Patients first.</strong> Strong teams — at the bedside and in the business office — keep care organizations healthy enough to serve their communities.</li>
      <li><strong>Depth over volume.</strong> A few right-fit candidates beat a stack of maybe-fits every time.</li>
      <li><strong>Discretion.</strong> Confidential searches and blinded profiles protect clients and candidates alike.</li>
      <li><strong>Straight answers.</strong> Honest feedback on the market, pay, and candidates — even when it's not what you hoped to hear.</li>
    </ul>
  </div>
</section>

<!-- ── Settings ───────────────────────────────── -->
<section class="section section-alt" id="settings" style="scroll-margin-top:calc(var(--nav-h) + 8px);">
  <div class="container">
    <div class="centered">
      <span class="section-kicker">Care Settings We Serve</span>
      <h2 class="section-title">Healthcare Talent for Every Care Setting</h2>
      <div class="section-divider"></div>
      <p class="section-sub">Each setting runs, staffs, and bills differently. We recruit for the one you're in.</p>
    </div>
    <div class="industry-grid">
''' + settings_grid() + '''
    </div>
  </div>
</section>
''' + cta(h2="Let's Work Together", p="Hiring for your clinical or business team? Tell us about the role — we'll take it from there.")

# ───────────────────────────── Temp staffing ─────────────────────────────
def feat(icon, h4, p):
    return f'''      <div class="trio-card">
        <div class="feature-icon">[[ico:{icon}]]</div>
        <h4>{h4}</h4>
        <p>{p}</p>
      </div>'''


TEMP = page_hero("Temp Staffing", "Healthcare <em>Temp</em> Staffing",
                 "Nurses, medical assistants, techs, front office, and coding and billing temps — plus interim leaders — with MedPoint as Employer of Record.",
                 "photo-1631217868264-e5b90bb7e133") + '''
<!-- ── Use cases ──────────────────────────────── -->
<section class="section">
  <div class="container">
    <div class="centered">
      <span class="section-kicker">When Healthcare Organizations Call Us</span>
      <h2 class="section-title">Coverage for the Gaps That Hurt Patient Care</h2>
      <div class="section-divider"></div>
      <p class="section-sub">Short staffing means longer waits, burned-out teams, and unbilled claims. Temps close the gap while you hire — or for as long as you need.</p>
    </div>
    <div class="trio">
''' + "\n".join([
    feat("stethoscope", "Nursing Coverage", "RNs, LPNs, and CNAs for leaves, vacancies, and busy seasons — in clinics, surgery centers, and post-acute settings."),
    feat("users", "Medical Assistants", "MAs and CMAs who room patients, take vitals, and keep providers on schedule."),
    feat("activity", "Imaging &amp; Surgical Techs", "Radiology, CT, MRI, ultrasound, and surgical techs for vacancies and new service lines."),
    feat("phone", "Front Desk &amp; Patient Access", "Receptionists, schedulers, and referral and prior auth staff who keep phones answered and patients moving."),
    feat("file", "Coding &amp; Billing Backlogs", "Certified coders, billers, and A/R follow-up to clear backlogs and get claims out the door."),
    feat("briefcase", "Interim Leaders", "Interim practice administrators, nurse managers, revenue cycle directors, and finance leaders during a search or a turnaround."),
]) + '''
    </div>
  </div>
</section>

<!-- ── How it works ──────────────────────────── -->
<section class="section section-alt">
  <div class="container">
    <span class="section-kicker">How It Works</span>
    <h2 class="section-title">Healthcare Temps in Four Steps</h2>
    <div class="section-divider"></div>
    <div class="steps-row">
      <div class="step"><div class="step-num">1</div><h4>Tell Us the Gap</h4><p>The role, shifts, setting, and how long you need coverage.</p></div>
      <div class="step"><div class="step-num">2</div><h4>Meet Available Temps</h4><p>We send pre-screened, available-now candidates — often within 48–72 hours.</p></div>
      <div class="step"><div class="step-num">3</div><h4>They Start</h4><p>Onsite, hybrid, or remote. Assignments from a few days to 12+ months.</p></div>
      <div class="step"><div class="step-num">4</div><h4>We Run Payroll</h4><p>Weekly payroll, taxes, and workers' comp through our Employer of Record back office — one invoice to you.</p></div>
    </div>
  </div>
</section>
''' + EOR + '''
<!-- ── Request form ───────────────────────────── -->
<section class="section" id="request">
  <div class="container">
    <div class="centered">
      <span class="section-kicker">Request a Temp</span>
      <h2 class="section-title">Tell Us What You Need Covered</h2>
      <div class="section-divider"></div>
      <p class="section-sub">We'll reply within a few hours with availability and a bill rate.</p>
    </div>
    <div class="form-card form-narrow">
      <form data-form="medpoint-temp-request" action="mailto:{{EMAIL}}" method="POST" enctype="text/plain">
        <div class="form-row">
          <div class="form-group"><label for="c-first">First Name *</label><input type="text" id="c-first" name="first_name" class="form-control" required></div>
          <div class="form-group"><label for="c-last">Last Name *</label><input type="text" id="c-last" name="last_name" class="form-control" required></div>
        </div>
        <div class="form-row">
          <div class="form-group"><label for="c-email">Work Email *</label><input type="email" id="c-email" name="email" class="form-control" required></div>
          <div class="form-group"><label for="c-company">Organization *</label><input type="text" id="c-company" name="company" class="form-control" required></div>
        </div>
        <div class="form-row">
          <div class="form-group"><label for="c-role">Role *</label><input type="text" id="c-role" name="role_title" class="form-control" placeholder="e.g. 2 medical assistants" required></div>
          <div class="form-group"><label for="c-timeline">How long?</label>
            <select id="c-timeline" name="timeline" class="form-control">
              <option value="" disabled selected>Select</option>
              <option>Under 1 month</option><option>1–3 months</option><option>3–6 months</option><option>6+ months</option><option>Not sure yet</option>
            </select>
          </div>
        </div>
        <div class="form-group"><label for="c-notes">Shifts, setting, EHR, onsite?</label><textarea id="c-notes" name="notes" class="form-control" placeholder="e.g. Mon–Fri 8–5, ortho clinic, athenahealth, starts Monday"></textarea></div>
        <input type="hidden" name="hire_type" value="Temp">
        <button type="submit" class="btn btn-primary btn-lg btn-block">Request a Temp →</button>
        <p class="form-note">No commitment. Prefer to talk? Call <a href="tel:+14042500790" style="color:var(--blue);font-weight:600;">404-250-0790</a>.</p>
        <div class="alert alert-success">✓ Request received! We'll be in touch within a few hours.</div>
      </form>
    </div>
  </div>
</section>
''' + cta(h2="Need a Direct Hire Instead?", p="Our direct hire and retained searches deliver a shortlist in 48–72 hours.")

# ───────────────────────────── Request talent ─────────────────────────────
def optin_step(n, title, text):
    return f'''          <div class="optin-step">
            <div class="optin-step-num">{n}</div>
            <div><strong>{title}</strong><span>{text}</span></div>
          </div>'''


REQUEST = '''
<!-- ── Opt-in Hero ────────────────────────────── -->
<section class="optin-hero" style="background-image:url('{{UNS}}photo-1666214280391-8ff5bd3c0bf0?auto=format&fit=crop&w=1600&q=80');">
  <div class="container">
    <div class="hero-badge" style="color:rgba(255,255,255,.85);">For Hiring Managers</div>
    <h1>Get a Shortlist of<br><em>Qualified Candidates</em><br>in 48–72 Hours</h1>
    <p>Tell us about your open role and we'll get to work immediately — tapping our pre-screened network of clinical and non-clinical healthcare professionals.</p>
  </div>
</section>

<!-- ── Form + Pitch ───────────────────────────── -->
<section class="section" style="padding-top:0;background:var(--off-white);">
  <div class="container">
    <div class="optin-layout">
      <div class="optin-pitch">
        <span class="section-label">Why MedPoint Partners</span>
        <h2 class="section-title" style="font-size:1.6rem;">What Happens After<br>You Submit</h2>
        <div class="optin-steps">
''' + "\n".join([
    optin_step(1, "Discovery Call (same day)", "We reach out within hours to clarify the role, schedule, setting, and timeline."),
    optin_step(2, "Targeted Search (24–48 hrs)", "We search our active network and reach passive candidates not on job boards."),
    optin_step(3, "Shortlist Delivered (48–72 hrs)", "Receive a curated shortlist of pre-screened, interview-ready candidates — licenses checked, questionnaire answered."),
    optin_step(4, "You Interview. We Coordinate.", "We handle scheduling, feedback, offers, and back every direct hire placement with our replacement guarantee."),
]) + '''
        </div>
        <div class="optin-box">
          <div class="box-label">What We Place</div>
          <div class="tags">
            <span class="tag">RNs</span><span class="tag">LPNs &amp; CNAs</span><span class="tag">Nurse Practitioners</span>
            <span class="tag">PA-Cs</span><span class="tag">Physicians</span><span class="tag">Medical Assistants</span>
            <span class="tag">Imaging Techs</span><span class="tag">Therapists</span><span class="tag">Front Desk</span>
            <span class="tag">Coders &amp; Billers</span><span class="tag">Practice Administrators</span><span class="tag">+ more</span>
          </div>
        </div>
      </div>

      <div class="form-card form-card--lift">
        <h3>Request Healthcare Talent</h3>
        <p class="form-intro">No commitment required — let's see if we can help.</p>
        <form data-form="medpoint-talent-request" action="mailto:{{EMAIL}}" method="POST" enctype="text/plain">
          <div class="form-legend">About You</div>
          <div class="form-row">
            <div class="form-group"><label for="r-first">First Name *</label><input type="text" id="r-first" name="first_name" class="form-control" placeholder="Jane" required></div>
            <div class="form-group"><label for="r-last">Last Name *</label><input type="text" id="r-last" name="last_name" class="form-control" placeholder="Smith" required></div>
          </div>
          <div class="form-row">
            <div class="form-group"><label for="r-email">Work Email *</label><input type="email" id="r-email" name="email" class="form-control" placeholder="jane@yourpractice.com" required></div>
            <div class="form-group"><label for="r-phone">Phone</label><input type="tel" id="r-phone" name="phone" class="form-control" placeholder="(404) 555-0100"></div>
          </div>
          <div class="form-row">
            <div class="form-group"><label for="r-company">Organization *</label><input type="text" id="r-company" name="company" class="form-control" placeholder="Your hospital or practice" required></div>
            <div class="form-group"><label for="r-title">Your Title</label><input type="text" id="r-title" name="your_title" class="form-control" placeholder="Practice Administrator"></div>
          </div>
          <div class="form-legend">About the Role</div>
          <div class="form-row">
            <div class="form-group"><label for="r-role">Role Title *</label><input type="text" id="r-role" name="role_title" class="form-control" placeholder="Registered Nurse (RN)" required></div>
            <div class="form-group"><label for="r-type">Hire Type *</label>
              <select id="r-type" name="hire_type" class="form-control" required>
                <option value="" disabled selected>Select</option>
                <option>Direct Hire</option><option>Temp</option><option>Temp-to-Perm</option><option>Retained Search</option><option>Not sure yet</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group"><label for="r-setting">Care Setting</label>
              <select id="r-setting" name="setting" class="form-control">
                <option value="" disabled selected>Select</option>
                <option>Hospital / Health System</option><option>Physician Group / Specialty Practice</option><option>Ambulatory Surgery Center</option>
                <option>Urgent Care / Primary Care</option><option>Home Health / Hospice</option><option>Behavioral Health</option>
                <option>Senior Living / Post-Acute</option><option>Lab / Imaging / Diagnostics</option><option>PT / Rehab Clinic</option><option>Other</option>
              </select>
            </div>
            <div class="form-group"><label for="r-location">Location *</label><input type="text" id="r-location" name="location" class="form-control" placeholder="Atlanta, GA or Remote" required></div>
          </div>
          <div class="form-row">
            <div class="form-group"><label for="r-timeline">Timeline</label>
              <select id="r-timeline" name="timeline" class="form-control">
                <option value="" disabled selected>Select</option>
                <option>ASAP — within 2 weeks</option><option>1 month</option><option>1–3 months</option><option>Planning ahead (3+ months)</option>
              </select>
            </div>
            <div class="form-group"><label for="r-comp">Pay Range</label><input type="text" id="r-comp" name="compensation" class="form-control" placeholder="e.g. $85K – $95K or $32/hr"></div>
          </div>
          <div class="form-group"><label for="r-notes">Anything else we should know?</label><textarea id="r-notes" name="notes" class="form-control" placeholder="Must-haves, licenses (RN, PA-C, ARRT, CPC), schedule, EHR (Epic, athena), team size…"></textarea></div>
          <button type="submit" class="btn btn-primary btn-lg btn-block">Submit Talent Request →</button>
          <p class="form-note">No commitment to submit. We'll reach out within a few hours.</p>
          <div class="alert alert-success">✓ Request received! We'll be in touch within a few hours to discuss your search.</div>
        </form>
      </div>
    </div>
  </div>
</section>

<script>
/* Card links arrive as ?candidate=GR-01 — note it in the form so we know who they asked about */
(function(){var c=new URLSearchParams(location.search).get('candidate');if(!c||!/^[A-Z]{2}-\\d{1,3}$/.test(c))return;
var n=document.getElementById('r-notes');if(n&&!n.value)n.value="I'd like to talk about candidate "+c+".";})();
</script>

<!-- ── Proof strip ────────────────────────────── -->
<section style="background:var(--white);padding:48px 0;border-top:1px solid var(--border);">
  <div class="container">
    <div class="stats-box" style="margin:0;">
      <div class="stat-item"><div class="stat-num">48–72 hrs</div><div class="stat-label">Average Shortlist Delivery</div></div>
      <div class="stat-item"><div class="stat-num">1,000+</div><div class="stat-label">Candidate Video Intros Filmed</div></div>
      <div class="stat-item"><div class="stat-num">105+</div><div class="stat-label">Years Combined Experience</div></div>
      <div class="stat-item"><div class="stat-num">20+</div><div class="stat-label">Years Recruiting &amp; Staffing</div></div>
    </div>
  </div>
</section>
'''

# ───────────────────────────── Contact ─────────────────────────────
CONTACT = page_hero("Contact", "Get in Touch",
                    "Whether you're hiring, exploring a career move, or just have a question — we'd love to hear from you.",
                    "photo-1576091160399-112ba8d25d1d", "center 30%") + '''
<section class="section">
  <div class="container">
    <div class="contact-grid">
      <div>
        <span class="section-label">Contact Information</span>
        <h2 class="section-title">Let's Start a Conversation</h2>
        <p style="color:var(--text-muted);line-height:1.8;">We typically respond within one business day. For urgent staffing needs, call or email directly and mention your timeline.</p>
        <div class="contact-list">
          <div class="contact-item">
            <div class="contact-icon">[[ico:phone]]</div>
            <div><div class="contact-label">Phone</div><a href="tel:+14042500790">404-250-0790</a><br><a href="tel:+16787775627">678-777-5627</a></div>
          </div>
          <div class="contact-item">
            <div class="contact-icon">[[ico:mail]]</div>
            <div><div class="contact-label">Email</div><a href="mailto:{{EMAIL}}">{{EMAIL}}</a></div>
          </div>
          <div class="contact-item">
            <div class="contact-icon">[[ico:pin]]</div>
            <div><div class="contact-label">Location</div><strong>Atlanta, GA</strong><div class="contact-sub">Serving the Southeast &amp; nationwide</div></div>
          </div>
          <div class="contact-item">
            <div class="contact-icon">[[ico:briefcase]]</div>
            <div><div class="contact-label">Job Board</div><a href="{{JOB_BOARD}}" target="_blank" rel="noopener" style="color:var(--blue);">View Open Positions ↗</a></div>
          </div>
        </div>
        <div class="note-card">
          <h4>Looking for a job?</h4>
          <p>Browse current healthcare openings on our job board.</p>
          <a href="{{JOB_BOARD}}" target="_blank" rel="noopener" class="btn btn-primary">Browse Open Jobs ↗</a>
        </div>
      </div>

      <div class="form-card">
        <h3>Send Us a Message</h3>
        <p class="form-intro">We'll get back to you within one business day.</p>
        <form data-form="medpoint-contact" action="mailto:{{EMAIL}}" method="POST" enctype="text/plain">
          <div class="form-row">
            <div class="form-group"><label for="m-first">First Name *</label><input type="text" id="m-first" name="first_name" class="form-control" required></div>
            <div class="form-group"><label for="m-last">Last Name *</label><input type="text" id="m-last" name="last_name" class="form-control" required></div>
          </div>
          <div class="form-row">
            <div class="form-group"><label for="m-email">Email *</label><input type="email" id="m-email" name="email" class="form-control" required></div>
            <div class="form-group"><label for="m-phone">Phone</label><input type="tel" id="m-phone" name="phone" class="form-control"></div>
          </div>
          <div class="form-row">
            <div class="form-group"><label for="m-company">Organization</label><input type="text" id="m-company" name="company" class="form-control"></div>
            <div class="form-group"><label for="m-topic">I'm…</label>
              <select id="m-topic" name="topic" class="form-control">
                <option>Hiring for my organization</option><option>Looking for a new role</option><option>Interested in the Partner Program</option><option>Something else</option>
              </select>
            </div>
          </div>
          <div class="form-group"><label for="m-message">Message *</label><textarea id="m-message" name="message" class="form-control" required></textarea></div>
          <button type="submit" class="btn btn-primary btn-lg btn-block">Send Message →</button>
          <div class="alert alert-success">✓ Message sent! We'll be in touch within one business day.</div>
        </form>
        <p class="form-note" style="margin-top:20px;">Privacy: we use what you send only to respond to you, and we never sell your information.</p>
      </div>
    </div>
  </div>
</section>
'''

# ───────────────────────────── Partners ─────────────────────────────
def earn(num, h4, p):
    return f'''      <div class="earn-card">
        <div class="earn-num">{num}</div>
        <h4>{h4}</h4>
        <p>{p}</p>
      </div>'''


PARTNERS = page_hero("Partner Program", "Join Our Partner Program",
                     "You spent your career building relationships in healthcare. Put them to work — you bring the hiring need, we do all the recruiting, and you get paid.",
                     "photo-1542744173-8e7e53415bb0") + '''
<section class="section">
  <div class="container">
    <div class="centered">
      <span class="section-kicker">For Physicians, Healthcare Leaders &amp; Anyone Whose Network Hires</span>
      <h2 class="section-title">You get the order. We fill it.</h2>
      <div class="section-divider"></div>
      <p class="section-sub">You get paid for every hour someone works.</p>
    </div>
    <div class="trio">
''' + "\n".join([
    feat("handshake", "You get the order", 'Hear "we need to hire" from someone in your network — and make the introduction.'),
    feat("search", "We fill it", "Our recruiters run the entire search — sourcing, screening, and placing. Temp, temp-to-perm, or direct hire."),
    feat("receipt", "You get paid", "A referral fee on direct hire placements, and a recurring share of every hour your client's temps work — for the life of the assignment."),
]) + '''
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <div class="centered">
      <span class="section-kicker">What You Earn</span>
      <h2 class="section-title">Simple, generous, recurring.</h2>
      <div class="section-divider"></div>
    </div>
    <div class="earn-grid">
''' + "\n".join([
    earn("10%", "Direct hire placements", "Your client hires direct through us — you earn 10% of the placement fee we collect. Paid when we collect from the client."),
    earn("25%", "Temp net spread", "Your client runs temps or temp-to-perm workers — you earn 25% of the net spread on every hour they bill."),
    earn("Recurring", "While they work", "Temp commissions aren't one-time. They keep paying as long as your client's temps keep billing. Build a book."),
    earn("15th", "Paid every month", "Commissions are calculated on money actually received and paid on the 15th of the following month. Every dollar tracked for you."),
]) + '''
    </div>
  </div>
</section>

<section class="section">
  <div class="container split" style="align-items:start;">
    <div>
      <span class="section-kicker">Who This Is For</span>
      <h2 class="section-title">Anyone whose network hires.</h2>
      <div class="section-divider"></div>
      <p class="section-sub">Physicians and practice owners. Nurse leaders and practice administrators. Hospital executives. Healthcare consultants, CPAs, and vendors. Retired healthcare executives. You never become a recruiter — you bring the hiring need and stay the relationship owner; our team fills the order.</p>
    </div>
    <div>
      <span class="section-kicker">How It Works</span>
      <h2 class="section-title">Four simple steps.</h2>
      <ol class="num-steps">
        <li><strong>Apply below</strong> — we review every partner personally and set you up.</li>
        <li><strong>Hear "we need two medical assistants"</strong> (or a nurse manager, a PA, a whole front office) — send it in.</li>
        <li><strong>Our recruiters fill the order</strong> — temp, temp-to-perm, or direct hire.</li>
        <li><strong>You're paid on the 15th of the following month</strong> — 10% of the fee on direct hire, 25% of net spread on temps, recurring while the worker bills.</li>
      </ol>
    </div>
  </div>
  <div class="container">
    <p class="fine-print">Net spread = what the client pays, minus worker wages and employer burden (taxes, workers comp, benefits, compliance). Commissions are calculated on payments actually received; refunded or unpaid invoices are reversed. Self-referrals and organizations already under agreement with us don't qualify. Earned commissions are never reduced.</p>
  </div>
</section>

<section class="section section-alt" id="apply">
  <div class="container">
    <div class="centered">
      <span class="section-kicker">Apply</span>
      <h2 class="section-title">Become a Partner</h2>
      <div class="section-divider"></div>
      <p class="section-sub">Sixty seconds. We review every application personally and reply within one business day.</p>
    </div>
    <div class="form-card form-narrow">
      <form data-form="medpoint-partner" action="mailto:{{EMAIL}}" method="POST" enctype="text/plain">
        <div class="form-row">
          <div class="form-group"><label for="p-name">Your Name *</label><input type="text" id="p-name" name="name" class="form-control" required></div>
          <div class="form-group"><label for="p-company">Company / Organization</label><input type="text" id="p-company" name="company" class="form-control"></div>
        </div>
        <div class="form-row">
          <div class="form-group"><label for="p-email">Work Email *</label><input type="email" id="p-email" name="email" class="form-control" required></div>
          <div class="form-group"><label for="p-phone">Phone</label><input type="tel" id="p-phone" name="phone" class="form-control"></div>
        </div>
        <div class="form-group"><label for="p-notes">Tell us about your network</label><textarea id="p-notes" name="notes" class="form-control" placeholder="e.g. Practice administrator; I know office managers at 30+ Atlanta clinics"></textarea></div>
        <button type="submit" class="btn btn-primary btn-lg btn-block">Apply to be a Partner →</button>
        <div class="alert alert-success">✓ Application received. We'll be in touch within one business day.</div>
      </form>
    </div>
  </div>
</section>
'''

PAGES = [
    ("index.html", "Healthcare Recruiting &amp; Staffing in Atlanta | MedPoint Partners",
     "Atlanta healthcare recruiting and staffing. Nurses, NPs, PAs, physicians, allied health, medical office, revenue cycle, and leadership. Temp, temp-to-perm, and direct hire.",
     HOME, faq_schema(), HOME_HEAD),
    ("services.html", "Healthcare Recruiting &amp; Staffing Services | MedPoint Partners",
     "Direct hire, temp, temp-to-perm, retained search, and RPO for clinical and non-clinical healthcare roles.",
     SERVICES, None, ""),
    ("about.html", "About | Healthcare Recruiters in Atlanta | MedPoint Partners",
     "MedPoint Partners helps hospitals, physician practices, and healthcare organizations hire clinical and non-clinical talent, so they can focus on their patients. Powered by NorthPoint, based in Atlanta.",
     ABOUT, None, ""),
    ("temp-staffing.html", "Healthcare Temp &amp; Temp-to-Perm Staffing | MedPoint Partners",
     "Healthcare temps: nurses, medical assistants, techs, front office, coding and billing, and interim leaders, with MedPoint as Employer of Record.",
     TEMP, None, ""),
    ("request-talent.html", "Request Talent | Healthcare Recruiting | MedPoint Partners",
     "Tell us about your open healthcare role and get a shortlist of qualified candidates in 48–72 hours.",
     REQUEST, None, ""),
    ("contact.html", "Contact | MedPoint Partners | Healthcare Recruiting in Atlanta",
     "Call 404-250-0790 or send a message. Healthcare recruiting and staffing for hospitals, physician practices, and healthcare organizations.",
     CONTACT, None, ""),
    ("partners.html", "Partner Program | Refer &amp; Earn | MedPoint Partners",
     "Physicians and healthcare leaders: refer a hiring need, we fill it, and you earn 10% on direct hire placements and 25% of temp net spread.",
     PARTNERS, None, ""),
]

# Old ClickFunnels addresses -> the new page that covers the same thing. Each gets a tiny page
# that forwards at once (Render's own redirect rules never took effect for these).
OLD_LINKS = {
    "about-us.html": "/about.html",
    "our-mission.html": "/about.html",
    "how-we-work.html": "/services.html",
    "contract-staffing.html": "/temp-staffing.html",
    "blog.html": "/services.html",
    "blog/index.html": "/services.html",
    "blog/director-of-revenue-cycle.html": "/",
    "blog/director-of-revenue-cycle--443fc.html": "/",
    "thankyou.html": "/",
    "product3.html": "/",
    "sitemap.html": "/sitemap.xml",
}


def forward_page(to):
    url = SITE + to
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<title>MedPoint Partners</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{url}">
<meta http-equiv="refresh" content="0; url={to}">
<script>location.replace("{to}" + location.hash);</script>
</head><body><p>This page moved. <a href="{to}">Go to the new page</a>.</p></body></html>
'''


if __name__ == "__main__":
    for file, title, desc, body, schema, extra in PAGES:
        html = head(file, title, desc, schema, extra) + NAV + body + FOOTER
        (OUT / file).write_text(fill(html), encoding="utf-8")
        print("wrote", file)
    for file, to in OLD_LINKS.items():
        (OUT / file).parent.mkdir(exist_ok=True)
        (OUT / file).write_text(forward_page(to), encoding="utf-8")
    print("wrote", len(OLD_LINKS), "forwarding pages for old addresses")
