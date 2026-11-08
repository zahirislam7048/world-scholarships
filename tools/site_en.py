"""English version of the scholarship directory under /en/ (the data itself is in English)."""
import html

from build_preview import CONTINENTS, COUNTRIES, is_watch, load_rows
import site_extra

E = html.escape
TYPE_EN = {"government": "Government", "eu": "European Union", "consortium": "Consortium", "public": "Public university",
           "private": "Private university", "international": "International organisation"}
NAV_EN = [("/en/deadlines/", "Upcoming deadlines"), ("/en/scholarships/", "All scholarships"), ("/en/about/", "About")]


def nav_en(current="", bn_path="/"):
    cur = ' aria-current="page"'
    links = "".join(f'<a href="{h}"{cur if h == current else ""}>{t}</a>' for h, t in NAV_EN)
    return (f'<nav class="topnav" aria-label="Menu"><a class="brand" href="/en/">Higher Study Info</a>'
            f'<span class="links">{links}<a href="{bn_path}" lang="bn" hreflang="bn">বাংলা</a></span></nav>')


def footer_en():
    regions = "".join(f'<li><a href="/en/{k}/">{v[0]}</a></li>' for k, v in CONTINENTS.items())
    return (f'<footer class="sitefoot"><nav class="fcols" aria-label="Site links">'
            f'<div><h4>Regions</h4><ul>{regions}</ul></div>'
            f'<div><h4>Directory</h4><ul><li><a href="/en/scholarships/">All scholarships (A–Z)</a></li><li><a href="/en/deadlines/">Upcoming deadlines</a></li>'
            f'<li><a href="/deadlines.ics">Deadline calendar (.ics)</a></li><li><a href="/en/about/">About this site</a></li></ul></div>'
            f'<div><h4>Guides (Bangla)</h4><ul><li><a href="/guides/" lang="bn">গাইড ও টুল</a></li><li><a href="/guides/visa/" lang="bn">স্টুডেন্ট ভিসা</a></li>'
            f'<li><a href="/tools/eligibility/" lang="bn">যোগ্যতা যাচাই</a></li></ul></div></nav>'
            f'<p class="fbase"><a href="/privacy/">Privacy Policy</a> · Contact: <a href="mailto:{site_extra.EMAIL}">{site_extra.EMAIL}</a>'
            f' · Data from official sources, updated weekly</p></footer>')


NOTICE_EN = ('<p class="notice">Information is collected from official websites. Before applying, open each scholarship\'s source link '
             'and confirm the amount, conditions and deadline.</p>')


def _rows(pages, slug):
    return [(i, r, pages[(slug, i)]) for i, r in enumerate(load_rows(slug)) if (slug, i) in pages]


def _item(r, ps, country=False):
    meta = [E(r["provider"]), E(r["level"])]
    if country:
        meta.insert(0, E(COUNTRIES[r["_slug"]][0]))
    if r.get("deadline"):
        meta.append(f'deadline <b>{E(r["deadline"])}</b>')
    badge = ' <span class="meta">· ⏳ next round awaited</span>' if is_watch(r) else ""
    return f'<li><a href="/en/scholarship/{ps}/">{E(r["scholarship_name"])}</a>{badge}<br><span class="meta">{" · ".join(meta)}</span></li>'


