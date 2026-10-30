"""Build every MedPoint Partners page from this one file.

The pages share one menu and footer, so edit the copy here and rebuild
instead of editing the .html files by hand (a rebuild overwrites them):

    python tools/build_pages.py            # writes into the site folder
    python tools/build_pages.py <folder>   # writes somewhere else (for a test)

School staffing copy lives beside this file: tools/school_roles.py (the 23 roles),
tools/school_states.py (state pages) and tools/school_articles.py (explainers).
"""
import json
import re
import sys
from html import unescape
from pathlib import Path

from school_articles import ARTICLES
from school_pay import GUIDE, PAY, money, school_share
from school_roles import DISPLAY_ORDER, GROUPS, ROLES
from school_states import STATES

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
    "speech": '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/><path d="M8 12h.01"/><path d="M12 12h.01"/><path d="M16 12h.01"/>',
    "idea": '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/>',
    "puzzle": '<path d="M19.439 7.85c-.049.322.059.648.289.878l1.568 1.568c.47.47.706 1.087.706 1.704s-.235 1.233-.706 1.704l-1.611 1.611a.98.98 0 0 1-.837.276c-.47-.07-.802-.48-.968-.925a2.501 2.501 0 1 0-3.214 3.214c.446.166.855.497.925.968a.979.979 0 0 1-.276.837l-1.61 1.61a2.404 2.404 0 0 1-1.705.707 2.402 2.402 0 0 1-1.704-.706l-1.568-1.568a1.026 1.026 0 0 0-.877-.29c-.493.074-.84.504-1.02.968a2.5 2.5 0 1 1-3.237-3.237c.464-.18.894-.527.967-1.02a1.026 1.026 0 0 0-.289-.877l-1.568-1.568A2.402 2.402 0 0 1 1.998 12c0-.617.236-1.234.706-1.704L4.23 8.77c.24-.24.581-.353.917-.303.515.077.877.528 1.073 1.01a2.5 2.5 0 1 0 3.259-3.259c-.482-.196-.933-.558-1.01-1.073-.05-.336.062-.676.303-.917l1.525-1.525A2.402 2.402 0 0 1 12 1.998c.617 0 1.234.236 1.704.706l1.568 1.568c.23.23.556.338.877.29.493-.074.84-.504 1.02-.968a2.5 2.5 0 1 1 3.237 3.237c-.464.18-.894.527-.967 1.02Z"/>',
    "school": '<path d="M21.42 10.922a1 1 0 0 0-.019-1.838L12.83 5.18a2 2 0 0 0-1.66 0L2.6 9.08a1 1 0 0 0 0 1.832l8.57 3.908a2 2 0 0 0 1.66 0z"/><path d="M22 10v6"/><path d="M6 12.5V16a6 3 0 0 0 12 0v-3.5"/>',
    "qr": '<rect width="5" height="5" x="3" y="3" rx="1"/><rect width="5" height="5" x="16" y="3" rx="1"/><rect width="5" height="5" x="3" y="16" rx="1"/><path d="M21 16h-3a2 2 0 0 0-2 2v3"/><path d="M21 21v.01"/><path d="M12 7v3a2 2 0 0 1-2 2H7"/><path d="M3 12h.01"/><path d="M12 3h.01"/><path d="M12 16v.01"/><path d="M16 12h1"/><path d="M21 12v.01"/><path d="M12 21v-1"/>',
    "ear": '<path d="M6 8.5a6.5 6.5 0 1 1 13 0c0 6-6 6-6 10a3.5 3.5 0 1 1-7 0"/><path d="M15 8.5a2.5 2.5 0 0 0-5 0v1a2 2 0 1 1 0 4"/>',
    "hand": '<path d="M18 11V6a2 2 0 0 0-2-2a2 2 0 0 0-2 2"/><path d="M14 10V4a2 2 0 0 0-2-2a2 2 0 0 0-2 2v2"/><path d="M10 10.5V6a2 2 0 0 0-2-2a2 2 0 0 0-2 2v8"/><path d="M18 8a2 2 0 1 1 4 0v6a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.86-5.99-2.34l-3.6-3.6a2 2 0 0 1 2.83-2.82L7 15"/>',
    "eye": '<path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"/><circle cx="12" cy="12" r="3"/>',
    "compass": '<path d="m16.24 7.76-1.804 5.411a2 2 0 0 1-1.265 1.265L7.76 16.24l1.804-5.411a2 2 0 0 1 1.265-1.265z"/><circle cx="12" cy="12" r="10"/>',
    "book": '<path d="M12 7v14"/><path d="M3 18a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h5a4 4 0 0 1 4 4 4 4 0 0 1 4-4h5a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1h-6a3 3 0 0 0-3 3 3 3 0 0 0-3-3z"/>',
    "monitor": '<rect width="20" height="14" x="2" y="3" rx="2"/><line x1="8" x2="16" y1="21" y2="21"/><line x1="12" x2="12" y1="17" y2="21"/>',
    "printer": '<path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><path d="M6 9V3a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v6"/><rect x="6" y="14" width="12" height="8" rx="1"/>',
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
        <li class="has-mega">
          <a href="school-staffing.html">School Roles <span class="chevron">▾</span></a>
          <div class="mega-menu">
{{SCHOOL_MEGA}}
            <div class="mega-featured">
              <div class="mega-featured-placeholder">[[ico:speech]]</div>
              <h4>Speech-Language Pathologists: Our Most-Requested Role</h4>
              <a href="school-slp-staffing.html" class="learn">School SLP Staffing →</a>
            </div>
          </div>
        </li>
        <li><a href="school-teletherapy-staffing.html">Teletherapy</a></li>
        <li class="has-mega">
          <a href="school-staffing.html#states">States <span class="chevron">▾</span></a>
          <div class="dropdown-menu">
{{STATE_NAV}}
          </div>
        </li>
        <li><a href="school-resources.html">Resources</a></li>
        <li class="has-mega">
          <a href="services.html">Healthcare <span class="chevron">▾</span></a>
          <div class="dropdown-menu">
            <a href="services.html">Healthcare Recruiting Services</a>
            <a href="services.html#titles">Healthcare Specialties</a>
            <a href="temp-staffing.html">Healthcare Temps</a>
            <a href="about.html#settings">Care Settings</a>
            <a href="request-talent.html">Request Healthcare Talent</a>
            <a href="partners.html">Partner Program</a>
          </div>
        </li>
        <li><a href="sell-for-us.html">Sell for Us</a></li>
        <li><a href="about.html">About</a></li>
      </ul>
      <div class="nav-ctas">
        <a href="{{JOB_BOARD}}" target="_blank" rel="noopener" class="btn btn-outline-dark">Job Board</a>
        <a href="hire-school-staff.html" class="btn btn-primary">Hire School Staff</a>
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
        <p>School staffing for K&#8209;12 districts and charter schools — therapy, special education, behavior, mental health, hearing, vision and nursing — plus healthcare recruiting, backed by NorthPoint's 20+ years of recruiting.</p>
      </div>
      <div class="footer-col">
        <h4>Explore</h4>
        <ul>
          <li><a href="school-staffing.html">School Roles</a></li>
          <li><a href="school-teletherapy-staffing.html">Teletherapy</a></li>
          <li><a href="hire-school-staff.html">Hire School Staff</a></li>
          <li><a href="school-match.html">Match a Job Description</a></li>
          <li><a href="sell-for-us.html">Sell for Us</a></li>
          <li><a href="school-resources.html">Resources</a></li>
          <li><a href="salary-guide.html">School Therapist Salary Guide</a></li>
          <li><a href="services.html">Healthcare Recruiting</a></li>
          <li><a href="about.html">About Us</a></li>
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
          <li><a href="hire-school-staff.html">Place a School Job Order</a></li>
          <li><a href="request-talent.html">Request Healthcare Talent</a></li>
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
    "description": "K-12 school staffing and healthcare recruiting firm in Atlanta, GA. We staff school districts and charter schools with speech-language pathologists, occupational and physical therapists, school psychologists, BCBAs and RBTs, counselors, social workers, special education teachers and paraprofessionals, interpreters, teachers of the deaf and visually impaired, and school nurses — on contract, onsite or by teletherapy. We also place clinical and non-clinical healthcare professionals — nurses, nurse practitioners, physician assistants, physicians, allied health and therapy, medical assistants and front office, coding, billing and revenue cycle, finance, and leadership — as temp, temp-to-perm, and direct hire, with payrolling as Employer of Record.",
    "address": {"@type": "PostalAddress", "addressLocality": "Atlanta", "addressRegion": "GA", "addressCountry": "US"},
    "telephone": ["+1-404-250-0790", "+1-678-777-5627"],
    "email": EMAIL,
    "areaServed": ["Atlanta, GA", "Georgia", "Southeast United States", "United States"],
    "sameAs": [],
}


OG_IMAGES = {"salary-guide.html": GUIDE["og"]}   # shared links show this instead of og-image.png


def head(file, title, desc, extra_schema=None, extra_head="", robots="index, follow"):
    url = SITE + "/" + ("" if file == "index.html" else file)
    og = f'{SITE}/img/{OG_IMAGES.get(file, "og-image.png")}'
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
  <meta name="robots" content="{robots}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="MedPoint Partners">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{og}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:locale" content="en_US">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{og}">
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
{actions}
    </div>
  </div>
</div>
'''

CTA_ACTIONS = '''      <a href="request-talent.html" class="btn btn-white btn-lg">Request Talent Now</a>
      <a href="{{JOB_BOARD}}" target="_blank" rel="noopener" class="btn btn-outline-white btn-lg">Browse Open Jobs ↗</a>'''


def cta(h2="Ready to Find Your Next<br>Healthcare Hire?",
        p="Tell us about your open role and we'll deliver a shortlist — guaranteed.", actions=CTA_ACTIONS):
    return CTA.replace("{h2}", h2).replace("{p}", p).replace("{actions}", actions)


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


def faq_schema(faq=None):
    strip = lambda s: s.replace("&amp;", "&")
    return [{"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in (faq or FAQ)]}]


def faq_html(faq=None):
    items = []
    for q, a in (faq or FAQ):
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

# The healthcare half of the home page: below the school sections since the 2026-10-29
# school pivot, so its heading is an h2 (the page's h1 is the school hero's).
HEALTH_HOME = '''
<!-- ── Healthcare recruiting & staffing ─────── -->
<section class="hero hero--second" id="healthcare">
  <div class="container hero-grid">
    <div class="hero-inner">
      <span class="hero-kicker">Also: Healthcare Recruiting &amp; Staffing · Atlanta, GA</span>
      <h2 class="hero-title">Specialized <em>Healthcare</em><br>Recruiting &amp; Staffing</h2>
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
{{HOME_FAQ}}
    </div>
  </div>
