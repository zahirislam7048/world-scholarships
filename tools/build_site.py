"""Build the static website (higherstudyinfo.com) into site/.

Usage: python3 tools/build_site.py [YYYY-MM-DD]

Every page gets tools/site_head.html (Google verification + Analytics) in <head>.
"""
import datetime
import html
import json
import pathlib
import shutil
import sys
import urllib.parse

from build_preview import CONTINENTS, COUNTRIES, ROOT, is_watch, load_rows, page_slugs, render
import site_extra
from site_extra import (FOOTER, GUIDE_CSS, NAV_CSS, PAGE_CSS, about_body, budget_body, cgpa_body, deadlines_body,
                        documents_body, english_tests_body, guides_index_body, nav, privacy_body, search_body,
                        tuition_body, visa_body, sop_body, motivation_body, OUTLINE_CSS, professors_body, eligibility_body,
                        lor_body, proposal_body, prof_email_body,
                        LINK_CSS, country_links, scholarship_links, scholarships_index_body,
                        funded_phd_body, part_time_body, interview_body, student_file_body, pre_departure_body, other_tests_body, fraud_body, faq_body, post_study_body)

DOMAIN = "https://higherstudyinfo.com"
OUT = ROOT / "site"
BASE_CSS = "body{margin:0}img{max-width:100%}[hidden]{display:none!important}"


