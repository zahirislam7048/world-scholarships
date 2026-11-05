"""Build the static website (higherstudyinfo.com) into site/.

Usage: python3 tools/build_site.py [YYYY-MM-DD]

Every page gets tools/site_head.html (Google verification + Analytics) in <head>.
"""
import datetime
import html
import pathlib
import shutil
import sys

from build_preview import CONTINENTS, COUNTRIES, ROOT, load_rows, render
import site_extra
from site_extra import (FOOTER, GUIDE_CSS, NAV_CSS, PAGE_CSS, about_body, budget_body, cgpa_body, deadlines_body,
                        documents_body, english_tests_body, guides_index_body, nav, privacy_body, search_body,
                        tuition_body, visa_body, sop_body, motivation_body, OUTLINE_CSS, professors_body)

DOMAIN = "https://higherstudyinfo.com"
OUT = ROOT / "site"
BASE_CSS = "body{margin:0}img{max-width:100%}[hidden]{display:none!important}"


def page(title, description, path, head_extra, body):
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
{(ROOT / "tools" / "site_head.html").read_text(encoding="utf-8").strip()}
<style>{BASE_CSS}</style>
{head_extra}
</head>
<body>
{body}
</body>
</html>
"""


def country_page(slug, updated):
    frag = render(slug, site_extra.CHECKED)
    head, body = frag.split('<div class="wrap">', 1)
    # <title> and the claude-only meta come from page(); keep fonts and styles.
    head = "\n".join(l for l in head.splitlines() if not l.startswith(("<title>", '<meta name="claude:')))
    cont = slug.split("/")[0]
    crumbs = f'<nav class="crumbs"><a href="/">হোম</a> / <a href="/{cont}/">{CONTINENTS[cont][1]}</a></nav>'
    body = '<div class="wrap">\n' + nav() + crumbs + body
    # The repo-maintenance footer is for the preview pages only.
    start = body.index("<footer>")
    body = body[:start] + FOOTER + body[body.index("</footer>") + 9:]
    head += "\n" + NAV_CSS + "\n<style>.crumbs a{color:var(--accent);text-decoration:none;font-size:14px}.crumbs a:hover{text-decoration:underline}</style>"
    name_en, title, heading = COUNTRIES[slug]
    desc = f"{heading}: এখন চালু আছে বা সামনে আসছে এমন স্কলারশিপ, শেষ তারিখ আর অফিসিয়াল সোর্স লিংকসহ।"
    return page(f"{title} | Higher Study Info", desc, f"/{slug}/", head, body)


def card(slug, updated):
    name_en, title, heading = COUNTRIES[slug]
    rows = load_rows(slug)
    upcoming = sorted(r["deadline"] for r in rows if r.get("deadline") and r["deadline"] >= updated)
    nxt = f"পরের শেষ তারিখ: {upcoming[0]}" if upcoming else "নিয়মিত চালু স্কলারশিপ"
    return f"""<a class="card" href="/{slug}/">
  <span class="eyebrow">{html.escape(name_en)}</span>
  <h2>{html.escape(heading)}</h2>
  <span class="meta"><b>{len(rows)}</b> স্কলারশিপ · {html.escape(nxt)}</span>
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
    upcoming = sum(1 for r in all_rows if r.get("deadline") and r["deadline"] >= updated)
    body = f"""<div class="wrap">
{nav("/")}
<header class="hero">
  <div class="hero-text">
    <span class="eyebrow">Higher Study Info · সর্বশেষ যাচাই {site_extra.CHECKED}</span>
    <h1>দেশভিত্তিক স্কলারশিপের তালিকা</h1>
    <p class="lede">প্রতিটি দেশে এখন চালু আছে বা সামনে আসছে এমন স্কলারশিপ, শেষ তারিখ আর প্রতিষ্ঠানের অফিসিয়াল সাইটের লিংক। মেয়াদ পেরোনো স্কলারশিপ বাদ দেওয়া হয়, তালিকা প্রতি সপ্তাহে আপডেট হয়।</p>
  </div>
  <aside class="total" aria-label="মোট স্কলারশিপ">
    <b>{len(all_rows)}</b>
    <span>মোট স্কলারশিপ</span>
    <ul>
      <li><strong>{len(COUNTRIES)}</strong> দেশ/প্রোগ্রাম</li>
      <li><strong>{upcoming}</strong>টির শেষ তারিখ সামনে</li>
    </ul>
  </aside>
</header>
{chr(10).join(sections)}
{NOTICE}
{FOOTER}
</div>"""
    return page("Higher Study Info | দেশভিত্তিক স্কলারশিপ", "এশিয়া, GCC, ইউরোপ, আমেরিকা, ওশেনিয়া ও আফ্রিকার দেশভিত্তিক চালু ও আসন্ন স্কলারশিপের তালিকা, শেষ তারিখ আর অফিসিয়াল সোর্স লিংকসহ।", "/", LIST_HEAD, body)


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
        "tools/budget": ("বাজেট ক্যালকুলেটর | Higher Study Info", "বিদেশে পড়ার প্রথম বছরের আনুমানিক খরচ আর ভিসার জন্য কত টাকা দেখাতে হবে — হিসাব করুন।", budget_body),
    }
    for name, (title, desc, body_fn) in extra.items():
        (OUT / name).mkdir(parents=True)
        (OUT / name / "index.html").write_text(page(title, desc, f"/{name}/", LIST_HEAD + GUIDE_CSS + OUTLINE_CSS, body_fn(updated)), encoding="utf-8")
    for old, target in REDIRECTS.items():
        (OUT / old).mkdir(parents=True)
        (OUT / old / "index.html").write_text(redirect_page(target), encoding="utf-8")
    urls = ["/", "/deadlines/", "/search/", "/guides/", "/guides/documents/", "/guides/english-tests/", "/tools/cgpa/", "/guides/visa/", "/guides/tuition-free/", "/tools/budget/", "/guides/sop/", "/guides/motivation-letter/", "/professors/", "/about/", "/privacy/"] + [f"/{c}/" for c in CONTINENTS] + [f"/{s}/" for s in COUNTRIES]
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{DOMAIN}{u}</loc><lastmod>{site_extra.CHECKED}</lastmod></url>\n" for u in urls)
        + "</urlset>\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n", encoding="utf-8")
    print(f"site/ built: {len(urls)} pages")


if __name__ == "__main__":
    main()