</section>
'''

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
    ("K&#8209;12 Schools (our focus)", ["Speech-Language Pathologists &amp; Clinical Fellows",
                                         "School OTs, PTs &amp; Educational Audiologists", "School Psychologists &amp; Diagnosticians",
                                         "BCBAs, RBTs &amp; ABA Therapists", "Counselors, Social Workers &amp; Therapists",
                                         "SPED Teachers, Paras &amp; School Nurses"]),
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
{{SCHOOL_SERVICES}}
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
            <span class="tag">Coders &amp; Billers</span><span class="tag">Practice Administrators</span><span class="tag">School Therapists</span><span class="tag">+ more</span>
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
                <option>Senior Living / Post-Acute</option><option>Lab / Imaging / Diagnostics</option><option>PT / Rehab Clinic</option><option>K–12 School / District</option><option>Other</option>
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

# ───────────────────────────── School staffing (K-12) ─────────────────────────────
# Since 2026-10-29 the site leads with school staffing (Gus: "we focus on schools"). The law (IDEA)
# creates the demand and public budgets pay for it, so school pages say "required by law" and
# "publicly funded", lead with contract and teletherapy, and put direct hire second. Every school
# page also leads with our edge: the live candidate ticker, the QR code that opens a district's
# best-matched blinded candidate, and local independent reps ("We put you in business for yourself").
# The tickers are the home page's 100X spotlight strip: data-only keeps one role's candidates (each
# word matched anywhere in the spotlight's title and eyebrow); when none match, the strip stays
# empty and the "recruiting now" chips under it show instead (CSS :empty).
SPOTLIGHT_JS = "https://100xrecruiting.com/static/spotlight_ticker.js?v=2"
REP_JOB = "https://100xjobs.com/job/9853"
PARTNER_APP = "https://100xrecruiting.com/partners"
ROLE = {r["key"]: r for r in ROLES}
SHOWN = sorted(ROLES, key=lambda r: DISPLAY_ORDER.index(r["key"]))   # display order; ROLES' order is for matching
TELE_ROLES = [r for r in SHOWN if r.get("tele_file")]
SCHOOL_BUYERS = ["Special Education Directors", "Student Services Directors", "Superintendents",
                 "Principals", "Charter School Leaders", "District HR &amp; Talent Acquisition"]
# An industry view from one national school staffing firm's public job board (Gus, 2026-10-29).
# Don't name the firm on our pages.
MARKET = [("18,484", "open jobs on one national school staffing job board"), ("78%", "of those jobs are contract"),
          ("~3,000", "new postings every week")]
MARKET_NOTE = ("An industry view from one national school staffing firm's public job board on October 29, 2026. "
               "The counts may include some healthcare roles.")
CONTRACT_TEXT = ("Contract first — for the school year, the semester or a leave — on MedPoint's payroll with one "
                 "invoice. Contract-to-hire and direct hire when you want to keep them.")

FAQ_FAST = ("How fast can you send candidates?",
            "We send a blinded shortlist of screened candidates within 48 to 72 hours of your request — credentials checked and your screening questions answered.")
FAQ_BLIND = ("What does a blinded candidate mean?",
             "A blinded profile shows a candidate's credentials, experience and location — but no name, employer or school. When you ask for the introduction, we set it up.")
FAQ_CONTRACT = ("How does contract staffing work?",
                "Your clinician or teacher works on MedPoint's payroll for the school year, the semester or a set number of weeks. We handle weekly payroll, taxes and workers' comp, and you get one invoice at the agreed rate. If you want to keep them, contract-to-hire and direct hire are available.")
FAQ_IDEA = ("Why does a fully staffed school matter for IDEA compliance?",
            "Under IDEA, every student with an IEP is owed the special education and related services written into it, on the schedule written into it. When a position sits empty, minutes are missed, evaluations slip past their timelines, and districts can owe make-up (compensatory) services or face state complaints. Filling the seat quickly — on contract or by teletherapy — keeps services on schedule.")
FAQ_FUNDS = ("Who pays for these services?",
             "Public funds. Federal IDEA Part B grants flow through your state alongside state and local special education funding, and many districts recover part of the cost through school-based Medicaid for eligible students and services.")
FAQ_TELE = ("Can services be delivered by teletherapy?",
            "Many can. Speech therapy, counseling, school psychology, behavior consultation, vision and hearing services and some instruction work by live video, with a provider licensed in your state and an onsite helper when students need one. PT, nursing, RBTs, orientation and mobility and paraprofessionals are onsite. Your IEP team decides what fits each student.")
FAQ_QR = ("How does the QR code work?",
          "Scan it with your phone camera. It opens our match page, where you paste or pick your job description and see the best-matched candidate we're representing right now — blinded, with no name or employer — and the video intro we invite every candidate to film. Ask for the introduction from there.")
FAQ_ROLES = ("Which school roles do you staff?",
             "Twenty-three: speech-language pathologists and clinical fellows, occupational and physical therapists, educational audiologists, sign language interpreters, teachers of the deaf and hard of hearing, teachers of the visually impaired, orientation and mobility specialists, school nurses, school psychologists, educational diagnosticians, BCBAs, RBTs and ABA therapists, school counselors, school social workers, mental health therapists, special education teachers, paraprofessionals, reading specialists, adaptive PE teachers and classroom teachers.")
SCHOOL_COMMON_FAQ = [FAQ_FAST, FAQ_CONTRACT, FAQ_BLIND]
HUB_FAQ = [FAQ_ROLES, FAQ_IDEA, FAQ_FUNDS, FAQ_TELE, FAQ_QR, FAQ_FAST, FAQ_CONTRACT]
HOME_FAQ = [FAQ_IDEA, FAQ_FUNDS, FAQ_CONTRACT, FAQ_TELE, FAQ_QR] + FAQ
TELE_FAQ = [("Does a teletherapy provider need a license in our state?",
             "Yes. Providers must hold the license or credential your state requires for students located there. We check it before we propose anyone."),
            ("What do we need on our side?",
             "A quiet room or corner, a computer with a camera and headset, reliable internet — and for young students or students with significant needs, an adult nearby who can help, often a para or classroom aide.")]
TELE_BASICS = ["A provider licensed or credentialed in your state",
               "Live, real-time sessions on a secure video platform your district approves",
               "Sessions scheduled around your bell schedule",
               "IEP minutes, progress notes and service logs documented like in-person services",
               "IEP meetings and parent conferences joined by video"]
TELE_ROOM = ["A quiet room or corner", "A computer with a camera, headset and reliable internet",
             "An adult nearby for young students or students with significant needs",
             "Materials and test kits sent ahead when needed"]
TELE_STEPS = [("Plan the Caseload", "We review students, minutes and schedules with your team."),
              ("Set Up the Room", "Camera, headset, internet — and an onsite helper where students need one."),
              ("Sessions Start", "Live sessions on your bell schedule, with minutes logged from day one."),
              ("Review &amp; Adjust", "Regular check-ins with your team. Students who need in-person time get it.")]
SCHOOL_STEPS = [("Send the Job Order", "Use our two-step form, scan a QR code, or call — role, caseload, campuses and start date."),
                ("Meet Your Matches", "A blinded shortlist in 48–72 hours, credentials checked, with the video intros candidates film."),
                ("They Start", "On contract for the school year or semester — onsite, itinerant or by teletherapy."),
                ("We Run Payroll", "MedPoint is the employer of record: weekly payroll, taxes and workers' comp, one invoice.")]


def plain(s):
    """Copy as plain text (for schema and the match page's data): no tags or entities."""
    return unescape(re.sub(r"<[^>]+>", "", s))


def tele_label(r):
    f = r["tele_file"]
    return ("Video Remote" if f.startswith("video-remote") else "Virtual" if f.startswith("virtual")
            else "Remote" if f.startswith("remote") else "Teletherapy")


def qr_name(key=""):
    return "school-" + (key or "all")


def qr_url(key=""):
    """Where a printed QR code lands. src=qr tells us the inquiry came from a scan."""
    return SITE + "/school-match.html?" + (f"d={key}&" if key else "") + "src=qr"


def steps_row(steps):
    return '<div class="steps-row">' + "".join(
        f'<div class="step"><div class="step-num">{i}</div><h4>{h}</h4><p>{p}</p></div>'
        for i, (h, p) in enumerate(steps, 1)) + "</div>"


def school_hero(crumb, h1, sub, photo, pills=(), key=""):
    """Inner-page hero for school pages: delivery pills plus the two school CTAs."""
    q = f"?d={key}" if key else ""
    pill = lambda x: x if x.startswith("<a") else f'<span class="hero-pill">{x}</span>'   # noqa: E731
    return f'''
<!-- ── Page Hero ──────────────────────────────── -->
<section class="page-hero" style="background-image:url('{UNS}{photo}?auto=format&fit=crop&w=1600&q=80');">
  <div class="container">
    <div class="breadcrumb"><a href="index.html">Home</a><span>/</span>{crumb}</div>
    <h1>{h1}</h1>
    <p>{sub}</p>
    <div class="hero-pills">{"".join(pill(x) for x in pills)}</div>
    <div class="hero-ctas">
      <a href="hire-school-staff.html{q}" class="btn btn-white btn-lg">Hire School Staff</a>
      <a href="school-match.html{q}" class="btn btn-outline-white btn-lg">[[ico:qr]] Match a Job Description</a>
    </div>
  </div>
</section>
'''


def edge_strip(key="", here=True):
    """Our edge over the big school staffing firms, at the top of every school page."""
    q = f"?d={key}" if key else ""
    return f'''
<!-- ── Our edge: live ticker, QR match with video intro, local reps ── -->
<div class="edge-strip">
  <div class="container edge-grid">
    <a class="edge-item" href="{"#spotlights" if here else "school-staffing.html#spotlights"}">
      <span class="edge-ico">[[ico:pulse]]</span>
      <span><strong>Live candidate ticker</strong>The school candidates we're representing right now — blinded, updated as they finish screening.</span>
    </a>
    <a class="edge-item" href="school-match.html{q}">
      <span class="edge-ico">[[ico:qr]]</span>
      <span><strong>Scan for your match</strong>Scan the QR code, paste your job description, meet your best-matched blinded candidate — and the 30-second video intro we invite every candidate to film.</span>
    </a>
    <a class="edge-item" href="sell-for-us.html">
      <span class="edge-ico">[[ico:handshake]]</span>
      <span><strong>Local independent reps</strong>A rep who knows your district, backed by our recruiters. Want to be one? We put you in business for yourself.</span>
    </a>
  </div>
</div>
'''


def school_ticker(roles, label, single=False, chips=None, sid="spotlights"):
    """The 100X spotlight strip for some school roles, with 'recruiting now' chips that show
    while no spotlight matches. chips = [(text, href, icon)] replaces the default chips; sid
    keeps two strips on one page apart."""
    only = ",".join(r["only"] for r in roles)
    if chips:
        items = [f'<a class="role-chip" href="{h}">[[ico:{i}]] {t}</a>' for t, h, i in chips]
    elif single:
        r = roles[0]
        items = [f'<a class="role-chip" href="school-match.html?d={r["key"]}">[[ico:{r["icon"]}]] {t}</a>' for t in r["roles"]]
    else:
        items = [f'<a class="role-chip" href="{r["file"]}">[[ico:{r["icon"]}]] {r["nav"]}</a>' for r in roles]
    while len(items) < 14:   # a few chips, repeated so the loop fills a wide screen
        items += items
    chips = "".join(items)
    dup = chips.replace('<a class="role-chip"', '<a class="role-chip" aria-hidden="true" tabindex="-1"')
    q = f"?d={roles[0]['key']}" if single else ""
    return f'''
<!-- ── Candidate spotlights (blinded: no name, employer or school), fed from 100xrecruiting.com ── -->
<section class="school-live" id="{sid}" aria-label="{label}">
  <div id="hx-school-{sid}" class="school-ticker"></div>
  <div class="school-fallback">
    <div class="school-fallback-head"><b>🌟 {label}</b><span>Blinded spotlights scroll here as candidates finish screening — no name, employer or school. Recruiting now:</span></div>
    <div class="mpc-marquee"><div class="mpc-track" style="animation-duration:{len(items) * 7}s">{chips}{dup}</div></div>
  </div>
  <script src="{SPOTLIGHT_JS}" data-target="hx-school-{sid}" data-theme="light" data-title="{label}"
          data-only="{only}"
          data-fallback="{{{{SITE}}}}/school-match.html{q}" defer></script>
</section>
'''


SLP = ROLE["slp"]
SLP_FLAG = SLP["flagship"]
SLP_CHIPS = [(t, h, "monitor" if "teletherapy" in h else "speech") for t, h in SLP_FLAG["family"]]


def slp_ticker():
    """The first ticker on the home page: the whole SLP family (CCC-SLPs, CFs, SLPAs, bilingual, teletherapy)."""
    return school_ticker([SLP, ROLE["cfy"]], "Speech-Language Pathologist Spotlights", chips=SLP_CHIPS)


def slp_band(alt=False):
    """SLPs lead the site: the biggest school role, flagged on the home page and the roles hub."""
    n, label = SLP_FLAG["stat"]
    fam = "".join(f'<a class="tag" href="{h}">[[ico:{i}]] {t}</a>' for t, h, i in SLP_CHIPS)
    return f'''
<!-- ── SLPs: our flagship role ────────────────── -->
<section class="section{" section-alt" if alt else ""}" id="slps">
  <div class="container">
    <div class="slp-band">
      <div>
        <span class="section-kicker">Our Flagship Role</span>
        <h2 class="section-title">Speech-Language Pathologists, <em>On Contract This School Year</em></h2>
        <div class="section-divider"></div>
        <p class="section-sub">{SLP["pitch"]}</p>
        <div class="tags" style="margin-top:20px;">{fam}</div>
        <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:24px;">
          <a href="{SLP["file"]}" class="btn btn-primary">School SLP Staffing →</a>
          <a href="{SLP["tele_file"]}" class="btn btn-outline-dark">[[ico:monitor]] Teletherapy SLPs</a>
          <a href="hire-school-staff.html?d=slp" class="btn btn-outline-dark">Hire an SLP</a>
        </div>
      </div>
      <div class="slp-stat">
        <div class="slp-stat-num">{n}</div>
        <p>{label}</p>
        <small>{SLP_FLAG["note"]}</small>
      </div>
    </div>
  </div>
</section>
'''


def slp_deep_dive():
    """The SLP page's extra sections: IDEA, onsite vs teletherapy, and the CF-to-CCC path."""
    f = SLP_FLAG
    idea = "\n".join(f'      <p class="section-sub" style="margin-bottom:16px;">{x}</p>' for x in f["idea"])
    onsite = "".join(f"<li>{x}</li>" for x in f["onsite"])
    tele = "".join(f"<li>{x}</li>" for x in f["tele"])
    n, label = f["stat"]
    return f'''
<!-- ── Speech services under IDEA ─────────────── -->
<section class="section" id="idea">
  <div class="container two-col" style="align-items:start;">
    <div>
      <span class="section-kicker">Speech Services Under IDEA</span>
      <h2 class="section-title">Why the Minutes <em>Can't Wait</em></h2>
      <div class="section-divider"></div>
{idea}
      <a href="{f["article"]}" class="btn btn-outline-dark" style="margin-top:8px;">What Does a School SLP Do? →</a>
    </div>
    <div class="slp-stat">
      <div class="slp-stat-num">{n}</div>
      <p>{label}</p>
      <small>{f["note"]}</small>
    </div>
  </div>
</section>

<!-- ── Onsite vs teletherapy ──────────────────── -->
<section class="section section-alt" id="onsite-or-teletherapy">
  <div class="container">
    <div class="centered">
      <span class="section-kicker">Onsite or Teletherapy?</span>
      <h2 class="section-title">Pick the Delivery That <em>Fits the Caseload</em></h2>
      <div class="section-divider"></div>
      <p class="section-sub">Many districts use both: an onsite SLP for the youngest and highest-need students, teletherapy for the rest. Your IEP team decides what fits each student.</p>
    </div>
    <div class="compare-grid">
      <div class="compare-card">
        <div class="feature-icon">[[ico:pin]]</div>
        <h3>Onsite SLPs</h3>
        <p>Best when the work is hands-on or the students are young.</p>
        <ul class="checklist">{onsite}</ul>
        <a href="hire-school-staff.html?d=slp" class="trio-link">Hire an onsite SLP →</a>
      </div>
      <div class="compare-card compare-card--tele">
        <div class="feature-icon">[[ico:monitor]]</div>
        <h3>Teletherapy SLPs</h3>
        <p>Best when no one local can be found — licensed in your state, live by video.</p>
        <ul class="checklist">{tele}</ul>
        <a href="{SLP["tele_file"]}" class="trio-link">How SLP teletherapy works →</a>
      </div>
    </div>
  </div>
</section>

<!-- ── From clinical fellow to CCC-SLP ────────── -->
<section class="section" id="cf-ccc">
  <div class="container">
    <span class="section-kicker">From Clinical Fellow to CCC-SLP</span>
    <h2 class="section-title">The Path to <em>Certification</em> — and Why It Helps You Hire</h2>
    <div class="section-divider"></div>
    {steps_row(f["path"])}
    <div class="example-callout" style="margin-top:28px;">
      <div class="example-icon">[[ico:award]]</div>
      <div>
        <span class="section-kicker">For Your District</span>
        <h4>Grow your own SLPs</h4>
        <p>{f["path_note"]} <a href="slp-clinical-fellow-staffing.html" class="trio-link">Clinical fellow staffing →</a></p>
      </div>
    </div>
  </div>
</section>
'''


# ── Big metro or small and rural: one call either way ──
def rural_metro_band(alt=False):
    big = "".join(f"<li>{x}</li>" for x in [
        "Several SLPs at once for the start of the school year",
        "Bilingual SLPs, psychologists and interpreters for the languages your students speak",
        "Evaluation backlogs cleared on a deadline",
        "Fast replacements for leaves and mid-year resignations",
        "One point of contact and one invoice across every campus"])
    small = "".join(f"<li>{x}</li>" for x in [
        "Teletherapy when no SLP or psychologist lives within driving distance",
        "One itinerant clinician for all your campuses — or shared with neighboring districts through your cooperative or regional service agency",
        "Low-incidence roles a few hours a week: TVI, O&amp;M, deaf and hard of hearing, interpreting, audiology",
        "Part-time contracts sized to a small caseload",
        "One point of contact for every role — no juggling five agencies"])
    return f'''
<!-- ── Big metro or small and rural ───────────── -->
<section class="section{" section-alt" if alt else ""}" id="rural-metro">
  <div class="container">
    <div class="centered">
      <span class="section-kicker">Big Metro or Small and Rural</span>
      <h2 class="section-title">Every District Size, <em>One Call</em></h2>
      <div class="section-divider"></div>
      <p class="section-sub">A big district needs volume. A small rural one needs someone who will come — or connect by video. We staff both.</p>
    </div>
    <div class="compare-grid">
      <div class="compare-card compare-card--tele">
        <div class="feature-icon">[[ico:pin]]</div>
        <h3>Small &amp; Rural Districts</h3>
        <ul class="checklist">{small}</ul>
        <a href="school-teletherapy-staffing.html" class="trio-link">See teletherapy roles →</a>
      </div>
      <div class="compare-card">
        <div class="feature-icon">[[ico:building]]</div>
        <h3>Metro &amp; Suburban Districts</h3>
        <ul class="checklist">{big}</ul>
        <a href="hire-school-staff.html" class="trio-link">Place a job order →</a>
      </div>
    </div>
  </div>