def jsonld(*objs):
    return "".join('<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False).replace("</", "<\\/") + "</script>" for o in objs)


def crumbs_ld(items):
    """items: [(name, path)] -> BreadcrumbList."""
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": DOMAIN + p} for i, (n, p) in enumerate(items)]}


def page(title, description, path, head_extra, body, ld=""):
    return f"""<!doctype html>
<html lang="bn">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="canonical" href="{DOMAIN}{path}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{DOMAIN}{path}">
<meta property="og:site_name" content="Higher Study Info">
<meta property="og:locale" content="bn_BD">
<meta property="og:image" content="{DOMAIN}/og.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="theme-color" content="#0b6b4a">
{ld}
{(ROOT / "tools" / "site_head.html").read_text(encoding="utf-8").strip()}
<style>{BASE_CSS}</style>
{head_extra}
</head>
<body>
{body}
</body>
</html>
"""


PAGES = {}


def country_page(slug, updated):
    frag = render(slug, site_extra.CHECKED, PAGES)
    head, body = frag.split('<div class="wrap">', 1)
    # <title> and the claude-only meta come from page(); keep fonts and styles.
    head = "\n".join(l for l in head.splitlines() if not l.startswith(("<title>", '<meta name="claude:')))
    cont = slug.split("/")[0]
    crumbs = f'<nav class="crumbs"><a href="/">হোম</a> / <a href="/{cont}/">{CONTINENTS[cont][1]}</a></nav>'
    body = '<div class="wrap">\n' + nav() + crumbs + body
    # The repo-maintenance footer is for the preview pages only.
    start = body.index("<footer>")
    body = body[:start] + country_links(slug) + FOOTER + body[body.index("</footer>") + 9:]
    head += "\n" + NAV_CSS + LINK_CSS + "\n<style>.crumbs a{color:var(--accent);text-decoration:none;font-size:14px}.crumbs a:hover{text-decoration:underline}</style>"
    name_en, title, heading = COUNTRIES[slug]
    desc = f"{heading}: এখন চালু আছে বা সামনে আসছে এমন স্কলারশিপ, শেষ তারিখ আর অফিসিয়াল সোর্স লিংকসহ।"
    ld = jsonld(crumbs_ld([("হোম", "/"), (CONTINENTS[cont][1], f"/{cont}/"), (name_en, f"/{slug}/")]))
    return page(f"{title} | Higher Study Info", desc, f"/{slug}/", head, body, ld)


def card(slug, updated):
    name_en, title, heading = COUNTRIES[slug]
    rows = load_rows(slug)
    watch = sum(map(is_watch, rows))
    rows = [r for r in rows if not is_watch(r)]
    upcoming = sorted(r["deadline"] for r in rows if r.get("deadline") and r["deadline"] >= updated)
    nxt = f"পরের শেষ তারিখ: {upcoming[0]}" if upcoming else "নিয়মিত চালু স্কলারশিপ"
    return f"""<a class="card" href="/{slug}/">
  <span class="eyebrow">{html.escape(name_en)}</span>
  <h2>{html.escape(heading)}</h2>
  <span class="meta"><b>{len(rows)}</b> স্কলারশিপ · {html.escape(nxt) if rows else ""}{f" · {watch}টি পরের রাউন্ডের অপেক্ষায়" if watch else ""}</span>
</a>"""


LIST_HEAD = """<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anek+Bangla:wght@500;700&family=Hind+Siliguri:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{--bg:#f5f7f4;--surface:#fff;--fg:#17211b;--muted:#5b6a61;--line:#dde4de;--accent:#0b6b4a;--accent-soft:#e3f1ea;
  --display:"Anek Bangla","Hind Siliguri",system-ui,sans-serif;--body:"Hind Siliguri","Anek Bangla",system-ui,sans-serif;--mono:"IBM Plex Mono",ui-monospace,Menlo,monospace}
@media (prefers-color-scheme:dark){:root{--bg:#0f1512;--surface:#161e1a;--fg:#e6ede8;--muted:#97a69d;--line:#26322b;--accent:#4fc394;--accent-soft:#173226;color-scheme:dark}}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--fg);font-family:var(--body);font-size:16px;line-height:1.55;
  padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.wrap{max-width:1080px;margin:0 auto;padding-block:40px 56px;display:flex;flex-direction:column;gap:28px}
h1{font-family:var(--display);font-weight:700;font-size:clamp(30px,6vw,46px);line-height:1.1;margin:0;text-wrap:balance}
.lede{color:var(--muted);max-width:62ch;margin:0}
.hero{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:20px 32px}
.hero-text{display:flex;flex-direction:column;gap:10px;flex:1 1 420px;min-width:0}
.total{flex:0 0 auto;display:flex;flex-direction:column;gap:2px;padding:16px 22px;background:var(--surface);border:1px solid var(--line);border-radius:10px}
.total b{font-family:var(--display);font-weight:700;font-size:clamp(40px,7vw,56px);line-height:1;color:var(--accent);font-variant-numeric:tabular-nums}
.total>span{font-size:15px;font-weight:600}
.total ul{list-style:none;margin:8px 0 0;padding:8px 0 0;border-top:1px solid var(--line);display:flex;flex-direction:column;gap:2px;font-size:13px;color:var(--muted)}
.total strong{color:var(--fg);font-variant-numeric:tabular-nums}
.continent{display:flex;flex-direction:column;gap:12px}
.continent h3{font-family:var(--display);font-weight:700;font-size:24px;margin:0;display:flex;align-items:baseline;gap:10px}
.continent h3 a{color:inherit;text-decoration:none}.continent h3 a:hover{color:var(--accent)}
.continent h3 small{font-family:var(--body);font-weight:400;font-size:14px;color:var(--muted)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,300px),1fr));gap:14px}
.card{display:flex;flex-direction:column;gap:8px;padding:18px 20px;background:var(--surface);border:1px solid var(--line);border-radius:10px;color:inherit;text-decoration:none}
.card:hover,.card:focus-visible{border-color:var(--accent);outline:none}
.eyebrow{font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
h2{font-family:var(--display);font-weight:500;font-size:20px;line-height:1.3;margin:0}
.meta{font-size:14px;color:var(--muted)} .meta b{color:var(--accent);font-variant-numeric:tabular-nums}
.crumbs a{color:var(--accent);text-decoration:none;font-size:14px}.crumbs a:hover{text-decoration:underline}
.notice{font-size:14px;color:var(--muted);border-top:1px solid var(--line);padding-top:16px;margin:0}
</style>""" + NAV_CSS + PAGE_CSS
NOTICE = '<p class="notice">তথ্য অফিসিয়াল সাইট থেকে সংগ্রহ করা, তবে আবেদনের আগে প্রতিটি স্কলারশিপের সোর্স লিংক খুলে টাকা, শর্ত আর শেষ তারিখ মিলিয়ে নিন।</p>'


def slugs_in(cont):
    return [s for s in COUNTRIES if s.startswith(cont + "/")]


def home_page(updated):
    sections = []
    for cont, (en, bn, _) in CONTINENTS.items():
        cards = "\n".join(card(s, updated) for s in slugs_in(cont))
        sections.append(f"""<section class="continent">
<h3><a href="/{cont}/">{bn}</a><small>{len(slugs_in(cont))}টি দেশ/প্রোগ্রাম</small></h3>
<div class="grid">
{cards}
</div>
</section>""")
    all_rows = [r for s in COUNTRIES for r in load_rows(s)]
    watch = sum(map(is_watch, all_rows))
    all_rows = [r for r in all_rows if not is_watch(r)]
    upcoming = sum(1 for r in all_rows if r.get("deadline") and r["deadline"] >= updated)
    body = f"""<div class="wrap">
{nav("/")}
<header class="hero">
  <div class="hero-text">
    <span class="eyebrow">Higher Study Info · সর্বশেষ যাচাই {site_extra.CHECKED}</span>
    <h1>দেশভিত্তিক স্কলারশিপের তালিকা</h1>
    <p class="lede">প্রতিটি দেশে এখন চালু আছে বা সামনে আসছে এমন স্কলারশিপ, শেষ তারিখ আর প্রতিষ্ঠানের অফিসিয়াল সাইটের লিংক। মেয়াদ পেরোনো স্কলারশিপ বাদ দেওয়া হয়, তালিকা প্রতি সপ্তাহে আপডেট হয়।</p>
    <p style="margin:0;font-weight:600"><a href="/tools/eligibility/" style="color:var(--accent)">✅ কোনগুলোতে আপনি যোগ্য, দেখুন →</a> · <a href="/deadlines/" style="color:var(--accent)">📅 শেষ তারিখ ক্যালেন্ডারে নিন →</a> · <a href="/scholarships/" style="color:var(--accent)">📋 সব স্কলারশিপের তালিকা →</a></p>
  </div>
  <aside class="total" aria-label="মোট স্কলারশিপ">
    <b>{len(all_rows)}</b>
    <span>মোট স্কলারশিপ</span>
    <ul>
      <li><strong>{len(COUNTRIES)}</strong> দেশ/প্রোগ্রাম</li>
      <li><strong>{upcoming}</strong>টির শেষ তারিখ সামনে</li>
      <li><strong>{watch}</strong>টি পরের রাউন্ডের অপেক্ষায়</li>
    </ul>
  </aside>
</header>
{chr(10).join(sections)}
{NOTICE}
{FOOTER}
</div>"""
    ld = jsonld({"@context": "https://schema.org", "@type": "WebSite", "name": "Higher Study Info", "url": DOMAIN + "/",
                 "inLanguage": "bn", "potentialAction": {"@type": "SearchAction", "target": DOMAIN + "/search/?q={search_term_string}",
                                                         "query-input": "required name=search_term_string"}},
                {"@context": "https://schema.org", "@type": "Organization", "name": "Higher Study Info", "url": DOMAIN + "/",
                 "logo": DOMAIN + "/apple-touch-icon.png", "email": site_extra.EMAIL})
    return page("Higher Study Info | দেশভিত্তিক স্কলারশিপ", "এশিয়া, GCC, ইউরোপ, আমেরিকা, ওশেনিয়া ও আফ্রিকার দেশভিত্তিক চালু ও আসন্ন স্কলারশিপের তালিকা, শেষ তারিখ আর অফিসিয়াল সোর্স লিংকসহ।", "/", LIST_HEAD, body, ld)


def continent_page(cont, updated):
    en, bn, bn_of = CONTINENTS[cont]
    cards = "\n".join(card(s, updated) for s in slugs_in(cont))
    body = f"""<div class="wrap">
{nav()}
<nav class="crumbs"><a href="/">হোম</a></nav>
<header style="display:flex;flex-direction:column;gap:10px">
  <span class="eyebrow">{en} · সর্বশেষ যাচাই {site_extra.CHECKED}</span>
  <h1>{bn_of} স্কলারশিপ</h1>
</header>
<div class="grid">
{cards}
</div>
{NOTICE}
{FOOTER}
</div>"""
    return page(f"{bn_of} স্কলারশিপ | Higher Study Info", f"{bn_of} দেশগুলোতে এখন চালু ও আসন্ন স্কলারশিপের তালিকা।", f"/{cont}/", LIST_HEAD, body)


def _ics_text(t):
    return t.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def _fold(line):
    """RFC 5545: lines longer than 75 octets continue on the next line after a space."""
    b, out = line.encode("utf-8"), []
    while len(b) > (74 if out else 75):
        cut = 74 if out else 75
        while cut and (b[cut] & 0xC0) == 0x80:
            cut -= 1
        out.append(b[:cut].decode("utf-8"))
        b = b[cut:]
    out.append(b.decode("utf-8"))
    return "\r\n ".join(out)


def ics(events, name):
    """events: [(row, page path)] with a deadline -> an iCalendar file with 7-day and 1-day reminders."""
    stamp = site_extra.CHECKED.replace("-", "") + "T000000Z"  # stable between builds, so unchanged files aren't recommitted
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Higher Study Info//Scholarship deadlines//BN",
             "CALSCALE:GREGORIAN", "METHOD:PUBLISH", f"X-WR-CALNAME:{_ics_text(name)}", "X-PUBLISHED-TTL:PT12H"]
    for r, path in events:
        d = datetime.date.fromisoformat(r["deadline"])
        url = DOMAIN + path
        summary = f"শেষ তারিখ: {r['scholarship_name']} ({COUNTRIES[r['_slug']][0]})"
        lines += ["BEGIN:VEVENT", f"UID:{path.strip('/').replace('/', '-')}-{d:%Y%m%d}@higherstudyinfo.com", f"DTSTAMP:{stamp}",
                  f"DTSTART;VALUE=DATE:{d:%Y%m%d}", f"DTEND;VALUE=DATE:{d + datetime.timedelta(days=1):%Y%m%d}",
                  f"SUMMARY:{_ics_text(summary)}", f"URL:{url}",
                  f"DESCRIPTION:{_ics_text('আবেদনের আগে অফিসিয়াল পেজে শেষ তারিখ আর সময় অঞ্চল মিলিয়ে নিন: ' + url)}"]
        for trig, label in (("-P7D", "৭ দিন বাকি"), ("-P1D", "কাল শেষ তারিখ")):
            lines += ["BEGIN:VALARM", "ACTION:DISPLAY", f"TRIGGER:{trig}", f"DESCRIPTION:{_ics_text(label + ' — ' + r['scholarship_name'])}", "END:VALARM"]
        lines.append("END:VEVENT")
    lines.append("END:VCALENDAR")
    return "\r\n".join(_fold(l) for l in lines) + "\r\n"


