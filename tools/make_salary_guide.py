"""Build the MedPoint Partners school therapist salary guide.

Same report layout as the 100X, Staff Financial and LawStaff guides, built from BLS data
alone: there are no therapist questionnaires yet, so it has no "what they ask for" pages.
Numbers live in tools/school_pay.py.

    python tools/make_salary_guide.py

Writes downloads/<pdf>, downloads/<web>, img/<cover> and img/<og> into the site folder.
"""
import base64
import html
import subprocess
from pathlib import Path

import pymupdf

from school_pay import GUIDE, PAY, gap, money, school_share

ROOT = Path(__file__).resolve().parent.parent
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
JOB_BOARD = "https://host.pcrecruiter.net/pcrbin/jobboard.aspx?uid=Staff%20Financial.npsg"
LOGO = "data:image/png;base64," + base64.b64encode((ROOT / "img/medpoint-logo.png").read_bytes()).decode()
FONTS = ("https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800"
         "&family=Inter:wght@400;500;600;700;800&display=swap")
SCHOOL_DAYS, YEAR_DAYS = 190, 260
AMBER = "#D9822B"
esc = html.escape

SLP = PAY[0]
OT = PAY[1]
PT = PAY[2]
PSYCH = PAY[3]
COUNSELOR = PAY[4]