</section>
'''


def qr_block(key="", who="School Candidate"):
    q = f"?d={key}" if key else ""
    return f'''
<!-- ── QR: match a job description ─────────────── -->
<section class="section section-alt" id="match">
  <div class="container">
    <div class="qr-block">
      <div>
        <span class="section-kicker">Scan · Paste · Meet Your Match</span>
        <h2 class="section-title">See the Best-Matched {who} for <em>Your Job Description</em></h2>
        <p class="section-sub">Scan the code with your phone camera, or open the match page. Paste or pick your job description and we show the best-matched candidate we're representing right now — blinded, with no name, employer or school until you ask for the introduction — and the 30-second video intro we invite every candidate to film.</p>
        <div class="qr-actions">
          <a href="school-match.html{q}" class="btn btn-primary">Match My Job Description →</a>
          <a href="school-flyer.html{q}" class="btn btn-outline-dark">[[ico:printer]] Print a Flyer</a>
        </div>
      </div>
      <figure class="qr-figure">
        <img class="qr-img" src="img/qr/{qr_name(key)}.svg" alt="QR code that opens the MedPoint Partners school match page" width="200" height="200" loading="lazy">
        <figcaption>Scan with your phone camera</figcaption>
      </figure>
    </div>
  </div>
</section>
'''


def role_card(r, tele=False):
    file = r["tele_file"] if tele else r["file"]
    text = r["tele"]["hero"] if tele else r["card"]
    name = f'{tele_label(r)} {r["nav"]}' if tele else r["nav"]
    badges = "".join(f'<span class="mpc-badge">{t}</span>' for t in r["roles"][:3])
    return f'''      <a class="dept-card" href="{file}">
        <span class="feature-icon">[[ico:{"monitor" if tele else r["icon"]}]]</span>
        <h3>{name}</h3>
        <p>{text}</p>
        <div class="mpc-badges">{badges}</div>
        <span class="dept-card-go">{"See remote staffing" if tele else "See candidates &amp; match"} →</span>
      </a>'''


def role_groups(tag="h2"):
    out = []
    for key, name, icon in GROUPS:
        cards = "\n".join(role_card(r) for r in SHOWN if r["group"] == key)
        out.append(f'''    <div class="role-group" id="{key}">
      <{tag} class="role-group-title"><span class="feature-icon">[[ico:{icon}]]</span>{name}</{tag}>
      <div class="dept-grid">
{cards}
      </div>
    </div>''')
    return "\n".join(out)


def role_columns():
    """Every role as a compact link list, one column per group (home page)."""
    cols = []
    for key, name, icon in GROUPS:
        links = "".join(f'<li><a href="{r["file"]}">{r["nav"]}</a></li>' for r in SHOWN if r["group"] == key)
        cols.append(f'<div class="role-col"><h3><span class="feature-icon">[[ico:{icon}]]</span>{name}</h3><ul>{links}</ul></div>')
    return '<div class="role-cols">' + "".join(cols) + "</div>"


def school_mega():
    tabs = "".join(f'<button class="mega-tab-btn{" active" if i == 0 else ""}" onclick="switchMegaTab(\'{k}\',this)">{n}</button>'
                   for i, (k, n, _) in enumerate(GROUPS))
    panels = []
    for i, (k, n, _) in enumerate(GROUPS):
        links = "\n".join(f'              <a href="{r["file"]}">{r["nav"]}</a>' for r in SHOWN if r["group"] == k)
        panels.append(f'''            <div class="mega-panel{" active" if i == 0 else ""}" id="mega-{k}">
{links}
              <a class="mega-all" href="school-staffing.html#{k}">All {n} →</a>
            </div>''')
    return f'''            <div class="mega-sidebar">
              {tabs}
              <a class="mega-tab-btn" href="hire-school-staff.html" style="color:var(--blue);">Hire School Staff →</a>
            </div>
''' + "\n".join(panels)


NAV = (NAV.replace("{{SCHOOL_MEGA}}", school_mega())
       .replace("{{STATE_NAV}}", "\n".join(f'            <a href="{st["file"]}">{st["name"]}</a>' for st in STATES)
                + '\n            <a href="school-staffing.html#states">All States →</a>'))


def law_band():
    return '''
<!-- ── Required by law, publicly funded ─────── -->
<section class="section">
  <div class="container">
    <div class="centered">
      <span class="section-kicker">Why School Staffing Holds Up in Any Economy</span>
      <h2 class="section-title">Required by Law. <em>Publicly Funded.</em></h2>
      <div class="section-divider"></div>
      <p class="section-sub">These services aren't optional extras that disappear when budgets tighten. The law requires them, and public education budgets pay for them.</p>
    </div>
    <div class="trio">
''' + "\n".join([
        feat("landmark", "Required by Law",
             "The Individuals with Disabilities Education Act (IDEA) entitles every student with an IEP to the special education and related services written into it — speech, OT, PT, psychology, counseling, interpreting, school nursing and more."),
        feat("receipt", "Publicly Funded",
             "Federal IDEA Part B grants, state and local special education funds, and school-based Medicaid for eligible services pay for the work — every year, in every district."),
        feat("refresh", "Every School Year",
             "IEPs are reviewed every year and students are re-evaluated at least every three years, so the caseloads come back each fall — and so does the need to staff them."),
    ]) + '''
    </div>
    <p class="fine-print"><a href="idea-staffing-guide-for-superintendents.html" style="color:var(--blue);font-weight:600;">Read our superintendent's guide to IDEA staffing →</a></p>
  </div>
</section>
'''


def delivery_band(r=None, alt=True):
    if r and r.get("tele_file"):
        second = feat("monitor", f"{tele_label(r)} Option",
                      r["tele"]["hero"] + f' <a href="{r["tele_file"]}" class="trio-link">See {tele_label(r).lower()} staffing →</a>')
    elif r:
        second = feat("pin", "Onsite &amp; Itinerant",
                      "This role is delivered in person — at one campus or across several. We find people used to your schedule and your drive times.")
    else:
        second = feat("monitor", "Teletherapy Where It Fits",
                      'Speech, counseling, psychology, behavior consultation, vision and hearing services and some instruction by live video, from providers licensed in your state. <a href="school-teletherapy-staffing.html" class="trio-link">See remote roles →</a>')
    return f'''
<!-- ── How you can hire ───────────────────────── -->
<section class="section{" section-alt" if alt else ""}">
  <div class="container">
    <div class="centered">
      <span class="section-kicker">How You Can Hire</span>
      <h2 class="section-title">Contract First. <em>Teletherapy Where It Fits.</em></h2>
      <div class="section-divider"></div>
      <p class="section-sub">Most districts fill hard-to-fill roles on contract. Direct hire is there when you want it.</p>
    </div>
    <div class="trio">
''' + "\n".join([
        feat("clock", "Contract for the Year or Semester",
             "Your clinician or teacher works on MedPoint's payroll for the school year, the semester, a leave or a set number of weeks. Weekly payroll, taxes and workers' comp handled — one invoice to you."),
        second,
        feat("refresh", "Contract-to-Hire &amp; Direct Hire",
             "Want to keep them? Convert a contract hire to your payroll with a fee agreed up front, or hire directly from day one with our replacement guarantee."),
    ]) + '''
    </div>
  </div>
</section>
'''


def market_band(title="The School Staffing Market <em>Runs on Contract</em>"):
    stats = "".join(f'<div class="stat-item"><div class="stat-num">{n}</div><div class="stat-label">{l}</div></div>' for n, l in MARKET)
    return f'''
<!-- ── Market view ────────────────────────────── -->
<section class="section" style="padding:72px 0 56px;">
  <div class="container">
    <div class="centered">
      <span class="section-kicker">An Industry View</span>
      <h2 class="section-title">{title}</h2>
      <div class="section-divider"></div>
    </div>
    <div class="stats-box">{stats}<div class="stat-item"><div class="stat-num">48–72 hrs</div><div class="stat-label">for our blinded shortlist</div></div></div>
    <p class="fine-print">{MARKET_NOTE}</p>
  </div>
</section>
'''


def states_band(alt=False):
    tags = "\n".join(f'      <a class="tag" href="{st["file"]}">[[ico:pin]] {st["name"]}</a>' for st in STATES)
    return f'''
<!-- ── States ─────────────────────────────────── -->
<section class="section{" section-alt" if alt else ""}" id="states" style="padding:64px 0;">
  <div class="container centered">
    <span class="section-kicker">Where We Staff</span>
    <h2 class="section-title" style="font-size:clamp(1.5rem,2.6vw,2rem);">School Staffing by State</h2>
    <p class="section-sub">Credentials and local structures differ by state. Start with yours — teletherapy providers are licensed where your students are.</p>
    <div class="tags" style="justify-content:center;margin-top:22px;">
{tags}
    </div>
    <p class="fine-print">Based in Atlanta, Georgia. We staff contract and teletherapy roles nationwide.</p>
  </div>
</section>
'''


def reps_band():
    return f'''
<!-- ── Independent reps ───────────────────────── -->
<section class="section section-dark" id="reps">
  <div class="container split">
    <div>
      <span class="section-kicker">For Independent Reps</span>
      <h2 class="section-title">Know Special Education Directors?<br><em>We Put You in Business for Yourself.</em></h2>
      <p>Sell school staffing as an independent rep. You open the doors at the districts you know; our recruiters find, screen, place and payroll the staff — and you earn commission.</p>
      <div style="display:flex;gap:12px;flex-wrap:wrap;">
        <a href="sell-for-us.html" class="btn btn-white btn-lg">Sell for Us →</a>
        <a href="{REP_JOB}" target="_blank" rel="noopener" class="btn btn-outline-white btn-lg">See the Rep Opening ↗</a>
      </div>
    </div>
    <div class="feature-list">
      <div class="feature"><div class="feature-icon">[[ico:handshake]]</div><div><h4>You Open the Door</h4><p>Special education directors, student services directors, superintendents, principals and charter leaders.</p></div></div>
      <div class="feature"><div class="feature-icon">[[ico:search]]</div><div><h4>We Fill the Order</h4><p>Sourcing, screening, credential checks, placement and payroll — all on our side.</p></div></div>
      <div class="feature"><div class="feature-icon">[[ico:qr]]</div><div><h4>You Leave a Flyer</h4><p>Every role has a flyer with a QR code that shows the district its best-matched candidate.</p></div></div>
    </div>
  </div>
</section>
'''


def school_faq(faq, title="What Districts Ask Us"):
    return f'''
<!-- ── FAQ ────────────────────────────────────── -->
<section class="section section-alt" aria-label="Frequently asked questions">
  <div class="container">
    <div class="centered">
      <span class="section-kicker">Common Questions</span>
      <h2 class="section-title">{title}</h2>
    </div>
    <div class="faq" itemscope itemtype="https://schema.org/FAQPage">
{faq_html(faq)}
    </div>
  </div>
</section>
'''


def school_cta(h2, p, key=""):
    q = f"?d={key}" if key else ""
    return cta(h2=h2, p=p, actions=f'''      <a href="hire-school-staff.html{q}" class="btn btn-white btn-lg">Hire School Staff</a>
      <a href="school-match.html{q}" class="btn btn-outline-white btn-lg">Match a Job Description</a>''')


def school_schema(file, name, desc, crumbs, faq=None, kind="Service"):
    url = SITE + "/" + file
    trail = [("Home", SITE + "/")] + crumbs
    graph = [{"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": plain(n), "item": u} for i, (n, u) in enumerate(trail)]}]
    if kind == "Service":
        graph.insert(0, {"@type": "Service", "name": plain(name), "serviceType": plain(name), "url": url,
                         "description": plain(desc), "provider": {"@id": SITE + "/#organization"},
                         "areaServed": "US",
                         "audience": {"@type": "Audience", "audienceType": "K-12 school districts and charter schools"}})
    return graph + (faq_schema(faq) if faq else [])


ROLES_CRUMB = ("School Roles", SITE + "/school-staffing.html")
TELE_CRUMB = ("Teletherapy", SITE + "/school-teletherapy-staffing.html")


def role_page(r):
    tele = r.get("tele_file")
    crumb = f'<a href="school-staffing.html">School Roles</a><span>/</span>{r["nav"]}'
    pills = ["Contract first", "Onsite &amp; itinerant"]
    pills += [f'<a class="hero-pill hero-pill--link" href="{tele}">{tele_label(r)} option →</a>'] if tele else []
    pills += ["Contract-to-hire or direct hire"]
    covers = "\n".join(f"          <li>{c}</li>" for c in r["covers"])
    titles = "\n".join(f"          <li>{t}</li>" for t in r["roles"])
    qs = "\n".join(f"          <li>{q}</li>" for q in r["questions"])
    related = "\n".join(f'      <a class="tag" href="{x["file"]}">{x["nav"]}</a>'
                        for x in SHOWN if x["group"] == r["group"] and x is not r)
    flagship = r.get("flagship")
    ticker = (school_ticker([r, ROLE["cfy"]], "Speech-Language Pathologist Spotlights", chips=SLP_CHIPS) if flagship
              else school_ticker([r], plain(r["nav"]) + " Candidate Spotlights", single=True))
    return school_hero(crumb, r["h1"], r["hero"], r["photo"], pills, r["key"]) + edge_strip(r["key"]) + ticker + f'''
<!-- ── What we cover ──────────────────────────── -->
<section class="section section-alt">
  <div class="container">
    <div class="svc-block svc-block--top" style="margin-top:0;background:var(--white);">
      <div>
        <span class="pill-tag">{r["nav"]}</span>
        <h3>What We Cover</h3>
        <p>{r["pitch"]}</p>
        <ul class="checklist">
{covers}
        </ul>
        <a href="hire-school-staff.html?d={r["key"]}" class="btn btn-primary">Place a Job Order →</a>
      </div>
      <div class="svc-aside">
        <div class="aside-ico">[[ico:{r["icon"]}]]</div>
        <h4>Roles We Place</h4>
        <ul>
{titles}
        </ul>
        <div class="fee">
          <div class="fee-label">How You Can Hire</div>
          <div class="fee-text">{CONTRACT_TEXT}</div>
        </div>
      </div>
    </div>
  </div>