def home_en(pages, checked):
    total = sum(1 for (s, i) in pages if not is_watch(load_rows(s)[i]))
    secs = []
    for k, (en, _, _) in CONTINENTS.items():
        cards = []
        for s in COUNTRIES:
            if s.startswith(k + "/"):
                n = sum(1 for i, r, _ in _rows(pages, s) if not is_watch(r))
                cards.append(f'<a class="card" href="/en/{s}/"><h2>{E(COUNTRIES[s][0])}</h2><span class="meta"><b>{n}</b> scholarship{"" if n == 1 else "s"}</span></a>')
        secs.append(f'<section class="continent"><h3><a href="/en/{k}/">{E(en)}</a></h3><div class="grid">{"".join(cards)}</div></section>')
    return f"""<div class="wrap">
{nav_en("/en/", "/")}
<header class="hero">
  <div class="hero-text">
    <span class="eyebrow">Higher Study Info · last checked {checked}</span>
    <h1>Scholarships by country</h1>
    <p class="lede">Current and upcoming scholarships in {len(COUNTRIES)} countries and programmes, with deadlines, English-test requirements and the official application link. Expired calls are removed and the list is updated every week.</p>
  </div>
  <aside class="total" aria-label="Total scholarships"><b>{total}</b><span>scholarships</span></aside>
</header>
{"".join(secs)}
{NOTICE_EN}
{footer_en()}
</div>"""


def continent_en(k, pages, checked):
    en = CONTINENTS[k][0]
    blocks = []
    for s in COUNTRIES:
        if s.startswith(k + "/"):
            items = "".join(_item(r, ps) for i, r, ps in _rows(pages, s))
            blocks.append(f'<h2><a href="/en/{s}/">{E(COUNTRIES[s][0])}</a></h2><ul class="elist">{items or "<li class=meta>No current scholarship listed.</li>"}</ul>')
    return f"""<div class="wrap">
{nav_en("", f"/{k}/")}
<nav class="crumbs"><a href="/en/">Home</a></nav>
<header style="display:flex;flex-direction:column;gap:10px"><span class="eyebrow">{E(en)} · last checked {checked}</span><h1>Scholarships in {E(en)}</h1></header>
<section class="rel">{"".join(blocks)}</section>
{NOTICE_EN}
{footer_en()}
</div>"""


def country_en(s, pages, checked):
    k = s.split("/")[0]
    name = COUNTRIES[s][0]
    cards = []
    for i, r, ps in _rows(pages, s):
        rows = [("Provider", f'{E(r["provider"])} <span class="meta">({TYPE_EN.get(r["provider_type"], "")})</span>'), ("Level", E(r["level"])),
                ("Benefits", E(r["coverage_amount"])), ("English", E(r.get("english_requirement", ""))), ("Session", E(r.get("session_year", ""))),
                ("Deadline", E(r.get("deadline", "")))]
        tbl = "".join(f"<tr><th>{a}</th><td>{b}</td></tr>" for a, b in rows if b)
        badge = '<p class="warn">⏳ Next round awaited — not announced yet.</p>' if is_watch(r) else ""
        cards.append(f'<article class="vcard"><h2><a href="/en/scholarship/{ps}/">{E(r["scholarship_name"])}</a></h2>{badge}'
                     f'<div class="tbl-wrap"><table class="t fit">{tbl}</table></div></article>')
    others = "".join(f'<li><a href="/en/{o}/">{E(COUNTRIES[o][0])}</a></li>' for o in COUNTRIES if o.startswith(k + "/") and o != s)
    return f"""<div class="wrap">
{nav_en("", f"/{s}/")}
<nav class="crumbs"><a href="/en/">Home</a> / <a href="/en/{k}/">{E(CONTINENTS[k][0])}</a></nav>
<header style="display:flex;flex-direction:column;gap:10px"><span class="eyebrow">{E(name)} · last checked {checked}</span><h1>Scholarships in {E(name)}</h1></header>
<div style="display:flex;flex-direction:column;gap:14px;max-width:820px">{"".join(cards) or '<p class="empty">No current scholarship listed for this country.</p>'}</div>
<section class="rel"><h2>Other countries in {E(CONTINENTS[k][0])}</h2><ul class="tags">{others}</ul></section>
{NOTICE_EN}
{footer_en()}
</div>"""