CSS = """
:root { --ink:#0E2240; --navy:#0B1F3D; --panel:#12325A; --blue:#1A76A7; --cyan:#6FC5D4; --band:#D5E3EE;
  --paper:#FFFFFF; --wash:#F2F6FB; --muted:#4E607C; --rule:#D9E2EE;
  --font:'Inter','Segoe UI',Helvetica,Arial,sans-serif; --display:'Outfit','Segoe UI',Helvetica,Arial,sans-serif;
  color-scheme: light; }
* { box-sizing: border-box; }
body { background: var(--wash); color: var(--ink); font-family: var(--font); font-size: 17px; line-height: 1.5; margin: 0; }
.doc { max-width: 960px; margin: 0 auto; padding-inline: 16px; padding-block: 24px 64px; display: grid; gap: 22px; }
section { background: var(--paper); border: 1px solid var(--rule); border-radius: 6px; padding: clamp(22px, 4vw, 48px); display: grid; gap: 18px; }
h1, h2, h3 { margin: 0; line-height: 1.05; letter-spacing: -0.02em; text-wrap: balance; font-family: var(--display); }
h2 { font-size: clamp(1.7rem, 3.4vw, 2.4rem); font-weight: 800; }
h3 { font-size: 1.15rem; font-weight: 700; letter-spacing: 0; }
p { margin: 0; max-width: 66ch; }
.eyebrow { font-size: .78rem; font-weight: 800; letter-spacing: .16em; text-transform: uppercase; color: var(--blue); }
.muted { color: var(--muted); }
.small { font-size: .86rem; }
.cover { background: linear-gradient(150deg, #0B1F3D 0%, #136B99 100%); color: #fff; border: 0; position: relative; overflow: hidden; gap: 26px; }
.cover::after { content: ""; position: absolute; inset: 0; pointer-events: none;
  background-image: linear-gradient(rgba(111,197,212,.08) 1px, transparent 1px), linear-gradient(90deg, rgba(111,197,212,.08) 1px, transparent 1px);
  background-size: 44px 44px; -webkit-mask-image: radial-gradient(70% 80% at 85% 100%, #000 10%, transparent 70%); mask-image: radial-gradient(70% 80% at 85% 100%, #000 10%, transparent 70%); }
.cover > * { position: relative; z-index: 1; }
.cover .eyebrow { color: var(--cyan); }
.lsg { display: inline-block; width: fit-content; align-self: flex-start; background: #fff; border-radius: 12px; padding: 10px 16px; line-height: 0; }
.lsg img { height: 64px; width: auto; }
.cover h1 { font-size: clamp(2.6rem, 7vw, 4.6rem); font-weight: 800; }
.cover .lede { font-size: 1.25rem; color: #C9D6EE; max-width: 46ch; }
.tiles { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; }
.tile { background: var(--panel); border: 1px solid rgba(111,197,212,.25); border-radius: 10px; padding: 16px; }
.tile b { display: block; font-size: 1.85rem; font-weight: 800; color: var(--cyan); line-height: 1; font-variant-numeric: tabular-nums; }
.tile span { display: block; margin-top: 8px; font-size: .92rem; color: #DCE7F7; line-height: 1.3; }
.cover .src { font-size: .85rem; color: #A9BEDF; }
.chart { width: 100%; height: auto; display: block; }
.chart .grid { stroke: var(--rule); stroke-width: 1; }
.chart .tick { fill: var(--muted); font-weight: 600; font-size: 13px; font-family: var(--font); }
.chart .lab { fill: var(--ink); font-weight: 600; font-size: 14px; font-family: var(--font); }
.chart .val { fill: var(--ink); font-weight: 800; font-size: 15px; font-family: var(--font); font-variant-numeric: tabular-nums; }
.chart .band { fill: var(--band); }
.chart .dot { fill: var(--blue); stroke: #fff; stroke-width: 2.5; }
.chart .k12 { fill: """ + AMBER + """; stroke: #fff; stroke-width: 2.5; }
.chart .track { fill: var(--wash); }
.chart .fill { fill: var(--blue); }
.tablewrap { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; font-size: .92rem; font-variant-numeric: tabular-nums; }
th, td { padding: 8px 10px; border-bottom: 1px solid var(--rule); text-align: left; vertical-align: top; }
thead th { font-size: .7rem; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); font-weight: 800; border-bottom: 2px solid var(--ink); }
tbody th { font-weight: 700; }
td.num { text-align: right; white-space: nowrap; }
thead th.num { text-align: right; }
.strong { font-weight: 800; }
.takeaway { background: var(--wash); border-left: 4px solid var(--blue); padding: 14px 16px; border-radius: 0 8px 8px 0; font-weight: 600; max-width: none; }
.two { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 26px; }
.two > div { display: grid; gap: 12px; align-content: start; min-width: 0; }
ol.tips { margin: 0; padding-left: 1.3rem; display: grid; gap: 12px; max-width: 70ch; }
ol.tips li::marker { font-weight: 800; color: var(--blue); }
ol.tips b { display: block; }
.cta { background: var(--navy); color: #fff; border: 0; }
.cta h2 { color: #fff; }
.cta p { color: #C9D6EE; }
.cta p a { color: var(--cyan); }
.cta .go { display: inline-block; background: var(--cyan); color: var(--navy); font-weight: 800; font-size: 1.1rem; padding: 12px 18px; border-radius: 10px; text-decoration: none; justify-self: start; }
a { color: var(--blue); }
.sources { margin: 0; padding-left: 1.2rem; }
.sources li { margin-bottom: 5px; }
@media (max-width: 760px) { .tiles { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media screen and (max-width: 760px) { .two { grid-template-columns: 1fr; } }
@media print {
  @page { size: Letter; margin: 0.45in; }
  body { background: #fff; font-size: 12.5px; }
  .doc { max-width: none; padding: 0; gap: 0; }
  section { border: 0; border-radius: 0; padding: 0.12in 0.1in; gap: 11px; break-inside: avoid; }
  h2 { font-size: 26px; }
  h3 { font-size: 14px; }
  .small { font-size: 11px; }
  table { font-size: 11px; }
  th, td { padding: 5px 7px; }
  thead th { font-size: 9px; }
  .takeaway { padding: 10px 12px; }
  ol.tips { gap: 9px; }
  .two { gap: 22px; }
  section.page { break-before: page; }
  .cover { padding: 0.55in 0.45in; min-height: 9.9in; align-content: center; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .cta, .tile, .takeaway, .chart { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .cta { padding: 0.28in; margin-top: 8px; }
  .cover .lede { font-size: 17px; }
  .cover h1 { font-size: 58px; }
}
"""


def pay_chart():
    left, right, top, rowh = 300, 830, 34, 36
    lo, hi = 40000, 150000
    w, h = 860, top + rowh * len(PAY) + 8

    def x(v):
        return left + (v - lo) / (hi - lo) * (right - left)
    out = [f'<svg class="chart" viewBox="0 0 {w} {h}" role="img" '
           'aria-label="Pay by role: median in K-12 schools, median in all settings, and the lowest and highest 10 percent">']
    for t in range(50000, 150001, 25000):
        out.append(f'<line x1="{x(t):.1f}" y1="{top - 10}" x2="{x(t):.1f}" y2="{h - 4}" class="grid"/>')
        out.append(f'<text x="{x(t):.1f}" y="{top - 16}" class="tick" text-anchor="middle">${t // 1000}K</text>')
    for i, r in enumerate(PAY):
        y = top + i * rowh + rowh / 2
        out.append(f'<text x="{left - 12}" y="{y + 5:.1f}" class="lab" text-anchor="end">{esc(r["role"])}</text>')
        out.append(f'<rect x="{x(r["p10"]):.1f}" y="{y - 8:.1f}" width="{x(r["p90"]) - x(r["p10"]):.1f}" height="16" rx="4" class="band"/>')
        # Values this close would hide one mark, so stack them in the row.
        close = abs(x(r["k12"]) - x(r["all"])) < 20
        dot_y, k12_y = (y - 8, y + 8) if close else (y, y)
        k, d = x(r["k12"]), 11
        out.append(f'<path d="M{k:.1f} {k12_y - d:.1f}L{k + d:.1f} {k12_y:.1f}L{k:.1f} {k12_y + d:.1f}L{k - d:.1f} {k12_y:.1f}Z" class="k12"/>')
        out.append(f'<circle cx="{x(r["all"]):.1f}" cy="{dot_y:.1f}" r="9" class="dot"/>')
    out.append("</svg>")
    return "".join(out)