</section>
''' + (slp_deep_dive() if flagship else delivery_band(r, alt=False)) + f'''
<!-- ── Sample screening questions ─────────────── -->
<section class="section section-alt" style="padding:64px 0;">
  <div class="container">
    <div class="example-callout" style="margin-top:0;">
      <div class="example-icon">[[ico:clipboard]]</div>
      <div>
        <span class="section-kicker">Sample: Screening Questionnaire</span>
        <h4>{plain(r["one"])} — your questions, answered before the first call</h4>
        <p>We build every questionnaire with your input. For this search it might look like this — and every résumé arrives with the candidate's answers.</p>
        <ul class="sample-q">
{qs}
        </ul>
      </div>
    </div>
  </div>
</section>
''' + qr_block(r["key"], plain(r["one"])).replace("section section-alt", "section") + f'''
<!-- ── Related roles ──────────────────────────── -->
<section class="section" style="padding:24px 0 72px;">
  <div class="container centered">
    <span class="section-kicker">Related Roles</span>
    <div class="tags" style="justify-content:center;margin-top:14px;">
{related}
      <a class="tag" href="school-staffing.html">All 23 School Roles →</a>
    </div>
    <p class="fine-print">For {", ".join(SCHOOL_BUYERS[:-1])}, and {SCHOOL_BUYERS[-1]}. By state: {", ".join(f'<a href="{st["file"]}">{st["name"]}</a>' for st in STATES)}.</p>
  </div>
</section>
''' + school_faq(r["faq"] + SCHOOL_COMMON_FAQ) + school_cta(
        f"Need a {r['one']}?", "Place a job order or paste your job description and meet your best-matched candidate.", r["key"])


def tele_page(r):
    label = tele_label(r)
    crumb = (f'<a href="school-staffing.html">School Roles</a><span>/</span>'
             f'<a href="school-teletherapy-staffing.html">Teletherapy</a><span>/</span>{r["nav"]}')
    pills = ["Live by video", "Licensed in your state", "Contract first",
             f'<a class="hero-pill hero-pill--link" href="{r["file"]}">Onsite option →</a>']
    covers = "\n".join(f"          <li>{c}</li>" for c in r["tele"]["covers"] + TELE_BASICS[:2])
    room = "\n".join(f"          <li>{c}</li>" for c in TELE_ROOM)
    others = "\n".join(f'      <a class="tag" href="{x["tele_file"]}">{tele_label(x)} {x["nav"]}</a>' for x in TELE_ROLES if x is not r)
    return school_hero(crumb, f'{label} <em>{r["nav"]}</em> for Schools', r["tele"]["hero"], r["photo"], pills, r["key"]) \
        + edge_strip(r["key"]) + school_ticker([r], plain(r["nav"]) + " Candidate Spotlights", single=True) + f'''
<!-- ── How remote services work ───────────────── -->
<section class="section section-alt">
  <div class="container">
    <div class="svc-block svc-block--top" style="margin-top:0;background:var(--white);">
      <div>
        <span class="pill-tag">{label} {r["nav"]}</span>
        <h3>How Remote Services Work</h3>
        <p>A provider licensed in your state works with your students live by video, on contract for the school year or semester. When no one local can be found, the services still happen on schedule.</p>
        <ul class="checklist">
{covers}
        </ul>
        <a href="hire-school-staff.html?d={r["key"]}" class="btn btn-primary">Place a Job Order →</a>
      </div>
      <div class="svc-aside">
        <div class="aside-ico">[[ico:monitor]]</div>
        <h4>What You Need Onsite</h4>
        <ul>
{room}
        </ul>
        <div class="fee">
          <div class="fee-label">When Onsite Is Better</div>
          <div class="fee-text">Some students and some services need a person in the room. Your IEP team decides — and we staff <a href="{r["file"]}">onsite {r["nav"].lower()}</a> too.</div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ── Steps ──────────────────────────────────── -->
<section class="section" style="padding:72px 0;">
  <div class="container">
    <span class="section-kicker">Getting Started</span>
    <h2 class="section-title">From Job Order to First Session</h2>
    <div class="section-divider"></div>
    {steps_row(TELE_STEPS)}
  </div>
</section>
''' + qr_block(r["key"], plain(r["one"])) + f'''
<!-- ── Other remote roles ─────────────────────── -->
<section class="section" style="padding:64px 0;">
  <div class="container centered">
    <span class="section-kicker">Other Roles We Staff Remotely</span>
    <div class="tags" style="justify-content:center;margin-top:14px;">
{others}
      <a class="tag" href="school-teletherapy-staffing.html">All Teletherapy Roles →</a>
    </div>
  </div>
</section>
''' + school_faq([r["tele"]["faq"]] + TELE_FAQ + [FAQ_FAST, FAQ_CONTRACT]) + school_cta(
        f"Need {r['nav']} by Video?",
        "Place a job order or paste your job description and meet your best-matched candidate.", r["key"])


ROLES_HUB = school_hero("School Roles", "Every <em>School Role</em> We Staff",
                        "Twenty-three roles across therapy and related services, special education, behavior and mental health, hearing, vision and nursing — on contract for the school year or semester, onsite or by teletherapy.",
                        "photo-1594608661623-aa0bd3a69d98",
                        ["Required by law", "Publicly funded", "Contract first", "Teletherapy where it fits"]) \
    + edge_strip() + school_ticker(SHOWN, "School Candidate Spotlights") + slp_band(alt=True) + '''
<!-- ── Every role, by group ───────────────────── -->
<section class="section" id="roles">
  <div class="container">
    <div class="centered">
      <span class="section-kicker">23 Roles, One Call</span>
      <h2 class="section-title">Every School Department We Serve</h2>
      <div class="section-divider"></div>
      <p class="section-sub">Pick a role to see the candidates we're representing now — and match your job description to the best one.</p>
    </div>
''' + role_groups("h3") + '''
  </div>
</section>
''' + law_band().replace('class="section"', 'class="section section-alt"', 1) + delivery_band(alt=False) \
    + rural_metro_band(alt=True) + states_band() \
    + qr_block().replace("section section-alt", "section") + school_faq(HUB_FAQ) + school_cta(
        "Fill the Seat Before the Minutes Pile Up",
        "Place a job order, or paste your job description and meet your best-matched candidate.")

TELE_HUB = school_hero('<a href="school-staffing.html">School Roles</a><span>/</span>Teletherapy',
                       "<em>Teletherapy</em> &amp; Remote School Staffing",
                       "When no one local can be found, licensed providers deliver IEP services by live video — speech, OT, psychology, counseling, behavior, hearing, vision and instruction.",
                       "photo-1588072432836-e10032774350",
                       ["Licensed in your state", "Live, real-time sessions", "Onsite helper when needed", "Contract first"]) \
    + edge_strip() + school_ticker(TELE_ROLES, "Remote-Ready Candidate Spotlights") + '''
<!-- ── How teletherapy works ──────────────────── -->
<section class="section section-alt">
  <div class="container two-col" style="align-items:start;">
    <div>
      <span class="section-kicker">How Teletherapy Works</span>
      <h2 class="section-title">The Services Happen. <em>The Provider Is on Screen.</em></h2>
      <div class="section-divider"></div>
      <p class="section-sub" style="margin-bottom:16px;">A licensed provider works with your students live by video, on contract for the school year or semester. An adult in the room helps the students who need it. IEP minutes are delivered and logged like any other session.</p>
      <p class="section-sub" style="margin-bottom:28px;">Teletherapy fills the roles rural and hard-to-staff districts wait longest for — and it's how one specialist can serve students spread across many campuses.</p>
      <a href="hire-school-staff.html" class="btn btn-primary">Place a Job Order →</a>
    </div>
    <div class="panel" style="padding:28px;">
      <span class="panel-label">What Every Remote Placement Includes</span>
      <ul class="checklist" style="margin-top:16px;">
''' + "\n".join(f"        <li>{b}</li>" for b in TELE_BASICS) + '''
      </ul>
    </div>
  </div>
</section>

<!-- ── Every remote role ──────────────────────── -->
<section class="section">
  <div class="container">
    <div class="centered">
      <span class="section-kicker">Every Role We Staff Remotely</span>
      <h2 class="section-title">Fifteen Roles, Delivered by Video</h2>
      <div class="section-divider"></div>
    </div>
    <div class="dept-grid">
''' + "\n".join(role_card(r, tele=True) for r in TELE_ROLES) + '''
    </div>
  </div>
</section>

<!-- ── Steps + when onsite is better ──────────── -->
<section class="section section-alt">
  <div class="container">
    <span class="section-kicker">Getting Started</span>
    <h2 class="section-title">From Job Order to First Session</h2>
    <div class="section-divider"></div>
    ''' + steps_row(TELE_STEPS) + '''
    <div class="example-callout" style="margin-top:28px;">
      <div class="example-icon">[[ico:pin]]</div>
      <div>
        <span class="section-kicker">When Onsite Is the Better Call</span>
        <h4>Some services need a person in the room</h4>
        <p>Physical therapy, school nursing, RBT and paraprofessional support, orientation and mobility and adaptive PE are hands-on, so we staff them onsite. Very young students and students with significant needs often do better in person too. Your IEP team decides — we staff both.</p>
      </div>
    </div>
  </div>
</section>
''' + rural_metro_band() + qr_block() + school_faq(TELE_FAQ + [FAQ_TELE, FAQ_IDEA, FAQ_FAST]) + school_cta(
        "Can't Find Someone Local?", "Tell us the role and the caseload — we'll send remote candidates licensed in your state.")


def guide_band():
    """The salary guide banner at the very top of the home page. It says who it's for,
    because the rest of the page speaks to districts."""
    return f'''
<!-- ── Salary guide banner ────────────────────── -->
<a class="guide-band" href="salary-guide.html">
  <div class="container guide-band-inner">
    <img class="guide-band-cover" src="img/{GUIDE["cover"]}" alt="" width="46" height="60">
    <div class="guide-band-text">
      <strong>For school therapists: the 2026 Salary Guide</strong>
      <span>What schools pay SLPs, OTs, PTs and more, from BLS data. Median K-12 pay for an SLP: {money(PAY[0]["k12"])}.</span>
    </div>
    <span class="guide-band-go">Get the Free Guide &rarr;</span>
  </div>
</a>
'''


def home_top():
    return guide_band() + '''
<!-- ── Hero: school staffing ──────────────────── -->
<section class="hero">
  <div class="container hero-grid">
    <div class="hero-inner">
      <span class="hero-kicker">K&#8209;12 School Staffing · Contract · Teletherapy</span>
      <h1>School Staffing for <em>Every IEP Service</em></h1>
      <p class="hero-lede">Speech-language pathologists first — plus OT, PT, psychology, behavior, special education, hearing, vision and nursing: 23 school roles on contract, onsite or by teletherapy, for big metro districts and small rural ones.</p>
      <p class="hero-service-line">Required by law &nbsp;·&nbsp; Publicly funded &nbsp;·&nbsp; Staffed by MedPoint</p>
      <div class="hero-search-sub">
        <a href="hire-school-staff.html" class="btn-hero-pill btn-hero-pill--filled">Hire School Staff →</a>
        <a href="school-slp-staffing.html" class="btn-hero-pill">[[ico:speech]] School SLPs</a>
        <a href="school-teletherapy-staffing.html" class="btn-hero-pill">[[ico:monitor]] Teletherapy</a>
        <a href="school-staffing.html" class="btn-hero-pill">All 23 Roles</a>
      </div>
    </div>
    <aside class="hero-card" aria-label="Scan to meet your best-matched candidate">
      <div class="hero-card-head">
        <div>
          <span class="hero-card-kicker">Scan · Paste · Match</span>
          <h2>Meet your best-matched candidate</h2>
        </div>
        <span class="live-pill">Live</span>
      </div>
      <div class="hero-qr"><img src="img/qr/school-all.svg" alt="QR code that opens the MedPoint Partners school match page" width="190" height="190"></div>
      <p class="hero-card-fine">Paste your job description and see the blinded candidate we'd send — plus the 30-second video intro we invite every candidate to film.</p>
      <a class="hero-card-go" href="school-match.html">Open the Match Page &rarr;</a>
    </aside>
  </div>
</section>
''' + edge_strip() + slp_ticker() + slp_band() + market_band() \
        + school_ticker(SHOWN, "Every School Role: Candidate Spotlights", sid="all-spotlights") + '''
<!-- ── Every role ─────────────────────────────── -->
<section class="section section-alt">
  <div class="container">
    <div class="centered">
      <span class="section-kicker">23 School Roles, One Call</span>
      <h2 class="section-title">Related Services, Special Education <em>&amp; Student Health</em></h2>
      <div class="section-divider"></div>
      <p class="section-sub">Every role a special education director answers for — staffed on contract, onsite or by teletherapy.</p>
    </div>
''' + role_columns() + '''
    <div style="display:flex;gap:12px;flex-wrap:wrap;justify-content:center;margin-top:32px;">
      <a href="school-staffing.html" class="btn btn-primary">See Every Role →</a>
      <a href="school-teletherapy-staffing.html" class="btn btn-outline-dark">[[ico:monitor]] Teletherapy Roles</a>
    </div>
  </div>
</section>
''' + law_band() + delivery_band() + rural_metro_band() + f'''
<!-- ── How it works ───────────────────────────── -->
<section class="section section-alt">
  <div class="container">
    <span class="section-kicker">How It Works</span>
    <h2 class="section-title">From Job Order to First Day</h2>
    <div class="section-divider"></div>
    {steps_row(SCHOOL_STEPS)}
  </div>
</section>
''' + states_band() + reps_band() + '''
<!-- ── Resources ──────────────────────────────── -->
<section class="section">
  <div class="container">
    <div class="section-head">
      <div>
        <span class="section-kicker">Resources for District Leaders</span>
        <h2 class="section-title">Explainers &amp; Guides</h2>
      </div>
      <a href="school-resources.html" class="btn btn-outline-dark" style="flex-shrink:0;">All Resources →</a>
    </div>
    <div class="trio">
''' + "\n".join(article_card(a) for a in ARTICLES) + '''
    </div>
  </div>