def scholarship_en(s, i, r, ps, checked):
    k = s.split("/")[0]
    name = COUNTRIES[s][0]
    apply_url = r.get("apply_url") or r["source_url"]
    direct = apply_url != r["source_url"] and not is_watch(r)
    rows = [("Provider", f'{E(r["provider"])} <span class="meta">({TYPE_EN.get(r["provider_type"], "")})</span>'), ("Country", f'<a href="/en/{s}/">{E(name)}</a>'),
            ("Level", E(r["level"])), ("Benefits", E(r["coverage_amount"])), ("Eligibility", E(r.get("eligibility", ""))),
            ("English", E(r.get("english_requirement", "")) + (f' <a href="{E(r["english_source"])}" target="_blank" rel="noopener">source ↗</a>' if r.get("english_source") else "")),
            ("Session", E(r.get("session_year", ""))),
            ("Deadline", f'<b class="dl" data-d="{E(r["deadline"])}">{E(r["deadline"])}</b> <span id="left" class="meta"></span>' if r.get("deadline") else ""),
            ("Notes", E(r.get("notes", "")))]
    tbl = "".join(f"<tr><th>{a}</th><td>{b}</td></tr>" for a, b in rows if b)
    cal = (f'<p class="vlinks" id="cal">📅 <a href="/scholarship/{ps}/deadline.ics" download>Add the deadline to your calendar (.ics)</a> '
           f'<span class="meta">— reminders 7 days and 1 day before</span></p>') if r.get("deadline") else ""
    badge = '<p class="warn">⏳ <b>Next round awaited</b> — the new round has not been announced; details below are from the previous round.</p>' if is_watch(r) else ""
    sib = "".join(f'<li><a href="/en/scholarship/{p2}/">{E(o["scholarship_name"])}</a> <span class="meta">· {E(o["level"])}</span></li>'
                  for j, o, p2 in _rows(site_extra.PAGES, s) if j != i)
    return f"""<div class="wrap">
{nav_en("", f"/scholarship/{ps}/")}
<nav class="crumbs"><a href="/en/">Home</a> / <a href="/en/{k}/">{E(CONTINENTS[k][0])}</a> / <a href="/en/{s}/">{E(name)}</a></nav>
<article class="vcard" style="max-width:820px">
  <span class="eyebrow">{E(name)} · {E(r["provider"])} · last checked {checked}</span>
  <h1 style="font-size:clamp(26px,5vw,38px)">{E(r["scholarship_name"])}</h1>
  {badge}
  <p id="expired" class="warn" hidden>The deadline for this round has passed; it will be removed in the next weekly update.</p>
  <div class="tbl-wrap"><table class="t">{tbl}</table></div>
  {cal}
  <p class="vlinks"><a class="apply" href="{E(apply_url)}" target="_blank" rel="noopener">{"Apply ↗" if direct else "Official page ↗"}</a></p>
  <p class="vsrc">{site_extra.report_link(r["scholarship_name"], f"/en/scholarship/{ps}/", "en")}</p>
  <p class="vsrc">Source: <a href="{E(r["source_url"])}" target="_blank" rel="noopener">{E(r["source_domain"])}</a> · collected {E(r.get("collected_on", ""))}. "Not stated in source snippet" means the source did not state it — check the official page.</p>
</article>
{f'<section class="rel"><h2>More scholarships in {E(name)}</h2><ul>{sib}</ul></section>' if sib else ""}
{NOTICE_EN}
{footer_en()}
</div>
<script>
(function(){{var el=document.querySelector(".dl");if(!el)return;var t=new Date();t.setHours(0,0,0,0);
var n=Math.round((new Date(el.dataset.d+"T00:00:00")-t)/864e5);
if(n<0){{document.getElementById("expired").hidden=false;var c=document.getElementById("cal");if(c)c.hidden=true}}else{{document.getElementById("left").textContent="("+n+" days left)"}}}})();
</script>"""


