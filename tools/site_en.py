"""English version of the scholarship directory under /en/ (the data itself is in English)."""
import html

from build_preview import CONTINENTS, COUNTRIES, is_watch, load_rows
import site_extra

E = html.escape
TYPE_EN = {"government": "Government", "eu": "European Union", "consortium": "Consortium", "public": "Public university",
           "private": "Private university", "international": "International organisation"}
NAV_EN = [("/en/deadlines/", "Upcoming deadlines"), ("/en/scholarships/", "All scholarships"), ("/en/guides/", "Guides"), ("/en/about/", "About")]


def nav_en(current="", bn_path="/"):
    cur = ' aria-current="page"'
    links = "".join(f'<a href="{h}"{cur if h == current else ""}>{t}</a>' for h, t in NAV_EN)
    return (f'<nav class="topnav" aria-label="Menu"><a class="brand" href="/en/">Higher Study Info</a>'
            '<form class="gsearch" role="search" action="/search/" method="get"><input type="search" name="q" autocomplete="off" '
            'placeholder="Search scholarships, countries, guides…" aria-label="Search the site"><ul hidden></ul></form><script src="/search.js" defer></script>'
            f'<span class="links">{links}<a href="{bn_path}" lang="bn" hreflang="bn">বাংলা</a></span></nav>')