</section>
'''


def article_card(a):
    return f'''      <a class="trio-card article-card" href="{a["file"]}">
        <span class="section-kicker">{a["kicker"]}</span>
        <h4>{plain(a["h1"])}</h4>
        <p>{a["summary"]}</p>
        <span class="dept-card-go">Read →</span>
      </a>'''


HOME = home_top() + HEALTH_HOME.replace("{{HOME_FAQ}}", faq_html(HOME_FAQ)) + school_cta(
    "Fill the Seat Before the Minutes Pile Up",
    "Place a job order, or paste your job description and meet your best-matched candidate.")


# ── Hire School Staff: the district's two-step job order ──
# js/hire-school.js posts it to 100X's MEDPOINT_SCHOOL_ORDER_v1 endpoint (Gus OK'd 2026-10-29;
# modeled on /api/public/lawstaff/job-order), which makes an unlisted draft job order, the inbox
# request, the team alert and the PCR contact. If that endpoint can't be reached (e.g. before it's
# deployed), the form falls back to /api/public/inquiry with the whole job order in the notes.
JOB_ORDER_API = "https://100xrecruiting.com/api/public/medpoint/job-order"
US_STATES = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware",
             "District of Columbia", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas",
             "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
             "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York",
             "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island",
             "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
             "West Virginia", "Wisconsin", "Wyoming"]


def role_options(slp_first=False):
    """Roles as <optgroup>s. slp_first (the district job-order form) opens with the SLP family,
    since SLPs are the role districts ask for most."""
    out = []
    if slp_first:
        fam = [("slp", "Speech-Language Pathologist (CCC-SLP)"), ("cfy", "SLP Clinical Fellow (CF-SLP)"),
               ("slp", "SLP Assistant (SLPA)"), ("slp", "Bilingual SLP"), ("slp", "Teletherapy SLP")]
        out.append('<optgroup label="Speech-Language Pathology — most requested">'
                   + "".join(f'<option value="{k}">{t}</option>' for k, t in fam) + "</optgroup>")
    for key, name, _ in GROUPS:
        opts = "".join(f'<option value="{r["key"]}">{r["nav"]}</option>' for r in SHOWN
                       if r["group"] == key and not (slp_first and r["key"] in ("slp", "cfy")))
        out.append(f'<optgroup label="{name}">{opts}</optgroup>')
    return "".join(out)


HARD_TO_FILL = ["tvi", "om", "dhh", "interpreter", "audiologist", "bcba"]

HIRE = '''
<!-- ── Opt-in Hero ────────────────────────────── -->
<section class="optin-hero" style="background-image:url('{{UNS}}photo-1509062522246-3755977927d7?auto=format&fit=crop&w=1600&q=80');">
  <div class="container">
    <div class="hero-badge" style="color:rgba(255,255,255,.85);">For Districts &amp; Charter Schools</div>
    <h1>Hire School Staff —<br><em>Contract, Teletherapy</em><br>or Direct Hire</h1>
    <p>Two quick steps: who you are, then who you need. We reply within a few hours and send a blinded shortlist in 48–72 hours.</p>
  </div>
</section>

<!-- ── Form + Pitch ───────────────────────────── -->
<section class="section" style="padding-top:0;background:var(--off-white);">
  <div class="container">
    <div class="optin-layout">
      <div class="optin-pitch">
        <span class="section-label">What Happens After You Submit</span>
        <h2 class="section-title" style="font-size:1.6rem;">Your Job Order,<br>Staffed</h2>
        <div class="optin-steps">
''' + "\n".join([
    optin_step(1, "We call you (same day)", "We confirm the caseload, campuses, schedule, credentials and start date."),
    optin_step(2, "We search (24–48 hrs)", "Our live candidate pool, plus licensed providers who aren't on job boards."),
    optin_step(3, "Blinded shortlist (48–72 hrs)", "Credentials checked, your screening questions answered, video intros attached when candidates have filmed them."),
    optin_step(4, "They start. We run payroll.", "On contract for the year or semester, onsite or by teletherapy — one invoice to you."),
]) + '''
        </div>
        <div class="optin-box">
          <div class="box-label">Our Edge</div>
          <ul class="checklist">
            <li><strong>Live candidate ticker</strong> — see who we're representing right now.</li>
            <li><strong>QR match</strong> — paste a job description, meet your best-matched blinded candidate.</li>
            <li><strong>Local independent reps</strong> — a person who knows your district.</li>
          </ul>
        </div>
      </div>

      <div class="form-card form-card--lift">
        <h3>Place a School Job Order</h3>
        <p class="form-intro">No commitment. Two steps, about a minute.</p>
        <ol class="form-steps" aria-label="Form steps">
          <li class="active" data-step-tab="1">1. Your contact info</li>
          <li data-step-tab="2">2. Your hiring need</li>
        </ol>
        <form id="jobOrder" data-api="''' + JOB_ORDER_API + '''" novalidate>
          <fieldset class="form-step" data-step="1">
            <legend class="sr-only">Your contact info</legend>
            <div class="form-row">
              <div class="form-group"><label for="h-first">First Name *</label><input type="text" id="h-first" name="first_name" class="form-control" autocomplete="given-name" required></div>
              <div class="form-group"><label for="h-last">Last Name *</label><input type="text" id="h-last" name="last_name" class="form-control" autocomplete="family-name" required></div>
            </div>
            <div class="form-row">
              <div class="form-group"><label for="h-email">Work Email *</label><input type="email" id="h-email" name="email" class="form-control" autocomplete="email" required></div>
              <div class="form-group"><label for="h-phone">Phone</label><input type="tel" id="h-phone" name="phone" class="form-control" autocomplete="tel"></div>
            </div>
            <div class="form-row">
              <div class="form-group"><label for="h-company">District or School *</label><input type="text" id="h-company" name="company" class="form-control" autocomplete="organization" required></div>
              <div class="form-group"><label for="h-title">Your Title</label><input type="text" id="h-title" name="contact_title" class="form-control" placeholder="Special Education Director"></div>
            </div>
            <div class="form-group"><label for="h-state">State *</label>
              <select id="h-state" name="state" class="form-control" required>
                <option value="" disabled selected>Select your state</option>
''' + "".join(f"<option>{s}</option>" for s in US_STATES) + '''
              </select>
            </div>
            <button type="button" class="btn btn-primary btn-lg btn-block" data-next>Next: Your Hiring Need →</button>
          </fieldset>

          <fieldset class="form-step" data-step="2" hidden>
            <legend class="sr-only">Your hiring need</legend>
            <div class="form-row">
              <div class="form-group"><label for="h-role">Role *</label>
                <select id="h-role" name="role" class="form-control" required>
                  <option value="" disabled selected>Select a role</option>
''' + role_options(slp_first=True) + '''<option value="other">Other school role</option>
                </select>
              </div>
              <div class="form-group"><label for="h-count">How Many?</label><input type="number" id="h-count" name="count" class="form-control" min="1" value="1"></div>
            </div>
            <div class="form-row">
              <div class="form-group"><label for="h-delivery">Delivery *</label>
                <select id="h-delivery" name="work_setup" class="form-control" required>
                  <option value="" disabled selected>Select</option>
                  <option>Onsite</option><option>Teletherapy / remote</option><option>Hybrid</option><option>Either — whatever fills it</option>
                </select>
              </div>
              <div class="form-group"><label for="h-engagement">Kind of Hire *</label>
                <select id="h-engagement" name="engagement" class="form-control" required>
                  <option value="" disabled selected>Select</option>
                  <option>Contract — school year</option><option>Contract — semester</option><option>Contract — leave or short-term</option>
                  <option>Contract-to-hire</option><option>Direct hire</option><option>Not sure yet</option>
                </select>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group"><label for="h-schedule">Schedule</label>
                <select id="h-schedule" name="schedule" class="form-control">
                  <option value="" disabled selected>Select</option><option>Full-time</option><option>Part-time</option>
                </select>
              </div>
              <div class="form-group"><label for="h-location">City or Campuses *</label><input type="text" id="h-location" name="location" class="form-control" placeholder="e.g. Marietta — 3 elementary schools" required></div>
            </div>
            <div class="form-row">
              <div class="form-group"><label for="h-caseload">Grades &amp; Caseload</label><input type="text" id="h-caseload" name="caseload" class="form-control" placeholder="e.g. K–5, about 45 students"></div>
              <div class="form-group"><label for="h-start">Start Date</label><input type="text" id="h-start" name="start" class="form-control" placeholder="e.g. Jan 6 or ASAP"></div>
            </div>
            <div class="form-group"><label for="h-creds">Credentials or Languages Required</label><input type="text" id="h-creds" name="credentials" class="form-control" placeholder="e.g. CCC-SLP, state license; bilingual Spanish a plus"></div>
            <div class="form-group"><label for="h-details">Job Description or Details</label><textarea id="h-details" name="details" class="form-control" placeholder="Paste the job description, or tell us about the students, schedule and anything else we should know."></textarea></div>
            <div class="hp" aria-hidden="true"><label for="h-website">Website</label><input type="text" id="h-website" name="hp_website" tabindex="-1" autocomplete="off"></div>
            <div class="form-actions">
              <button type="button" class="btn btn-outline-dark btn-lg" data-back>← Back</button>
              <button type="submit" class="btn btn-primary btn-lg">Submit Job Order →</button>
            </div>
          </fieldset>
          <p class="form-note">Prefer to talk? Call <a href="tel:+14042500790" style="color:var(--blue);font-weight:600;">404-250-0790</a>.</p>
          <div class="alert alert-success" role="status">✓ Job order received! We'll call you within a few hours to confirm the details.</div>
        </form>
      </div>
    </div>
  </div>
</section>

''' + edge_strip(here=False) + '''
<!-- ── Staffing made simple ───────────────────── -->
<section class="section">
  <div class="container">
    <span class="section-kicker">Staffing Made Simple</span>
    <h2 class="section-title">One Job Order. <em>We Handle the Rest.</em></h2>
    <div class="section-divider"></div>
    ''' + steps_row(SCHOOL_STEPS) + '''
  </div>
</section>

<!-- ── Hard-to-fill roles ─────────────────────── -->
<section class="section section-alt">
  <div class="container">
    <div class="centered">
      <span class="section-kicker">Hard-to-Fill Roles, Filled</span>
      <h2 class="section-title">The Seats That Sit Empty the Longest</h2>
      <div class="section-divider"></div>
      <p class="section-sub">Low-incidence roles where a district may need one specialist — and can't find one. Contract and teletherapy are how they get filled.</p>
    </div>
    <div class="dept-grid">
''' + "\n".join(role_card(ROLE[k]) for k in HARD_TO_FILL) + '''
    </div>
  </div>
</section>
''' + rural_metro_band() + '''

<!-- ── Why partner with us ────────────────────── -->
<section class="section">
  <div class="container">
    <div class="centered">
      <span class="section-kicker">Why Districts Partner With Us</span>
      <h2 class="section-title">School Staffing, Done Differently</h2>
      <div class="section-divider"></div>
    </div>
    <div class="diff-grid">
''' + "\n".join([
    diff("pulse", "A Live Candidate Ticker", "See the blinded school candidates we're representing right now, on every page — not a promise to go looking."),
    diff("qr", "QR Match With Video Intros", "Scan a flyer or open the match page, paste your job description, and meet your best-matched candidate and the short video intro we invite every candidate to film."),
    diff("handshake", "Local Independent Reps", "A rep who knows your district and your board calendar, backed by our recruiters and back office."),
    diff("shield", "Credentials Checked First", "ASHA, NBCOT, NCSP, BACB, nursing, teaching and interpreting credentials checked before a candidate is sent."),
    diff("clipboard", "Your Questions, Answered Up Front", "We build a screening questionnaire with you. Every résumé arrives with the candidate's answers."),
    diff("receipt", "We're the Employer of Record", "Contract staff run through our payroll: weekly pay, taxes, workers' comp — one invoice to you."),
]) + '''
    </div>
  </div>
</section>

<!-- ── Results ────────────────────────────────── -->
<section class="hero-stats" style="padding:64px 0;">
  <div class="container">
    <div class="stats-section-title">Results You Can Hold Us To</div>
    <div class="stats-box">
      <div class="stat-item"><div class="stat-num">48–72 hrs</div><div class="stat-label">Blinded Shortlist After Your Job Order</div></div>
      <div class="stat-item"><div class="stat-num">1,000+</div><div class="stat-label">Candidate Video Intros Filmed</div></div>
      <div class="stat-item"><div class="stat-num">105+</div><div class="stat-label">Years Combined Recruiting Experience</div></div>
      <div class="stat-item"><div class="stat-num">20+</div><div class="stat-label">Years Recruiting &amp; Staffing</div></div>
    </div>
  </div>
</section>
''' + school_faq([FAQ_IDEA, FAQ_FUNDS, FAQ_CONTRACT, FAQ_TELE, FAQ_FAST, FAQ_BLIND]) + '''
<script src="js/hire-school.js" defer></script>
'''


# ── Sell for Us: independent reps ──
REPS = school_hero("Sell for Us", "<em>We Put You in Business</em> for Yourself",
                   "Sell school staffing as an independent rep. You open the doors at the districts you know; our recruiters find, screen, place and payroll the staff — and you earn commission.",
                   "photo-1580582932707-520aed937b7b",
                   ["Independent 1099 rep", "Commission", "Your own book of districts"]).replace(
    '''      <a href="hire-school-staff.html" class="btn btn-white btn-lg">Hire School Staff</a>
      <a href="school-match.html" class="btn btn-outline-white btn-lg">[[ico:qr]] Match a Job Description</a>''',
    f'''      <a href="{REP_JOB}" target="_blank" rel="noopener" class="btn btn-white btn-lg">Apply on 100X ↗</a>
      <a href="{PARTNER_APP}" target="_blank" rel="noopener" class="btn btn-outline-white btn-lg">Partner Application ↗</a>''') \
    + edge_strip() + school_ticker(SHOWN, "School Candidate Spotlights") + '''
<!-- ── Why schools ────────────────────────────── -->
<section class="section section-alt">
  <div class="container two-col" style="align-items:start;">
    <div>
      <span class="section-kicker">Why Build Your Book in School Staffing</span>
      <h2 class="section-title">Required by Law. Publicly Funded. <em>About as Recession-Proof as Staffing Gets.</em></h2>
      <div class="section-divider"></div>
      <p class="section-sub" style="margin-bottom:16px;">Districts don't stop needing speech therapists in a downturn. Federal law (IDEA) requires the services in every student's IEP, and public education budgets pay for them — every school year.</p>
      <p class="section-sub">And the work is mostly contract, which means districts come back every semester and every fall. Build relationships once; they keep ordering.</p>
    </div>
    <div class="panel" style="padding:28px;">
      <span class="panel-label">An Industry View</span>
      <div class="rep-stats">
''' + "".join(f'<div><div class="mini-stat-num">{n}</div><div class="mini-stat-label">{l}</div></div>' for n, l in MARKET) + '''
      </div>
      <p class="fine-print" style="text-align:left;margin-top:16px;">''' + MARKET_NOTE + '''</p>
    </div>
  </div>
</section>

<!-- ── How it works ───────────────────────────── -->
<section class="section">
  <div class="container">
    <span class="section-kicker">How It Works</span>
    <h2 class="section-title">You Open Doors. <em>We Do the Recruiting.</em></h2>
    <div class="section-divider"></div>
    ''' + steps_row([
        ("Apply", "Apply on 100X or through our partner application. We review every rep personally."),
        ("Get Your Toolkit", "Flyers with QR codes for every role, the match page, the live ticker and the job-order form."),
        ("Open District Doors", "Special education directors, student services directors, superintendents and charter leaders you know."),
        ("Earn Commission", "We fill the order and run payroll. You're paid commission — the posting has the details."),
    ]) + '''
  </div>
</section>