def legend():
    return (f'<p class="small muted" style="max-width:none"><svg width="16" height="16" viewBox="0 0 16 16" style="vertical-align:-3px"><path d="M8 0L16 8L8 16L0 8Z" fill="{AMBER}"/></svg> '
            'Median in K-12 schools &nbsp;&nbsp; '
            '<svg width="16" height="16" viewBox="0 0 16 16" style="vertical-align:-3px"><circle cx="8" cy="8" r="7.5" fill="#1A76A7"/></svg> '
            'Median in all settings &nbsp;&nbsp; '
            '<svg width="30" height="12" viewBox="0 0 30 12" style="vertical-align:-1px"><rect width="30" height="12" rx="3" fill="#D5E3EE"/></svg> '
            'Lowest 10% to highest 10%, all settings</p>')


def growth_chart():
    rows = sorted(PAY, key=lambda r: -r["growth"])
    left, right, rowh = 316, 790, 34
    w, h = 860, rowh * len(rows) + 8

    def x(v):
        return left + v / 25 * (right - left)
    out = [f'<svg class="chart" viewBox="0 0 {w} {h}" role="img" aria-label="Projected job growth by role, 2025 to 2035">']
    for i, r in enumerate(rows):
        y = i * rowh + rowh / 2 + 4
        out.append(f'<text x="{left - 12}" y="{y + 5:.1f}" class="lab" text-anchor="end">{esc(r["role"])}</text>')
        out.append(f'<rect x="{left}" y="{y - 10:.1f}" width="{x(r["growth"]) - left:.1f}" height="20" rx="4" class="fill"/>')
        out.append(f'<text x="{x(r["growth"]) + 10:.1f}" y="{y + 5:.1f}" class="val">{r["growth"]}%</text>')
    out.append("</svg>")
    return "".join(out)