def footer_en():
    regions = "".join(f'<li><a href="/en/{k}/">{v[0]}</a></li>' for k, v in CONTINENTS.items())
    return (f'<footer class="sitefoot"><nav class="fcols" aria-label="Site links">'
            f'<div><h4>Regions</h4><ul>{regions}</ul></div>'
            f'<div><h4>Directory</h4><ul><li><a href="/en/scholarships/">All scholarships (A–Z)</a></li><li><a href="/en/deadlines/">Upcoming deadlines</a></li>'
            f'<li><a href="/deadlines.ics">Deadline calendar (.ics)</a></li><li><a href="/en/about/">About this site</a></li></ul></div>'
            f'<div><h4>Guides</h4><ul><li><a href="/en/guides/visa/">Student visas</a></li><li><a href="/en/guides/funded-phd/">Funded PhD</a></li>'
            f'<li><a href="/en/guides/fraud/">Avoiding fraud</a></li><li><a href="/en/guides/faq/">FAQ</a></li><li><a href="/guides/" lang="bn">More guides (Bangla)</a></li></ul></div></nav>'
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
            ("Level", E(r["level"])), ("Funding", f'<span class="ftag f-{E(r.get("funding_type", "unknown"))}">{site_extra.FUND_EN.get(r.get("funding_type", "unknown"), "")}</span>'),
            ("Subjects", E(r.get("fields", ""))), ("Benefits", E(r["coverage_amount"])), ("Eligibility", E(r.get("eligibility", ""))),
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


# ---- English guides (translations of the Bangla guides; same official sources) ----
VISA_EN = {
    "Germany": ("At least €11,904 a year in a blocked account (€992 a month can be withdrawn) — or a scholarship, bank guarantee or formal obligation letter",
                "140 full or 280 half days a year without Federal Employment Agency approval; student-assistant jobs at the university are extra",
                "Non-EU graduates of German universities get a job-seeker residence permit of up to 18 months (not renewable); any job allowed meanwhile, living costs must be covered; switch to a work permit (e.g. EU Blue Card) once employed", ""),
    "United Kingdom": ("£1,483 a month in London or £1,136 outside London (up to 9 months) + remaining first-year tuition; held for 28 consecutive days",
                       "20 hours a week in term for full-time degree-level courses; full time in vacations",
                       "Graduate visa: 2 years if applying by 31 Dec 2026, 18 months from 1 Jan 2027; 3 years after a PhD", "£558 when applying from outside the UK (check gov.uk for the current fee)"),
    "United States": ("No fixed national amount — show the total cost stated on your I-20", "On campus, up to 20 hours a week while classes are in session",
                      "OPT: up to 12 months per higher degree level; +24 months STEM OPT for degrees on the DHS STEM list with an E-Verify employer; unemployment limit 90 days (150 with STEM)", "Visa (MRV) fee $185 + SEVIS I-901 fee $350"),
    "Canada": ("Single applicant: CAD 22,895 for living costs (from 1 Sep 2025) + first-year tuition + travel", "Off campus up to 24 hours a week in term; unlimited in scheduled breaks",
               "PGWP: up to 3 years after a programme of 2+ years; programme length for 8 months–2 years; 3 years after a master's of at least 8 months; PGWP-eligible institution, apply within 180 days, once in a lifetime", ""),
    "Australia": ("AUD 29,710 for 12 months' living costs + first-year course fees + travel; or annual income of at least AUD 60,000",
                  "48 hours per fortnight while the course is in session; unlimited in breaks; no limit for research master's and PhD students once the course starts",
                  "Temporary Graduate visa (subclass 485): 18 months to 3 years depending on the qualification", ""),
    "Italy": ("€10,179.85 a year (about €848 a month); some consulates also ask for return-travel funds (about €500)",
              "Up to 20 hours a week and 1,040 hours a year; more during breaks if the annual cap is respected",
              "Job-search permit (ricerca di lavoro) of 9–12 months without the 20-hour limit; convert to a work permit once employed", ""),
    "Japan": ("", "With permission, 28 hours a week (8 hours a day in long vacations); permission can be obtained at the airport",
              "If no job yet: Designated Activities status for job hunting, 6 months, usually renewable once (a second year under conditions); school recommendation letter needed", ""),
    "South Korea": ("At least KRW 900,000 a month × 6 months ≈ KRW 5,400,000", "With permission, about 30 hours a week (UG) or 35 (PG) — sources differ; Korean proficiency usually required",
                    "D-10-1 job-seeker visa for professional jobs (E-1–E-7 types); internships allowed; no financial proof on a first change from D-2", ""),
    "Malaysia": ("", "20 hours a week at approved places — EMGS says only in breaks of more than 7 days, Immigration says also during studies; ask the institution", "",
                 "Student Pass RM60 a year + visa fee (by nationality, up to RM50) + EMGS processing fee"),
    "France": ("At least €877.50 a month from 1 Aug 2026 (previously €615), excluding tuition, for the whole stay", "964 hours a year (about 20 hours a week), counted annually",
               "After a master's or equivalent: 12-month APS / job-search permit (usually not renewable); which one applies depends on nationality — ask the prefecture",
               "Visa fee €50 (per Campus France USA; may differ by country) + Campus France and VFS/TLS fees"),
    "Netherlands": ("IND study norm for university/hbo: €1,130.77 a month in 2026 (changes every 1 January); usually 12 months deposited with the university",
                    "Up to 16 hours a week, or full time only in June–August (not both in one year); employer needs a TWV work permit from UWV",
                    "Orientation year: 1 year to look for work within 3 years of graduating in the Netherlands, no work permit needed; not renewable; fee €254 (2026)", ""),
    "Ireland": ("€10,000 immediately available per year (€833 a month for 6–8-month courses); 6 months of bank statements; credit cards not accepted; pay at least €6,000 of fees (or all fees if lower) before applying",
                "20 hours a week in term; 40 hours in holidays (June–September and 15 Dec–15 Jan)",
                "Stamp 1G (Third Level Graduate Programme): full-time work, no business; length depends on degree level (up to 12 months at level 8)", ""),
    "Türkiye": ("", "A student residence permit does not allow work — a separate work permit is needed", "", ""),
    "Hungary": ("", "Up to 30 hours a week in study periods; full time for up to 90 days a year outside them (Act XC of 2023)",
                "Residence permit to seek work or start a business after graduating — apply while the study permit is still valid", ""),
}


def _en_guide(h1, lede, inner, sources, bn_path):
    src = "".join(f'<li><a href="{E(u)}" target="_blank" rel="noopener">{E(t)}</a></li>' for t, u in sources)
    return f"""<div class="wrap">
{nav_en("", bn_path)}
<nav class="crumbs"><a href="/en/">Home</a> / <a href="/en/guides/">Guides</a></nav>
<article class="prose" style="max-width:100%">
  <span class="eyebrow">Guide · sources checked {site_extra.GUIDES_CHECKED}</span>
  <h1>{h1}</h1>
  <div style="max-width:72ch;display:flex;flex-direction:column;gap:14px">
  <p class="lede">{lede}</p>
  {inner}
  </div>
  {f'<h2>Sources</h2><ul class="src-list">{src}</ul>' if src else ""}
</article>
{footer_en()}
</div>"""


EN_GUIDES = [("/en/guides/visa/", "Student visas by country", "Funds to show, work rules and post-study options in 14 countries."),
             ("/en/guides/funded-phd/", "Funded PhD — TA, RA and salaried PhD", "Assistantships in the US and Canada, minimum funding policies and salaried PhD posts in Europe."),
             ("/en/guides/fraud/", "Avoiding fraud", "Fake admission letters, forged documents and dishonest agents — warning signs from government sources."),
             ("/en/guides/faq/", "Frequently asked questions", "Studying without IELTS, low CGPA, study gaps, age limits, bank balance, agents and more.")]


def guides_index_en():
    cards = "".join(f'<a class="card" href="{h}"><h2>{E(t)}</h2><span class="meta">{E(d)}</span></a>' for h, t, d in EN_GUIDES)
    return f"""<div class="wrap">
{nav_en("", "/guides/")}
<nav class="crumbs"><a href="/en/">Home</a></nav>
<header style="display:flex;flex-direction:column;gap:10px"><span class="eyebrow">Higher Study Info · Guides</span><h1>Guides</h1>
<p class="lede">Practical guides for applying abroad, with links to official sources. More guides are available in Bangla: <a href="/guides/" lang="bn">গাইড ও টুল</a>.</p></header>
<div class="guides">{cards}</div>
{footer_en()}
</div>"""


def _en_visa_name(t):
    import re as _re
    t = t.split(" — ")[0]
    return _re.sub(r"\s*\([^)]*[\u0980-\u09ff][^)]*\)", "", t).strip()


def visa_en():
    blocks = []
    for v in site_extra.VISA:
        f, w, p, fee = VISA_EN.get(v["c"], ("", "", "", ""))
        rows = "".join(f"<tr><th>{k}</th><td>{E(x)}</td></tr>" for k, x in [("Visa", _en_visa_name(v["visa"])),
                                                                             ("Funds to show", f), ("Work while studying", w), ("After graduation", p), ("Visa fee", fee)] if x)
        src = " · ".join(f'<a href="{E(u)}" target="_blank" rel="noopener">{E(t)}</a>' for t, u in v["src"])
        blocks.append(f'<section class="vcard" id="{site_extra.VISA_IDS[v["c"]]}"><h2>{E(v["c"])}</h2><div class="tbl-wrap"><table class="t">{rows}</table></div>'
                      f'<p class="vlinks"><a class="apply" href="{E(v["apply"][1])}" target="_blank" rel="noopener">{E(v["apply"][0])} ↗</a></p><p class="vsrc">Sources: {src}</p></section>')
    toc = " · ".join(f'<a href="#{site_extra.VISA_IDS[v["c"]]}">{E(v["c"])}</a>' for v in site_extra.VISA)
    return _en_guide("Student visas by country",
                     "How much money you must show, how many hours you may work while studying, and what you can do after graduating — from each government's official pages. Fields left out were not stated in the official sources. Rules change often: check the source links before applying.",
                     f"<p>{toc}</p>{''.join(blocks)}", [], "/guides/visa/")


def funded_phd_en():
    return _en_guide("Funded PhD — TA, RA and salaried PhD",
        "Besides scholarships, the biggest way to pay for a PhD is university funding: teaching and research assistantships and minimum funding packages in the US and Canada, and salaried PhD positions in northern Europe. Often no separate scholarship application is needed — funding comes with admission.",
        """<h2>Terms</h2>
  <ul><li><b>Teaching Assistantship (TA):</b> tuition waiver + stipend in return for teaching labs or tutorials and grading.</li>
  <li><b>Research Assistantship (RA):</b> tuition waiver + stipend, usually from the supervisor's research grant, for work on their project — often your own PhD research.</li>
  <li><b>Fellowship:</b> a stipend that usually requires no work in return.</li>
  <li><b>Salaried PhD (Europe):</b> an employment contract with salary, leave and pension.</li></ul>
  <h2>United States</h2>
  <ul><li>Assistantships are very common at PhD level; competition is strong and funding is larger in STEM and research-based fields (EducationUSA).</li>
  <li>Stipends vary by university — for example, Rice University says its doctoral and thesis master's students often receive US$23,400–40,000 a year.</li>
  <li>Professors often decide who receives funding in their department, so contact them early. Some funding deadlines are up to 18 months before the start date.</li></ul>
  <h2>Canada — minimum funding policies</h2>
  <ul><li><b>UBC:</b> CA$40,000 a year for the first four years of a PhD from September 2026, for domestic and international students, subject to satisfactory progress.</li>
  <li><b>University of Waterloo:</b> CA$29,145 a year (from 1 May 2026) for up to four years, plus an International Doctoral Student Award roughly equal to the international–domestic tuition difference.</li>
  <li><b>McGill Biomedical Engineering (one department):</b> stipend CA$25,000 a year; total minimum including tuition CA$44,163 for an international PhD1 student (2026–27).</li></ul>
  <h2>Europe — the PhD is a job</h2>
  <ul><li><b>Sweden:</b> doctoral students are both students and university employees, with salary and benefits (Study in Sweden).</li>
  <li><b>Netherlands:</b> salaries follow the universities' collective agreement — e.g. one Radboud University vacancy offered €3,059 gross a month rising to €3,881 in year four.</li>
  <li><b>Norway:</b> e.g. a 2024 NTNU vacancy paid from NOK 532,200 gross a year.</li>
  <li><b>Denmark:</b> university PhD salaries follow the AC agreement (Study in Denmark).</li>
  <li>Positions are advertised like jobs — search <a href="https://euraxess.ec.europa.eu/jobs/search" target="_blank" rel="noopener">EURAXESS Jobs</a> and university vacancy pages.</li></ul>""",
        [("EducationUSA — Graduate funding", "https://educationusa.state.gov/your-5-steps-us-study/finance-your-studies/graduate"),
         ("UBC — Minimum funding policy", "https://www.grad.ubc.ca/awards/minimum-funding-policy-phd-students"),
         ("University of Waterloo — Funding for research-based programs", "https://uwaterloo.ca/future-graduate-students/funding/funding-research-based-graduate-programs"),
         ("McGill — Biomedical Engineering funding", "https://www.mcgill.ca/bbme/programs/funding"),
         ("Study in Sweden — PhD programmes", "https://studyinsweden.se/plan-your-studies/degree-programmes/phd-programmes/"),
         ("Study in Denmark — PhD and research", "https://studyindenmark.dk/study-options/what-can-i-study/phd-and-research")], "/guides/funded-phd/")


def fraud_en():
    return _en_guide("Avoiding fraud — agents, fake admissions and visas",
        "Fake admission letters, forged documents and \"guaranteed visa\" offers are a real risk. Canada's immigration authorities examined more than 2,000 cases of fake admission letters from 2023. Even if an agent prepares your application, you are responsible for everything in it.",
        """<h2>Warning signs</h2>
  <ul><li>Being told to apply for a visa before you have an admission letter, or offered an admission letter for a fee (IRCC).</li>
  <li>Being asked to pay tuition to an agent instead of the university. Agents should not hold your money or pay on your behalf (British Council).</li>
  <li>"100% visa guarantee" — only the embassy or immigration authority decides.</li>
  <li>Offers to "prepare" bank statements, certificates or experience letters. Forged documents lead to refusal and long bans — up to 5 years in Canada, possibly permanent in the US.</li>
  <li>Being asked to hand over your application-portal or email password.</li></ul>
  <h2>Protect yourself</h2>
  <ul><li>Have the university send the admission letter directly to you; verify it through the address on the university's official website.</li>
  <li>Pay tuition only to the institution, through legal banking channels.</li>
  <li>Keep control of your portal, visa and email accounts; read every document before it is submitted.</li></ul>
  <h2>If you use an agent, ask (British Council)</h2>
  <ul><li>How are you paid — commission from universities? What do you charge me, for which services?</li>
  <li>Which institutions do you officially represent, and do you get incentives to recommend some?</li>
  <li>Are your counsellors trained or certified? What is your complaints process?</li>
  <li>Can I speak to students you have placed before?</li></ul>""",
        [("Government of Canada (IRCC) — International student fraud", "https://www.canada.ca/en/immigration-refugees-citizenship/services/protect-fraud/study-permit-fraud.html"),
         ("British Council — Student and parent guide to choosing an education agent", "https://www.britishcouncil.org/sites/default/files/student_and_parent_guide_to_choosing_an_education_agent.pdf"),
         ("U.S. Embassy in Bangladesh — Supporting documents", "https://bd.usembassy.gov/supporting-documents/")], "/guides/fraud/")


FAQ_EN = [
    ("Can I study abroad or get a scholarship without IELTS?", 'In some cases. Many universities accept a Medium of Instruction letter if your previous degree was taught in English, and some accept Duolingo or TOEFL. The Commonwealth Shared Scholarship itself does not require IELTS, and Malaysia\'s MIS accepts an English-taught degree.'),
    ("Can I get a scholarship with a low CGPA?", 'Many scholarships set a minimum (e.g. 3.00 for an MIS master\'s); many do not state one. Use the <a href="/tools/eligibility/" lang="bn">eligibility checker</a> and explain weak results briefly in your statement of purpose.'),
    ("What if I have a study gap?", 'Rules differ. Some scholarships set limits — DAAD EPOS requires a bachelor\'s degree no older than 6 years — while others (e.g. the Swedish Institute) require work experience. Explain what you did during the gap.'),
    ("Are there age limits?", 'Some scholarships have them: Türkiye Scholarships (master\'s under 30, PhD under 35), France Eiffel (master\'s 29, PhD 35), MIS (master\'s 40, PhD 45). Check the eligibility row on each scholarship page.'),
    ("How much money must I show for the visa?", 'It depends on the country — e.g. €11,904 a year in a German blocked account, AUD 29,710 plus course fees for Australia. See <a href="/en/guides/visa/">Student visas by country</a>.'),
    ("How can I study without paying tuition?", 'Three routes: full government scholarships (<a href="/en/scholarships/">all scholarships</a>), tuition-free countries such as Germany or Norway, and university funding for a PhD (<a href="/en/guides/funded-phd/">Funded PhD</a>).'),
    ("Can I apply without an agent?", 'Yes. Most universities and government scholarships accept online applications directly, and every scholarship on this site links to the official application. If you use an agent, read <a href="/en/guides/fraud/">Avoiding fraud</a> first.'),
    ("Can part-time work pay for my studies?", 'Not fully. Work hours are capped (e.g. 20 hours a week in term in the UK, 1,040 hours a year in Italy), and visa funds must be shown separately.'),
    ("Do I need to contact a professor before a PhD application?", 'In many countries yes — especially the UK, Europe, Australia, and for RA funding in the US. Some DAAD scholarships require a supervisor\'s consent. Use the <a href="/professors/" lang="bn">professor search</a>.'),
    ("How reliable is this site and how often is it updated?", f'Everything comes from official websites — governments, embassies, universities or scholarship providers — with a source link on every entry. The list is updated weekly and expired calls are removed. Spotted a mistake? Email <a href="mailto:{site_extra.EMAIL}">{site_extra.EMAIL}</a>.'),
]


def faq_en():
    import json as _j, re as _re
    items = "".join(f'<details class="faq"><summary>{E(q)}</summary><p>{a}</p></details>' for q, a in FAQ_EN)
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": _re.sub(r"<[^>]+>", "", a)}} for q, a in FAQ_EN]}
    script = '<script type="application/ld+json">' + _j.dumps(ld, ensure_ascii=False).replace("</", "<\\/") + "</script>"
    css = ('<style>.faq{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:12px 16px}.faq summary{cursor:pointer;font-weight:600;font-size:17px}'
           '.faq p{margin:10px 0 0}.faq a{color:var(--accent)}.faqs{display:flex;flex-direction:column;gap:10px}</style>')
    return css + _en_guide("Frequently asked questions", "The questions students from Bangladesh ask most about studying abroad — with links to detailed guides and official sources.",
                           f'<div class="faqs">{items}</div>', [], "/guides/faq/") + script