def gcal_link(r, path):
    d = datetime.date.fromisoformat(r["deadline"])
    q = {"action": "TEMPLATE", "text": f"শেষ তারিখ: {r['scholarship_name']}",
         "dates": f"{d:%Y%m%d}/{d + datetime.timedelta(days=1):%Y%m%d}", "details": DOMAIN + path}
    return "https://calendar.google.com/calendar/render?" + urllib.parse.urlencode(q)


TYPE_BN = {"government": "সরকারি", "eu": "ইউরোপীয় ইউনিয়ন", "consortium": "কনসোর্টিয়াম", "public": "পাবলিক বিশ্ববিদ্যালয়",
           "private": "প্রাইভেট বিশ্ববিদ্যালয়", "international": "আন্তর্জাতিক সংস্থা"}


def scholarship_page(slug, i, r, updated):
    e = html.escape
    name_en, title, heading = COUNTRIES[slug]
    cont = slug.split("/")[0]
    path = f"/scholarship/{PAGES[(slug, i)]}/"
    watch = is_watch(r)
    apply_url = r.get("apply_url") or r["source_url"]
    direct = apply_url != r["source_url"] and not watch
    rows = [("প্রতিষ্ঠান", e(r["provider"]) + f' <span class="meta">({TYPE_BN.get(r["provider_type"], e(r["provider_type"]))})</span>'),
            ("দেশ", f'<a href="/{slug}/">{e(name_en)}</a>'), ("লেভেল", e(r["level"])), ("সুবিধা", e(r["coverage_amount"])),
            ("শর্ত", e(r.get("eligibility", ""))),
            ("IELTS / English", e(r.get("english_requirement", "")) + (f' <a href="{e(r["english_source"])}" target="_blank" rel="noopener">সূত্র ↗</a>' if r.get("english_source") else "")),
            ("সেশন", e(r.get("session_year", "")))]
    cal = ""
    if r.get("deadline"):
        rows.append(("শেষ তারিখ", f'<b class="dl" data-d="{e(r["deadline"])}">{e(r["deadline"])}</b> <span id="left" class="meta"></span>'))
        cal = (f'<p class="vlinks cal" id="cal">📅 শেষ তারিখ মনে রাখুন: <a href="{e(gcal_link(r, path))}" target="_blank" rel="noopener">Google Calendar-এ যোগ করুন</a>'
               f' · <a href="deadline.ics" download>ফোন/Outlook ক্যালেন্ডার (.ics)</a> <span class="meta">— ৭ দিন ও ১ দিন আগে রিমাইন্ডার</span></p>')
    if r.get("notes"):
        rows.append(("নোট", e(r["notes"])))
    table = "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in rows if v)
    others = [(j, o) for j, o in enumerate(load_rows(slug)) if j != i and (slug, j) in PAGES]
    related = "".join(f'<li><a href="/scholarship/{PAGES[(slug, j)]}/">{e(o["scholarship_name"])}</a> <span class="meta">· {e(o["level"])}</span></li>' for j, o in others)
    related = f'<section class="rel"><h2>{e(heading)} — আরও স্কলারশিপ</h2><ul>{related}</ul></section>' if related else ""
    badge = '<p class="warn">⏳ <b>পরের রাউন্ডের অপেক্ষায়</b> — নতুন রাউন্ড এখনো ঘোষণা হয়নি। নিচের তথ্য আগের রাউন্ডের; ঘোষণা হলে এখানে হালনাগাদ হবে।</p>' if watch else ""
    desc = f"{r['scholarship_name']} ({name_en}): {r['level']} লেভেলের স্কলারশিপ — সুবিধা, শর্ত, IELTS, শেষ তারিখ আর অফিসিয়াল আবেদনের লিংক।"
    body = f"""<div class="wrap">
{nav()}
<nav class="crumbs"><a href="/">হোম</a> / <a href="/{cont}/">{CONTINENTS[cont][1]}</a> / <a href="/{slug}/">{e(name_en)}</a></nav>
<article class="vcard" style="max-width:820px">
  <span class="eyebrow">{e(name_en)} · {e(r["provider"])} · সর্বশেষ যাচাই {site_extra.CHECKED}</span>
  <h1 style="font-size:clamp(26px,5vw,38px)">{e(r["scholarship_name"])}</h1>
  {badge}
  <p id="expired" class="warn" hidden>এই রাউন্ডের শেষ তারিখ পেরিয়ে গেছে। পরের সাপ্তাহিক আপডেটে তালিকা থেকে সরানো হবে।</p>
  <div class="tbl-wrap"><table class="t">{table}</table></div>
  {cal}
  <p class="vlinks"><a class="apply" href="{e(apply_url)}" target="_blank" rel="noopener">{"আবেদন করুন ↗" if direct else "অফিসিয়াল পেজ ↗"}</a></p>
  <p class="vsrc">সূত্র: <a href="{e(r["source_url"])}" target="_blank" rel="noopener">{e(r["source_domain"])}</a> · সংগ্রহ {e(r.get("collected_on", ""))}। "Not stated in source snippet" মানে সূত্রে এ তথ্য পাওয়া যায়নি — অফিসিয়াল পেজে মিলিয়ে নিন।</p>
</article>
{related}
{scholarship_links(slug, i, r)}
{NOTICE}
{FOOTER}
</div>
<script>
(function(){{var el=document.querySelector(".dl");if(!el)return;var t=new Date();t.setHours(0,0,0,0);
var d=new Date(el.dataset.d+"T00:00:00"),n=Math.round((d-t)/864e5),bn=function(x){{return String(x).replace(/\\d/g,function(c){{return "০১২৩৪৫৬৭৮৯"[c]}})}};
if(n<0){{document.getElementById("expired").hidden=false;document.getElementById("cal").hidden=true}}else{{document.getElementById("left").textContent="(আর "+bn(n)+" দিন)"}}}})();
</script>"""
    ld = jsonld(crumbs_ld([("হোম", "/"), (CONTINENTS[cont][1], f"/{cont}/"), (name_en, f"/{slug}/"), (r["scholarship_name"], path)]))
    return page(f"{r['scholarship_name']} — {name_en} | Higher Study Info", desc, path, LIST_HEAD + GUIDE_CSS + LINK_CSS, body, ld)