def build():
    pay_rows = "".join(
        f"<tr><th scope='row'>{esc(r['role'])}</th><td class='num strong'>{money(r['k12'])}</td>"
        f"<td class='num'>${r['k12_hour']:.2f}</td><td class='num'>{money(r['all'])}</td><td class='num'>{gap(r)}</td>"
        f"<td class='num'>{money(r['p10'])}</td><td class='num'>{money(r['p90'])}</td></tr>" for r in PAY)
    day_rows = "".join(
        f"<tr><th scope='row'>{esc(r['role'])}</th><td class='num strong'>{money(r['k12'] / SCHOOL_DAYS)}</td>"
        f"<td class='num'>{money(r['all'] / YEAR_DAYS)}</td></tr>" for r in PAY if r["soc"] in ("29-1127", "29-1122", "29-1123", "31-2011", "31-2021"))
    ga_rows = "".join(f"<tr><th scope='row'>{esc(r['role'])}</th><td class='num strong'>{money(r['ga'])}</td></tr>" for r in PAY)
    share_rows = "".join(
        f"<tr><th scope='row'>{esc(r['role'])}</th><td class='num'>{r['k12_jobs']:,}</td><td class='num strong'>{school_share(r)}</td></tr>"
        for r in sorted(PAY, key=lambda r: -r["k12_jobs"]))
    return f"""<div class="doc">

<section class="cover">
  <span class="lsg"><img src="{LOGO}" alt="MedPoint Partners"></span>
  <div style="display:grid;gap:14px;">
    <span class="eyebrow">Salary Guide 2026</span>
    <h1>School Therapists</h1>
    <p class="lede">What schools pay SLPs, OTs, PTs, psychologists, counselors, social workers and assistants, how that compares with other settings, and how to use it in your next contract.</p>
  </div>
  <div class="tiles">
    <div class="tile"><b>{money(SLP['k12'])}</b><span>Median K-12 pay for an SLP</span></div>
    <div class="tile"><b>{school_share(SLP)}</b><span>Of SLPs work in K-12 schools</span></div>
    <div class="tile"><b>{SLP['growth']}%</b><span>Projected SLP job growth, 2025 to 2035</span></div>
    <div class="tile"><b>{len(PAY)}</b><span>School roles in this guide</span></div>
  </div>
  <p class="src">Built from U.S. Bureau of Labor Statistics data: wages for May 2025 and job projections for 2025 to 2035.</p>
</section>

<section class="page">
  <span class="eyebrow">Pay</span>
  <h2>What schools pay</h2>
  <p>National median pay in K-12 schools against the median for the same role in every setting. A median is the middle: half earn more and half earn less. These include every experience level.</p>
  {pay_chart()}
  {legend()}
  <p class="takeaway">Schools pay SLPs and OTs nearly $15,000 less than the all-settings median. For PTs the gap is less than half that, and school psychologists are nearly even. Counselors and social workers earn more in schools than they do overall.</p>
  <div class="tablewrap"><table>
    <thead><tr><th>Role</th><th class="num">K-12 median</th><th class="num">K-12 hourly</th><th class="num">All settings</th><th class="num">Schools vs. all</th><th class="num">Lowest 10%</th><th class="num">Highest 10%</th></tr></thead>
    <tbody>{pay_rows}</tbody>
  </table></div>
</section>

<section class="page">
  <span class="eyebrow">How to compare</span>
  <h2>Compare by the day, not the year</h2>
  <p>BLS works out hourly pay by dividing the annual figure by 2,080 hours, a full year of 40-hour weeks. School contracts are usually shorter than that, so annual and hourly figures can make school pay look lower than it is for the days you work.</p>
  <div class="two">
    <div>
      <h3>An example</h3>
      <p class="small muted">Median pay divided by {SCHOOL_DAYS} days for schools and {YEAR_DAYS} days (52 five-day weeks) for all settings.</p>
      <div class="tablewrap"><table>
        <thead><tr><th>Role</th><th class="num">School, per day</th><th class="num">All settings, per day</th></tr></thead>
        <tbody>{day_rows}</tbody>
      </table></div>
    </div>
    <div>
      <h3>How to read this</h3>
      <p class="small">{SCHOOL_DAYS} days is a round number for illustration, not BLS data. Contracts vary, and some school roles run 11 or 12 months. {YEAR_DAYS} days is before any paid time off. Swap in your own numbers.</p>
      <p class="small">These are base wages. Benefits, pensions, caseload and paperwork time aren't included.</p>
    </div>
  </div>
  <p class="takeaway">On this example calendar, the school day rate comes out ahead for every role shown. Your contract days decide it, so ask for them before you compare offers.</p>
  <div class="two">
    <div>
      <h3>Georgia pay</h3>
      <p class="small muted">Median annual pay in Georgia, May 2025. This covers all settings, not just schools.</p>
      <div class="tablewrap"><table><tbody>{ga_rows}</tbody></table></div>
    </div>
    <div>
      <h3>Small groups</h3>
      <p class="small">Treat the K-12 medians for assistants as rough. BLS counts about {PAY[6]['k12_jobs']:,} OT assistants and {PAY[7]['k12_jobs']:,} PT assistants in K-12 schools, far fewer than the other roles here.</p>
      <p class="small">School SLP assistants aren't in this guide because BLS doesn't report them as a separate job.</p>
    </div>
  </div>
</section>

<section class="page">
  <span class="eyebrow">Outlook</span>
  <h2>Where the job growth is</h2>
  <p>Projected U.S. job growth from 2025 to 2035, across all work settings. BLS expects about 12,500 SLP, 10,000 OT and 13,400 PT openings a year, on average.</p>
  {growth_chart()}
  <p class="takeaway">Assistants have the fastest projected growth, but few of them work in schools. SLPs pair strong growth with a large school presence: {school_share(SLP)} of SLPs work in K-12 schools.</p>
  <h3>Who works in schools</h3>
  <p class="small muted">Jobs in K-12 schools, May 2025, and their share of all U.S. jobs in that role.</p>
  <div class="tablewrap"><table>
    <thead><tr><th>Role</th><th class="num">Jobs in K-12 schools</th><th class="num">Share of the role</th></tr></thead>
    <tbody>{share_rows}</tbody>
  </table></div>
</section>

<section class="page">
  <span class="eyebrow">What to do</span>
  <h2>Five ways to use this in your next contract</h2>
  <ol class="tips">
    <li><b>Get the contract days in writing.</b> Divide the pay by the days. That's the number to compare, not the annual figure.</li>
    <li><b>Ask what the rate covers.</b> Evaluations, IEP meetings and paperwork can be paid differently from direct service. Find out before you sign.</li>
    <li><b>Pick your floor before the first call.</b> Start from the K-12 median for your role, then adjust for your state, your years of experience and your credentials.</li>
    <li><b>Count more than the rate.</b> Benefits, license fees, CEUs and travel time can change what an offer is really worth.</li>
    <li><b>Compare onsite and teletherapy separately.</b> Ask about caseload, schedule and equipment for each one.</li>
  </ol>
</section>

<section class="cta">
  <h2>Looking for your next school role?</h2>
  <p>MedPoint Partners places school therapists on contract, onsite or by teletherapy. See what's open now, or join the <a href="{GUIDE['group']}">School Therapist Network on LinkedIn</a> to compare notes with other school therapists. Group members get a free 30-second video intro.</p>
  <a class="go" href="{esc(JOB_BOARD)}">See open school jobs &rarr;</a>
</section>

<section>
  <span class="eyebrow">Method and sources</span>
  <p class="small">K-12 figures are the BLS estimates for Elementary and Secondary Schools. "School and career counselors" is the BLS group Educational, Guidance, and Career Counselors and Advisors, which includes college and career advisors. Pay ranges cover all settings. National job counts leave out the self-employed.</p>
  <p class="small">The Occupational Outlook Handbook also reports a wider "educational services" group that includes colleges, so its figures can differ a little from the K-12 figures here. For SLPs it shows {money(83120)}.</p>
  <ul class="sources small">
    <li>BLS Occupational Employment and Wage Statistics, May 2025: national, Elementary and Secondary Schools, and Georgia.</li>
    <li>BLS Occupational Outlook Handbook, job outlook 2025 to 2035.</li>
  </ul>
  <p class="small muted">MedPoint Partners &middot; medpointpartners.com &middot; &copy; 2026</p>
</section>

</div>"""