def index_en(pages, checked):
    parts = []
    for k, (en, _, _) in CONTINENTS.items():
        blocks = []
        for s in COUNTRIES:
            if s.startswith(k + "/"):
                rows = _rows(pages, s)
                if rows:
                    blocks.append(f'<h3><a href="/en/{s}/">{E(COUNTRIES[s][0])}</a></h3><ul>' + "".join(
                        f'<li><a href="/en/scholarship/{ps}/">{E(r["scholarship_name"])}</a></li>' for i, r, ps in rows) + "</ul>")
        parts.append(f'<h2><a href="/en/{k}/">{E(en)}</a></h2>' + "".join(blocks))
    return f"""<div class="wrap">
{nav_en("/en/scholarships/", "/scholarships/")}
<nav class="crumbs"><a href="/en/">Home</a></nav>
<header style="display:flex;flex-direction:column;gap:10px"><span class="eyebrow">last checked {checked}</span><h1>All scholarships (A–Z)</h1>
<p class="lede">{len(pages)} scholarships grouped by region and country. Sorted by deadline: <a href="/en/deadlines/">upcoming deadlines</a>.</p></header>
<section class="rel">{"".join(parts)}</section>
{footer_en()}
</div>"""


def deadlines_en(pages, updated, checked):
    rows = sorted(((r, ps, s) for (s, i), ps in pages.items() for r in [load_rows(s)[i]] if r.get("deadline") and r["deadline"] >= updated),
                  key=lambda x: x[0]["deadline"])
    items = "".join(f'<li data-d="{E(r["deadline"])}"><span class="when">{E(r["deadline"])} <span class="left meta"></span></span>'
                    f'<a href="/en/scholarship/{ps}/">{E(r["scholarship_name"])}</a> <span class="meta">· <a href="/en/{s}/">{E(COUNTRIES[s][0])}</a> · {E(r["level"])}</span></li>'
                    for r, ps, s in rows)
    return f"""<style>.tl{{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:10px;border-left:3px solid var(--accent);padding-left:14px}}
.tl .when{{display:block;font-family:var(--mono);font-size:13px;color:var(--muted)}}.tl a{{color:var(--accent)}}</style>
<div class="wrap">
{nav_en("/en/deadlines/", "/deadlines/")}
<header style="display:flex;flex-direction:column;gap:10px"><span class="eyebrow">last checked {checked}</span><h1>Upcoming deadlines</h1>
<p class="lede">Scholarships with a known deadline, earliest first. Subscribe to all of them in your calendar: <a href="https://calendar.google.com/calendar/r?cid=webcal%3A%2F%2Fhigherstudyinfo.com%2Fdeadlines.ics" target="_blank" rel="noopener">Google Calendar</a> · <a href="webcal://higherstudyinfo.com/deadlines.ics">iPhone / Outlook</a>.</p></header>
<ol class="tl">{items}</ol>
{NOTICE_EN}
{footer_en()}
</div>
<script>(function(){{var t=new Date();t.setHours(0,0,0,0);document.querySelectorAll(".tl li").forEach(function(li){{var n=Math.round((new Date(li.dataset.d+"T00:00:00")-t)/864e5);
if(n<0){{li.hidden=true;return}}li.querySelector(".left").textContent=n===0?"· closes today":"· "+n+" days left"}})}})();</script>"""


def about_en(checked):
    return f"""<div class="wrap">
{nav_en("/en/about/", "/about/")}
<article class="prose" style="max-width:68ch">
  <h1>About Higher Study Info</h1>
  <p class="lede">Higher Study Info is a free directory of current and upcoming scholarships for students from Bangladesh and beyond, organised by country.</p>
  <ul>
    <li>Every entry comes from an official source — a government, embassy, university or the scholarship provider — and links to it.</li>
    <li>Amounts and conditions are recorded only as the source states them; otherwise the entry says "Not stated in source snippet".</li>
    <li>The list is checked every week (last checked {checked}); expired calls are removed.</li>
    <li>Application guides (visa, documents, SOP, interviews, funding) are currently in Bangla: <a href="/guides/" lang="bn">গাইড ও টুল</a>.</li>
  </ul>
  <p>Spotted a mistake? Email <a href="mailto:{site_extra.EMAIL}">{site_extra.EMAIL}</a>.</p>
</article>
{footer_en()}
</div>"""