<!-- ── Toolkit ────────────────────────────────── -->
<section class="section section-alt">
  <div class="container">
    <div class="centered">
      <span class="section-kicker">Your Toolkit</span>
      <h2 class="section-title">Walk In With Something No One Else Has</h2>
      <div class="section-divider"></div>
    </div>
    <div class="trio">
''' + "\n".join([
        feat("pulse", "The Live Ticker", 'Blinded school candidates we\'re representing right now, on every page of this site. <a href="school-staffing.html#spotlights" class="trio-link">See it →</a>'),
        feat("qr", "QR Flyers for Every Role", 'A printable flyer for each of the 23 roles. The district scans it and meets its best-matched candidate. <a href="school-flyer.html" class="trio-link">See the flyers →</a>'),
        feat("clipboard", "A Two-Step Job Order", 'Districts place the order in a minute; our recruiters take it from there. <a href="hire-school-staff.html" class="trio-link">See the form →</a>'),
    ]) + '''
    </div>
  </div>
</section>

<!-- ── What you sell + who it's for ───────────── -->
<section class="section">
  <div class="container split" style="align-items:start;">
    <div>
      <span class="section-kicker">What You Sell</span>
      <h2 class="section-title">23 School Roles — <em>Contract &amp; Teletherapy</em></h2>
      <div class="section-divider"></div>
      <p class="section-sub">Therapy and related services, special education, behavior and mental health, hearing, vision and school nursing — on contract for the school year or semester, onsite or by teletherapy.</p>
      <a href="school-staffing.html" class="btn btn-outline-dark" style="margin-top:20px;">See Every Role →</a>
    </div>
    <div>
      <span class="section-kicker">Who This Is For</span>
      <ul class="checklist" style="margin-top:12px;">
        <li><strong>Former special education directors, teachers and administrators</strong> who know who decides.</li>
        <li><strong>SLPs, OTs and school psychologists</strong> who know the districts they've worked in.</li>
        <li><strong>Education sales reps</strong> who already call on districts.</li>
        <li><strong>Anyone whose network includes school leaders</strong> — and who wants to own their book.</li>
      </ul>
    </div>
  </div>
</section>
''' + school_faq([
    ("Is this a job or a business?",
     "A business. You work as an independent 1099 rep on commission, building your own book of districts. The posting on 100X has the details."),
    ("Do I have to recruit?",
     "No. You open the door and bring us the job order. Our recruiters find, screen and place the staff, and our back office runs payroll."),
    ("How am I paid?",
     "Commission on the business you bring in. See the rep posting on 100X for the current terms."),
    ("What about healthcare referrals?",
     "MedPoint also recruits for hospitals and practices. Our Partner Program covers healthcare referrals."),
], "What Reps Ask Us") + f'''
<!-- ── CTA band ───────────────────────────────── -->
<div class="cta-band">
  <div class="container">
    <h2>We Put You in Business for Yourself.</h2>
    <p>Apply on 100X or send our partner application — we review every rep personally.</p>
    <div class="cta-actions">
      <a href="{REP_JOB}" target="_blank" rel="noopener" class="btn btn-white btn-lg">Apply on 100X ↗</a>
      <a href="{PARTNER_APP}" target="_blank" rel="noopener" class="btn btn-outline-white btn-lg">Partner Application ↗</a>
    </div>
  </div>
</div>
'''


# ── Resources hub and explainers ──
RESOURCES = school_hero("Resources", "School Staffing <em>Resources</em>",
                        "Plain-English explainers and guides for special education directors, superintendents and district HR.",
                        "photo-1497633762265-9d179a990aa6", ["Role explainers", "IDEA staffing guide", "Market view"]) \
    + edge_strip() + school_ticker(SHOWN, "School Candidate Spotlights") + '''
<!-- ── Articles ───────────────────────────────── -->
<section class="section section-alt">
  <div class="container">
    <div class="centered">
      <span class="section-kicker">Explainers &amp; Guides</span>
      <h2 class="section-title">Read Before You Staff</h2>
      <div class="section-divider"></div>
    </div>
    <div class="trio">
''' + "\n".join(article_card(a) for a in ARTICLES) + '''
    </div>
  </div>
</section>
''' + market_band() + law_band().replace('class="section"', 'class="section section-alt"', 1) + states_band() + school_faq(HUB_FAQ) + school_cta(
    "Ready to Staff the Role?", "Place a job order, or paste your job description and meet your best-matched candidate.")


def article_page(a):
    secs = "\n".join(f"    <h2>{h}</h2>\n    {body}" for h, body in a["sections"])
    related = "\n".join(role_card(ROLE[k]) for k in a["roles"] if k in ROLE)
    crumb = f'<a href="school-resources.html">Resources</a><span>/</span>{a["kicker"]}'
    return f'''
<!-- ── Page Hero ──────────────────────────────── -->
<section class="page-hero page-hero--article">
  <div class="container">
    <div class="breadcrumb"><a href="index.html">Home</a><span>/</span>{crumb}</div>
    <h1>{a["h1"]}</h1>
    <p>Updated {a["updated"]} · MedPoint Partners</p>
  </div>
</section>
''' + edge_strip(here=False) + f'''
<!-- ── Article ────────────────────────────────── -->
<section class="section">
  <div class="container">
    <article class="prose">
    <div class="prose-answer"><span class="section-kicker">The Short Answer</span><p>{a["summary"]}</p></div>
{secs}
    </article>
  </div>
</section>

<!-- ── Related roles ──────────────────────────── -->
<section class="section section-alt">
  <div class="container">
    <div class="centered">
      <span class="section-kicker">Related Roles We Staff</span>
      <h2 class="section-title">Staff It on Contract — Onsite or by Teletherapy</h2>
      <div class="section-divider"></div>
    </div>
    <div class="dept-grid">
{related}
    </div>
  </div>
</section>
''' + school_faq(a["faq"], "Questions on This Topic").replace("section section-alt", "section") + school_cta(
        "Ready to Staff the Role?", "Place a job order, or paste your job description and meet your best-matched candidate.")


def article_schema(a):
    url = SITE + "/" + a["file"]
    art = {"@type": "Article", "headline": plain(a["h1"]), "description": plain(a["desc"]), "url": url,
           "mainEntityOfPage": url, "datePublished": a["updated"], "dateModified": a["updated"],
           "author": {"@id": SITE + "/#organization"}, "publisher": {"@id": SITE + "/#organization"},
           "image": SITE + "/img/og-image.png"}
    return [art] + school_schema(a["file"], a["h1"], a["desc"],
                                 [("Resources", SITE + "/school-resources.html"), (a["kicker"], url)], a["faq"], kind=None)


# ── State pages ──
def state_page(st):
    intro = "\n".join(f'      <p class="section-sub" style="margin-bottom:16px;">{p}</p>' for p in st["intro"])
    creds = "\n".join(f'''      <div class="diff-item">
        <div class="diff-icon">[[ico:{ROLE[k]["icon"]}]]</div>
        <div>
          <h4><a href="{ROLE[k]["file"]}">{ROLE[k]["nav"]}</a></h4>
          <p>{text}</p>
        </div>
      </div>''' for k, text in st["creds"] if k in ROLE)
    cards = "\n".join(role_card(ROLE[k]) for k in st["roles"] if k in ROLE)
    others = "\n".join(f'      <a class="tag" href="{x["file"]}">[[ico:pin]] {x["name"]}</a>' for x in STATES if x is not st)
    crumb = f'<a href="school-staffing.html#states">States</a><span>/</span>{st["name"]}'
    return school_hero(crumb, st["h1"], st["hero"], "photo-1580582932707-520aed937b7b",
                       ["Contract first", "Onsite &amp; teletherapy", f"Credentials checked for {st['name']}"]) \
        + edge_strip() + school_ticker(SHOWN, "School Candidate Spotlights") + f'''
<!-- ── Special education in the state ─────────── -->
<section class="section section-alt">
  <div class="container two-col" style="align-items:start;">
    <div>
      <span class="section-kicker">Special Education in {st["name"]}</span>
      <h2 class="section-title">How {st["name"]} Districts <em>Staff IEP Services</em></h2>
      <div class="section-divider"></div>
{intro}
    </div>
    <div class="panel" style="padding:28px;">
      <span class="panel-label">{st["local"]["h"]}</span>
      <p style="margin-top:12px;color:var(--text-muted);line-height:1.7;font-size:.95rem;">{st["local"]["p"]}</p>
    </div>
  </div>
</section>

<!-- ── Credentials ────────────────────────────── -->
<section class="section">
  <div class="container">
    <div class="centered">
      <span class="section-kicker">Credentials We Check in {st["name"]}</span>
      <h2 class="section-title">Licensed for {st["name"]} Students</h2>
      <div class="section-divider"></div>
      <p class="section-sub">Every candidate's {st["name"]} license or credential is checked before we send them — onsite or by teletherapy.</p>
    </div>
    <div class="diff-grid">
{creds}
    </div>
  </div>
</section>

<!-- ── Roles we lead with ─────────────────────── -->
<section class="section section-alt">
  <div class="container">
    <div class="centered">
      <span class="section-kicker">Roles We Staff in {st["name"]}</span>
      <h2 class="section-title">On Contract for the School Year or Semester</h2>
      <div class="section-divider"></div>
    </div>
    <div class="dept-grid">
{cards}
    </div>
    <p class="fine-print"><a href="school-staffing.html" style="color:var(--blue);font-weight:600;">See all 23 school roles →</a></p>
  </div>
</section>

<!-- ── Teletherapy in the state ───────────────── -->
<section class="section">
  <div class="container">
    <div class="example-callout" style="margin-top:0;">
      <div class="example-icon">[[ico:monitor]]</div>
      <div>
        <span class="section-kicker">Teletherapy in {st["name"]}</span>
        <h4>Remote providers, licensed where your students are</h4>
        <p>{st["tele"]}</p>
        <p style="margin-top:10px;"><a href="school-teletherapy-staffing.html" style="color:var(--blue);font-weight:600;">See every role we staff remotely →</a></p>
      </div>
    </div>
  </div>
</section>
''' + qr_block() + f'''
<!-- ── Other states ───────────────────────────── -->
<section class="section" style="padding:56px 0;">
  <div class="container centered">
    <span class="section-kicker">Other States</span>
    <div class="tags" style="justify-content:center;margin-top:14px;">
{others}
    </div>
  </div>
</section>
''' + school_faq(st["faq"] + [FAQ_IDEA, FAQ_FAST], f"What {st['name']} Districts Ask Us") + school_cta(
        f"Staffing a {st['name']} School?", "Place a job order, or paste your job description and meet your best-matched candidate.")


# ── Match page (where the QR codes land) ──
def match_data():
    """What js/school-match.js needs, as JSON in the page (plain text, not HTML)."""
    data = {"feed": "https://100xrecruiting.com/api/public/spotlights", "terms": SCHOOL_TERMS,
            "depts": [{"key": r["key"], "name": plain(r["nav"]), "one": plain(r["one"]), "file": r["file"],
                       "only": r["only"].split(","), "words": r["words"], "jd": r["jd"]} for r in ROLES]}
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")


# Words the match page scores a job description against a spotlight on (js/school-match.js)
SCHOOL_TERMS = ["ccc", "cf-slp", "clinical fellow", "slpa", "bilingual", "spanish", "teletherapy", "virtual", "remote",
                "preschool", "early childhood", "elementary", "middle school", "high school", "secondary", "autism",
                "aac", "life skills", "self-contained", "inclusion", "resource", "iep", "evaluation", "medicaid",
                "diabetes", "seizure", "trach", "g-tube", "itinerant", "ncsp", "lssp", "bcba", "bcaba", "rbt", "otr",
                "cota", "pta", "dpt", "rn", "lpn", "cpi", "fba", "bip", "articulation", "fluency", "handwriting",
                "sensory", "dyslexia", "reading", "math", "co-teach", "case manag", "full-time", "part-time", "asl",
                "eipa", "braille", "coms", "lpc", "lcsw", "lmft", "msw", "aud", "cape", "structured literacy"]

SCHOOL_MATCH_HEAD = '''
  <script>window.MP_SCHOOL = ''' + match_data() + ''';</script>
  <script src="js/school-match.js" defer></script>'''

SCHOOL_MATCH_TOP = page_hero('<a href="school-staffing.html">School Roles</a><span>/</span>Match',
                         "Meet Your <em>Best-Matched</em> Candidate",
                         "Paste your job description or pick a sample. We show the best-matched school candidate we're representing right now — blinded, with no name, employer or school — and their video intro when they've filmed one.",
                         "photo-1580582932707-520aed937b7b") + edge_strip() + '''
<!-- ── Match ──────────────────────────────────── -->
<section class="section section-alt" style="padding-top:56px;">
  <div class="container">
    <div class="match-layout">
      <div class="form-card">
        <h3>Your Job Description</h3>
        <p class="form-intro">Pick the role, then paste your job description — or start from a sample.</p>
        <div class="form-group">
          <label for="dept">Role</label>
          <select id="dept" class="form-control">
            <option value="">Any school role</option>
''' + role_options() + '''
          </select>
        </div>
        <div class="form-group">
          <label for="jd-sample">Start from a sample (optional)</label>
          <select id="jd-sample" class="form-control">
            <option value="">Choose a sample job description…</option>
''' + role_options() + '''
          </select>
        </div>
        <div class="form-group">
          <label for="jd">Job description</label>
          <textarea id="jd" class="form-control" placeholder="Paste the job description: role, caseload, campuses, schedule, credentials, start date…"></textarea>
        </div>
        <button type="button" id="matchGo" class="btn btn-primary btn-lg btn-block">Show My Best Match →</button>
        <p class="form-note">Your job description stays in your browser until you send it to us below.</p>
      </div>
      <div class="match-results" id="matchOut" aria-live="polite">
        <div class="match-empty">
          <div class="feature-icon">[[ico:target]]</div>
          <h3>Your best match shows here</h3>
          <p>We compare your job description with the blinded candidate spotlights we're publishing right now — role, credentials, setting and location. A recruiter confirms every match before an introduction.</p>
        </div>
      </div>
    </div>
  </div>