def page(title, body, extra=""):
    return ("<!doctype html><html lang='en'><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width, initial-scale=1'>"
            f"<title>{esc(title)}</title>{extra}<link href='{FONTS}' rel='stylesheet'>"
            f"<style>{CSS}</style></head><body>{body}</body></html>")


def og_image(path):
    """1200 x 630, the picture LinkedIn shows when the landing page link is shared."""
    body = f"""
<div style="position:relative;width:1200px;height:630px;overflow:hidden;background:linear-gradient(150deg,#0B1F3D 0%,#136B99 100%);color:#fff;padding:96px 64px;font-family:var(--font)">
  <span class="lsg"><img src="{LOGO}" alt="MedPoint Partners"></span>
  <div style="margin-top:38px;font-size:22px;font-weight:800;letter-spacing:.16em;color:#6FC5D4">SALARY GUIDE 2026</div>
  <h1 style="font-size:92px;font-weight:700;margin-top:14px">School Therapists</h1>
  <p style="font-size:32px;color:#DCE7F7;margin-top:24px;max-width:none">{money(SLP['k12'])} median K-12 pay for an SLP. Free download.</p>
</div>"""
    html_file = path.with_suffix(".tmp.html")
    html_file.write_text(page("og", body, "<style>html,body{width:1200px;height:630px;overflow:hidden;background:#0B1F3D}</style>"), encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--window-size=1200,630",
                    "--virtual-time-budget=8000", f"--screenshot={path}", html_file.as_uri()],
                   check=True, capture_output=True, timeout=120)
    html_file.unlink()


def main():
    (ROOT / "downloads").mkdir(exist_ok=True)
    web = ROOT / "downloads" / GUIDE["web"]
    web.write_text(page("Salary Guide 2026: School Therapists | MedPoint Partners", build(),
                        "<meta name='robots' content='noindex'>"), encoding="utf-8")
    pdf = ROOT / "downloads" / GUIDE["pdf"]
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=8000",
                    f"--print-to-pdf={pdf}", web.as_uri()], check=True, capture_output=True, timeout=180)
    doc = pymupdf.open(pdf)
    doc[0].get_pixmap(dpi=80).save(ROOT / "img" / GUIDE["cover"])
    og_image(ROOT / "img" / GUIDE["og"])
    print(pdf.name, f"{pdf.stat().st_size // 1024} KB, {doc.page_count} pages")
    if doc.page_count != GUIDE["pages"]:
        print(f"Update GUIDE['pages'] in school_pay.py: the landing page says {GUIDE['pages']}.")


if __name__ == "__main__":
    main()
