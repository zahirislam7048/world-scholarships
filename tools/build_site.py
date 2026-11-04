"""Build the static website (higherstudyinfo.com) into site/.

Usage: python3 tools/build_site.py [YYYY-MM-DD]

Every page gets tools/site_head.html (Google verification + Analytics) in <head>.
"""
import datetime
import html
import pathlib
import shutil
import sys

from build_preview import COUNTRIES, ROOT, load_rows, render

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
    frag = render(slug, updated)
    head, body = frag.split('<div class="wrap">', 1)
    # <title> and the claude-only meta come from page(); keep fonts and styles.
    head = "\n".join(l for l in head.splitlines() if not l.startswith(("<title>", '<meta name="claude:')))
    nav = '<nav class="crumbs"><a href="/">← সব দেশ</a></nav>'
    body = '<div class="wrap">\n' + nav + body
    # The repo-maintenance footer is for the preview pages only.
    start = body.index("<footer>")
    body = body[:start] + '<footer><a href="/">higherstudyinfo.com</a> · প্রতি সপ্তাহে আপডেট হয়</footer>' + body[body.index("</footer>") + 9:]
    head += "\n<style>.crumbs a{color:var(--accent);text-decoration:none;font-size:14px}.crumbs a:hover{text-decoration:underline}</style>"
    name_en, title, heading = COUNTRIES[slug]
    desc = f"{heading}: এখন চালু আছে বা সামনে আসছে এমন স্কলারশিপ, শেষ তারিখ আর অফিসিয়াল সোর্স লিংকসহ।"
    return page(f"{title} | Higher Study Info", desc, f"/{slug}/", head, body)


def home_page(updated):
    cards = []
    for slug, (name_en, title, heading) in COUNTRIES.items():
        rows = load_rows(slug)
        upcoming = sorted(r["deadline"] for r in rows if r.get("deadline") and r["deadline"] >= updated)
        nxt = f"পরের শেষ তারিখ: {upcoming[0]}" if upcoming else "নিয়মিত চালু স্কলারশিপ"
        cards.append(f"""<a class="card" href="/{slug}/">
  <span class="eyebrow">{html.escape(name_en)}</span>
  <h2>{html.escape(heading)}</h2>
  <span class="meta"><b>{len(rows)}</b> স্কলারশিপ · {html.escape(nxt)}</span>
</a>""")
    head = """<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anek+Bangla:wght@500;700&family=Hind+Siliguri:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
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
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,300px),1fr));gap:14px}
.card{display:flex;flex-direction:column;gap:8px;padding:18px 20px;background:var(--surface);border:1px solid var(--line);border-radius:10px;color:inherit;text-decoration:none}
.card:hover,.card:focus-visible{border-color:var(--accent);outline:none}
.eyebrow{font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
h2{font-family:var(--display);font-weight:500;font-size:20px;line-height:1.3;margin:0}
.meta{font-size:14px;color:var(--muted)} .meta b{color:var(--accent);font-variant-numeric:tabular-nums}
.notice{font-size:14px;color:var(--muted);border-top:1px solid var(--line);padding-top:16px;margin:0}
</style>"""
    body = f"""<div class="wrap">
<header style="display:flex;flex-direction:column;gap:10px">
  <span class="eyebrow">Higher Study Info · সর্বশেষ আপডেট {updated}</span>
  <h1>দেশভিত্তিক স্কলারশিপের তালিকা</h1>
  <p class="lede">প্রতিটি দেশে এখন চালু আছে বা সামনে আসছে এমন স্কলারশিপ, শেষ তারিখ আর প্রতিষ্ঠানের অফিসিয়াল সাইটের লিংক। মেয়াদ পেরোনো স্কলারশিপ বাদ দেওয়া হয়, তালিকা প্রতি সপ্তাহে আপডেট হয়।</p>
</header>
<section class="grid">
{chr(10).join(cards)}
</section>
<p class="notice">তথ্য অফিসিয়াল সাইট থেকে সংগ্রহ করা, তবে আবেদনের আগে প্রতিটি স্কলারশিপের সোর্স লিংক খুলে টাকা, শর্ত আর শেষ তারিখ মিলিয়ে নিন।</p>
</div>"""
    return page("Higher Study Info | দেশভিত্তিক স্কলারশিপ", "বাংলাদেশ, ইতালি ও Erasmus Mundus-সহ দেশভিত্তিক চালু ও আসন্ন স্কলারশিপের তালিকা, শেষ তারিখ আর অফিসিয়াল সোর্স লিংকসহ।", "/", head, body)


def main():
    updated = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
    shutil.rmtree(OUT, ignore_errors=True)
    OUT.mkdir()
    (OUT / "index.html").write_text(home_page(updated), encoding="utf-8")
    for slug in COUNTRIES:
        (OUT / slug).mkdir()
        (OUT / slug / "index.html").write_text(country_page(slug, updated), encoding="utf-8")
    urls = ["/"] + [f"/{s}/" for s in COUNTRIES]
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{DOMAIN}{u}</loc><lastmod>{updated}</lastmod></url>\n" for u in urls)
        + "</urlset>\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n", encoding="utf-8")
    print(f"site/ built: {len(urls)} pages")


if __name__ == "__main__":
    main()