</section>
'''

SCHOOL_MATCH = SCHOOL_MATCH_TOP + '''
<!-- ── Send it to us ──────────────────────────── -->
<section class="section" id="send">
  <div class="container">
    <div class="centered">
      <span class="section-kicker">Ask for the Introduction</span>
      <h2 class="section-title">Send Us the Job Description</h2>
      <div class="section-divider"></div>
      <p class="section-sub">We'll reply within a few hours, and send a blinded shortlist in 48–72 hours. Want to send the full job order? <a href="hire-school-staff.html" style="color:var(--blue);font-weight:600;">Use our two-step form →</a></p>
    </div>
    <div class="form-card form-narrow">
      <p class="match-asked" id="matchAsked" hidden></p>
      <form data-form="medpoint-school-match" action="mailto:{{EMAIL}}" method="POST" enctype="text/plain">
        <div class="form-row">
          <div class="form-group"><label for="s-first">First Name *</label><input type="text" id="s-first" name="first_name" class="form-control" required></div>
          <div class="form-group"><label for="s-last">Last Name *</label><input type="text" id="s-last" name="last_name" class="form-control" required></div>
        </div>
        <div class="form-row">
          <div class="form-group"><label for="s-email">Work Email *</label><input type="email" id="s-email" name="email" class="form-control" required></div>
          <div class="form-group"><label for="s-phone">Phone</label><input type="tel" id="s-phone" name="phone" class="form-control"></div>
        </div>
        <div class="form-row">
          <div class="form-group"><label for="s-company">District or School *</label><input type="text" id="s-company" name="company" class="form-control" required></div>
          <div class="form-group"><label for="s-title">Your Title</label><input type="text" id="s-title" name="your_title" class="form-control" placeholder="Special Education Director"></div>
        </div>
        <div class="form-row">
          <div class="form-group"><label for="s-role">Role *</label><input type="text" id="s-role" name="role_title" class="form-control" placeholder="School SLP (CCC-SLP)" required></div>
          <div class="form-group"><label for="s-location">Location *</label><input type="text" id="s-location" name="location" class="form-control" placeholder="City, state — or teletherapy" required></div>
        </div>
        <div class="form-group"><label for="s-type">Kind of Hire</label>
          <select id="s-type" name="hire_type" class="form-control">
            <option value="" disabled selected>Select</option>
            <option>Contract — school year</option><option>Contract — semester</option><option>Contract-to-hire</option><option>Direct hire</option><option>Not sure yet</option>
          </select>
        </div>
        <div class="form-group"><label for="s-notes">Job description</label><textarea id="s-notes" name="notes" class="form-control" placeholder="Paste or edit the job description"></textarea></div>
        <input type="hidden" name="setting" value="K–12 School / District">
        <input type="hidden" name="topic" id="s-topic" value="School match">
        <button type="submit" class="btn btn-primary btn-lg btn-block">Send My Job Description →</button>
        <p class="form-note">No commitment. Prefer to talk? Call <a href="tel:+14042500790" style="color:var(--blue);font-weight:600;">404-250-0790</a>.</p>
        <div class="alert alert-success">✓ Received! We'll be in touch within a few hours.</div>
      </form>
    </div>
  </div>
</section>
'''


# ── Printable flyers (one per role; ?d= picks one) ──
def flyer(r=None):
    key = r["key"] if r else ""
    h1 = r["h1"] if r else "School Staffing for <em>Every IEP Service</em>"
    pitch = r["pitch"] if r else ("Required by law and publicly funded: speech, OT, PT, psychology, behavior, special education, "
                                  "hearing, vision and nursing — 23 school roles on contract for the school year or semester, onsite or by teletherapy.")
    items = r["roles"] if r else [n for _, n, _ in GROUPS] + ["Teletherapy for hard-to-fill roles"]
    lis = "\n".join(f"          <li>{x}</li>" for x in items)
    page = r["file"] if r else "school-staffing.html"
    delivery = ("Onsite or " + tele_label(r).lower()) if r and r.get("tele_file") else "Onsite &amp; itinerant" if r else "Onsite or teletherapy"
    return f'''
    <article class="flyer" data-d="{key}"{" hidden" if key else ""}>
      <div class="flyer-top">
        <img src="img/medpoint-logo.png" alt="MedPoint Partners — powered by NorthPoint" width="170" height="58">
        <span class="flyer-kicker">K&#8209;12 School Staffing</span>
      </div>
      <h1>{h1}</h1>
      <p class="flyer-pitch">{pitch}</p>
      <div class="flyer-body">
        <ul class="checklist">
{lis}
        </ul>
        <div class="flyer-qr">
          <img src="img/qr/{qr_name(key)}.svg" alt="QR code that opens the MedPoint Partners school match page" width="240" height="240">
          <strong>Scan to meet your best-matched candidate</strong>
          <span>Paste your job description — we show the best-matched blinded candidate we're representing now, and their video intro.</span>
        </div>
      </div>
      <div class="flyer-strip"><span>Contract first · Contract-to-hire · Direct hire</span><span>{delivery}</span><span>Shortlist in 48–72 hrs</span><span>Credentials checked</span></div>
      <div class="flyer-foot">
        <span>404-250-0790 · {{{{EMAIL}}}}</span>
        <span>medpointpartners.com/{page}</span>
      </div>
    </article>'''


SCHOOL_FLYER = '''
<!-- ── Printable flyers (one per role; ?d= picks one) ── -->
<section class="section section-alt flyer-page">
  <div class="container">
    <div class="flyer-tools">
      <select id="flyerPick" class="form-control" aria-label="Which flyer">
        <option value="">All school staffing</option>
''' + role_options() + '''
      </select>
      <button type="button" class="btn btn-primary" onclick="window.print()">[[ico:printer]] Print This Flyer</button>
    </div>
''' + flyer() + "".join(flyer(r) for r in SHOWN) + '''
  </div>
</section>
<script>
(function(){
  var pick=document.getElementById('flyerPick'), all=document.querySelectorAll('.flyer');
  function show(k){ if(!document.querySelector('.flyer[data-d="'+k+'"]')) k='';
    all.forEach(function(f){ f.hidden=f.getAttribute('data-d')!==k; }); pick.value=k; }
  show(new URLSearchParams(location.search).get('d')||'');
  pick.addEventListener('change',function(){ show(pick.value); history.replaceState(null,'',pick.value?'?d='+pick.value:location.pathname); });
})();
</script>
'''

# Services (now the healthcare page) keeps a pointer to the school side
SERVICES = SERVICES.replace("{{SCHOOL_SERVICES}}", '''
<!-- ── School staffing ────────────────────────── -->
<section class="section section-alt" id="schools" style="scroll-margin-top:calc(var(--nav-h) + 8px);">
  <div class="container">
    <div class="centered">
      <span class="section-kicker">K&#8209;12 Schools &amp; Districts</span>
      <h2 class="section-title">School Staffing Is Our Focus</h2>
      <div class="section-divider"></div>
      <p class="section-sub">Required by law and publicly funded: 23 school roles on contract for the school year or semester, onsite or by teletherapy.</p>
    </div>
''' + role_columns() + '''
    <div style="display:flex;gap:12px;flex-wrap:wrap;justify-content:center;margin-top:32px;">
      <a href="school-staffing.html" class="btn btn-primary">Explore School Staffing →</a>
      <a href="hire-school-staff.html" class="btn btn-outline-dark">Hire School Staff</a>
    </div>
  </div>
