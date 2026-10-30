"""School therapist pay and job outlook: the numbers behind the salary guide.

tools/make_salary_guide.py (the PDF) and tools/build_pages.py (salary-guide.html) both
read this file, so the two can't disagree.

Wages are BLS Occupational Employment and Wage Statistics, May 2025, checked against the
BLS public API on 2026-10-30. Series are OEUN0000000<industry><soc><type> for the U.S.
(industry 000000 = all, 611100 = Elementary and Secondary Schools) and
OEUS1300000000000<soc><type> for Georgia; types 01 employment, 08 hourly median,
11 / 13 / 15 annual 10th percentile / median / 90th percentile.
Growth is the Occupational Outlook Handbook, 2025-35, read from bls.gov on 2026-10-30.
"""

PAY = [
    {"role": "Speech-language pathologists", "short": "SLPs", "soc": "29-1127",
     "all": 97870, "p10": 62900, "p90": 134160, "k12": 83080, "k12_hour": 39.94,
     "ga": 96760, "k12_jobs": 72130, "all_jobs": 183390, "growth": 17},
    {"role": "Occupational therapists", "short": "OTs", "soc": "29-1122",
     "all": 100330, "p10": 71690, "p90": 131950, "k12": 85610, "k12_hour": 41.16,
     "ga": 104010, "k12_jobs": 20390, "all_jobs": 162450, "growth": 15},
    {"role": "Physical therapists", "short": "PTs", "soc": "29-1123",
     "all": 102760, "p10": 77140, "p90": 135140, "k12": 96080, "k12_hour": 46.19,
     "ga": 102700, "k12_jobs": 6650, "all_jobs": 267330, "growth": 12},
    {"role": "School psychologists", "short": "School psychologists", "soc": "19-3034",
     "all": 95990, "p10": 63070, "p90": 142330, "k12": 94120, "k12_hour": 45.25,
     "ga": 99110, "k12_jobs": 53670, "all_jobs": 63940, "growth": 1},
    {"role": "School and career counselors", "short": "Counselors", "soc": "21-1012",
     "all": 64330, "p10": 45020, "p90": 104770, "k12": 76760, "k12_hour": 36.91,
     "ga": 63720, "k12_jobs": 173950, "all_jobs": 353310, "growth": 3},
    {"role": "Child, family and school social workers", "short": "Social workers", "soc": "21-1021",
     "all": 59550, "p10": 42280, "p90": 95530, "k12": 69620, "k12_hour": 33.47,
     "ga": 47510, "k12_jobs": 64500, "all_jobs": 392550, "growth": 4},
    {"role": "OT assistants", "short": "OT assistants", "soc": "31-2011",
     "all": 72300, "p10": 51490, "p90": 89780, "k12": 60110, "k12_hour": 28.90,
     "ga": 75920, "k12_jobs": 2840, "all_jobs": 51290, "growth": 21},
    {"role": "PT assistants", "short": "PT assistants", "soc": "31-2021",
     "all": 68380, "p10": 47750, "p90": 89510, "k12": 61050, "k12_hour": 29.35,
     "ga": 72800, "k12_jobs": 590, "all_jobs": 112430, "growth": 23},
]

GUIDE = {
    "pdf": "MedPoint-Partners-Salary-Guide-2026-School-Therapists.pdf",
    "web": "medpoint-salary-guide-school-therapists.html",
    "cover": "medpoint-school-therapists-cover.png",
    "og": "salary-guide-og.png",
    "pages": 5,
    "group": "https://www.linkedin.com/groups/42843404/",
}


def money(n):
    return f"${n:,.0f}"


def gap(row):
    """School pay against the all-settings median, signed the way a reader says it."""
    d = row["k12"] - row["all"]
    return ("+" if d > 0 else "−") + money(abs(d))


def school_share(row):
    share = row["k12_jobs"] / row["all_jobs"] * 100
    return "under 1%" if share < 1 else f"{share:.0f}%"