def redirect_page(target):
    return f"""<!doctype html>
<html lang="bn"><head><meta charset="utf-8"><title>Moved</title>
<link rel="canonical" href="{DOMAIN}{target}"><meta http-equiv="refresh" content="0; url={target}">
</head><body><a href="{target}">{DOMAIN}{target}</a></body></html>
"""


# Pages that moved when the site was grouped by continent.
REDIRECTS = {
    "bangladesh": "/asia/bangladesh/", "italy": "/europe/italy/", "erasmus-mundus": "/europe/erasmus-mundus/",
    "asia/saudi-arabia": "/gcc/saudi-arabia/", "asia/uae": "/gcc/uae/", "asia/qatar": "/gcc/qatar/",
}


def main():
    # `updated` is today's date: deadlines before it are dropped. The date shown on the
    # pages is when the data was last checked (data/LAST_CHECKED, written by the weekly update).
    updated = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
    site_extra.CHECKED = (ROOT / "data" / "LAST_CHECKED").read_text(encoding="utf-8").strip()
    shutil.rmtree(OUT, ignore_errors=True)
    OUT.mkdir()
    for f in (ROOT / "tools" / "static").iterdir():
        shutil.copy(f, OUT / f.name)
    PAGES.update((k, v) for k, v in page_slugs().items()
                 if not (load_rows(k[0])[k[1]].get("deadline") or "9999") < updated)
    site_extra.PAGES = PAGES
    for (slug, i), ps in PAGES.items():
        (OUT / "scholarship" / ps).mkdir(parents=True)
        (OUT / "scholarship" / ps / "index.html").write_text(scholarship_page(slug, i, load_rows(slug)[i], updated), encoding="utf-8")
        r = load_rows(slug)[i]
        if r.get("deadline"):
            (OUT / "scholarship" / ps / "deadline.ics").write_bytes(ics([({**r, "_slug": slug}, f"/scholarship/{ps}/")], r["scholarship_name"]).encode("utf-8"))
    upcoming = sorted(((({**load_rows(sl)[i], "_slug": sl}), f"/scholarship/{ps}/") for (sl, i), ps in PAGES.items()
                       if load_rows(sl)[i].get("deadline")), key=lambda x: x[0]["deadline"])
    (OUT / "deadlines.ics").write_bytes(ics(upcoming, "স্কলারশিপের শেষ তারিখ — Higher Study Info").encode("utf-8"))
    (OUT / "index.html").write_text(home_page(updated), encoding="utf-8")
    for cont in CONTINENTS:
        (OUT / cont).mkdir()
        (OUT / cont / "index.html").write_text(continent_page(cont, updated), encoding="utf-8")
    for slug in COUNTRIES:
        (OUT / slug).mkdir(parents=True)
        (OUT / slug / "index.html").write_text(country_page(slug, updated), encoding="utf-8")
    extra = {
        "deadlines": ("শেষ তারিখ সামনে | Higher Study Info", "সব দেশের স্কলারশিপ শেষ তারিখ অনুযায়ী সাজানো, আবেদনের লিংকসহ।", deadlines_body),
        "search": ("সব স্কলারশিপ খুঁজুন | Higher Study Info", "সব দেশের স্কলারশিপ এক জায়গায় খুঁজুন: দেশ, লেভেল, IELTS আর শেষ তারিখ দিয়ে।", search_body),
        "about": ("আমাদের সম্পর্কে | Higher Study Info", "Higher Study Info কী, তথ্য কোথা থেকে আসে আর কীভাবে আপডেট হয়।", about_body),
        "privacy": ("Privacy Policy | Higher Study Info", "higherstudyinfo.com-এর Privacy Policy: Google Analytics ও কুকি।", privacy_body),
        "guides": ("গাইড ও টুল | Higher Study Info", "উচ্চশিক্ষার আবেদনের গাইড ও টুল: সত্যায়ন, IELTS, CGPA রূপান্তর।", guides_index_body),
        "guides/documents": ("কাগজপত্র ও সত্যায়ন | Higher Study Info", "বিদেশে উচ্চশিক্ষার জন্য বাংলাদেশি সার্টিফিকেট সত্যায়ন, e-Apostille আর পুলিশ ক্লিয়ারেন্স — ধাপে ধাপে।", documents_body),
        "guides/english-tests": ("IELTS, TOEFL, Duolingo, PTE | Higher Study Info", "বাংলাদেশে IELTS, TOEFL, Duolingo, PTE-র ফি ও বুকিং, আর IELTS ছাড়ের পথ আছে এমন স্কলারশিপ।", english_tests_body),
        "tools/cgpa": ("CGPA রূপান্তর | Higher Study Info", "বাংলাদেশের CGPA থেকে জার্মান গ্রেড (modified Bavarian formula) রূপান্তর।", cgpa_body),
        "guides/visa": ("স্টুডেন্ট ভিসা — দেশভিত্তিক | Higher Study Info", "জার্মানি, যুক্তরাজ্য, যুক্তরাষ্ট্র, কানাডা, অস্ট্রেলিয়া, ইতালি, জাপান, কোরিয়া, মালয়েশিয়ার স্টুডেন্ট ভিসায় কত টাকা দেখাতে হয় ও কাজের নিয়ম।", visa_body),
        "guides/tuition-free": ("টিউশন-ফ্রি ও কম খরচের দেশ | Higher Study Info", "জার্মানি, অস্ট্রিয়া, ফ্রান্স, নরওয়েতে EU-র বাইরের শিক্ষার্থীদের টিউশন — অফিসিয়াল সূত্রে।", tuition_body),
        "guides/sop": ("Statement of Purpose (SOP) লেখার গাইড | Higher Study Info", "SOP-এর কাঠামো, দৈর্ঘ্য, ভুলগুলো আর আউটলাইন বানানোর টুল — বিশ্ববিদ্যালয়ের অফিসিয়াল নির্দেশনা অনুযায়ী।", sop_body),
        "guides/motivation-letter": ("Motivation Letter লেখার গাইড | Higher Study Info", "DAAD ও ইউরোপীয় স্কলারশিপের Motivation Letter: প্রশ্ন, কাঠামো, দৈর্ঘ্য আর আউটলাইন টুল।", motivation_body),
        "professors": ("প্রফেসর সার্চ — বিষয় ও ডিপার্টমেন্ট অনুযায়ী | Higher Study Info", "MS/PhD সুপারভাইজার খুঁজুন: বিশ্ববিদ্যালয়, ডিপার্টমেন্ট ও গবেষণার বিষয় অনুযায়ী প্রফেসরদের তালিকা, অফিসিয়াল প্রোফাইল লিংকসহ।", professors_body),
        "tools/eligibility": ("কোন স্কলারশিপে আমি যোগ্য? | Higher Study Info", "লেভেল, IELTS, বয়স আর CGPA দিয়ে দেখুন কোন স্কলারশিপের শর্তের সাথে আপনি মেলেন।", eligibility_body),
        "guides/lor": ("Recommendation Letter (LOR) গাইড | Higher Study Info", "রেকমেন্ডেশন লেটার কাকে, কখন, কীভাবে চাইবেন — বিশ্ববিদ্যালয়ের অফিসিয়াল নির্দেশনা অনুযায়ী।", lor_body),
        "guides/research-proposal": ("Research Proposal লেখার গাইড | Higher Study Info", "PhD ও DAAD গবেষণা স্কলারশিপের Research Proposal: কাঠামো, দৈর্ঘ্য, পদ্ধতি ও সময়সূচি।", proposal_body),
        "guides/professor-email": ("প্রফেসরকে ইমেইল করার নিয়ম | Higher Study Info", "PhD সুপারভাইজারকে ইমেইল: কাঠামো, কী সংযুক্ত করবেন, কখন ফলো-আপ — বিশ্ববিদ্যালয়ের নির্দেশনা অনুযায়ী।", prof_email_body),
        "scholarships": ("সব স্কলারশিপের তালিকা (A–Z) | Higher Study Info", "অঞ্চল ও দেশ অনুযায়ী সাজানো সব চালু ও আসন্ন স্কলারশিপের তালিকা, প্রতিটির আলাদা পেজসহ।", scholarships_index_body),
        "guides/funded-phd": ("ফান্ডেড PhD — TA, RA ও বেতনভুক্ত PhD | Higher Study Info", "যুক্তরাষ্ট্র ও কানাডায় Teaching/Research Assistantship, ন্যূনতম PhD ফান্ডিং আর ইউরোপে বেতনসহ PhD পদ — অফিসিয়াল সূত্রে।", funded_phd_body),
        "guides/part-time-work": ("পড়ার সময় পার্ট-টাইম কাজ — দেশভিত্তিক নিয়ম | Higher Study Info", "জার্মানি, যুক্তরাজ্য, যুক্তরাষ্ট্র, কানাডা, অস্ট্রেলিয়া, ইতালি, ফ্রান্স, জাপান, কোরিয়া, মালয়েশিয়ায় স্টুডেন্ট ভিসায় কত ঘণ্টা কাজ করা যায়।", part_time_body),
        "guides/interview": ("ভিসা ও স্কলারশিপ ইন্টারভিউর প্রস্তুতি | Higher Study Info", "Chevening-ধরনের স্কলারশিপ ইন্টারভিউ আর ঢাকায় US F-1 স্টুডেন্ট ভিসা ইন্টারভিউ: কী সাথে নেবেন, কী জিজ্ঞেস করা হয়।", interview_body),
        "guides/student-file": ("স্টুডেন্ট ফাইল ও বিদেশে টাকা পাঠানো | Higher Study Info", "বাংলাদেশ ব্যাংকের নিয়মে স্টুডেন্ট ফাইল খুলে টিউশন ফি ও জীবনযাত্রার খরচ বিদেশে পাঠানোর নিয়ম।", student_file_body),
        "guides/pre-departure": ("বিদেশে যাওয়ার আগের চেকলিস্ট | Higher Study Info", "ভিসা পাওয়ার পর থেকে পৌঁছানো পর্যন্ত কাগজ, টাকা, স্বাস্থ্য ও যাত্রার টিক-দেওয়া চেকলিস্ট।", pre_departure_body),
        "guides/other-tests": ("GRE, GMAT, SAT ও ভাষার পরীক্ষা | Higher Study Info", "GRE, GMAT, SAT-এর ফি ও তারিখ আর বাংলাদেশে Goethe/TestDaF, JLPT, TOPIK পরীক্ষা — অফিসিয়াল সূত্রে।", other_tests_body),
        "guides/fraud": ("প্রতারণা থেকে সাবধান — এজেন্ট, ভুয়া ভর্তি ও ভিসা | Higher Study Info", "বিদেশে পড়ার আবেদনে ভুয়া ভর্তির চিঠি, জাল কাগজ আর অসৎ এজেন্ট চেনার লক্ষণ ও নিজেকে রক্ষার উপায়।", fraud_body),
        "guides/faq": ("বিদেশে উচ্চশিক্ষা — সচরাচর জিজ্ঞাসা (FAQ) | Higher Study Info", "IELTS ছাড়া পড়া, কম CGPA, স্টাডি গ্যাপ, বয়সসীমা, ব্যাংক ব্যালান্স, এজেন্ট, পার্ট-টাইম কাজ — প্রশ্নোত্তর।", faq_body),
        "guides/post-study-work": ("পড়া শেষে কাজের ভিসা — দেশভিত্তিক | Higher Study Info", "জার্মানির ১৮ মাসের চাকরি-খোঁজার পারমিট, কানাডার PGWP, যুক্তরাষ্ট্রের OPT/STEM OPT, অস্ট্রেলিয়ার ৪৮৫, জাপান ও কোরিয়া — সরকারি সূত্রে।", post_study_body),
        "tools/budget": ("বাজেট ক্যালকুলেটর | Higher Study Info", "বিদেশে পড়ার প্রথম বছরের আনুমানিক খরচ আর ভিসার জন্য কত টাকা দেখাতে হবে — হিসাব করুন।", budget_body),
    }
    for name, (title, desc, body_fn) in extra.items():
        (OUT / name).mkdir(parents=True)
        (OUT / name / "index.html").write_text(page(title, desc, f"/{name}/", LIST_HEAD + GUIDE_CSS + OUTLINE_CSS + LINK_CSS, body_fn(updated)), encoding="utf-8")
    for old, target in REDIRECTS.items():
        (OUT / old).mkdir(parents=True)
        (OUT / old / "index.html").write_text(redirect_page(target), encoding="utf-8")
    urls = ["/", "/scholarships/", "/deadlines/", "/search/", "/guides/", "/guides/documents/", "/guides/english-tests/", "/tools/cgpa/", "/guides/visa/", "/guides/tuition-free/", "/tools/budget/", "/guides/sop/", "/guides/motivation-letter/", "/professors/", "/tools/eligibility/", "/guides/lor/", "/guides/research-proposal/", "/guides/professor-email/", "/guides/funded-phd/", "/guides/part-time-work/", "/guides/interview/", "/guides/student-file/", "/guides/pre-departure/", "/guides/other-tests/", "/guides/fraud/", "/guides/faq/", "/guides/post-study-work/", "/about/", "/privacy/"] + [f"/{c}/" for c in CONTINENTS] + [f"/{s}/" for s in COUNTRIES] + [f"/scholarship/{ps}/" for ps in PAGES.values()]
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{DOMAIN}{u}</loc><lastmod>{site_extra.CHECKED}</lastmod></url>\n" for u in urls)
        + "</urlset>\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n", encoding="utf-8")
    print(f"site/ built: {len(urls)} pages")


if __name__ == "__main__":
    main()