</section>
''')


def role_title(r):
    """'School SLP Staffing: Contract & Teletherapy', without a second 'for Schools' or a tail that
    pushes the title past ~70 characters."""
    base = r["seo"] + " Staffing" + ("" if r["seo"].startswith("School") else " for Schools")
    tail = ": Contract &amp; Teletherapy" if r.get("tele_file") else ": Contract &amp; Onsite"
    brand = " | MedPoint Partners"
    return (base + tail if len(plain(base + tail + brand)) <= 70 else base) + brand


def tele_title(r):
    t = f'{tele_label(r)} {r["seo"]} Staffing | MedPoint Partners'
    return t if len(plain(t)) <= 70 else t.replace(" School ", " ", 1)


def role_entry(r):
    crumbs = [ROLES_CRUMB, (r["nav"], SITE + "/" + r["file"])]
    return (r["file"], role_title(r), r["desc"], role_page(r),
            school_schema(r["file"], r["seo"] + " Staffing", r["desc"], crumbs, r["faq"] + SCHOOL_COMMON_FAQ), "")


def tele_entry(r):
    label = tele_label(r)
    desc = f'{label} {plain(r["nav"]).lower()} for K-12 districts: {plain(r["tele"]["hero"])[0].lower()}{plain(r["tele"]["hero"])[1:]}'
    desc = desc if len(desc) <= 165 else desc[:160].rsplit(" ", 1)[0] + "…"
    crumbs = [ROLES_CRUMB, TELE_CRUMB, (f'{label} {r["nav"]}', SITE + "/" + r["tele_file"])]
    return (r["tele_file"], tele_title(r), desc, tele_page(r),
            school_schema(r["tele_file"], f'{label} {r["seo"]} Staffing', desc, crumbs,
                          [r["tele"]["faq"]] + TELE_FAQ + [FAQ_FAST, FAQ_CONTRACT]), "")


def state_entry(st):
    crumbs = [("States", SITE + "/school-staffing.html#states"), (st["name"], SITE + "/" + st["file"])]
    return (st["file"], st["title"], st["desc"], state_page(st),
            school_schema(st["file"], f'School Staffing in {st["name"]}', st["desc"], crumbs, st["faq"] + [FAQ_IDEA, FAQ_FAST]), "")


# ── School therapist salary guide ─────────────────────────────
# Same layout as the LawStaff salary guide page. The numbers come from tools/school_pay.py and
# the files from tools/make_salary_guide.py. The audience is therapists, so it asks for their role
# instead of a company, and the lead goes through the same /api/public/inquiry as the site's forms.
SALARY_ROLES = ["SLP", "SLPA", "Clinical Fellow (CF-SLP)", "OT", "COTA", "PT", "PTA", "School Psychologist",
                "School Counselor", "School Social Worker", "Other"]

SALARY_CSS = """
  <style>
    [hidden] { display: none !important; }
    .optin-hero { background: linear-gradient(150deg, #0B1F3D 0%, #136B99 100%); padding: 120px 0 140px; position: relative; overflow: hidden; }
    .optin-hero::before { content: ''; position: absolute; top: -80px; right: -100px; width: 500px; height: 500px; border-radius: 50%;
      background: radial-gradient(circle, rgba(111,197,212,.16) 0%, transparent 70%); }
    .optin-layout { display: grid; grid-template-columns: 1fr 1.1fr; gap: 60px; align-items: start; margin-top: -60px; position: relative; z-index: 10; }
    .optin-pitch { padding-top: 20px; }
    .sg-tiles { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; margin-top: 26px; max-width: 640px; }
    .sg-tile { background: rgba(255,255,255,.08); border: 1px solid rgba(111,197,212,.35); border-radius: 12px; padding: 14px; }
    .sg-tile b { display: block; font-family: var(--font-head); font-size: 1.9rem; font-weight: 700; color: var(--teal-light); line-height: 1; }
    .sg-tile span { display: block; margin-top: 6px; font-size: .86rem; color: rgba(255,255,255,.82); line-height: 1.35; }
    .sg-table { width: 100%; border-collapse: collapse; background: var(--white); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; }
    .sg-table td { padding: 11px 16px; border-bottom: 1px solid var(--border); font-size: .95rem; }
    .sg-table td.n { text-align: right; font-weight: 700; font-family: var(--font-head); color: var(--navy); }
    .sg-table tr:last-child td { border-bottom: 0; }
    .sg-inside { margin: 16px 0 0; padding-left: 1.1rem; display: grid; gap: 8px; font-size: .95rem; color: var(--text); }
    .sg-gh { display: flex; gap: 16px; align-items: flex-start; justify-content: space-between; margin-bottom: 8px; }
    .sg-cover { width: 92px; flex: none; border-radius: 6px; box-shadow: 0 6px 18px rgba(11,31,61,.25); }
    .sg-hp { position: absolute; left: -9999px; width: 1px; height: 1px; overflow: hidden; }
    .sg-err { color: #b91c1c; font-weight: 600; font-size: .88rem; margin-top: 10px; }
    .sg-done { display: grid; gap: 12px; text-align: center; }
    .sg-done a:not(.btn) { color: var(--blue); text-decoration: underline; }
    @media (max-width: 860px) { .optin-layout { grid-template-columns: 1fr; gap: 28px; } .optin-pitch { padding-top: 0; } }
    @media (max-width: 640px) { .sg-tiles { grid-template-columns: 1fr; } }
  </style>"""

SALARY_JS = """
<script>
(function () {
  var form = document.getElementById('guide-form');
  if (!form) return;
  var err = document.getElementById('g-err'), btn = document.getElementById('g-go');
  function ready() { form.hidden = true; document.getElementById('g-done').hidden = false; }
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var d = Object.fromEntries(new FormData(form));
    if (!d.name.trim() || !/^[^@\\s]+@[^@\\s]+\\.[a-z]{2,}$/i.test(d.email.trim()) || !d.role) {
      err.textContent = 'Please add your name, email and role.'; err.hidden = false; return;
    }
    btn.disabled = true; btn.textContent = 'One moment…'; err.hidden = true;
    var notes = ['Source: MedPoint Partners (medpointpartners.com)', 'Salary guide download: School Therapists 2026',
                 'Role: ' + d.role, d.state ? 'State: ' + d.state : ''].filter(Boolean).join('\\n');
    // A missed lead is better than a therapist who can't get the guide, so a failed save still opens it.
    fetch('https://100xrecruiting.com/api/public/inquiry', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ employer_name: d.name.trim(), employer_email: d.email.trim(), employer_company: '',
                             inquiry_type: 'medpoint-salary-guide', notes: notes, hp_website: d.hp_website })
    }).then(ready, ready);
  });
})();
</script>"""

SALARY_ROWS = "".join(f'<tr><td>{r["role"]}</td><td class="n">{money(r["k12"])}</td></tr>' for r in PAY)
SALARY_OPTIONS = "".join(f"<option>{o}</option>" for o in SALARY_ROLES)
_SLP = PAY[0]

SALARY_GUIDE = f"""
<section class="optin-hero">
  <div class="container" style="position:relative;z-index:2;">
    <div style="max-width:680px;position:relative;z-index:2;">
      <div class="hero-badge">Salary Guide 2026 · School Therapists</div>
      <h1 style="color:var(--white);font-size:clamp(1.9rem,4vw,2.9rem);margin-bottom:16px;">What School Therapists <em style="color:var(--teal-light);font-style:normal;">Get Paid</em></h1>
      <p style="color:rgba(255,255,255,.78);font-size:1.05rem;line-height:1.7;">U.S. Bureau of Labor Statistics data for {len(PAY)} school roles: K-12 pay against every other setting, Georgia pay and job growth.</p>
      <div class="sg-tiles">
        <div class="sg-tile"><b>{money(_SLP["k12"])}</b><span>Median K-12 pay for an SLP</span></div>
        <div class="sg-tile"><b>{school_share(_SLP)}</b><span>Of SLPs work in K-12 schools</span></div>
        <div class="sg-tile"><b>{_SLP["growth"]}%</b><span>Projected SLP job growth, 2025 to 2035</span></div>
      </div>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0;background:var(--off-white);">
  <div class="container">
    <div class="optin-layout">

      <div class="optin-pitch">
        <div class="section-label" style="margin-top:60px;">Inside the guide</div>
        <h2 class="section-title" style="font-size:1.6rem;">K-12 Median Pay by Role</h2>
        <table class="sg-table" style="margin-top:18px;"><tbody>{SALARY_ROWS}</tbody></table>
        <p style="font-size:.82rem;color:var(--text-muted);margin-top:10px;">National medians for elementary and secondary schools, May 2025, every experience level. The guide also has all-settings pay, hourly rates and pay ranges.</p>
        <ul class="sg-inside">
          <li>K-12 pay against the all-settings median for {len(PAY)} roles</li>
          <li>Why to compare offers by the day, not the year</li>
          <li>Georgia pay by role</li>
          <li>Job growth through 2035</li>
          <li>Five ways to use this in your next contract</li>
        </ul>
      </div>

      <div class="form-card" style="margin-top:-30px;box-shadow:var(--shadow-lg);">
        <form id="guide-form" novalidate>
          <div class="sg-gh">
            <div>
              <h3 style="margin-bottom:4px;">Get the Salary Guide</h3>
              <p style="color:var(--text-muted);font-size:.88rem;margin:0;">{GUIDE["pages"]} pages. Download it right away.</p>
            </div>
            <img class="sg-cover" src="img/{GUIDE["cover"]}" alt="Cover of the MedPoint Partners Salary Guide 2026: School Therapists" width="92" height="119">
          </div>
          <div class="sg-hp" aria-hidden="true"><label for="g-website">Website</label><input id="g-website" name="hp_website" tabindex="-1" autocomplete="off"></div>
          <div class="form-group"><label for="g-name">Your Name *</label><input type="text" id="g-name" name="name" class="form-control" autocomplete="name" required></div>
          <div class="form-group"><label for="g-email">Email *</label><input type="email" id="g-email" name="email" class="form-control" autocomplete="email" required></div>
          <div class="form-group"><label for="g-role">Your Role *</label><select id="g-role" name="role" class="form-control" required><option value="">Choose one</option>{SALARY_OPTIONS}</select></div>
          <div class="form-group"><label for="g-state">State</label><input type="text" id="g-state" name="state" class="form-control" autocomplete="address-level1"></div>
          <button type="submit" id="g-go" class="btn btn-gold btn-lg" style="width:100%;justify-content:center;">Download the Salary Guide &rarr;</button>
          <p class="sg-err" id="g-err" hidden></p>
          <p style="font-size:.78rem;color:var(--text-muted);text-align:center;margin-top:12px;">We'll send school job openings now and then. You can tell us to stop any time.</p>
        </form>
        <div class="sg-done" id="g-done" hidden>
          <h3 style="margin:0;">Your guide is ready.</h3>
          <a class="btn btn-gold btn-lg" href="downloads/{GUIDE["pdf"]}" style="justify-content:center;">Download the PDF</a>
          <a href="downloads/{GUIDE["web"]}">Or read it online</a>
          <p style="font-size:.88rem;color:var(--text-muted);margin:6px 0 0;">Looking for a school role? <a href="{{{{JOB_BOARD}}}}" target="_blank" rel="noopener">See open jobs</a> or <a href="{GUIDE["group"]}" target="_blank" rel="noopener">join the School Therapist Network</a>.</p>
        </div>
      </div>

    </div>
  </div>
</section>
""" + SALARY_JS


SCHOOL_PAGES = [
    ("school-staffing.html", "Every School Role We Staff: K-12 Districts | MedPoint Partners",
     "23 K-12 school roles on contract, onsite or by teletherapy: SLPs, OTs, PTs, school psychologists, BCBAs, counselors, SPED teachers, TVIs and nurses.",
     ROLES_HUB, school_schema("school-staffing.html", "K-12 School Staffing",
                              "Contract and teletherapy staffing for K-12 school districts and charter schools.",
                              [ROLES_CRUMB], HUB_FAQ), ""),
    ("school-teletherapy-staffing.html", "Teletherapy &amp; Remote School Staffing | MedPoint Partners",
     "Teletherapy staffing for K-12 districts: SLPs, OTs, school psychologists, counselors, BCBAs, vision and DHH teachers, licensed in your state.",
     TELE_HUB, school_schema("school-teletherapy-staffing.html", "School Teletherapy Staffing",
                             "Remote and teletherapy staffing for K-12 school districts.", [ROLES_CRUMB, TELE_CRUMB],
                             TELE_FAQ + [FAQ_TELE, FAQ_IDEA, FAQ_FAST]), ""),
    ("hire-school-staff.html", "Hire School Staff: Place a Job Order | MedPoint Partners",
     "Place a school job order in two steps: SLPs, OTs, school psychologists, BCBAs, SPED teachers, nurses and more, on contract, by teletherapy or direct hire.",
     HIRE, school_schema("hire-school-staff.html", "Hire School Staff",
                         "Place a K-12 school staffing job order.", [("Hire School Staff", SITE + "/hire-school-staff.html")],
                         [FAQ_IDEA, FAQ_FUNDS, FAQ_CONTRACT, FAQ_TELE, FAQ_FAST, FAQ_BLIND]), ""),
    ("sell-for-us.html", "Sell School Staffing as an Independent Rep | MedPoint Partners",
     "We put you in business for yourself: sell K-12 school staffing as an independent 1099 rep. You open district doors; we recruit, place and payroll.",
     REPS, school_schema("sell-for-us.html", "Sell for Us", "Independent rep opportunity.",
                         [("Sell for Us", SITE + "/sell-for-us.html")], None, kind=None), ""),
    ("school-resources.html", "School Staffing Resources for District Leaders | MedPoint Partners",
     "Explainers and guides for special education directors and superintendents: what school SLPs and psychologists do, and how to staff IDEA services.",
     RESOURCES, school_schema("school-resources.html", "School Staffing Resources", "Resources for district leaders.",
                              [("Resources", SITE + "/school-resources.html")], HUB_FAQ, kind=None), ""),
    ("salary-guide.html", "School Therapist Salary Guide 2026 | MedPoint Partners",
     "What schools pay SLPs, OTs, PTs, school psychologists, counselors and social workers, from BLS data, and how it compares with other settings. Free download.",
     SALARY_GUIDE, school_schema("salary-guide.html", "School Therapist Salary Guide 2026", "BLS pay data for school therapists.",
                                 [("Salary Guide", SITE + "/salary-guide.html")], None, kind=None), SALARY_CSS),
    ("school-match.html", "Match a School Job Description | MedPoint Partners",
     "Paste a school job description and see the best-matched blinded candidate we're representing now: SLPs, OTs, psychologists, BCBAs, nurses and more.",
     SCHOOL_MATCH, school_schema("school-match.html", "School Job Description Match",
                                 "Match a K-12 school job description to a blinded candidate.",
                                 [ROLES_CRUMB, ("Match", SITE + "/school-match.html")], None, kind=None), SCHOOL_MATCH_HEAD),
] + [role_entry(r) for r in SHOWN] + [tele_entry(r) for r in TELE_ROLES] + [state_entry(st) for st in STATES] + [
    (a["file"], a["title"], a["desc"], article_page(a), article_schema(a), "") for a in ARTICLES]
# Pages that open with the school edge strip themselves; every other page gets it above the footer
SCHOOL_LED = {"index.html"} | {e[0] for e in SCHOOL_PAGES}

PAGES = [
    ("index.html", "School Staffing for K-12 Districts | MedPoint Partners",
     "Contract school staffing for K-12 districts: SLPs, OTs, PTs, school psychologists, BCBAs, SPED teachers and nurses, onsite or by teletherapy.",
     HOME, faq_schema(HOME_FAQ), HOME_HEAD),
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
] + SCHOOL_PAGES

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


def write_qr_codes():
    """One SVG QR code per school role (plus one for all of them) for the pages and flyers.
    Needs segno (pip install segno); without it the committed SVGs are kept."""
    try:
        import segno
    except ImportError:
        print("segno not installed: kept the existing QR codes in img/qr/")
        return
    (OUT / "img" / "qr").mkdir(parents=True, exist_ok=True)
    for key in [""] + [r["key"] for r in ROLES]:
        segno.make(qr_url(key), error="m").save(str(OUT / "img" / "qr" / (qr_name(key) + ".svg")), kind="svg",
                                                 border=2, dark="#0e2240", xmldecl=False, omitsize=True)
    print("wrote", len(ROLES) + 1, "QR codes")


BUILD_DATE = "2026-10-30"   # lastmod for sitemap.xml; bump it when pages change


def page_priority(file):
    if file == "index.html":
        return "1.0"
    if file in ("school-staffing.html", "hire-school-staff.html"):
        return "0.9"
    if file in ("school-teletherapy-staffing.html", "services.html") or file in {r["file"] for r in ROLES}:
        return "0.8"
    if file in {r.get("tele_file") for r in ROLES} or file in {st["file"] for st in STATES}:
        return "0.7"
    return "0.6"


def write_sitemap():
    rows = "\n".join(f"  <url><loc>{SITE}/{'' if f == 'index.html' else f}</loc><lastmod>{BUILD_DATE}</lastmod>"
                     f"<changefreq>{'weekly' if f in SCHOOL_LED else 'monthly'}</changefreq><priority>{page_priority(f)}</priority></url>"
                     for f, *_ in PAGES)
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
                                     '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + rows + "\n</urlset>\n",
                                     encoding="utf-8")
    print("wrote sitemap.xml with", len(PAGES), "pages")


def write_llms():
    """llms.txt: what the firm does and every page worth reading, school staffing first."""
    u = lambda f: f"{SITE}/{f}"   # noqa: E731
    groups = []
    for key, name, _ in GROUPS:
        lines = [f"- {plain(r['nav'])}: {plain(r['card'])} {u(r['file'])}"
                 + (f" (remote: {u(r['tele_file'])})" if r.get("tele_file") else "")
                 for r in SHOWN if r["group"] == key]
        groups.append(f"### {plain(name)}\n" + "\n".join(lines))
    text = f"""# MedPoint Partners

> K-12 school staffing firm in Atlanta, GA, powered by NorthPoint. MedPoint Partners staffs school districts and charter schools with the people IEP services depend on: speech-language pathologists, occupational and physical therapists, school psychologists, BCBAs and RBTs, counselors, social workers, special education teachers and paraprofessionals, interpreters, teachers of the deaf and visually impaired, and school nurses. Contract for the school year or semester comes first, onsite or by teletherapy; contract-to-hire and direct hire are available. MedPoint also recruits for hospitals and physician practices.

## Why school staffing
- Required by law: the Individuals with Disabilities Education Act (IDEA) entitles every student with an IEP to the special education and related services written into it.
- Publicly funded: federal IDEA Part B grants, state and local special education funds, and school-based Medicaid for eligible services.
- Industry view: on October 29, 2026, one national school staffing firm's public job board listed {MARKET[0][0]} open jobs, {MARKET[1][0]} of them contract, with about 3,000 new postings a week (the counts may include some healthcare roles).

## Speech-language pathologists first
SLPs are the largest school role ({SLP_FLAG["note"][:-1]}). MedPoint staffs CCC-SLPs, clinical fellows (CF-SLP), SLP assistants, bilingual SLPs and teletherapy SLPs: {u(SLP["file"])} (teletherapy: {u(SLP["tele_file"])}).

## Big metro and small rural districts
Metro districts get volume, bilingual staff, backlog help and fast replacements. Small and rural districts get teletherapy when no one lives within driving distance, itinerant clinicians shared across campuses, low-incidence roles a few hours a week, and one point of contact for every role.

## What makes MedPoint different
- A live ticker of blinded school candidates (no name, employer or school) on every school page.
- QR codes on every school page and printable flyer open a match page: a district pastes or picks its job description and sees its best-matched blinded candidate, plus the 30-second video intro every candidate is invited to film. {u("school-match.html")}
- Local independent reps ("We put you in business for yourself"): {u("sell-for-us.html")}
- Blinded shortlist in 48 to 72 hours; licenses and certifications checked before a candidate is sent; every résumé arrives with answers to the district's screening questions; MedPoint is employer of record for contract staff (weekly payroll, taxes, workers' comp, one invoice).

## Contact
- Place a school job order (two steps): {u("hire-school-staff.html")}
- Phone: 404-250-0790 or 678-777-5627
- Email: {EMAIL}
- Location: Atlanta, GA. Contract and teletherapy school roles nationwide; healthcare roles across the Southeast, remote roles nationwide.

## School roles (23)
- All roles: {u("school-staffing.html")}
- Teletherapy and remote roles: {u("school-teletherapy-staffing.html")}

""" + "\n\n".join(groups) + """

## School staffing by state
""" + "\n".join(f"- {st['name']}: {u(st['file'])}" for st in STATES) + """

## Resources for district leaders
""" + "\n".join(f"- {plain(a['h1'])}: {u(a['file'])}" for a in ARTICLES) + f"""
- All resources: {u("school-resources.html")}
- School therapist salary guide 2026 (BLS pay for SLPs, OTs, PTs, school psychologists and more): {u("salary-guide.html")}

## Healthcare recruiting and staffing
MedPoint also helps hospitals, physician practices and healthcare organizations hire clinical and non-clinical people as temp, temp-to-perm or direct hire, plus retained search and RPO, and payrolls temps as Employer of Record.
- Roles: nursing (RN, LPN, CNA, nurse leaders); physicians, NPs, PAs and CRNAs; allied health and therapy; medical assistants and front office; revenue cycle, coding and healthcare finance; healthcare leadership.
- Services: {u("services.html")}
- Healthcare temps: {u("temp-staffing.html")}
- Request healthcare talent: {u("request-talent.html")}
- Partner Program (10% of direct hire fees, 25% of temp net spread, paid monthly): {u("partners.html")}
- Job board: {JOB_BOARD}

## Pages
- Home: {SITE}/
- About: {u("about.html")}
- Contact: {u("contact.html")}
"""
    (OUT / "llms.txt").write_text(text, encoding="utf-8")
    print("wrote llms.txt")


EDGE_FOOT = '<div class="edge-foot"><div class="container"><span class="section-kicker">School Staffing Is Our Focus</span></div></div>' + edge_strip(here=False)


if __name__ == "__main__":
    for file, title, desc, body, schema, extra in PAGES:
        foot = "" if file in SCHOOL_LED else EDGE_FOOT   # the school edge on every page
        html = head(file, title, desc, schema, extra) + NAV + body + foot + FOOTER
        (OUT / file).write_text(fill(html), encoding="utf-8")
    print("wrote", len(PAGES), "pages")
    # The flyer page is for printing, not for search results
    html = head("school-flyer.html", "School Staffing Flyers | MedPoint Partners",
                "Printable K-12 school staffing flyers with a QR code that matches a district's job description to a blinded candidate.",
                None, "", robots="noindex, follow") + NAV + SCHOOL_FLYER + FOOTER
    (OUT / "school-flyer.html").write_text(fill(html), encoding="utf-8")
    print("wrote school-flyer.html")
    write_qr_codes()
    write_sitemap()
    write_llms()
    for file, to in OLD_LINKS.items():
        (OUT / file).parent.mkdir(exist_ok=True)
        (OUT / file).write_text(forward_page(to), encoding="utf-8")
    print("wrote", len(OLD_LINKS), "forwarding pages for old addresses")
