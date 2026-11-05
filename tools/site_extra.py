"""Site-wide navigation and the cross-country pages: deadlines, search, about, privacy."""
import html
import json
import pathlib
import re

from build_preview import CONTINENTS, COUNTRIES, load_rows

NAV_CSS = """<style>
.topnav{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:8px 20px;padding-block:14px;border-bottom:1px solid var(--line)}
.topnav .brand{font-family:var(--display);font-weight:700;font-size:18px;color:var(--fg);text-decoration:none}
.topnav .links{display:flex;flex-wrap:wrap;gap:4px 18px}
.topnav .links a{color:var(--muted);text-decoration:none;font-size:15px}
.topnav .links a:hover,.topnav .links a[aria-current]{color:var(--accent)}
.sitefoot{font-size:13px;color:var(--muted);border-top:1px solid var(--line);padding-top:14px}
.sitefoot a{color:var(--muted)}
.fcols{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,200px),1fr));gap:12px 24px;margin-bottom:12px}
.fcols h4{font-size:13px;margin:0 0 6px;color:var(--fg)}.fcols ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:4px}
.fbase{margin:0;padding-top:10px;border-top:1px solid var(--line)}
a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
</style>"""

NAV_ITEMS = [("/deadlines/", "শেষ তারিখ সামনে"), ("/search/", "সব স্কলারশিপ খুঁজুন"), ("/guides/", "গাইড ও টুল"), ("/professors/", "প্রফেসর সার্চ"), ("/about/", "আমাদের সম্পর্কে")]


def nav(current=""):
    cur = ' aria-current="page"'
    links = "".join(f'<a href="{href}"{cur if href == current else ""}>{label}</a>' for href, label in NAV_ITEMS)
    return f'<nav class="topnav" aria-label="মেনু"><a class="brand" href="/">Higher Study Info</a><span class="links">{links}<a href="/en/" lang="en" hreflang="en">English</a></span></nav>'


EMAIL = "higherstudyinfo30@gmail.com"
PHONE_DISPLAY = "+880 1644-842785"
PHONE_TEL = "+8801644842785"
CONTACT_HTML = (f'<ul><li>ইমেইল: <a href="mailto:{EMAIL}">{EMAIL}</a></li>'
                f'<li>ফোন: <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li></ul>')

CHECKED = ""  # set by build_site.main from data/LAST_CHECKED
PAGES = {}  # (country slug, row index) -> scholarship page slug; set by build_site.main
GUIDES_CHECKED = "2026-11-04"  # when the guide and tool figures were last verified
PRIVACY_EFFECTIVE = "2026-11-04"

FOOTER_CORE = (f'<p class="fbase"><a href="/about/">আমাদের সম্পর্কে</a> · <a href="/privacy/">Privacy Policy</a>'
               f' · যোগাযোগ: <a href="mailto:{EMAIL}">{EMAIL}</a> · তথ্য অফিসিয়াল সূত্র থেকে, প্রতি সপ্তাহে আপডেট হয়</p>')


def _footer():
    """Site-wide footer hub: every page links to each region, the main tools and the guides."""
    regions = "".join(f'<li><a href="/{k}/">{v[2]} স্কলারশিপ</a></li>' for k, v in CONTINENTS.items())
    tools = ('<li><a href="/scholarships/">সব স্কলারশিপের তালিকা (A–Z)</a></li><li><a href="/deadlines/">শেষ তারিখ সামনে</a></li>'
             '<li><a href="/search/">স্কলারশিপ খুঁজুন</a></li><li><a href="/tools/eligibility/">কোন স্কলারশিপে আমি যোগ্য?</a></li>'
             '<li><a href="/shortlist/">আমার শর্টলিস্ট</a></li><li><a href="/tools/timeline/">টাইমলাইন প্ল্যানার</a></li><li><a href="/professors/">প্রফেসর সার্চ</a></li><li><a href="/tools/cgpa/">CGPA রূপান্তর</a></li><li><a href="/tools/budget/">বাজেট ক্যালকুলেটর</a></li>')
    guides = "".join(f'<li><a href="{h}">{t.split(" ", 1)[1]}</a></li>' for h, t, _ in GUIDES if h.startswith("/guides/"))
    return (f'<footer class="sitefoot"><nav class="fcols" aria-label="সাইটের লিংক">'
            f'<div><h4>অঞ্চলভিত্তিক</h4><ul>{regions}</ul></div><div><h4>টুল</h4><ul>{tools}</ul></div>'
            f'<div><h4>গাইড</h4><ul>{guides}</ul></div></nav>{FOOTER_CORE}</footer>')


BN_MONTHS = ["জানুয়ারি", "ফেব্রুয়ারি", "মার্চ", "এপ্রিল", "মে", "জুন", "জুলাই", "আগস্ট", "সেপ্টেম্বর", "অক্টোবর", "নভেম্বর", "ডিসেম্বর"]
BN_DIGITS = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")


def bn(n):
    return str(n).translate(BN_DIGITS)


def all_rows():
    out = []
    for slug, (name_en, title, heading) in COUNTRIES.items():
        cont = slug.split("/")[0]
        for i, r in enumerate(load_rows(slug)):
            page = PAGES.get((slug, i))
            out.append({**r, "slug": slug, "section": cont, "section_bn": CONTINENTS[cont][1],
                        "page": f"/scholarship/{page}/" if page else f"/{slug}/"})
    return out


PAGE_CSS = """<style>
.month{display:flex;flex-direction:column;gap:8px}
.month h2{font-family:var(--display);font-weight:700;font-size:22px;margin:0}
.dl{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:8px}
.dl li{display:grid;grid-template-columns:72px 1fr auto;gap:4px 14px;align-items:start;padding:12px 16px;background:var(--surface);border:1px solid var(--line);border-radius:10px}
.dl .date{font-family:var(--display);font-weight:700;font-size:15px;line-height:1.2;color:var(--accent);font-variant-numeric:tabular-nums}
.dl .date small{display:block;font-family:var(--body);font-weight:400;font-size:12px;color:var(--muted)}
.dl .what{min-width:0;display:flex;flex-direction:column;gap:2px}
.dl .what a{color:var(--fg);font-weight:600;text-decoration:none}
.dl .what a:hover{color:var(--accent);text-decoration:underline}
.dl .what span{font-size:13px;color:var(--muted);overflow-wrap:anywhere}
.dl .what span a{font-weight:400;color:var(--accent)}
.lede a{color:var(--accent)}
.left{font-size:12px;font-weight:600;white-space:nowrap;padding:2px 9px;border-radius:999px;border:1px solid var(--line);color:var(--muted)}
.left.soon{color:#b3261e;border-color:currentColor}
@media (prefers-color-scheme:dark){.left.soon{color:#ff8a80}}
@media (max-width:520px){.dl li{grid-template-columns:64px 1fr}.dl .left{grid-column:2;justify-self:start}}
.filters{display:flex;flex-wrap:wrap;gap:10px;align-items:center}
.filters input[type=search],.filters select{font:inherit;color:var(--fg);background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:8px 12px;min-width:0}
.filters input[type=search]{flex:1 1 260px}
.filters label{font-size:14px;color:var(--muted);display:flex;gap:6px;align-items:center}
.count{font-size:13px;color:var(--muted)}
.results{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,330px),1fr));gap:12px}
.res{display:flex;flex-direction:column;gap:6px;padding:14px 16px;background:var(--surface);border:1px solid var(--line);border-radius:10px;min-width:0}
.res .where{font-family:var(--mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.res h3{font-family:var(--display);font-weight:500;font-size:17px;line-height:1.3;margin:0}
.res p{margin:0;font-size:14px;color:var(--muted);overflow-wrap:anywhere}
.res p b{color:var(--fg);font-weight:600}
.res .row{display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center;margin-top:4px}
.res .apply{font-weight:600;font-size:14px;text-decoration:none;border-radius:8px;padding:6px 12px;background:var(--accent);color:var(--surface)}
.res .apply.info{background:transparent;color:var(--accent);border:1px solid var(--accent)}
.res .more{font-size:13px;color:var(--accent)}
.empty{color:var(--muted)}
.prose{max-width:68ch;display:flex;flex-direction:column;gap:14px}
.prose h2{font-family:var(--display);font-weight:700;font-size:22px;margin:12px 0 0}
.prose p,.prose li{margin:0;line-height:1.7}
.prose ul{margin:0;padding-left:20px;display:flex;flex-direction:column;gap:6px}
.prose a{color:var(--accent)}
</style>"""


def deadlines_body(updated):
    rows = sorted((r for r in all_rows() if r.get("deadline") and r["deadline"] >= updated), key=lambda r: r["deadline"])
    months, order = {}, []
    for r in rows:
        key = r["deadline"][:7]
        if key not in months:
            months[key] = []
            order.append(key)
        months[key].append(r)
    sections = []
    for key in order:
        y, m = key.split("-")
        items = []
        for r in months[key]:
            d = r["deadline"]
            day = int(d[8:10])
            apply = r.get("apply_url") or r["source_url"]
            name_en = COUNTRIES[r["slug"]][0]
            items.append(f"""<li data-d="{d}">
  <span class="date">{bn(day)} {BN_MONTHS[int(m) - 1]}<small>{bn(y)}</small></span>
  <span class="what"><a href="{r["page"]}">{html.escape(r["scholarship_name"])}</a>
  <span><a href="/{r["slug"]}/">{html.escape(name_en)}</a> · {html.escape(r["provider"])} · {html.escape(r["level"])} · <a href="{html.escape(apply)}" target="_blank" rel="noopener">আবেদন ↗</a></span></span>
  <span class="left"></span>
</li>""")
        sections.append(f"""<section class="month" data-month="{key}">
<h2>{BN_MONTHS[int(m) - 1]} {bn(y)}</h2>
<ul class="dl">
{chr(10).join(items)}
</ul>
</section>""")
    script = """<script>
(function(){
  var bn=function(n){return String(n).replace(/\\d/g,function(d){return "০১২৩৪৫৬৭৮৯"[d]})};
  var t=new Date();var today=new Date(t.getFullYear(),t.getMonth(),t.getDate());
  document.querySelectorAll(".dl li").forEach(function(li){
    var p=li.dataset.d.split("-");var d=new Date(+p[0],p[1]-1,+p[2]);
    var days=Math.round((d-today)/86400000);var badge=li.querySelector(".left");
    if(days<0){li.hidden=true;return}
    badge.textContent=days===0?"আজ শেষ":bn(days)+" দিন বাকি";
    if(days<=14)badge.classList.add("soon");
  });
  document.querySelectorAll(".month").forEach(function(s){
    if(!s.querySelector("li:not([hidden])"))s.hidden=true;
  });
})();
</script>"""
    return f"""<div class="wrap">
{nav("/deadlines/")}
<header style="display:flex;flex-direction:column;gap:10px">
  <span class="eyebrow">সব দেশ · সর্বশেষ যাচাই {CHECKED}</span>
  <h1>শেষ তারিখ সামনে</h1>
  <p class="lede">যেসব স্কলারশিপের শেষ তারিখ জানা আছে, সেগুলো তারিখ অনুযায়ী সাজানো। নাম চাপলে স্কলারশিপের বিস্তারিত পেজ খুলবে। ১৪ দিনের কম বাকি থাকলে লাল চিহ্ন দেখাবে। শেষ তারিখ নেই এমন স্কলারশিপ দেখতে <a href="/search/">সব স্কলারশিপ খুঁজুন</a>।</p>
</header>
<p class="warn">📅 <b>সব শেষ তারিখ নিজের ক্যালেন্ডারে:</b> <a href="https://calendar.google.com/calendar/r?cid=webcal%3A%2F%2Fhigherstudyinfo.com%2Fdeadlines.ics" target="_blank" rel="noopener">Google Calendar-এ সাবস্ক্রাইব</a> · <a href="webcal://higherstudyinfo.com/deadlines.ics">iPhone / Outlook</a> · <a href="/deadlines.ics" download>.ics ফাইল</a>. সাবস্ক্রাইব করলে নতুন স্কলারশিপ যোগ হলে ক্যালেন্ডারও নিজে থেকে হালনাগাদ হবে, আর প্রতিটির ৭ দিন ও ১ দিন আগে রিমাইন্ডার পাবেন।</p>
{chr(10).join(sections) if sections else '<p class="empty">এই মুহূর্তে শেষ তারিখসহ কোনো স্কলারশিপ নেই।</p>'}
<p class="notice">শেষ তারিখ অফিসিয়াল সূত্র থেকে নেওয়া; সময় অঞ্চল আর ভেতরের আগের ডেডলাইন আলাদা হতে পারে। আবেদনের আগে সূত্র মিলিয়ে নিন।</p>
{FOOTER}
</div>
{script}"""


def search_body(updated):
    data = [{
        "n": r["scholarship_name"], "p": r["provider"], "c": COUNTRIES[r["slug"]][0], "s": r["section"],
        "l": r["level"], "cov": r["coverage_amount"], "e": r.get("english_requirement", ""),
        "d": r.get("deadline", ""), "a": r.get("apply_url") or r["source_url"], "src": r["source_url"],
        "u": r["page"], "el": r.get("eligibility", ""), "w": r.get("session_year", "").startswith("Next round"),
    } for r in all_rows()]
    sections = "".join(f'<option value="{k}">{v[1]}</option>' for k, v in CONTINENTS.items())
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    script = """<script>
var DATA = __DATA__;
(function(){
  var esc=function(s){return String(s).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})};
  var bn=function(n){return String(n).replace(/\\d/g,function(d){return "০১২৩৪৫৬৭৮৯"[d]})};
  var t=new Date();var today=t.getFullYear()+"-"+String(t.getMonth()+1).padStart(2,"0")+"-"+String(t.getDate()).padStart(2,"0");
  function lvl(l,f){if(!f)return true;if(f==="UG")return /\\bUG\\b/.test(l);if(f==="PG")return /PG|Masters|MS|MA|MPhil|MSc/.test(l);if(f==="PhD")return /PhD|Postdoc/.test(l);if(f==="School")return /Secondary|HSC|Degree/.test(l);return true}
  var q=document.getElementById("q"),sec=document.getElementById("sec"),lv=document.getElementById("lvl"),dl=document.getElementById("hasdl"),out=document.getElementById("out"),cnt=document.getElementById("cnt");
  function render(){
    var s=q.value.trim().toLowerCase();
    var rows=DATA.filter(function(r){
      if(r.d&&r.d<today)return false;
      if(sec.value&&r.s!==sec.value)return false;
      if(!lvl(r.l,lv.value))return false;
      if(dl.checked&&!(r.d&&r.d>=today))return false;
      return !s||[r.n,r.p,r.c,r.l,r.cov,r.e,r.el].join(" ").toLowerCase().indexOf(s)>=0;
    }).sort(function(a,b){var ka=(a.w?"1":"0")+(a.d&&a.d>=today?a.d:"9999"),kb=(b.w?"1":"0")+(b.d&&b.d>=today?b.d:"9999");return ka<kb?-1:ka>kb?1:0});
    cnt.textContent=bn(rows.length)+"টি স্কলারশিপ";
    if(!rows.length){out.innerHTML='<p class="empty">কিছু পাওয়া যায়নি। অন্য শব্দ দিয়ে খুঁজুন বা ফিল্টার সরান।</p>';return}
    out.innerHTML=rows.map(function(r){
      var info=r.a===r.src||r.w;
      return '<article class="res"><span class="where">'+esc(r.c)+'</span><h3>'+esc(r.n)+'</h3>'+
        '<p>'+esc(r.p)+' · '+esc(r.l)+'</p>'+
        (r.cov?'<p><b>সুবিধা:</b> '+esc(r.cov)+'</p>':'')+
        (r.e?'<p><b>IELTS / English:</b> '+esc(r.e)+'</p>':'')+
        (r.d&&r.d>=today?'<p><b>শেষ তারিখ:</b> '+esc(r.d)+'</p>':'')+(r.w?'<p class="warn">⏳ পরের রাউন্ডের অপেক্ষায় — এখনো ঘোষণা হয়নি</p>':'')+
        '<div class="row"><a class="apply'+(info?' info':'')+'" href="'+esc(r.a)+'" target="_blank" rel="noopener">'+(info?'আবেদনের তথ্য ↗':'আবেদন করুন ↗')+'</a><a class="more" href="'+r.u+'">বিস্তারিত</a></div></article>';
    }).join("");
  }
  [q,sec,lv,dl].forEach(function(el){el.addEventListener("input",render);el.addEventListener("change",render)});
  var h=new URLSearchParams(location.search).get("q");if(h)q.value=h;
  render();
})();
</script>""".replace("__DATA__", payload)
    return f"""<div class="wrap">
{nav("/search/")}
<header style="display:flex;flex-direction:column;gap:10px">
  <span class="eyebrow">সব দেশ · সর্বশেষ যাচাই {CHECKED}</span>
  <h1>সব স্কলারশিপ খুঁজুন</h1>
  <p class="lede">সব দেশের স্কলারশিপ এক জায়গায়। নাম, দেশ, বিশ্ববিদ্যালয়, শর্ত বা IELTS স্কোর লিখে খুঁজুন; অঞ্চল আর লেভেল দিয়ে ছাঁকুন। যেগুলোর শেষ তারিখ আগে, সেগুলো উপরে দেখায়।</p>
</header>
<div class="filters" role="search">
  <input id="q" type="search" placeholder="যেমন: PhD, Germany, IELTS 6.5, fully funded" aria-label="খুঁজুন">
  <select id="sec" aria-label="অঞ্চল"><option value="">সব অঞ্চল</option>{sections}</select>
  <select id="lvl" aria-label="লেভেল"><option value="">সব লেভেল</option><option value="UG">স্নাতক (UG)</option><option value="PG">স্নাতকোত্তর / Master's</option><option value="PhD">PhD / Postdoc</option><option value="School">স্কুল / কলেজ</option></select>
  <label><input id="hasdl" type="checkbox"> শুধু শেষ তারিখ সামনে</label>
  <span class="count" id="cnt"></span>
</div>
<section class="results" id="out"><p class="empty">স্কলারশিপের তালিকা লোড হচ্ছে…</p></section>
<p class="meta">সব স্কলারশিপ একসাথে দেশ অনুযায়ী দেখতে: <a href="/scholarships/">সব স্কলারশিপের তালিকা (A–Z)</a></p>
{FOOTER}
</div>
{script}"""


def about_body(updated):
    total = sum(not r.get("session_year", "").startswith("Next round") for r in all_rows())
    return f"""<div class="wrap">
{nav("/about/")}
<article class="prose">
  <span class="eyebrow">Higher Study Info</span>
  <h1>আমাদের সম্পর্কে</h1>
  <p>Higher Study Info দেশভিত্তিক স্কলারশিপের একটি তালিকা। এখানে শুধু সেই স্কলারশিপ রাখা হয় যেগুলো এখন চালু আছে বা সামনে আবেদন খুলবে; মেয়াদ পেরোলে তা বাদ দেওয়া হয়। বর্তমানে {bn(len(COUNTRIES))}টি দেশ/প্রোগ্রামের {bn(total)}টি স্কলারশিপ আছে।</p>
  <h2>তথ্য কোথা থেকে আসে</h2>
  <ul>
    <li>প্রতিটি তথ্য সরকারি দপ্তর, বিশ্ববিদ্যালয় বা স্কলারশিপ প্রোগ্রামের <b>অফিসিয়াল ওয়েবসাইট</b> থেকে নেওয়া। প্রতিটি কার্ডে সেই সূত্রের লিংক আছে।</li>
    <li>এগ্রিগেটর বা অন্য স্কলারশিপ-তালিকার সাইট সূত্র হিসেবে ব্যবহার করা হয় না।</li>
    <li>অফিসিয়াল সূত্রে যে তথ্য নেই (যেমন টাকার পরিমাণ বা IELTS স্কোর), সেখানে লেখা থাকে "Not stated in source snippet" — অনুমান করে কিছু বসানো হয় না।</li>
    <li>"যাচাই বাকি" মানে তথ্যটি অফিসিয়াল পেজের সারাংশ থেকে নেওয়া, পুরো পেজ খুলে মেলানো হয়নি। তাই আবেদনের আগে সূত্র লিংক খুলে মিলিয়ে নিন।</li>
  </ul>
  <h2>কত ঘন ঘন আপডেট হয়</h2>
  <p>প্রতি সপ্তাহে তালিকা আপডেট হয়: নতুন বিজ্ঞপ্তি যোগ হয়, মেয়াদ শেষ হওয়া স্কলারশিপ বাদ যায়, আর নতুন দেশ যোগ হয়। সর্বশেষ যাচাই: {CHECKED}।</p>
  <h2>আমরা কারা নই</h2>
  <p>Higher Study Info কোনো সরকার, বিশ্ববিদ্যালয় বা স্কলারশিপ প্রদানকারী প্রতিষ্ঠানের অংশ নয়, আর আবেদন গ্রহণ করে না। আবেদন সবসময় সংশ্লিষ্ট প্রতিষ্ঠানের অফিসিয়াল সাইটে করতে হয়। কেউ এই সাইটের নামে টাকা চাইলে তা প্রতারণা।</p>
  <h2>যোগাযোগ</h2>
  <p>কোনো তথ্য ভুল বা পুরনো মনে হলে, নতুন স্কলারশিপের খবর দিতে চাইলে বা অন্য কোনো প্রশ্ন থাকলে যোগাযোগ করুন:</p>
  {CONTACT_HTML}
  <p><a href="/privacy/">Privacy Policy</a></p>
</article>
{FOOTER}
</div>"""


def privacy_body(updated):
    return f"""<div class="wrap">
{nav()}
<article class="prose">
  <span class="eyebrow">Higher Study Info · কার্যকর: {PRIVACY_EFFECTIVE}</span>
  <h1>Privacy Policy</h1>
  <p>এই পেজে বলা আছে higherstudyinfo.com ভিজিট করলে কোন তথ্য সংগ্রহ হয় আর তা কীভাবে ব্যবহার হয়।</p>
  <h2>আমরা যে তথ্য নিই না</h2>
  <p>এই সাইটে কোনো অ্যাকাউন্ট, ফর্ম বা আবেদন নেই। আমরা আপনার নাম, ইমেইল, ফোন নম্বর বা কোনো কাগজপত্র চাই না, সংগ্রহও করি না।</p>
  <h2>Google Analytics</h2>
  <p>সাইট কতজন ব্যবহার করছেন আর কোন পেজ বেশি দেখা হচ্ছে তা বুঝতে আমরা Google Analytics (Google LLC) ব্যবহার করি। এটি কুকি ব্যবহার করে এবং আপনার ব্রাউজার থেকে কিছু তথ্য সংগ্রহ করে, যেমন:</p>
  <ul>
    <li>কোন পেজ দেখেছেন, কতক্ষণ, কোন লিংক থেকে এসেছেন</li>
    <li>ডিভাইস, ব্রাউজার, অপারেটিং সিস্টেম আর আনুমানিক অবস্থান (দেশ/শহর)</li>
    <li>IP ঠিকানা (Google এটি প্রক্রিয়া করে; আমরা আলাদা করে সংরক্ষণ করি না)</li>
  </ul>
  <p>এই তথ্য শুধু সামষ্টিক পরিসংখ্যান হিসেবে দেখা হয়, কাউকে আলাদাভাবে শনাক্ত করতে নয়। Google কীভাবে তথ্য ব্যবহার করে তা জানতে দেখুন <a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener">How Google uses information from sites that use its services</a> এবং <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">Google Privacy Policy</a>।</p>
  <h2>কুকি বন্ধ করতে চাইলে</h2>
  <ul>
    <li>ব্রাউজারের সেটিংস থেকে কুকি ব্লক বা মুছে ফেলতে পারেন।</li>
    <li>Google Analytics পুরোপুরি বন্ধ করতে Google-এর <a href="https://tools.google.com/dlpage/gaoptout" target="_blank" rel="noopener">Analytics Opt-out Browser Add-on</a> ব্যবহার করতে পারেন।</li>
  </ul>
  <h2>বাইরের সাইটের লিংক</h2>
  <p>প্রতিটি স্কলারশিপে অফিসিয়াল সাইটের লিংক আছে। সেসব সাইটের নিজস্ব privacy policy প্রযোজ্য; সেগুলোর ওপর আমাদের নিয়ন্ত্রণ নেই।</p>
  <h2>শিশুদের তথ্য</h2>
  <p>আমরা জেনেশুনে কারো ব্যক্তিগত তথ্য সংগ্রহ করি না, শিশুদেরও নয়।</p>
  <h2>পরিবর্তন ও যোগাযোগ</h2>
  <p>এই নীতিতে পরিবর্তন হলে এই পেজে তারিখসহ আপডেট করা হবে। প্রশ্ন থাকলে যোগাযোগ করুন:</p>
  {CONTACT_HTML}
</article>
{FOOTER}
</div>"""


# ---------------------------------------------------------------- guides & tools

def _sources(items):
    return '<h2>সূত্র</h2><ul class="src-list">' + "".join(
        f'<li><a href="{html.escape(u)}" target="_blank" rel="noopener">{html.escape(t)}</a></li>' for t, u in items) + "</ul>"


GUIDE_CSS = """<style>
.steps{counter-reset:s;list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:10px}
.steps>li{counter-increment:s;position:relative;padding:14px 16px 14px 52px;background:var(--surface);border:1px solid var(--line);border-radius:10px}
.steps>li::before{content:counter(s);position:absolute;left:16px;top:14px;width:24px;height:24px;border-radius:50%;background:var(--accent);color:var(--surface);font-weight:700;font-size:13px;display:grid;place-items:center}
.steps h3{font-family:var(--display);font-weight:500;font-size:18px;margin:0 0 4px}
.steps p{margin:4px 0 0}
.warn{background:var(--accent-soft);border-radius:8px;padding:10px 14px;font-size:14px}
.src-list{font-size:14px}
.guides{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,300px),1fr));gap:14px}
.tbl-wrap{overflow-x:auto}
table.t{border-collapse:collapse;font-size:14px;min-width:420px}
table.t th,table.t td{border-bottom:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}
table.t th{font-weight:600;color:var(--muted)}
table.t.fit{min-width:0;width:100%}
.calc{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;padding:16px;background:var(--surface);border:1px solid var(--line);border-radius:10px}
.calc label{display:flex;flex-direction:column;justify-content:space-between;gap:4px;font-size:14px;color:var(--muted)}
.calc input{font:inherit;font-size:18px;color:var(--fg);background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:8px 10px;width:100%}
.out{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px}
.out div{padding:14px 16px;background:var(--surface);border:1px solid var(--line);border-radius:10px}
.out b{display:block;font-family:var(--display);font-size:32px;line-height:1.1;color:var(--accent);font-variant-numeric:tabular-nums}
.out span{font-size:13px;color:var(--muted)}
.vcard{display:flex;flex-direction:column;gap:8px;padding:16px 18px;background:var(--surface);border:1px solid var(--line);border-radius:10px;scroll-margin-top:16px}
.vcard h2{margin:0}.vcard h2 small{font-family:var(--mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);font-weight:400;margin-left:6px}
.vcard table.t{min-width:0;width:100%}.vcard table.t th{width:30%;min-width:110px}
.vlinks{margin:0}.vlinks .apply{display:inline-block;font-weight:600;font-size:14px;text-decoration:none;border-radius:8px;padding:7px 12px;background:var(--accent);color:var(--surface)}
.vsrc{font-size:13px;color:var(--muted);margin:0}
.vcard td a,.vsrc a{color:var(--accent)}
</style>"""

GUIDES = [
    ("/tools/timeline/", "🗓️ আবেদনের টাইমলাইন প্ল্যানার", "শেষ তারিখ দিন — কোন মাসে পরীক্ষা, LOR, SOP, ভিসা, উল্টো দিক থেকে হিসাব।"),
    ("/guides/faq/", "❓ সচরাচর জিজ্ঞাসা (FAQ)", "IELTS ছাড়া, কম CGPA, স্টাডি গ্যাপ, বয়স, ব্যাংক ব্যালান্স — সবচেয়ে বেশি প্রশ্নের উত্তর।"),
    ("/guides/fraud/", "🚩 প্রতারণা থেকে সাবধান", "ভুয়া ভর্তির চিঠি, জাল কাগজ আর অসৎ এজেন্ট চেনার উপায় — সরকারি সূত্রে।"),
    ("/tools/eligibility/", "✅ কোন স্কলারশিপে আমি যোগ্য?", "লেভেল, IELTS, বয়স আর CGPA দিয়ে তালিকা ছেঁকে দেখুন কোনগুলো আপনার সাথে মেলে।"),
    ("/guides/documents/", "📄 কাগজপত্র ও সত্যায়ন", "বাংলাদেশ থেকে আবেদনের জন্য সার্টিফিকেট সত্যায়ন, e-Apostille আর পুলিশ ক্লিয়ারেন্স — ধাপে ধাপে।"),
    ("/guides/english-tests/", "🗣️ IELTS, TOEFL, Duolingo, PTE", "বাংলাদেশে ফি, কোথায় বুক করবেন, আর কোন স্কলারশিপে IELTS ছাড়ের পথ আছে।"),
    ("/guides/other-tests/", "📝 GRE, GMAT, SAT ও ভাষার পরীক্ষা", "GRE/GMAT/SAT-এর ফি ও তারিখ, আর ঢাকায় জার্মান (Goethe, TestDaF), জাপানি (JLPT), কোরিয়ান (TOPIK) পরীক্ষা।"),
    ("/tools/cgpa/", "🧮 CGPA রূপান্তর", "বাংলাদেশের CGPA থেকে জার্মান গ্রেড (Bavarian formula) আর গ্রেড-ব্যান্ড।"),
    ("/guides/visa/", "🛂 স্টুডেন্ট ভিসা — দেশভিত্তিক", "১৪টি দেশে কত টাকা দেখাতে হয়, পড়ার সময় কাজ, ভিসা ফি — অফিসিয়াল সূত্রে।"),
    ("/guides/post-study-work/", "🧭 পড়া শেষে কাজের ভিসা", "জার্মানি ১৮ মাস, কানাডা PGWP, যুক্তরাষ্ট্র OPT, অস্ট্রেলিয়া ৪৮৫, জাপান, কোরিয়া — দেশভিত্তিক তুলনা।"),
    ("/guides/tuition-free/", "💶 টিউশন-ফ্রি ও কম খরচের দেশ", "জার্মানি, অস্ট্রিয়া, ফ্রান্স, নরওয়ে — EU-র বাইরের শিক্ষার্থীদের টিউশন।"),
    ("/tools/budget/", "💰 বাজেট ক্যালকুলেটর", "প্রথম বছরের আনুমানিক খরচ আর ভিসার জন্য কত দেখাতে হবে — টাকায়।"),
    ("/guides/sop/", "✍️ Statement of Purpose (SOP)", "কাঠামো, দৈর্ঘ্য, কী করবেন না — আর নিজের তথ্য দিয়ে আউটলাইন বানানোর টুল।"),
    ("/guides/application-portals/", "🖥️ আবেদন পোর্টাল — uni-assist, UCAS, Common App, Studielink", "কোন দেশে কোন পোর্টালে আবেদন, ফি আর শেষ তারিখ।"),
    ("/guides/cv/", "📄 একাডেমিক CV ও Europass CV", "রিজিউম আর CV-র পার্থক্য, অংশগুলো, কাঠামো আর Europass।"),
    ("/guides/lor/", "🤝 Recommendation Letter (LOR)", "কাকে বলবেন, কখন, কোন কাগজ দেবেন — আর কোন ভুল আবেদন বাতিল করাতে পারে।"),
    ("/guides/research-proposal/", "🔬 Research Proposal", "PhD ও DAAD গবেষণা স্কলারশিপের জন্য প্রস্তাবের কাঠামো, দৈর্ঘ্য আর সময়সূচি।"),
    ("/guides/professor-email/", "✉️ প্রফেসরকে ইমেইল", "সুপারভাইজার খোঁজা, ইমেইলের কাঠামো আর ফলো-আপের নিয়ম।"),
    ("/guides/funded-phd/", "🎓 ফান্ডেড PhD — TA, RA, বেতনভুক্ত PhD", "যুক্তরাষ্ট্র-কানাডার Assistantship ও ন্যূনতম ফান্ডিং, ইউরোপে বেতনসহ PhD পদ।"),
    ("/guides/part-time-work/", "💼 পড়ার সময় পার্ট-টাইম কাজ", "দেশভিত্তিক কাজের ঘণ্টার সীমা আর ভিসা বাঁচিয়ে কাজের সতর্কতা।"),
    ("/guides/interview/", "🎤 ভিসা ও স্কলারশিপ ইন্টারভিউ", "Chevening-ধরনের স্কলারশিপ ইন্টারভিউ আর ঢাকায় US F-1 ভিসা ইন্টারভিউর প্রস্তুতি।"),
    ("/guides/student-file/", "🏦 স্টুডেন্ট ফাইল ও টাকা পাঠানো", "বাংলাদেশ ব্যাংকের নিয়মে টিউশন ও জীবনযাত্রার খরচ বিদেশে পাঠানো।"),
    ("/guides/pre-departure/", "🧳 যাওয়ার আগের চেকলিস্ট", "কাগজ, টাকা, স্বাস্থ্য, যাত্রা আর পৌঁছানোর প্রথম সপ্তাহ — টিক দেওয়ার তালিকা।"),
    ("/guides/motivation-letter/", "📝 Motivation Letter", "DAAD, Erasmus Mundus-এর মতো ইউরোপীয় আবেদনের জন্য — প্রশ্ন, কাঠামো আর আউটলাইন টুল।"),
]


FOOTER = _footer()


def guides_index_body(updated):
    cards = "".join(f'<a class="card" href="{h}"><h2>{t}</h2><span class="meta">{d}</span></a>' for h, t, d in GUIDES)
    return f"""<div class="wrap">
{nav("/guides/")}
<header style="display:flex;flex-direction:column;gap:10px">
  <span class="eyebrow">Higher Study Info · গাইড ও টুল</span>
  <h1>উচ্চশিক্ষার গাইড ও টুল</h1>
  <p class="lede">আবেদনের প্রস্তুতির জন্য দরকারি তথ্য, অফিসিয়াল সূত্রের লিংকসহ।</p>
</header>
<div class="guides">{cards}</div>
{FOOTER}
</div>"""


def documents_body(updated):
    return f"""<div class="wrap">
{nav("/guides/")}
<article class="prose">
  <nav class="crumbs"><a href="/guides/">গাইড ও টুল</a></nav>
  <span class="eyebrow">গাইড · সর্বশেষ যাচাই {GUIDES_CHECKED}</span>
  <h1>কাগজপত্র ও সত্যায়ন</h1>
  <p class="lede">বিদেশে ভর্তি, স্কলারশিপ বা ভিসার আবেদনে বাংলাদেশি সার্টিফিকেট সাধারণত সত্যায়িত করে দিতে হয়। কোন কাগজ কীভাবে সত্যায়ন করতে হবে তা প্রতিটি বিশ্ববিদ্যালয়, স্কলারশিপ বা দূতাবাস আলাদাভাবে বলে দেয় — নিচের ধাপগুলো সাধারণ ক্রম, আপনার প্রতিষ্ঠানের নির্দেশনা আগে দেখে নিন।</p>
  <h2>সাধারণত যেসব কাগজ লাগে</h2>
  <ul>
    <li>পাসপোর্ট (মেয়াদ যথেষ্ট আছে কিনা দেখুন)</li>
    <li>SSC, HSC, স্নাতক ও স্নাতকোত্তরের সার্টিফিকেট এবং মার্কশিট/ট্রান্সক্রিপ্ট</li>
    <li>ইংরেজি দক্ষতার প্রমাণ (IELTS/TOEFL/Duolingo, বা Medium of Instruction সনদ — যেখানে গ্রহণযোগ্য)</li>
    <li>CV, Statement of Purpose (SOP), রেফারেন্স/সুপারিশপত্র</li>
    <li>ভিসার সময়: পুলিশ ক্লিয়ারেন্স, আর্থিক সামর্থ্যের প্রমাণ, স্বাস্থ্য সনদ — দেশভেদে আলাদা</li>
  </ul>
  <h2>সত্যায়নের ধাপ</h2>
  <ol class="steps">
    <li><h3>শিক্ষা মন্ত্রণালয়ে অনলাইন সত্যায়ন</h3>
      <p>মাধ্যমিক ও উচ্চ শিক্ষা বিভাগ "বিদেশগামী শিক্ষার্থীদের সার্টিফিকেট এবং ট্রান্সক্রিপ্ট অনলাইনের মাধ্যমে সত্যায়ন" সেবা দেয়। SSC/HSC সনদ ও ট্রান্সক্রিপ্ট এবং সরকারি ও বেসরকারি বিশ্ববিদ্যালয়ের সনদ/ট্রান্সক্রিপ্টের জন্য আলাদা আবেদন ফর্ম আছে; নিজের প্রতিষ্ঠানের ধরন অনুযায়ী সঠিক ফর্ম বেছে নিন। নির্দেশিকা PDF আর আবেদনের লিংক একই পেজে।</p>
      <p><a href="https://shed.gov.bd/pages/static-pages/694146bba31054345f0fc944" target="_blank" rel="noopener">শিক্ষা মন্ত্রণালয়ের অনলাইন সত্যায়ন পেজ ↗</a></p></li>
    <li><h3>পররাষ্ট্র মন্ত্রণালয় — e-Apostille</h3>
      <p>বাংলাদেশে এখন e-Apostille ব্যবস্থা চালু: সরকারি e-Apostille প্ল্যাটফর্মে নিবন্ধন করে কাগজ আপলোড, অনলাইনে ফি পরিশোধ, তারপর QR কোডসহ e-Apostille সনদ পাওয়া যায়। কোপেনহেগেনের বাংলাদেশ দূতাবাস জানায়, Apostille করা কাগজে ঢাকায় পররাষ্ট্র মন্ত্রণালয়ের আলাদা হাতে-সত্যায়ন লাগে না।</p>
      <p class="warn">Apostille সাধারণত Apostille Convention-ভুক্ত দেশে চলে। আপনার গন্তব্য দেশ বা প্রতিষ্ঠান কোনটা চায় (Apostille, নাকি দূতাবাস সত্যায়ন) তা আগে নিশ্চিত হোন।</p>
      <p><a href="https://copenhagen.mofa.gov.bd/pages/static-pages/6952668835ce18e1c05a9da2" target="_blank" rel="noopener">e-Apostille সম্পর্কে দূতাবাসের নোটিশ ↗</a></p></li>
    <li><h3>পুলিশ ক্লিয়ারেন্স সার্টিফিকেট (ভিসার জন্য)</h3>
      <p>অনলাইনে <a href="https://pcc.police.gov.bd/ords/r/pcc/pcc/home" target="_blank" rel="noopener">pcc.police.gov.bd</a>-এ নিবন্ধন করে আবেদন: ব্যক্তিগত তথ্য ও ঠিকানা, কাগজ আপলোড, যাচাই করে জমা (জমার পর আর সম্পাদনা করা যায় না), শেষে ফি পরিশোধ। পাসপোর্টের কপি প্রথম শ্রেণির গেজেটেড কর্মকর্তা দিয়ে সত্যায়িত করতে হয়; পোর্টাল অনুযায়ী পাসপোর্টের মেয়াদ অন্তত তিন মাস থাকতে হবে। বর্তমান ঠিকানার জেলা/মেট্রোপলিটন পুলিশ সনদ দেয়; অবস্থা জানতে পোর্টালে দেওয়া ফরম্যাটে 26969-এ SMS।</p>
      <p class="warn">ফি: পোর্টালের বাংলা পেজে প্রায় ৳১,৫০০; পুরনো একটি পেজে ৳৫০০ লেখা — জমা দেওয়ার আগে পোর্টালে বর্তমান ফি দেখে নিন।</p></li>
    <li><h3>গন্তব্য দেশের দূতাবাস (যদি চায়)</h3>
      <p>কিছু দেশ বা প্রতিষ্ঠান ঢাকায় তাদের দূতাবাস থেকেও সত্যায়ন চায়। আবেদনের নির্দেশনায় এটা উল্লেখ থাকে।</p></li>
  </ol>
  {_sources([
      ("শিক্ষা মন্ত্রণালয় — বিদেশগামী শিক্ষার্থীদের অনলাইন সত্যায়ন", "https://shed.gov.bd/pages/static-pages/694146bba31054345f0fc944"),
      ("Embassy of Bangladesh, The Hague — Attestation of documents (e-Apostille)", "https://hague.mofa.gov.bd/pages/static-pages/attestation-of-documents-695d21c101f260dcf5c90aa9"),
      ("Embassy of Bangladesh, Copenhagen — Attestation of documents", "https://copenhagen.mofa.gov.bd/pages/static-pages/6952668835ce18e1c05a9da2"),
      ("Bangladesh Police — Police Clearance Certificate portal", "https://pcc.police.gov.bd/ords/r/pcc/pcc/home"),
      ("Bangladesh Police — Police clearance certificate", "https://www.police.gov.bd/en/police_clearance_certificate"),
  ])}
</article>
{FOOTER}
</div>"""


WAIVER_RE = r"waiv|exempt|medium[- ]of[- ]instruction|English[- ]medium|English-taught|taught (entirely )?in English|No test certificate|no IELTS|optional|No TaiwanICDF minimum|No SI requirement"


def english_tests_body(updated):
    import re
    rows = [r for r in all_rows() if r.get("english_requirement") and re.search(WAIVER_RE, r["english_requirement"], re.I)]
    trs = "".join(
        f'<tr><td>{html.escape(COUNTRIES[r["slug"]][0])}</td><td><a href="{r["page"]}">{html.escape(r["scholarship_name"])}</a></td>'
        f'<td>{html.escape(r["english_requirement"])}</td></tr>' for r in rows)
    return f"""<div class="wrap">
{nav("/guides/")}
<article class="prose" style="max-width:100%">
  <nav class="crumbs"><a href="/guides/">গাইড ও টুল</a></nav>
  <span class="eyebrow">গাইড · সর্বশেষ যাচাই {GUIDES_CHECKED}</span>
  <h1>IELTS, TOEFL, Duolingo, PTE</h1>
  <p class="lede" style="max-width:68ch">বাংলাদেশ থেকে কোন পরীক্ষা কোথায় দেবেন, ফি কত — অফিসিয়াল সূত্র অনুযায়ী। প্রতিটি স্কলারশিপের নির্দিষ্ট স্কোর তার কার্ডে "IELTS / English" অংশে আছে।</p>
  <div class="tbl-wrap"><table class="t">
    <tr><th>পরীক্ষা</th><th>বাংলাদেশে ফি</th><th>কোথায় বুক করবেন</th></tr>
    <tr><td><b>IELTS</b> (Academic / General)</td><td>কম্পিউটারে ৳৩১,১০০; UKVI ৳৩৪,৮৫০ (British Council)। কাগজে কেন্দ্রভেদে আলাদা — বুকিং পেজে দেখুন।</td><td><a href="https://www.britishcouncil.org.bd/en/exam/ielts/book-test" target="_blank" rel="noopener">British Council</a> · <a href="https://ielts.idp.com/bangladesh/about/ielts-exam-fee" target="_blank" rel="noopener">IDP</a></td></tr>
    <tr><td><b>TOEFL iBT</b></td><td>দেশভেদে আলাদা — ETS-এর ফি পেজে Bangladesh বেছে নিন।</td><td><a href="https://www.ets.org/toefl/test-takers/ibt/register/fees.html" target="_blank" rel="noopener">ETS</a></td></tr>
    <tr><td><b>Duolingo English Test</b></td><td>US$৭০; বাসা থেকে অনলাইনে, প্রায় ১ ঘণ্টা। Duolingo-র হিসাবে ৬,৫০০+ প্রোগ্রাম গ্রহণ করে।</td><td><a href="https://englishtest.duolingo.com/applicants" target="_blank" rel="noopener">Duolingo</a></td></tr>
    <tr><td><b>PTE Academic</b></td><td>দেশভেদে আলাদা — Pearson-এর কেন্দ্র ও ফি পেজে দেখুন।</td><td><a href="https://www.pearsonpte.com/pte-academic/" target="_blank" rel="noopener">Pearson PTE</a></td></tr>
  </table></div>
  <p class="warn">TOEFL iBT-এর স্কোর-স্কেল ২১ জানুয়ারি ২০২৬ থেকে বদলেছে (নতুন স্কেল ১–৬)। তাই অনেক বিশ্ববিদ্যালয় দুটো স্কোর লেখে — যেমন "TOEFL 4.5 (আগের স্কেলে 90)"। কোনো বিশ্ববিদ্যালয় IELTS Online বা Home Edition গ্রহণ নাও করতে পারে; আবেদনের আগে দেখে নিন।</p>
  <h2>IELTS ছাড়ের পথ আছে এমন স্কলারশিপ ({bn(len(rows))}টি)</h2>
  <p>নিচের স্কলারশিপগুলোর অফিসিয়াল তথ্যে IELTS ছাড়া যোগ্যতা প্রমাণের কোনো পথ উল্লেখ আছে — যেমন আগের ডিগ্রি ইংরেজি মাধ্যমে হলে (Medium of Instruction সনদ), বা নির্দিষ্ট দেশ থেকে ডিগ্রি থাকলে, বা টেস্ট ঐচ্ছিক হলে। শর্ত প্রত্যেকটির জন্য আলাদা — পুরো লেখা পড়ুন।</p>
  <div class="tbl-wrap"><table class="t">
    <tr><th>দেশ</th><th>স্কলারশিপ</th><th>ইংরেজির শর্ত (অফিসিয়াল সূত্র অনুযায়ী)</th></tr>
    {trs}
  </table></div>
  {_sources([
      ("IDP Bangladesh — IELTS exam fee", "https://ielts.idp.com/bangladesh/about/ielts-exam-fee"),
      ("British Council Bangladesh — Book IELTS", "https://www.britishcouncil.org.bd/en/exam/ielts/book-test"),
      ("ETS — TOEFL iBT registration fee", "https://www.ets.org/toefl/test-takers/ibt/register/fees.html"),
      ("Duolingo English Test — accepting institutions", "https://englishtest.duolingo.com/test_takers/accepting_institutions"),
      ("Pearson — PTE Academic", "https://www.pearsonpte.com/pte-academic/"),
  ])}
</article>
{FOOTER}
</div>"""


def cgpa_body(updated):
    bands = [("A+", "4.00", "80% বা বেশি"), ("A", "3.75", "75% – 79%"), ("A-", "3.50", "70% – 74%"), ("B+", "3.25", "65% – 69%"),
             ("B", "3.00", "60% – 64%"), ("B-", "2.75", "55% – 59%"), ("C+", "2.50", "50% – 54%"), ("C", "2.25", "45% – 49%"),
             ("D", "2.00", "40% – 44%"), ("F", "0.00", "40%-এর কম")]
    rows = "".join(f"<tr><td>{g}</td><td>{p}</td><td>{m}</td></tr>" for g, p, m in bands)
    script = """<script>
(function(){
  var B=[[4.00,"A+","80% বা বেশি"],[3.75,"A","75% – 79%"],[3.50,"A-","70% – 74%"],[3.25,"B+","65% – 69%"],[3.00,"B","60% – 64%"],[2.75,"B-","55% – 59%"],[2.50,"C+","50% – 54%"],[2.25,"C","45% – 49%"],[2.00,"D","40% – 44%"]];
  var c=document.getElementById("cg"),mx=document.getElementById("mx"),mn=document.getElementById("mn");
  var g=document.getElementById("ger"),b=document.getElementById("band"),msg=document.getElementById("msg");
  function run(){
    var nd=parseFloat(c.value),nmax=parseFloat(mx.value),nmin=parseFloat(mn.value);
    if(isNaN(nd)||isNaN(nmax)||isNaN(nmin)||nmax<=nmin){g.textContent="—";b.textContent="—";msg.textContent="সঠিক সংখ্যা দিন (সর্বোচ্চ > ন্যূনতম পাস)।";msg.hidden=false;return}
    if(nd>nmax||nd<nmin){g.textContent="—";b.textContent="—";msg.textContent="CGPA ন্যূনতম পাস ও সর্বোচ্চের মধ্যে হতে হবে।";msg.hidden=false;return}
    msg.textContent="";msg.hidden=true;
    var de=1+3*(nmax-nd)/(nmax-nmin);g.textContent=(Math.floor(de*10)/10).toFixed(1);
    if(nmax===4){var hit=B.find(function(x){return nd>=x[0]});b.textContent=hit?hit[1]+" · "+hit[2]:"—"}else{b.textContent="৪.০০ স্কেলে প্রযোজ্য"}
  }
  [c,mx,mn].forEach(function(e){e.addEventListener("input",run)});run();
})();
</script>"""
    return f"""<div class="wrap">
{nav("/guides/")}
<article class="prose" style="max-width:100%">
  <nav class="crumbs"><a href="/guides/">গাইড ও টুল</a></nav>
  <span class="eyebrow">টুল</span>
  <h1>CGPA রূপান্তর</h1>
  <p class="lede" style="max-width:68ch">জার্মানি ও ইউরোপের অনেক বিশ্ববিদ্যালয় বিদেশি গ্রেডকে "modified Bavarian formula" দিয়ে জার্মান গ্রেডে (১.০ সবচেয়ে ভালো, ৪.০ পাস) রূপান্তর করে। আপনার CGPA দিন:</p>
  <div class="calc">
    <label for="cg">আপনার CGPA<input id="cg" type="number" step="0.01" min="0" value="3.50" inputmode="decimal"></label>
    <label for="mx">সর্বোচ্চ সম্ভব (Nmax)<input id="mx" type="number" step="0.01" value="4.00" inputmode="decimal"></label>
    <label for="mn">ন্যূনতম পাস (Nmin)<input id="mn" type="number" step="0.01" value="2.00" inputmode="decimal"></label>
  </div>
  <div class="out" aria-live="polite">
    <div><b id="ger">—</b><span>জার্মান গ্রেড (আনুমানিক)</span></div>
    <div><b id="band" style="font-size:22px">—</b><span>সমান গ্রেড-পয়েন্টের ব্যান্ড (৪.০০ স্কেল)</span></div>
  </div>
  <p id="msg" class="warn" hidden></p>
  <p><b>সূত্র:</b> জার্মান গ্রেড = 1 + 3 × (Nmax − আপনার CGPA) ÷ (Nmax − Nmin)। ফলাফল এক দশমিকে কেটে দেখানো হয়। ন্যূনতম পাস CGPA আপনার বিশ্ববিদ্যালয়ের নিয়ম অনুযায়ী বদলে নিন — আর মনে রাখুন, প্রতিটি জার্মান বিশ্ববিদ্যালয় বা uni-assist নিজস্ব Nmin ধরতে পারে; চূড়ান্ত রূপান্তর তারাই করে।</p>
  <h2>বাংলাদেশের প্রচলিত গ্রেডিং (UGC-অনুমোদিত)</h2>
  <p>অনেক বাংলাদেশি বিশ্ববিদ্যালয় এই স্কেল ব্যবহার করে (BUET-এর প্রকাশিত টেবিল)। কিছু বিভাগ বা প্রোগ্রাম আলাদা স্কেল ব্যবহার করে — আপনার ট্রান্সক্রিপ্টের পেছনের টেবিল দেখুন। মনে রাখুন, CGPA থেকে শতাংশের কোনো অফিসিয়াল সূত্র নেই; ব্যান্ডটা শুধু কোন গ্রেড-পয়েন্ট কোন নম্বর-সীমার সমান তা দেখায়।</p>
  <div class="tbl-wrap"><table class="t"><tr><th>লেটার গ্রেড</th><th>গ্রেড পয়েন্ট</th><th>নম্বর</th></tr>{rows}</table></div>
  {_sources([
      ("TUM — Grade conversion using the Bavarian formula", "https://www.tum.de/en/studies/application/application-info-portal/grade-conversion-formula-for-grades-earned-outside-germany"),
      ("uni-assist — FAQs (grade conversion)", "https://www.uni-assist.de/en/faqs/get-information/"),
      ("BUET CSE — Undergraduate academic evaluation (grading table)", "https://cse.buet.ac.bd/academics/ug_eval"),
  ])}
</article>
{FOOTER}
</div>
{script}"""


# ---------------------------------------------------------------- visa, tuition, budget
# Every figure below comes from the official page cited next to it (checked 2026-11-04).
VISA = [
    {"c": "Germany", "bn": "জার্মানি", "visa": "National Visa (Study)",
     "funds": "ব্লকড অ্যাকাউন্টে বছরে অন্তত €11,904 (মাসে €992 তোলা যায়) — বা স্কলারশিপ, ব্যাংক গ্যারান্টি, Verpflichtungserklärung",
     "work": "বছরে 140 পূর্ণ দিন বা 280 অর্ধ দিন (Federal Employment Agency-র অনুমতি ছাড়া); বিশ্ববিদ্যালয়ের সহকারী-কাজ এর বাইরে",
     "post": "জার্মানিতে পড়া শেষ করা non-EU গ্র্যাজুয়েটরা যোগ্য চাকরি খুঁজতে সর্বোচ্চ 18 মাসের রেসিডেন্স পারমিট পান (নবায়নযোগ্য নয়); এই সময় যেকোনো কাজ করা যায়, জীবনযাত্রার খরচ চালানোর সামর্থ্য লাগে। চাকরি পেলে উপযুক্ত পারমিটে (যেমন EU Blue Card) বদলাতে হয়", "fee": "",
     "apply": ("German Embassy Dhaka — Study visa", "https://dhaka.diplo.de/bd-en/service/2685884-2685884"),
     "src": [("German Embassy Dhaka — Study visa checklist (June 2026)", "https://dhaka.diplo.de/resource/blob/2685888/1826aadb06dfc6b0224e91583b6836cb/p-01-checklist-students-data.pdf"),
             ("DAAD — Side jobs", "https://www.daad.de/en/studying-in-germany/work-career/side-jobs/"),
             ("Make it in Germany — Seeking employment after graduation", "https://www.make-it-in-germany.com/en/study-training/study/prospects/seeking-employment")]},
    {"c": "United Kingdom", "bn": "যুক্তরাজ্য", "visa": "Student visa",
     "funds": "লন্ডনে মাসে £1,483, লন্ডনের বাইরে মাসে £1,136 (সর্বোচ্চ 9 মাস) + প্রথম বছরের বাকি টিউশন; টাকা টানা 28 দিন অ্যাকাউন্টে থাকতে হবে",
     "work": "ডিগ্রি-লেভেল ফুল-টাইম কোর্সে টার্মে সপ্তাহে 20 ঘণ্টা, ছুটিতে ফুল-টাইম",
     "post": "Graduate visa: 31 Dec 2026 পর্যন্ত আবেদনে 2 বছর, 1 Jan 2027 থেকে 18 মাস; PhD হলে 3 বছর",
     "fee": "বাইরে থেকে আবেদন £558 (gov.uk-এ বর্তমান ফি দেখে নিন)",
     "apply": ("GOV.UK — Student visa", "https://www.gov.uk/student-visa"),
     "src": [("GOV.UK — Financial evidence for Student visa", "https://www.gov.uk/guidance/financial-evidence-for-student-and-child-student-route-applicants"),
             ("GOV.UK — Immigration Rules Appendix Student", "https://www.gov.uk/guidance/immigration-rules/immigration-rules-appendix-student"),
             ("GOV.UK — Graduate visa", "https://www.gov.uk/graduate-visa")]},
    {"c": "United States", "bn": "যুক্তরাষ্ট্র", "visa": "F-1 student visa",
     "funds": "নির্দিষ্ট জাতীয় অঙ্ক নেই — বিশ্ববিদ্যালয়ের I-20-তে লেখা মোট খরচ দেখাতে হয়",
     "work": "ক্লাস চলাকালীন ক্যাম্পাসে সপ্তাহে সর্বোচ্চ 20 ঘণ্টা",
     "post": "OPT: প্রতিটি উচ্চতর ডিগ্রি লেভেলে সর্বোচ্চ 12 মাস; DHS-এর STEM তালিকাভুক্ত ডিগ্রি হলে E-Verify-তে থাকা নিয়োগকর্তার অধীনে আরও 24 মাস (STEM OPT)। বেকার থাকার সীমা: প্রথম OPT-তে 90 দিন, STEM-সহ মোট 150 দিন", "fee": "ভিসা (MRV) ফি $185 + SEVIS I-901 ফি $350",
     "apply": ("U.S. Embassy Dhaka", "https://bd.usembassy.gov/"),
     "src": [("travel.state.gov — Student visa", "https://travel.state.gov/content/travel/en/us-visas/study/student-visa.html"),
             ("ICE — I-901 SEVIS fee", "https://www.ice.gov/sevis/i901"),
             ("Study in the States — Working in the US", "https://studyinthestates.dhs.gov/students/work/working-in-the-united-states"),
             ("USCIS — STEM OPT extension", "https://www.uscis.gov/working-in-the-united-states/students-and-exchange-visitors/optional-practical-training-extension-for-stem-students-stem-opt"),
             ("Study in the States — F-1 OPT", "https://studyinthestates.dhs.gov/sevis-help-hub/student-records/fm-student-employment/f-1-optional-practical-training-opt")]},
    {"c": "Canada", "bn": "কানাডা", "visa": "Study permit",
     "funds": "একক আবেদনকারী: জীবনযাত্রার জন্য CAD 22,895 (1 Sep 2025 থেকে) + প্রথম বছরের টিউশন + যাতায়াত",
     "work": "ক্যাম্পাসের বাইরে টার্মে সপ্তাহে 24 ঘণ্টা; নির্ধারিত ছুটিতে সীমাহীন",
     "post": "PGWP: ২ বছর বা বেশি মেয়াদের প্রোগ্রামে 3 বছর পর্যন্ত; 8 মাস–2 বছরের প্রোগ্রামে প্রোগ্রামের সমান; 2 বছরের কম মাস্টার্সেও (অন্তত 8 মাস) 3 বছর। PGWP-যোগ্য DLI-তে পড়তে হবে, কোর্স শেষের নিশ্চয়তার 180 দিনের মধ্যে আবেদন; জীবনে একবারই", "fee": "",
     "apply": ("IRCC — Study permit", "https://www.canada.ca/en/immigration-refugees-citizenship/services/study-canada/study-permit/get-documents.html"),
     "src": [("IRCC — International students (CIMM, Apr 2026)", "https://www.canada.ca/en/immigration-refugees-citizenship/corporate/transparency/committees/cimm-apr-22-2026/international-students.html"),
             ("IRCC — Work off campus", "https://www.canada.ca/en/immigration-refugees-citizenship/services/study-canada/work/work-off-campus.html"),
             ("IRCC — About the PGWP", "https://www.canada.ca/en/immigration-refugees-citizenship/services/study-canada/work/after-graduation/about.html"),
             ("IRCC — PGWP: Who can apply", "https://www.canada.ca/en/immigration-refugees-citizenship/services/study-canada/work/after-graduation/eligibility.html")]},
    {"c": "Australia", "bn": "অস্ট্রেলিয়া", "visa": "Student visa (subclass 500)",
     "funds": "AUD 29,710 (12 মাসের জীবনযাত্রা) + প্রথম 12 মাসের কোর্স ফি + যাতায়াত; অথবা বার্ষিক আয় অন্তত AUD 60,000",
     "work": "কোর্স চলাকালীন প্রতি ১৪ দিনে (fortnight) সর্বোচ্চ 48 ঘণ্টা; কোর্সের ছুটিতে সীমা নেই; গবেষণা-মাস্টার্স ও PhD শিক্ষার্থীদের কোর্স শুরুর পর সীমা নেই", "post": "Temporary Graduate visa (subclass 485): যোগ্যতাভেদে 18 মাস থেকে 3 বছর থাকা যায় — নিজের ডিগ্রির জন্য Post-Higher Education Work stream পেজে মেয়াদ দেখুন", "fee": "",
     "apply": ("Home Affairs — Student visa", "https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing/changes-to-student-visa-application-rules-500-590"),
     "src": [("Study Australia — Change to evidence of financial capacity", "https://www.studyaustralia.gov.au/en_in/tools-and-resources/news/change-to-evidence-of-financial-capacity-for-student-visas"),
             ("Home Affairs — Financial capacity evidence", "https://immi.homeaffairs.gov.au/help-text/evidence/Pages/et-h0185.aspx"),
             ("Home Affairs — Work restrictions for student visa holders", "https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing/student-500/temporary-relaxation-of-working-hours-for-student-visa-holders"),
             ("Home Affairs — Temporary Graduate visa (subclass 485)", "https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing/temporary-graduate-485")]},
    {"c": "Italy", "bn": "ইতালি", "visa": "Study visa (type D)",
     "funds": "বছরে €10,179.85 (মাসে প্রায় €848) — কিছু কনস্যুলেট ফেরার খরচও (প্রায় €500) চায়",
     "work": "সপ্তাহে সর্বোচ্চ 20 ঘণ্টা, বছরে 1,040 ঘণ্টা; বার্ষিক সীমা না ছাড়ালে ক্লাস বন্ধের সময় বেশি করা যায়", "post": "চাকরি খোঁজার পারমিট (ricerca di lavoro): 9–12 মাস, এই সময়ে সাপ্তাহিক 20 ঘণ্টার সীমা থাকে না; চাকরি পেলে কাজের পারমিটে রূপান্তর", "fee": "",
     "apply": ("Universitaly — pre-enrolment", "https://www.universitaly.it/"),
     "src": [("Italian Consulate — Study visa checklist 2026/2027", "https://consdubai.esteri.it/wp-content/uploads/2026/05/StudyVisa_2026_2027.pdf"),
             ("Integrazione Migranti (Ministry of Labour) — Working with a study permit", "https://integrazionemigranti.gov.it/it-it/Ricerca-news/Dettaglio-news/id/3085/-possibile-lavorare-con-un-permesso-per-motivi-di-studio-E-svolgere-un-tirocinio"),
             ("Integrazione Migranti — Working with a study permit", "https://integrazionemigranti.gov.it/it-it/Ricerca-news/Dettaglio-news/id/3085/-possibile-lavorare-con-un-permesso-per-motivi-di-studio-E-svolgere-un-tirocinio")]},
    {"c": "Japan", "bn": "জাপান", "visa": "Student (College Student)",
     "funds": "",
     "work": "অনুমতি নিয়ে সপ্তাহে 28 ঘণ্টা (দীর্ঘ ছুটিতে দিনে 8 ঘণ্টা); অনুমতি বিমানবন্দরেই নেওয়া যায়",
     "post": "চাকরি না পেলে Designated Activities স্ট্যাটাসে চাকরি খোঁজা: 6 মাস, সাধারণত একবার 6 মাস নবায়ন (শর্তসাপেক্ষে দ্বিতীয় বছর); বিশ্ববিদ্যালয়ের সুপারিশপত্র লাগে", "fee": "",
     "apply": ("Study in Japan — Part-time work", "https://www.studyinjapan.go.jp/en/work-in-japan/part-time-jobs/"),
     "src": [("Study in Japan — Part-time work", "https://www.studyinjapan.go.jp/en/work-in-japan/part-time-jobs/"),
             ("Study in Japan — For former international students", "https://www.studyinjapan.go.jp/en/faq/after/"),
             ("Immigration Services Agency — Designated Activities", "https://www.moj.go.jp/isa/applications/procedures/nyuukokukanri07_00208.html")]},
    {"c": "South Korea", "bn": "দক্ষিণ কোরিয়া", "visa": "D-2 student visa",
     "funds": "মাসে অন্তত KRW 900,000 × 6 মাস = প্রায় KRW 5,400,000",
     "work": "অনুমতি নিয়ে স্নাতকে সপ্তাহে 30, স্নাতকোত্তরে 35 ঘণ্টা (সূত্রভেদে আলাদা — বিশ্ববিদ্যালয়ে জেনে নিন); সাধারণত কোরিয়ান ভাষার দক্ষতা লাগে",
     "post": "D-10-1 চাকরি-খোঁজার ভিসা: পেশাদার (E-1–E-7 ধরনের) চাকরির জন্য, চাকরির আগে ইন্টার্নশিপও করা যায়; D-2 থেকে প্রথমবার বদলালে আর্থিক প্রমাণ লাগে না", "fee": "",
     "apply": ("Study in Korea — Visa and stay", "https://www.studyinkorea.go.kr/ko/plan/visaAndStay.do"),
     "src": [("Study in Korea — Residence and stay", "https://www.studyinkorea.go.kr/ko/life/residenceAndStayInfo.do"),
             ("Study in Korea — Residence eligibility and stay duration", "https://www.studyinkorea.go.kr/ko/life/residenceAndStayInfo.do")]},
    {"c": "Malaysia", "bn": "মালয়েশিয়া", "visa": "Student Pass (EMGS-এর মাধ্যমে)",
     "funds": "",
     "work": "অনুমোদিত জায়গায় সপ্তাহে 20 ঘণ্টা — EMGS বলে শুধু 7 দিনের বেশি ছুটিতে, Immigration বলে পড়ার সময়েও; প্রতিষ্ঠানে জেনে নিন",
     "post": "", "fee": "Student Pass RM60/বছর + ভিসা ফি (দেশভেদে, সর্বোচ্চ RM50) + EMGS প্রসেসিং ফি",
     "apply": ("EMGS — Student Pass", "https://visa.educationmalaysia.gov.my/"),
     "src": [("Immigration Malaysia — Student Pass", "https://www.imi.gov.my/index.php/en/main-services/pass/student-pass/"),
             ("EMGS — FAQ", "https://educationmalaysia.gov.my/get-in-touch/faq")]},
    {"c": "France", "bn": "ফ্রান্স", "visa": "Long-stay student visa (VLS-TS) — প্রথম বছর রেসিডেন্স পারমিট হিসেবেও কাজ করে; পৌঁছানোর ৩ মাসের মধ্যে অনলাইনে validate করতে হয়",
     "funds": "১ আগস্ট ২০২৬ থেকে মাসে অন্তত €877.50 (আগে €615) — টিউশন বাদ দিয়ে, পুরো থাকার সময়ের জন্য",
     "work": "বছরে 964 ঘণ্টা (প্রায় সপ্তাহে 20 ঘণ্টা); বার্ষিক হিসাব",
     "post": "মাস্টার্স বা সমমানের ডিগ্রির পর চাকরি খুঁজতে বা ব্যবসা শুরু করতে 12 মাসের APS / \"recherche d'emploi\" পারমিট (সাধারণত নবায়নযোগ্য নয়); কোনটা প্রযোজ্য তা জাতীয়তাভেদে আলাদা — প্রিফেকচারে জেনে নিন",
     "fee": "ভিসা আবেদন ফি €50 (Campus France USA-র উল্লেখ; দেশভেদে আলাদা হতে পারে) + Campus France ও VFS/TLS ফি",
     "apply": ("Campus France — Student long-stay visa", "https://www.campusfrance.org/en/student-long-stay-visa"),
     "src": [("Campus France — VLS-TS", "https://www.campusfrance.org/en/student-long-stay-visa"),
             ("Campus France — Student visa changes from 1 Aug 2026", "https://www.singapour.campusfrance.org/student-visa-changes-effective-from-01-august-2026"),
             ("Campus France — Working while studying", "https://www.campusfrance.org/en/working-student"),
             ("Campus France — Temporary resident permit (APS)", "https://www.campusfrance.org/en/temporary-resident-permit-aps"),
             ("Campus France USA — Student visa guide 2026-27 (PDF)", "https://www.usa.campusfrance.org/system/files/medias/documents/2026-07/Campus%20France%20USA%20Student%20Visa%20Guide%20(2026-2027).pdf")]},
    {"c": "Netherlands", "bn": "নেদারল্যান্ডস", "visa": "MVV + study residence permit — আবেদন করে বিশ্ববিদ্যালয় (recognised sponsor); মেয়াদ কোর্স + 3 মাস, সর্বোচ্চ 5 বছর",
     "funds": "IND-এর \"study norm\" অনুযায়ী ১ বছরের খরচ (12 × study norm) সাধারণত বিশ্ববিদ্যালয়ের অ্যাকাউন্টে জমা দিতে হয় — বর্তমান অঙ্ক IND-এর Income requirements study পেজে",
     "work": "সপ্তাহে সর্বোচ্চ 16 ঘণ্টা, অথবা শুধু জুন–আগস্টে ফুল-টাইম (একই বছরে দুটো নয়); নিয়োগকর্তাকে UWV থেকে ওয়ার্ক পারমিট (TWV) নিতে হয়",
     "post": "Orientation year: নেদারল্যান্ডসে ব্যাচেলর/মাস্টার্স শেষের 3 বছরের মধ্যে আবেদনে 1 বছর চাকরি খোঁজা, এ সময় ওয়ার্ক পারমিট ছাড়াই কাজ; নবায়নযোগ্য নয়, ফি €254 (২০২৬)",
     "fee": "",
     "apply": ("IND — Study", "https://ind.nl/en/income-requirements-study"),
     "src": [("IND — Income requirements study", "https://ind.nl/en/income-requirements-study"),
             ("IND — Coming to study in the Netherlands (PDF)", "https://ind.nl/en/forms/3087.pdf"),
             ("IND — Looking for work after study (form 7523)", "https://ind.nl/en/forms/7523.pdf")]},
    {"c": "Ireland", "bn": "আয়ারল্যান্ড", "visa": "Long-term study visa (D) → Stamp 2 immigration permission",
     "funds": "প্রতি বছরের জন্য €10,000 তাৎক্ষণিক প্রাপ্য (৬–৮ মাসের কোর্সে মাসে €833); ৬ মাসের ব্যাংক স্টেটমেন্ট, ক্রেডিট কার্ড গ্রহণযোগ্য নয়। ফি €6,000-এর বেশি হলে ভিসার আগে অন্তত €6,000, কম হলে পুরো ফি পরিশোধ",
     "work": "টার্মে সপ্তাহে 20 ঘণ্টা, ছুটিতে (জুন–সেপ্টেম্বর ও ১৫ ডিসেম্বর–১৫ জানুয়ারি) সপ্তাহে 40 ঘণ্টা",
     "post": "Stamp 1G (Third Level Graduate Programme): ফুল-টাইম কাজ করা যায়, ব্যবসা নয়; মেয়াদ ডিগ্রির লেভেল অনুযায়ী (লেভেল ৮-এ 12 মাস পর্যন্ত)",
     "fee": "",
     "apply": ("Irish Immigration — How to apply for a long-term study visa", "https://www.irishimmigration.ie/coming-to-study-in-ireland/what-are-my-study-visa-options/how-to-apply-for-long-term-study-visa/"),
     "src": [("Irish Immigration — Student finance requirements (from 30 June 2025)", "https://www.irishimmigration.ie/reminder-on-student-finance-requirements-from-30-june-2025/"),
             ("Irish Immigration — Immigration permission / stamps", "https://www.irishimmigration.ie/registering-your-immigration-permission/information-on-registering/immigration-permission-stamps/"),
             ("Irish Immigration — Third Level Graduate Programme (PDF)", "https://www.irishimmigration.ie/wp-content/uploads/2024/03/third-level-graduate-programme.pdf")]},
    {"c": "Türkiye", "bn": "তুরস্ক", "visa": "Student residence permit (ikamet) — e-İkamet-এ আবেদন; পুরো মেয়াদের স্বাস্থ্যবীমা বাধ্যতামূলক (দেশের ভেতরের বীমা কোম্পানির বা সরকারি General Health Insurance — ভর্তির ৩ মাসের মধ্যে আবেদন)",
     "funds": "",
     "work": "স্টুডেন্ট রেসিডেন্স পারমিট কাজের অনুমতি দেয় না — কাজ করতে আলাদা ওয়ার্ক পারমিট লাগে",
     "post": "",
     "fee": "",
     "apply": ("Presidency of Migration Management — e-İkamet", "https://e-ikamet.goc.gov.tr/"),
     "src": [("Göç İdaresi — Documents required for student residence permit", "https://e-ikamet.goc.gov.tr/Ikamet/BasvuruIstenenBelgeler/BasvuruFormuIstenenBelgeler?tur=5"),
             ("Göç İdaresi — General health insurance for foreigners (PDF)", "https://en.goc.gov.tr/kurumlar/goc.gov.tr/files/SGK_KITAPCIK_ing.pdf"),
             ("Ministry of Labour — Documents issued to foreigners", "https://csgb.gov.tr/uigm/en/general-information/yabancilara-duzenlenen-belgeler/")]},
    {"c": "Hungary", "bn": "হাঙ্গেরি", "visa": "Residence permit for the purpose of studies",
     "funds": "",
     "work": "পড়ার সময় সপ্তাহে সর্বোচ্চ 30 ঘণ্টা; পড়ার বাইরের সময়ে বছরে সর্বোচ্চ 90 দিন ফুল-টাইম (Act XC of 2023)",
     "post": "পড়া শেষে চাকরি খোঁজা বা ব্যবসা শুরুর রেসিডেন্স পারমিট — স্টুডেন্ট পারমিটের মেয়াদ থাকতে থাকতেই আবেদন করতে হয়",
     "fee": "",
     "apply": ("Immigration and Asylum Office (OIF) — Residence of the student", "https://oif.gov.hu/factsheets/residence-of-the-student-pupil"),
     "src": [("OIF — Residence of the student", "https://oif.gov.hu/factsheets/residence-of-the-student-pupil"),
             ("Study in Hungary — Work in Hungary", "https://studyinhungary.hu/living-in-hungary/menu/formalities/work-in-hungary.html"),
             ("Stipendium Hungaricum — Employment conditions for foreign students", "https://stipendiumhungaricum.hu/faq/are-the-employment-conditions-for-foreign-students-regulated-in-hungary/")]},
]


def visa_body(updated):
    blocks = []
    for v in VISA:
        rows = "".join(f"<tr><th>{k}</th><td>{html.escape(v[f])}</td></tr>" for k, f in
                       [("ভিসা", "visa"), ("কত টাকা দেখাতে হয়", "funds"), ("পড়ার সময় কাজ", "work"),
                        ("পড়া শেষে কাজের ভিসা", "post"), ("ভিসা ফি", "fee")] if v[f])
        src = " · ".join(f'<a href="{html.escape(u)}" target="_blank" rel="noopener">{html.escape(t)}</a>' for t, u in v["src"])
        blocks.append(f"""<section class="vcard" id="{v['c'].lower().replace(' ', '-')}">
  <h2>{v['bn']} <small>{v['c']}</small></h2>
  <div class="tbl-wrap"><table class="t">{rows}</table></div>
  <p class="vlinks"><a class="apply" href="{html.escape(v['apply'][1])}" target="_blank" rel="noopener">{html.escape(v['apply'][0])} ↗</a></p>
  <p class="vsrc">সূত্র: {src}</p>
</section>""")
    toc = " · ".join(f'<a href="#{v["c"].lower().replace(" ", "-")}">{v["bn"]}</a>' for v in VISA)
    return f"""<div class="wrap">
{nav("/guides/")}
<article class="prose" style="max-width:100%">
  <nav class="crumbs"><a href="/guides/">গাইড ও টুল</a></nav>
  <span class="eyebrow">গাইড · সর্বশেষ যাচাই {GUIDES_CHECKED}</span>
  <h1>স্টুডেন্ট ভিসা — দেশভিত্তিক</h1>
  <p class="lede" style="max-width:68ch">প্রতিটি দেশের স্টুডেন্ট ভিসায় কত টাকা দেখাতে হয়, পড়ার সময় কত ঘণ্টা কাজ করা যায়, আর কোথায় আবেদন — সরকারের অফিসিয়াল পেজ অনুযায়ী। যে তথ্য অফিসিয়াল সূত্রে পাইনি, সেটা লেখা হয়নি। ভিসার নিয়ম ঘন ঘন বদলায় — আবেদনের আগে সূত্র লিংক খুলে মিলিয়ে নিন।</p>
  <p>{toc}</p>
  {''.join(blocks)}
</article>
{FOOTER}
</div>"""


TUITION = [
    ("জার্মানি", "সরকারি বিশ্ববিদ্যালয়ে সাধারণত স্নাতক ও বেশিরভাগ মাস্টার্সে টিউশন নেই। ব্যতিক্রম: Baden-Württemberg-এ non-EU শিক্ষার্থীদের প্রতি সেমিস্টারে €1,500 (PhD বাদে); Bavaria-র বিশ্ববিদ্যালয় নিজেরা ফি ঠিক করতে পারে। আলাদা একটা সেমিস্টার ফি (প্রশাসন, ছাত্র-সংগঠন, অনেক সময় যাতায়াত টিকিট) সবাইকে দিতে হয়।",
     [("DAAD — Costs of education and living", "https://www.daad.de/en/studying-in-germany/living-in-germany/finances/")]),
    ("অস্ট্রিয়া", "সরকারি বিশ্ববিদ্যালয়ে non-EU শিক্ষার্থীদের প্রতি সেমিস্টারে €726.72 টিউশন + প্রায় €25–26 ছাত্র-সংগঠন (ÖH) ফি। (Study in Austria একটি পেজে €751.92 লেখে — বিশ্ববিদ্যালয়ে মিলিয়ে নিন।) কিছু উন্নয়নশীল দেশের নাগরিক ছাড় পেতে পারেন।",
     [("TU Wien — Tuition fee", "https://www.tuwien.at/en/studies/admission/students-union-fee-and-tuition-fee/tuition-fee"),
      ("University of Vienna — Tuition fee", "https://studieren.univie.ac.at/en/studying-and-learning/financial-matters/amount-of-the-tuition-fee/students-union-fee")]),
    ("ফ্রান্স", "সরকারি বিশ্ববিদ্যালয়ে EU-র বাইরের শিক্ষার্থীদের ২০২৬-২৭ সালের ফি: স্নাতক (licence) €2,902, মাস্টার্স €3,950 প্রতি বছর; PhD €398। প্রতিটি বিশ্ববিদ্যালয় চাইলে তার বিদেশি শিক্ষার্থীদের ১০% পর্যন্ত এই ফি থেকে ছাড় দিতে পারে।",
     [("French Ministry of Higher Education — Rentrée 2026 press kit", "https://www.enseignementsup-recherche.gouv.fr/sites/default/files/2026-09/rentree26_dp_A4_220926_DIGITAL_BD_0.pdf")]),
    ("নরওয়ে", "শরৎ ২০২৩ থেকে EU/EEA/সুইজারল্যান্ডের বাইরের নতুন শিক্ষার্থীদের টিউশন দিতে হয়; প্রতিটি প্রতিষ্ঠান নিজে ফি ঠিক করে (যেমন University of Oslo ২০২৭/২৮-এ বছরে NOK 218,000)। NORPART, NORHED-এর মতো সরকারি প্রোগ্রামের শিক্ষার্থীরা ছাড় পান।",
     [("University of Oslo — Tuition fees", "https://www.uio.no/english/studies/admission/tuition/"),
      ("Study in Norway — Cost and requirements", "https://studyinnorway.no/cost-and-requirements")]),
]


def tuition_body(updated):
    items = "".join(
        f'<section class="vcard"><h2>{c}</h2><p>{html.escape(t)}</p><p class="vsrc">সূত্র: ' +
        " · ".join(f'<a href="{html.escape(u)}" target="_blank" rel="noopener">{html.escape(n)}</a>' for n, u in s) + "</p></section>"
        for c, t, s in TUITION)
    return f"""<div class="wrap">
{nav("/guides/")}
<article class="prose">
  <nav class="crumbs"><a href="/guides/">গাইড ও টুল</a></nav>
  <span class="eyebrow">গাইড · সর্বশেষ যাচাই {GUIDES_CHECKED}</span>
  <h1>টিউশন-ফ্রি ও কম খরচের দেশ</h1>
  <p class="lede">ইউরোপের কিছু দেশে সরকারি বিশ্ববিদ্যালয়ে টিউশন নেই বা খুব কম — তবে নিয়ম বদলাচ্ছে। টিউশন কম হলেও থাকা-খাওয়ার খরচ আর ভিসার জন্য টাকা দেখাতে হয়; সেটা <a href="/guides/visa/">ভিসা গাইডে</a> আর <a href="/tools/budget/">বাজেট ক্যালকুলেটরে</a> দেখুন।</p>
  {items}
  <p class="warn">ফি প্রোগ্রাম ও বিশ্ববিদ্যালয়ভেদে আলাদা হতে পারে। আবেদনের আগে নির্দিষ্ট প্রোগ্রামের পেজে ফি দেখে নিন।</p>
</article>
{FOOTER}
</div>"""


# Preset values for the budget calculator, all from VISA sources above.
BUDGET = [
    {"k": "de", "n": "জার্মানি", "cur": "EUR", "funds": 11904, "fee": 0, "note": "ব্লকড অ্যাকাউন্টের ন্যূনতম (বছরে)। সরকারি বিশ্ববিদ্যালয়ে সাধারণত টিউশন নেই; Baden-Württemberg-এ non-EU সেমিস্টারে €1,500।"},
    {"k": "uk-l", "n": "যুক্তরাজ্য — লন্ডন", "cur": "GBP", "funds": 1483 * 9, "fee": 558, "note": "£1,483 × 9 মাস। এর সাথে প্রথম বছরের বাকি টিউশনও অ্যাকাউন্টে দেখাতে হয়।"},
    {"k": "uk-o", "n": "যুক্তরাজ্য — লন্ডনের বাইরে", "cur": "GBP", "funds": 1136 * 9, "fee": 558, "note": "£1,136 × 9 মাস। এর সাথে প্রথম বছরের বাকি টিউশনও দেখাতে হয়।"},
    {"k": "us", "n": "যুক্তরাষ্ট্র", "cur": "USD", "funds": 0, "fee": 185 + 350, "note": "জাতীয় ন্যূনতম নেই — I-20-তে লেখা জীবনযাত্রার খরচ বসান। ফি = ভিসা $185 + SEVIS $350।"},
    {"k": "ca", "n": "কানাডা", "cur": "CAD", "funds": 22895, "fee": 0, "note": "একক আবেদনকারীর জীবনযাত্রার ন্যূনতম; এর সাথে প্রথম বছরের টিউশন ও যাতায়াত দেখাতে হয়।"},
    {"k": "au", "n": "অস্ট্রেলিয়া", "cur": "AUD", "funds": 29710, "fee": 0, "note": "১২ মাসের জীবনযাত্রা; এর সাথে প্রথম ১২ মাসের কোর্স ফি ও যাতায়াত। ভিসা ফি Home Affairs-এ দেখে বসান।"},
    {"k": "it", "n": "ইতালি", "cur": "EUR", "funds": 10179.85, "fee": 0, "note": "বছরে ন্যূনতম; কিছু কনস্যুলেট ফেরার খরচ (প্রায় €500) আলাদা চায়।"},
    {"k": "kr", "n": "দক্ষিণ কোরিয়া", "cur": "KRW", "funds": 5400000, "fee": 0, "note": "মাসে KRW 900,000 × 6 মাস।"},
]


def budget_body(updated):
    opts = "".join(f'<option value="{b["k"]}">{b["n"]} ({b["cur"]})</option>' for b in BUDGET)
    data = json.dumps({b["k"]: b for b in BUDGET}, ensure_ascii=False)
    script = """<script>
(function(){
  var P=__DATA__;
  var $=function(i){return document.getElementById(i)};
  var cty=$("cty"),liv=$("liv"),tui=$("tui"),fee=$("fee"),oth=$("oth"),rate=$("rate");
  function fmt(n,c){try{return new Intl.NumberFormat("en",{style:"currency",currency:c,maximumFractionDigits:0}).format(n)}catch(e){return Math.round(n)+" "+c}}
  function load(){var p=P[cty.value];liv.value=p.funds;fee.value=p.fee;tui.value=0;oth.value=0;$("note").textContent=p.note;document.querySelectorAll(".cur").forEach(function(e){e.textContent=p.cur});
    try{var r=localStorage.getItem("rate-"+p.cur);rate.value=r||""}catch(e){rate.value=""}calc()}
  function num(e){var v=parseFloat(e.value);return isNaN(v)?0:v}
  function calc(){var p=P[cty.value];var t=num(liv)+num(tui)+num(fee)+num(oth);$("tot").textContent=fmt(t,p.cur);
    var r=num(rate);if(r>0){$("bdt").textContent="৳ "+new Intl.NumberFormat("en-IN",{maximumFractionDigits:0}).format(t*r);try{localStorage.setItem("rate-"+p.cur,rate.value)}catch(e){}}else{$("bdt").textContent="—"}}
  cty.addEventListener("change",load);[liv,tui,fee,oth,rate].forEach(function(e){e.addEventListener("input",calc)});load();
})();
</script>""".replace("__DATA__", data)
    return f"""<div class="wrap">
{nav("/guides/")}
<article class="prose" style="max-width:100%">
  <nav class="crumbs"><a href="/guides/">গাইড ও টুল</a></nav>
  <span class="eyebrow">টুল · ভিসার অঙ্ক যাচাই {GUIDES_CHECKED}</span>
  <h1>বাজেট ক্যালকুলেটর</h1>
  <p class="lede" style="max-width:68ch">প্রথম বছরে আনুমানিক কত টাকা লাগবে, আর ভিসার জন্য কত দেখাতে হবে। দেশ বাছলে সরকারের অফিসিয়াল ন্যূনতম জীবনযাত্রার অঙ্ক আর জানা ভিসা ফি বসে যাবে; টিউশন আর অন্যান্য খরচ নিজে দিন। টাকায় দেখতে আজকের বিনিময় হার লিখুন।</p>
  <div class="calc">
    <label for="cty">দেশ<select id="cty" style="font:inherit;font-size:16px;padding:8px 10px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--fg)">{opts}</select></label>
    <label for="liv"><span>জীবনযাত্রা — ভিসার ন্যূনতম (<span class="cur"></span>)</span><input id="liv" type="number" min="0" step="1" inputmode="decimal"></label>
    <label for="tui"><span>প্রথম বছরের টিউশন (<span class="cur"></span>)</span><input id="tui" type="number" min="0" step="1" value="0" inputmode="decimal"></label>
    <label for="fee"><span>ভিসা ও সংশ্লিষ্ট ফি (<span class="cur"></span>)</span><input id="fee" type="number" min="0" step="1" inputmode="decimal"></label>
    <label for="oth"><span>অন্যান্য: বিমান টিকিট, বীমা ইত্যাদি (<span class="cur"></span>)</span><input id="oth" type="number" min="0" step="1" value="0" inputmode="decimal"></label>
    <label for="rate"><span>১ <span class="cur"></span> = কত টাকা?</span><input id="rate" type="number" min="0" step="0.01" placeholder="যেমন ১৪০ হলে 140" inputmode="decimal"></label>
  </div>
  <p id="note" class="warn"></p>
  <div class="out" aria-live="polite">
    <div><b id="tot">—</b><span>প্রথম বছরের মোট (আনুমানিক)</span></div>
    <div><b id="bdt">—</b><span>বাংলাদেশি টাকায়</span></div>
  </div>
  <p>এটা একটা আনুমানিক হিসাব — ভিসার আসল শর্ত, টিউশন আর হার আবেদনের সময় অফিসিয়াল সূত্রে মিলিয়ে নিন। দেশভিত্তিক সূত্র <a href="/guides/visa/">ভিসা গাইডে</a> আছে।</p>
</article>
{FOOTER}
</div>
{script}"""


# ---------------------------------------------------------------- SOP & motivation letter

def _outline_tool(kind):
    """Fields -> an English outline skeleton the applicant fills in themselves (not a finished letter)."""
    if kind == "sop":
        fields = [("prog", "প্রোগ্রাম ও বিশ্ববিদ্যালয়", "e.g. MS in Computer Science, University of X"),
                  ("interest", "যে বিষয়ে আগ্রহ / গবেষণার প্রশ্ন", "e.g. low-resource NLP for Bangla"),
                  ("exp", "সবচেয়ে প্রাসঙ্গিক অভিজ্ঞতা (প্রজেক্ট/থিসিস/চাকরি) — আপনার ভূমিকা ও ফল", "e.g. undergrad thesis on ..., built ..., result ..."),
                  ("fit", "কেন এই প্রোগ্রাম — কোন অধ্যাপক/ল্যাব/কোর্স", "e.g. Prof. Y's lab on ..."),
                  ("goal", "পড়া শেষে লক্ষ্য", "e.g. research role in ..., return to teach at ...")]
        order = [("Opening", "State your field and the specific question or problem that drives you: {interest}."),
                 ("Preparation", "Your most relevant work, with your role and the outcome: {exp}. What did it teach you?"),
                 ("Fit", "Why {prog}: name the faculty, lab or courses — {fit} — and what you will contribute."),
                 ("Goals", "Where this degree leads: {goal}."),
                 ("Close", "One or two sentences tying interest, preparation and goals together.")]
    else:
        fields = [("name", "আপনার নাম", "e.g. Your full name"),
                  ("to", "প্রাপক — নাম জানলে নাম, না জানলে কমিটি", "e.g. Prof. Dr. X / Selection Committee"),
                  ("prog", "প্রোগ্রাম/স্কলারশিপ, বিশ্ববিদ্যালয় ও দেশ", "e.g. DAAD scholarship, MSc Water Management, University of X, Germany"),
                  ("deg", "আপনার শেষ ডিগ্রি ও ফল", "e.g. BSc in Civil Engineering, University of Y, CGPA 3.6/4"),
                  ("why", "কেন এই বিষয় — কী থেকে আগ্রহ শুরু", "e.g. flood work in my district ..."),
                  ("exp", "অভিজ্ঞতা: থিসিস/প্রজেক্ট/চাকরি/নেতৃত্ব — আপনার ভূমিকা ও ফল", "e.g. thesis on ..., 2 years at ..., led a team that ..."),
                  ("fit", "কেন এই প্রোগ্রাম, বিশ্ববিদ্যালয় ও দেশ — নির্দিষ্ট মডিউল/গবেষণা/অধ্যাপক", "e.g. modules on ..., Prof. Z's group on ..."),
                  ("back", "দেশে ফিরে কীভাবে কাজে লাগাবেন (প্রতিষ্ঠান, নীতি, SDG)", "e.g. join ... ministry, teach at ..., support SDG 6"),
                  ("need", "কেন স্কলারশিপ দরকার (ঐচ্ছিক, সংক্ষেপে)", "e.g. cannot fund tuition and living costs myself")]
        order = [("Header", "{name} · [email] · [phone]\n   [Date, e.g. 15 November 2026]\n   To: {to}, [Department / Admissions Office], [University, City]\n   Subject: Motivation letter — {prog}"),
                 ("Salutation", "Dear {to},  (unknown name → \"Dear Selection Committee,\")"),
                 ("Opening", "Which programme/scholarship you apply for, and who you are in one line: {deg}."),
                 ("Motivation", "What draws you to this field and why now: {why}."),
                 ("Background", "Studies and work that prepared you, with your role and results: {exp}."),
                 ("Choice", "Why {prog} — the programme, the university and the country: {fit}."),
                 ("Goals during the stay", "What you want to learn or achieve there; for a PhD, a short research plan."),
                 ("After the degree", "How you will use the qualification, especially back home: {back}."),
                 ("Why the scholarship", "Only if relevant, one or two honest sentences: {need}."),
                 ("Closing", "Restate your interest, thank the committee for its time, and say you look forward to discussing your application (e.g. at an interview)."),
                 ("Sign-off", "Yours sincerely,\n   [signature]\n   {name}")]
    inputs = "".join(
        f'<label for="o-{k}">{l}<textarea id="o-{k}" rows="2" placeholder="{html.escape(ph)}"></textarea></label>' for k, l, ph in fields)
    tpl = json.dumps(order, ensure_ascii=False)
    keys = json.dumps([k for k, _, _ in fields])
    return f"""<h2>আউটলাইন বানান</h2>
<p>নিচের ঘরগুলোতে নিজের তথ্য লিখুন (বাংলা বা ইংরেজিতে) — একটা অনুচ্ছেদ-ভিত্তিক কাঠামো তৈরি হবে। এটা খসড়ার কঙ্কাল মাত্র; চিঠিটা নিজের ভাষায় লিখুন। এখানে লেখা কিছুই কোথাও পাঠানো বা সংরক্ষণ হয় না।</p>
<div class="otool">{inputs}</div>
<pre id="o-out" class="ooutput" aria-live="polite"></pre>
<p><button type="button" id="o-copy" class="obtn">আউটলাইন কপি করুন</button> <span id="o-msg" class="count"></span></p>
<script>
(function(){{
  var T={tpl},K={keys};
  function v(k){{var e=document.getElementById("o-"+k);return e.value.trim()||"["+e.previousSibling.textContent.trim()+"]"}}
  function run(){{document.getElementById("o-out").textContent=T.map(function(p,i){{
    return (i+1)+". "+p[0]+"\\n   "+p[1].replace(/\\{{(\\w+)\\}}/g,function(_,k){{return K.indexOf(k)>=0?v(k):"_"}})}}).join("\\n\\n")}}
  K.forEach(function(k){{document.getElementById("o-"+k).addEventListener("input",run)}});run();
  document.getElementById("o-copy").addEventListener("click",function(){{
    var t=document.getElementById("o-out").textContent,m=document.getElementById("o-msg");
    var done=function(){{m.textContent="কপি হয়েছে"}},fail=function(){{var r=document.createRange();r.selectNodeContents(document.getElementById("o-out"));var s=getSelection();s.removeAllRanges();s.addRange(r);m.textContent="সিলেক্ট করা হয়েছে — Ctrl+C চাপুন"}};
    if(navigator.clipboard)navigator.clipboard.writeText(t).then(done,fail);else fail();
  }});
}})();
</script>"""


OUTLINE_CSS = """<style>
.otool{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:12px;padding:16px;background:var(--surface);border:1px solid var(--line);border-radius:10px}
.otool label{display:flex;flex-direction:column;justify-content:space-between;gap:4px;font-size:14px;color:var(--muted)}
.otool textarea{font:inherit;font-size:15px;color:var(--fg);background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:8px 10px;resize:vertical;width:100%}
.ooutput{white-space:pre-wrap;font-family:var(--mono);font-size:13px;line-height:1.6;padding:16px;background:var(--surface);border:1px solid var(--line);border-radius:10px;margin:0;overflow-x:auto}
.obtn{font:inherit;font-weight:600;font-size:14px;border:0;border-radius:8px;padding:8px 14px;background:var(--accent);color:var(--surface);cursor:pointer}
</style>"""


def sop_body(updated):
    return f"""<div class="wrap">
{nav("/guides/")}
<article class="prose" style="max-width:100%">
  <nav class="crumbs"><a href="/guides/">গাইড ও টুল</a></nav>
  <span class="eyebrow">গাইড · সূত্র যাচাই {GUIDES_CHECKED}</span>
  <h1>Statement of Purpose (SOP)</h1>
  <div style="max-width:68ch;display:flex;flex-direction:column;gap:14px">
  <p class="lede">SOP হলো একাডেমিক চিঠি: আপনি কী নিয়ে পড়তে বা গবেষণা করতে চান, তার জন্য কী প্রস্তুতি আছে, কেন এই প্রোগ্রাম, আর ভবিষ্যৎ লক্ষ্য কী। যুক্তরাষ্ট্র, কানাডা, অস্ট্রেলিয়ার মাস্টার্স/PhD আবেদনে সাধারণত SOP চাওয়া হয়। ইউরোপে একই ধরনের লেখাকে প্রায়ই <a href="/guides/motivation-letter/">Motivation Letter</a> বলে।</p>
  <h2>দৈর্ঘ্য</h2>
  <p>প্রোগ্রামের নির্দেশনাই আগে। উদাহরণ: UC Berkeley মোটামুটি ৫০০–১,০০০ শব্দ বলে, Cornell সাধারণত ১–২ পৃষ্ঠা, UCLA-র প্রশ্নে সর্বোচ্চ ৫০০ শব্দ, Harvard-এর ইংরেজি বিভাগে সর্বোচ্চ ১,০০০ শব্দ। সীমা পেরোবেন না।</p>
  <h2>কাঠামো</h2>
  <ol class="steps">
    <li><h3>শুরু: আগ্রহ ও প্রশ্ন</h3><p>কোন বিষয় বা সমস্যা নিয়ে কাজ করতে চান, আর কীভাবে সেখানে পৌঁছালেন — সংক্ষেপে। জীবনকাহিনি দিয়ে শুরু করবেন না; Berkeley আত্মজীবনীমূলক গল্প এড়াতে বলে।</p></li>
    <li><h3>প্রস্তুতি: নির্দিষ্ট উদাহরণ</h3><p>থিসিস, প্রজেক্ট, গবেষণা বা চাকরি — প্রজেক্টের নাম/বিষয়, তত্ত্বাবধায়ক, আপনার নির্দিষ্ট ভূমিকা, কী শিখলেন, ফল কী। শুধু CV আবার লিখবেন না; অভিজ্ঞতার মানে ব্যাখ্যা করুন।</p></li>
    <li><h3>কেন এই প্রোগ্রাম</h3><p>কোন অধ্যাপক, ল্যাব, কোর্স বা সুবিধা আপনার আগ্রহের সাথে মেলে — নাম ধরে। কিছু প্রোগ্রাম অধ্যাপকের নাম লেখা বাধ্যতামূলক করে।</p></li>
    <li><h3>লক্ষ্য</h3><p>ডিগ্রির পর কী করতে চান — বাস্তবসম্মত ও নির্দিষ্ট।</p></li>
  </ol>
  <h2>যা করবেন, যা করবেন না</h2>
  <ul>
    <li>প্রতিটি প্রোগ্রামের জন্য আলাদা SOP লিখুন — একই লেখা সবখানে পাঠাবেন না (Purdue OWL)।</li>
    <li>গুণ দাবি না করে উদাহরণ দিয়ে দেখান (Berkeley: "demonstrate everything by example")।</li>
    <li>CGPA কম হওয়া বা পড়ায় বিরতির মতো সমস্যা থাকলে সংক্ষেপে, ইতিবাচকভাবে ব্যাখ্যা করুন — অজুহাত নয়, কী শিখেছেন ও কীভাবে উন্নতি করেছেন।</li>
    <li>অন্যের SOP বা ইন্টারনেটের নমুনা কপি করবেন না; বিশ্ববিদ্যালয়গুলো অনেক সময় plagiarism যাচাই করে।</li>
    <li>জমার আগে বানান-ব্যাকরণ দেখুন, আর আপনার বিষয়ের বাইরের কাউকে দিয়েও একবার পড়িয়ে নিন।</li>
  </ul>
  </div>
  {_outline_tool("sop")}
  {related_scholarships("SOP লাগে এমন স্কলারশিপ — যুক্তরাষ্ট্র, কানাডা, অস্ট্রেলিয়া, নিউজিল্যান্ড", lambda s_, r: s_.startswith(("north-america/", "oceania/")), 15)}
  {_sources([
      ("UC Berkeley Graduate Division — Writing your statements", "https://grad.berkeley.edu/admissions/application-process/writing-your-statements/"),
      ("Cornell Graduate School — Academic statement of purpose", "https://gradschool.cornell.edu/admissions/application-steps/statements-of-purpose/"),
      ("Harvard GSAS — Statement of purpose", "https://gsas.harvard.edu/apply/applying-degree-programs/statement-purpose-personal-statement-and-writing-sample"),
      ("Purdue OWL — Drafting your statement of purpose", "https://owl.purdue.edu/owl/general_writing/graduate_school_applications/graduate_school_applications_statements_of_purpose/statements_of_purpose_drafting_your_statement.html"),
  ])}
</article>
{FOOTER}
</div>"""


def motivation_body(updated):
    return f"""<div class="wrap">
{nav("/guides/")}
<article class="prose" style="max-width:100%">
  <nav class="crumbs"><a href="/guides/">গাইড ও টুল</a></nav>
  <span class="eyebrow">গাইড · সূত্র যাচাই {GUIDES_CHECKED}</span>
  <h1>Motivation Letter</h1>
  <div style="max-width:68ch;display:flex;flex-direction:column;gap:14px">
  <p class="lede">ইউরোপের বিশ্ববিদ্যালয় আর স্কলারশিপ (DAAD, Erasmus Mundus ইত্যাদি) সাধারণত Motivation Letter চায়: কেন এই বিষয়, কেন এই প্রোগ্রাম ও দেশ, আপনার প্রস্তুতি কী, আর ডিগ্রি দিয়ে কী করবেন — বিশেষ করে দেশে ফিরে। একাডেমিক SOP-এর জন্য দেখুন <a href="/guides/sop/">SOP গাইড</a>।</p>
  <h2>দৈর্ঘ্য</h2>
  <p>স্কলারশিপের নির্দেশনা দেখুন। DAAD-এর উদাহরণ: STEM study scholarship-এ ১–৩ পৃষ্ঠা, ডক্টরাল ও রিসার্চ গ্রান্টে সাধারণত ১–২ পৃষ্ঠা, Helmut Schmidt Programme-এ সর্বোচ্চ ২ পৃষ্ঠা আর তারিখসহ।</p>
  <h2>DAAD যে প্রশ্নগুলোর উত্তর চায়</h2>
  <ol class="steps">
    <li><h3>এই পড়া থেকে কী পেতে চান</h3><p>ব্যক্তিগতভাবে আর ক্যারিয়ারে — জার্মানিতে (বা গন্তব্য দেশে) পড়ার একাডেমিক ও ব্যক্তিগত কারণ।</p></li>
    <li><h3>আগের অভিজ্ঞতা কীভাবে কাজে লাগবে</h3><p>পড়াশোনা আর কাজের অভিজ্ঞতা — এই প্রোগ্রামে কীভাবে সাহায্য করবে।</p></li>
    <li><h3>কেন এই প্রোগ্রাম ও বিশ্ববিদ্যালয়</h3><p>নির্দিষ্ট কোর্স, মডিউল, গবেষণা, প্রতিষ্ঠানের কোন দিক আপনাকে টানে।</p></li>
    <li><h3>থাকার সময় লক্ষ্য</h3><p>পড়ার সময় কী শিখতে বা করতে চান। ডক্টরাল আবেদনে গবেষণা-পরিকল্পনার সংক্ষিপ্ত রূপরেখা।</p></li>
    <li><h3>দেশে ফিরে কীভাবে কাজে লাগাবেন</h3><p>যোগ্যতাটা নিজের দেশে কোথায়, কীভাবে ব্যবহার করবেন — বাস্তব ও নির্দিষ্ট।</p></li>
  </ol>
  <h2>চিঠির ফরম্যাট</h2>
  <p>Motivation Letter একটা আনুষ্ঠানিক চিঠি, তাই চিঠির কাঠামো মেনে লিখুন। পোর্টালে শুধু লেখা পেস্ট করতে বললে হেডার বাদ দিন, তবে সম্বোধন আর শেষ অংশ রাখুন।</p>
  <div class="tbl-wrap"><table class="t">
    <tr><th>অংশ</th><th>কী লিখবেন</th></tr>
    <tr><td>হেডার</td><td>আপনার নাম, ইমেইল, ফোন (চাইলে আবেদন নম্বর)</td></tr>
    <tr><td>তারিখ</td><td>যেদিন জমা দিচ্ছেন, যেমন 15 November 2026। DAAD-এর কিছু প্রোগ্রামে তারিখ বাধ্যতামূলক।</td></tr>
    <tr><td>প্রাপক</td><td>নাম ও পদবি (জানা থাকলে), Admissions Committee / Selection Committee, ডিপার্টমেন্ট, বিশ্ববিদ্যালয়, শহর</td></tr>
    <tr><td>Subject</td><td>Motivation letter — [প্রোগ্রাম/স্কলারশিপের নাম]</td></tr>
    <tr><td>সম্বোধন</td><td>নাম জানলে "Dear Prof. Müller," বা "Dear Dr. Rahman,"; না জানলে "Dear Selection Committee," — "Dear Sir/Madam" বা "To whom it may concern"-এর চেয়ে এটা ভালো</td></tr>
    <tr><td>মূল অংশ</td><td>৪–৬টি অনুচ্ছেদ (নিচে দেখুন)</td></tr>
    <tr><td>শেষ অংশ</td><td>"Yours sincerely," বা "Sincerely,", তারপর সই আর টাইপ করা পুরো নাম। চিঠিতে সবসময় সই করুন; PDF-এ স্ক্যান করা সই দিতে পারেন।</td></tr>
  </table></div>
  <h2>অনুচ্ছেদ ধরে ধরে কাঠামো</h2>
  <ol class="steps">
    <li><h3>শুরু</h3><p>কোন প্রোগ্রাম/স্কলারশিপে, কোন বিশ্ববিদ্যালয়ে আবেদন করছেন, আর এক লাইনে আপনি কে (শেষ ডিগ্রি, বিশ্ববিদ্যালয়, ফল)।</p></li>
    <li><h3>আগ্রহ কোথা থেকে</h3><p>একটা নির্দিষ্ট ঘটনা, প্রজেক্ট বা সমস্যা দিয়ে দেখান আগ্রহ কেন তৈরি হলো। "ছোটবেলা থেকেই স্বপ্ন" ধরনের সাধারণ কথা নয়।</p></li>
    <li><h3>প্রস্তুতি</h3><p>থিসিস, গবেষণা, চাকরি, ক্লাব বা প্রতিযোগিতায় নেতৃত্ব — আপনার ভূমিকা কী ছিল, ফল কী হলো।</p></li>
    <li><h3>কেন এই বিশ্ববিদ্যালয়</h3><p>নির্দিষ্ট মডিউল, ল্যাব, অধ্যাপক বা গবেষণার ধারা, যা আপনার লক্ষ্যের সাথে মেলে। প্রয়োজনে <a href="/professors/">প্রফেসর সার্চ</a> দেখুন।</p></li>
    <li><h3>ভবিষ্যৎ লক্ষ্য</h3><p>দেশে ফিরে কোথায়, কীভাবে কাজে লাগাবেন — বিশ্ববিদ্যালয়, সরকারি প্রতিষ্ঠান, নীতিনির্ধারণ বা কোনো নির্দিষ্ট SDG (যেমন SDG 2 Zero Hunger)। আন্তর্জাতিক পরিবেশে শেখা আর নেটওয়ার্কিং কীভাবে কাজে দেবে, তা-ও লিখতে পারেন।</p></li>
    <li><h3>কেন স্কলারশিপ (প্রাসঙ্গিক হলে)</h3><p>নিজে খরচ চালাতে না পারলে এক–দুই বাক্যে সৎভাবে বলুন। পুরো চিঠি আর্থিক কষ্টের গল্প বানাবেন না।</p></li>
    <li><h3>শেষ অনুচ্ছেদ</h3><p>আগ্রহ আবার বলুন, সময় দেওয়ার জন্য ধন্যবাদ দিন, আর ইন্টারভিউ বা আরও আলোচনার সুযোগের অপেক্ষায় আছেন বলে শেষ করুন।</p></li>
  </ol>
  <h2>ইন্টারনেটের নমুনা থেকে সাবধান</h2>
  <ul>
    <li>Template-এর <em>[Your Name]</em>, ভুল তারিখ বা অন্য প্রতিষ্ঠানের নাম থেকে গেলে আবেদন সরাসরি বাতিল হতে পারে — জমার আগে সব ঘর মিলিয়ে নিন।</li>
    <li>"esteemed institution", "golden opportunity", "passionate since childhood" — এমন সাধারণ বাক্য সবাই লেখে; এর বদলে নির্দিষ্ট তথ্য দিন।</li>
    <li>ছোট ব্যাকরণগত ভুল অর্থ উল্টে দেয় (যেমন "able" লিখতে গিয়ে "unable"-এর জায়গায়) — জোরে পড়ে দেখুন।</li>
    <li>জমার পর ইমেইল/পোর্টাল নিয়মিত দেখুন; ফলাফলের নির্ধারিত তারিখ পেরোলে তবেই একবার ভদ্রভাবে খোঁজ নিন।</li>
  </ul>
  <h2>যা করবেন, যা করবেন না</h2>
  <ul>
    <li>লেখার আগে প্রশ্নগুলো নিয়ে ভাবুন, নোট নিন, তারপর আউটলাইন বানান — DAAD এভাবেই বলে।</li>
    <li>শুরুতে CV আবার লিখবেন না; অলংকারপূর্ণ বা তোষামোদের ভাষা এড়ান (DAAD)।</li>
    <li>দক্ষতার নাম বলাই যথেষ্ট নয় — সেটা দিয়ে কী অর্জন করেছেন, উদাহরণ দিন। CV বা রেফারেন্স লেটার থেকে কপি করা লেখা মূল্যায়নকারীরা ধরে ফেলেন (Chevening)।</li>
    <li>Chevening তাদের প্রবন্ধে AI দিয়ে তৈরি উত্তর নিষিদ্ধ করেছে — নিজের ভাষায়, নিজের অভিজ্ঞতা দিয়ে লিখুন।</li>
    <li>শেষে আবার পড়ে অপ্রয়োজনীয় ও পুনরাবৃত্ত অংশ কেটে দিন (DAAD)।</li>
  </ul>
  </div>
  {_outline_tool("motivation")}
  {related_scholarships("Motivation Letter লাগে এমন ইউরোপীয় স্কলারশিপ", lambda s_, r: s_.startswith("europe/") and r["provider_type"] in ("government", "eu", "consortium"), 15)}
  {_sources([
      ("DAAD — Letter of motivation (instruction sheet)", "https://www2.daad.de/medien/letter_of_motivation_nawam.pdf"),
      ("DAAD — Study scholarships for STEM disciplines", "https://www2.daad.de/deutschland/stipendium/datenbank/en/21148-scholarship-database/?detail=57742130"),
      ("DAAD — Helmut Schmidt Programme FAQ", "https://static.daad.de/media/daad_de/pdfs_nicht_barrierefrei/in-deutschland-studieren-forschen-lehren/daad_helmut_schmidt_programme_frequently_asked_questions.pdf"),
      ("Chevening — Application advice", "https://www.chevening.org/news/application-advice/"),
      ("Chevening — Application criteria", "https://www.chevening.org/resource-hub/guidance/application-criteria/"),
  ])}
</article>
{FOOTER}
</div>"""


SUBJECT_BN = {
    "Computer Science / AI": "কম্পিউটার সায়েন্স / AI", "Natural Language Processing": "ন্যাচারাল ল্যাঙ্গুয়েজ প্রসেসিং (NLP)",
    "Bioinformatics": "বায়োইনফরমেটিক্স", "Cybersecurity": "সাইবার সিকিউরিটি", "Robotics": "রোবোটিক্স",
    "Electrical / Power Engineering": "ইলেকট্রিক্যাল / পাওয়ার ইঞ্জিনিয়ারিং",
    "Environmental Engineering / Water": "এনভায়রনমেন্টাল ইঞ্জিনিয়ারিং / পানি", "Public Health": "পাবলিক হেলথ",
    "Economics / Business": "অর্থনীতি / বিজনেস", "Mechanical Engineering": "মেকানিক্যাল ইঞ্জিনিয়ারিং",
    "Civil / Geotechnical Engineering": "সিভিল / জিওটেকনিক্যাল ইঞ্জিনিয়ারিং", "Agriculture / Food": "কৃষি / খাদ্য",
    "Pharmacy / Pharmaceutical Sciences": "ফার্মেসি / ফার্মাসিউটিক্যাল সায়েন্স", "Energy": "এনার্জি / নবায়নযোগ্য শক্তি",
}
COUNTRY_BN = {"Australia": "অস্ট্রেলিয়া", "Canada": "কানাডা", "China": "চীন", "Finland": "ফিনল্যান্ড", "Germany": "জার্মানি",
              "Italy": "ইতালি", "Japan": "জাপান", "Malaysia": "মালয়েশিয়া", "Netherlands": "নেদারল্যান্ডস", "Saudi Arabia": "সৌদি আরব",
              "Singapore": "সিঙ্গাপুর", "South Korea": "দক্ষিণ কোরিয়া", "Sweden": "সুইডেন", "UAE": "সংযুক্ত আরব আমিরাত",
              "United Kingdom": "যুক্তরাজ্য", "United States": "যুক্তরাষ্ট্র"}
SUPERVISOR_TIPS = [  # (countries, tip, source link) — how supervision works, from guides already on the site
    ("যুক্তরাষ্ট্র", "PhD-তে ভর্তি হয় প্রোগ্রামে, তবে ফান্ডিং (RA) প্রায়ই প্রফেসরের অনুদান থেকে আসে — ডিপার্টমেন্টের প্রফেসররাই অনেক সময় ঠিক করেন কে ফান্ডিং পাবে (EducationUSA)।", "/guides/funded-phd/"),
    ("যুক্তরাজ্য", "PhD আবেদনে গবেষণা প্রকল্প আর সম্ভাব্য সুপারভাইজার ঠিক করা আবেদনের অংশ — আগে যোগাযোগ করুন (Oxford, Cambridge)।", "/guides/professor-email/"),
    ("জার্মানি", "DAAD-এর ডক্টরাল স্কলারশিপে গবেষণা প্রস্তাব জার্মানির সম্ভাব্য সুপারভাইজারের সাথে আলোচনা করে লিখতে হয়।", "/guides/research-proposal/"),
    ("সুইডেন, নেদারল্যান্ডস, নরওয়ে, ডেনমার্ক", "PhD সাধারণত বেতনভুক্ত চাকরি — বিজ্ঞপ্তি দেখে আবেদন (EURAXESS, বিশ্ববিদ্যালয়ের vacancy পেজ); বিজ্ঞপ্তির যোগাযোগ-ব্যক্তিকে প্রশ্ন করা যায়।", "/guides/funded-phd/"),
    ("কানাডা", "অনেক বিশ্ববিদ্যালয়ে PhD-র ন্যূনতম ফান্ডিং নিশ্চিত, যার একটা অংশ আসে সুপারভাইজার বা প্রোগ্রাম থেকে (UBC) — তাই সম্ভাব্য সুপারভাইজারের সাথে আগে কথা বলা কাজে লাগে।", "/guides/funded-phd/"),
    ("মালয়েশিয়া", "Universiti Malaya-র GRAS-এর মতো সহায়তায় আগে সুপারভাইজারের সাথে যোগাযোগ করে তাঁর শর্ত পূরণ করতে হয়।", "/asia/malaysia/"),
    ("জাপান", "MEXT গবেষণা-শিক্ষার্থী আবেদনে গবেষণা পরিকল্পনা আর পছন্দের বিশ্ববিদ্যালয়ের তালিকা জমা দিতে হয় — যে ল্যাবে যেতে চান তার প্রফেসরের কাজ আগে দেখে নিন।", "/asia/japan/"),
]


def professors_body(updated):
    import csv
    rows = list(csv.DictReader(open(pathlib.Path(__file__).resolve().parent.parent / "data" / "professors" / "professors.csv", encoding="utf-8")))
    data = [{"n": r["name"], "t": r["title"], "u": r["university"], "c": r["country"], "d": r["department"],
             "s": r["subject"], "r": r["research_interests"], "p": r["profile_url"], "x": r["directory_url"],
             "cs": next((f"/{k}/" for k, v in COUNTRIES.items() if v[0] == {"UAE": "United Arab Emirates"}.get(r["country"], r["country"])), "")} for r in rows]
    ctry = sorted({r["country"] for r in rows})
    c_opts = "".join(f'<option value="{html.escape(c)}">{html.escape(COUNTRY_BN.get(c, c))} ({bn(sum(r["country"] == c for r in rows))})</option>' for c in ctry)
    tips = "".join(f'<li><b>{c}:</b> {t} <a href="{h}">আরও →</a></li>' for c, t, h in SUPERVISOR_TIPS)
    subj = sorted({r["subject"] for r in rows})
    unis = sorted({r["university"] for r in rows})
    s_opts = "".join(f'<option value="{html.escape(s)}">{html.escape(SUBJECT_BN.get(s, s))}</option>' for s in subj)
    u_opts = "".join(f'<option value="{html.escape(u)}">{html.escape(u)}</option>' for u in unis)
    chips = "".join(f'<button type="button" class="chip" data-s="{html.escape(s)}">{html.escape(SUBJECT_BN.get(s, s))} '
                    f'<small>{bn(sum(r["subject"] == s for r in rows))}</small></button>' for s in subj)
    dirs = {}
    for r in rows:
        dirs.setdefault(r["country"], {}).setdefault((r["university"], r["department"]), r["directory_url"])
    dir_list = "".join(f'<li><b>{html.escape(COUNTRY_BN.get(c, c))}:</b> ' + " · ".join(
        f'<a href="{html.escape(x)}" target="_blank" rel="noopener">{html.escape(u)} — {html.escape(d)}</a>' for (u, d), x in sorted(dirs[c].items())) + "</li>"
        for c in sorted(dirs))
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    script = """<script>
var DATA = __DATA__;
(function(){
  var esc=function(s){return String(s).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})};
  var bn=function(n){return String(n).replace(/\\d/g,function(d){return "০১২৩৪৫৬৭৮৯"[d]})};
  var q=document.getElementById("q"),sj=document.getElementById("subj"),un=document.getElementById("uni"),ct=document.getElementById("ctry"),out=document.getElementById("out"),cnt=document.getElementById("cnt");
  function render(){
    var s=q.value.trim().toLowerCase();
    var rows=DATA.filter(function(r){
      if(sj.value&&r.s!==sj.value)return false;
      if(un.value&&r.u!==un.value)return false;
      if(ct.value&&r.c!==ct.value)return false;
      return !s||[r.n,r.t,r.u,r.c,r.d,r.s,r.r].join(" ").toLowerCase().indexOf(s)>=0;
    });
    document.querySelectorAll(".chip").forEach(function(b){b.classList.toggle("on",b.dataset.s===sj.value)});
    cnt.textContent=bn(rows.length)+" জন প্রফেসর";
    if(!rows.length){out.innerHTML='<p class="empty">কাউকে পাওয়া যায়নি। অন্য শব্দ দিয়ে খুঁজুন বা ফিল্টার সরান।</p>';return}
    out.innerHTML=rows.map(function(r){
      return '<article class="res"><span class="where">'+esc(r.u)+' · '+esc(r.c)+'</span><h3>'+esc(r.n)+'</h3>'+
        '<p>'+esc(r.t)+' · '+esc(r.d)+'</p>'+
        '<p><b>গবেষণার বিষয়:</b> '+esc(r.r)+'</p>'+
        '<div class="row">'+(r.p?'<a class="apply" href="'+esc(r.p)+'" target="_blank" rel="noopener">অফিসিয়াল প্রোফাইল ↗</a>':'')+
        '<a class="'+(r.p?'more':'apply info')+'" href="'+esc(r.x)+'" target="_blank" rel="noopener">ফ্যাকাল্টি তালিকা ↗</a>'+(r.cs?'<a class="more" href="'+r.cs+'">এই দেশের স্কলারশিপ</a>':'')+'</div></article>';
    }).join("");
  }
  [q,sj,un,ct].forEach(function(el){el.addEventListener("input",render);el.addEventListener("change",render)});
  document.querySelectorAll(".chip").forEach(function(b){b.addEventListener("click",function(){sj.value=sj.value===b.dataset.s?"":b.dataset.s;render()})});
  render();
})();
</script>""".replace("__DATA__", payload)
    return f"""<style>
.chips{{display:flex;flex-wrap:wrap;gap:8px}}
.chip{{font:inherit;font-size:14px;cursor:pointer;border:1px solid var(--line);background:var(--surface);color:var(--fg);border-radius:999px;padding:6px 12px}}
.chip small{{color:var(--muted)}}.chip.on{{background:var(--accent);color:var(--surface);border-color:var(--accent)}}.chip.on small{{color:inherit}}
</style>
<div class="wrap">
{nav("/professors/")}
<header style="display:flex;flex-direction:column;gap:10px">
  <span class="eyebrow">প্রফেসর সার্চ · {bn(len(rows))} জন · {bn(len(unis))}টি বিশ্ববিদ্যালয় · {bn(len(ctry))}টি দেশ</span>
  <h1>প্রফেসর খুঁজুন — বিষয় ও ডিপার্টমেন্ট অনুযায়ী</h1>
  <p class="lede">MS/PhD-র জন্য সুপারভাইজার খুঁজতে: নাম, বিশ্ববিদ্যালয়, ডিপার্টমেন্ট বা গবেষণার বিষয় (যেমন “machine learning”, “dengue”, “desalination”) লিখে খুঁজুন। প্রতিটি নাম বিশ্ববিদ্যালয়ের অফিসিয়াল পেজ থেকে নেওয়া; যোগাযোগের ঠিকানা ওই প্রোফাইলেই পাবেন।</p>
</header>
<div class="chips" aria-label="বিষয়">{chips}</div>
<div class="filters" role="search">
  <input id="q" type="search" placeholder="যেমন: machine learning, NUS, epidemiology" aria-label="খুঁজুন">
  <select id="subj" aria-label="বিষয়"><option value="">সব বিষয়</option>{s_opts}</select>
  <select id="ctry" aria-label="দেশ"><option value="">সব দেশ</option>{c_opts}</select>
  <select id="uni" aria-label="বিশ্ববিদ্যালয়"><option value="">সব বিশ্ববিদ্যালয়</option>{u_opts}</select>
  <span class="count" id="cnt"></span>
</div>
<section class="results" id="out"><p class="empty">তালিকা লোড হচ্ছে…</p></section>
<h2>প্রফেসরকে ইমেইল করার আগে <small class="meta"><a href="/guides/professor-email/">— পূর্ণ গাইড</a></small></h2>
<ul>
  <li>প্রোফাইল আর সাম্প্রতিক ২–৩টি পেপার পড়ুন; ইমেইলে নির্দিষ্ট করে লিখুন তাঁর কোন কাজের সঙ্গে আপনার আগ্রহ মেলে।</li>
  <li>ছোট রাখুন (১৫০–২৫০ শব্দ), CV সংযুক্ত করুন, বিষয়ের লাইনে লিখুন কোন প্রোগ্রাম/সেশনের জন্য।</li>
  <li>সবাইকে একই কপি-পেস্ট ইমেইল পাঠাবেন না; উত্তর না এলে ৩–৪ সপ্তাহ পর একবার ভদ্রভাবে মনে করিয়ে দিন (Edinburgh)।</li>
  <li>অনেক বিশ্ববিদ্যালয়ে (যেমন ইউরোপের অনেক Master's) আগে প্রফেসরকে ইমেইল করা লাগে না — প্রোগ্রামের অফিসিয়াল নির্দেশনা দেখুন।</li>
</ul>
<h2>দেশভিত্তিক: সুপারভাইজার কখন, কীভাবে</h2>
<ul>{tips}</ul>
<h2>নিজে আরও প্রফেসর খুঁজবেন যেভাবে</h2>
<ul>
  <li>লক্ষ্য বিশ্ববিদ্যালয়ের ডিপার্টমেন্ট → "People" / "Faculty" পেজ → গবেষণা গ্রুপ বা ল্যাবের পেজ।</li>
  <li>ইউরোপে বেতনসহ PhD পদ: ইউরোপীয় কমিশনের <a href="https://euraxess.ec.europa.eu/jobs/search" target="_blank" rel="noopener">EURAXESS Jobs</a>।</li>
  <li>আগ্রহের বিষয়ের সাম্প্রতিক পেপারের লেখকদের তালিকা দেখুন — যাঁরা নিয়মিত লেখেন, তাঁদের প্রোফাইল খুলুন।</li>
  <li>তালিকায় নিজের বিষয় না পেলে জানান: <a href="mailto:higherstudyinfo30@gmail.com">higherstudyinfo30@gmail.com</a> — প্রতি সপ্তাহে নতুন বিশ্ববিদ্যালয় যোগ হয়।</li>
</ul>
<h2>পূর্ণ ফ্যাকাল্টি তালিকা (অফিসিয়াল) — দেশ অনুযায়ী</h2>
<ul class="src-list">{dir_list}</ul>
<p class="vsrc">পদবি ও গবেষণার বিষয় অফিসিয়াল পেজের সার্চ-স্নিপেট থেকে নেওয়া, সংগ্রহ: {html.escape(rows[0]["collected_on"])}। পদবি বদলে যেতে পারে — যোগাযোগের আগে প্রোফাইলে মিলিয়ে নিন। স্প্যাম এড়াতে এখানে কোনো ইমেইল বা ফোন নম্বর রাখা হয়নি।</p>
{FOOTER}
</div>
{script}"""


def _ielts_min(t):
    m = re.search(r"IELTS[^0-9;]{0,25}?(\d(?:\.\d)?)\b", t)
    return float(m.group(1)) if m and 4 <= float(m.group(1)) <= 9 else None


def _age_limits(t):
    rng = re.findall(r"[Aa]ge[^0-9]{0,4}\d{2}\s*[–-]\s*(\d{2})", t)
    caps = re.findall(r"(?:≤|<|under|not more than|up to|below)\s*(\d{2})\b", t, re.I)
    return sorted({int(x) for x in rng + caps if 17 <= int(x) <= 60})


def _cgpa_min(t):
    m = re.search(r"(?:CGPA|GPA)[^0-9;]{0,12}?(\d\.\d{1,2})", t)
    return float(m.group(1)) if m else None


def eligibility_body(updated):
    data = []
    for r in all_rows():
        e, el = r.get("english_requirement", ""), r.get("eligibility", "")
        data.append({"n": r["scholarship_name"], "c": COUNTRIES[r["slug"]][0], "s": r["section"], "bd": r["slug"] == "asia/bangladesh",
                     "l": r["level"], "d": r.get("deadline", ""), "u": r["page"], "e": e, "el": el,
                     "im": _ielts_min(e), "wv": bool(re.search(WAIVER_RE, e, re.I)), "ag": _age_limits(el), "cg": _cgpa_min(el),
                     "w": r.get("session_year", "").startswith("Next round")})
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    script = """<script>
var DATA = __DATA__;
(function(){
  var esc=function(s){return String(s).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})};
  var bn=function(n){return String(n).replace(/\\d/g,function(d){return "০১২৩৪৫৬৭৮৯"[d]})};
  var t=new Date();var today=t.getFullYear()+"-"+String(t.getMonth()+1).padStart(2,"0")+"-"+String(t.getDate()).padStart(2,"0");
  function lvl(l,f){if(f==="UG")return /\\bUG\\b|Diploma/.test(l);if(f==="PG")return /PG|Masters|MS|MA|MPhil|MSc/.test(l);if(f==="PhD")return /PhD|Postdoc/.test(l);return true}
  var $=function(id){return document.getElementById(id)};
  function check(r,f){
    var why=[];
    if(r.d&&r.d<today)return null;
    if(f.where==="abroad"&&r.bd||f.where==="bd"&&!r.bd)return null;
    if(!lvl(r.l,f.lv))return null;
    if(r.bd){}else if(f.ielts===null){
      if(r.im!==null&&!r.wv)return null;
      if(r.wv)why.push("IELTS ছাড়ের পথ আছে — শর্ত মিলিয়ে নিন");
      else if(r.im===null)why.push("ইংরেজির শর্ত সূত্রে স্পষ্ট নয়");
    }else if(r.im!==null&&f.ielts<r.im){
      if(!r.wv)return null;
      why.push("IELTS "+bn(r.im)+" লাগে, তবে ছাড়ের পথ আছে");
    }else if(r.im===null&&!r.wv)why.push("ইংরেজির শর্ত সূত্রে স্পষ্ট নয়");
    if(f.age&&r.ag.length){
      if(f.age>Math.max.apply(null,r.ag))return null;
      if(f.age>Math.min.apply(null,r.ag))why.push("বয়সসীমা লেভেলভেদে আলাদা — শর্ত দেখুন");
    }
    if(f.cg&&r.cg&&f.cg<r.cg)why.push("CGPA "+bn(r.cg)+" চাওয়া হতে পারে");
    if(r.w)why.push("পরের রাউন্ড এখনো ঘোষণা হয়নি");
    return why;
  }
  function run(){
    var iv=$("e-ielts").value.trim(),f={where:$("e-where").value,lv:$("e-lvl").value,ielts:$("e-noielts").checked?null:(iv?+iv:9),
      age:+$("e-age").value||0,cg:+$("e-cg").value||0};
    $("e-ielts").disabled=$("e-noielts").checked;
    var ok=[],maybe=[];
    DATA.forEach(function(r){var w=check(r,f);if(w===null)return;(w.length?maybe:ok).push([r,w])});
    function li(x){var r=x[0];return '<li><a href="'+r.u+'">'+esc(r.n)+'</a> <span class="meta">· '+esc(r.c)+' · '+esc(r.l)+(r.d?' · শেষ তারিখ '+esc(r.d):'')+'</span>'+(x[1].length?'<br><small class="why">'+x[1].map(esc).join(" · ")+'</small>':'')+'</li>'}
    $("e-ok").innerHTML=ok.length?ok.map(li).join(""):'<li class="meta">এই তথ্যে সরাসরি মেলে এমন কিছু পাওয়া যায়নি।</li>';
    $("e-maybe").innerHTML=maybe.length?maybe.map(li).join(""):'<li class="meta">—</li>';
    $("e-n1").textContent=bn(ok.length);$("e-n2").textContent=bn(maybe.length);
  }
  ["e-where","e-lvl","e-ielts","e-noielts","e-age","e-cg"].forEach(function(id){$(id).addEventListener("input",run);$(id).addEventListener("change",run)});
  run();
})();
</script>""".replace("__DATA__", payload)
    return f"""<style>
.elist{{display:flex;flex-direction:column;gap:10px;padding-left:20px;margin:0}}.elist a{{color:var(--accent);font-weight:600}}
.why{{color:var(--muted)}}.calc select{{font:inherit;font-size:16px;color:var(--fg);background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:8px 10px;width:100%}}
.calc .chk{{flex-direction:row;align-items:center;justify-content:flex-start;gap:8px}}.calc .chk input{{width:auto}}
</style>
<div class="wrap">
{nav("/guides/")}
<article class="prose" style="max-width:100%">
  <nav class="crumbs"><a href="/guides/">গাইড ও টুল</a></nav>
  <span class="eyebrow">টুল · সর্বশেষ যাচাই {CHECKED}</span>
  <h1>কোন স্কলারশিপে আমি যোগ্য?</h1>
  <p class="lede">লেভেল, IELTS, বয়স আর CGPA দিন — তালিকার কোন স্কলারশিপগুলো আপনার সাথে মেলে তা দেখাবে। হিসাব হয় শুধু আপনার ব্রাউজারে; কিছুই পাঠানো বা সংরক্ষণ হয় না।</p>
  <div class="calc">
    <label>কোথায় পড়তে চান<select id="e-where"><option value="abroad">বিদেশে</option><option value="bd">বাংলাদেশে</option><option value="">দুটোই</option></select></label>
    <label>লেভেল<select id="e-lvl"><option value="PG">মাস্টার্স</option><option value="PhD">PhD / Postdoc</option><option value="UG">স্নাতক (UG)</option></select></label>
    <label>IELTS ওভারঅল স্কোর<input id="e-ielts" type="number" min="4" max="9" step="0.5" placeholder="যেমন 6.5"></label>
    <label class="chk"><input id="e-noielts" type="checkbox"> IELTS নেই / দিইনি</label>
    <label>বয়স (বছর)<input id="e-age" type="number" min="15" max="70" placeholder="যেমন 26"></label>
    <label>CGPA (৪-এর মধ্যে)<input id="e-cg" type="number" min="0" max="4" step="0.01" placeholder="যেমন 3.40"></label>
  </div>
  <h2>✅ মিলছে (<span id="e-n1"></span>)</h2>
  <ul class="elist" id="e-ok"></ul>
  <h2>⚠️ শর্তসাপেক্ষে — যাচাই করুন (<span id="e-n2"></span>)</h2>
  <ul class="elist" id="e-maybe"></ul>
  <p class="warn">এটা প্রাথমিক ছাঁকনি মাত্র। শর্তগুলো অফিসিয়াল সূত্রের লেখা থেকে স্বয়ংক্রিয়ভাবে পড়া হয়েছে; নাগরিকত্ব, বিষয়, কাজের অভিজ্ঞতা, জন্মতারিখের মতো শর্ত এখানে ধরা হয়নি। IELTS ফাঁকা রাখলে ধরে নেওয়া হয় স্কোর কোনো বাধা নয়। আবেদনের আগে প্রতিটি স্কলারশিপের পেজ খুলে শর্ত মিলিয়ে নিন।</p>
</article>
{FOOTER}
</div>
{script}"""


def _guide(path_title, h1, lede, inner, sources, extra=""):
    return f"""<div class="wrap">
{nav("/guides/")}
<article class="prose" style="max-width:100%">
  <nav class="crumbs"><a href="/guides/">গাইড ও টুল</a></nav>
  <span class="eyebrow">গাইড · সূত্র যাচাই 2026-11-05</span>
  <h1>{h1}</h1>
  <div style="max-width:68ch;display:flex;flex-direction:column;gap:14px">
  <p class="lede">{lede}</p>
  {inner}
  </div>
  {extra}
  {_sources(sources)}
</article>
{FOOTER}
</div>"""


def lor_body(updated):
    return _guide("lor", "Recommendation Letter (LOR)",
        "বেশিরভাগ মাস্টার্স/PhD আবেদন আর স্কলারশিপে ২–৩টি রেকমেন্ডেশন লেটার লাগে। চিঠিটা লেখেন শিক্ষক বা সুপারভাইজার — আপনার কাজ হলো ঠিক মানুষকে, ঠিক সময়ে, ঠিকভাবে অনুরোধ করা।",
        """<h2>কাকে বলবেন</h2>
  <ul>
    <li>যিনি আপনাকে ভালোভাবে চেনেন এবং নির্দিষ্ট উদাহরণ দিতে পারবেন — থিসিস সুপারভাইজার, যাঁর কোর্সে ভালো করেছেন বা যাঁর সাথে প্রজেক্ট/গবেষণা করেছেন (UCLA)।</li>
    <li>আপনি যে বিষয়ে পড়তে চান সেই বিষয়ের শিক্ষক হলে ভালো। বড় পদবির কিন্তু আপনাকে না চেনা কারও চেয়ে চেনা শিক্ষকের নির্দিষ্ট চিঠি বেশি কাজের।</li>
    <li>চাকরি করলে একটি চিঠি সরাসরি সুপারভাইজারের কাছ থেকে নেওয়া যায় — প্রোগ্রাম কী চায় দেখে নিন।</li>
    <li>শিক্ষকেরা সাধারণত চিঠিতে আপনার কোর্সের গ্রেড উল্লেখ করেন, তাই কাকে বলবেন সাবধানে ঠিক করুন (Berkeley)।</li>
  </ul>
  <h2>কীভাবে অনুরোধ করবেন</h2>
  <ol class="steps">
    <li><h3>আগেভাগে বলুন</h3><p>অন্তত কয়েক সপ্তাহ, সম্ভব হলে ২–৩ মাস আগে (Cornell, UCLA)। স্কলারশিপের শেষ তারিখের ঠিক আগে বললে ভালো চিঠি আশা করা কঠিন।</p></li>
    <li><h3>সরাসরি দেখা করে জিজ্ঞেস করুন</h3><p>পরিকল্পনা বুঝিয়ে বলুন, আর জিজ্ঞেস করুন তিনি একটা <em>strong</em> চিঠি লিখতে পারবেন কিনা। দ্বিধা করলে বা "neutral" চিঠির কথা বললে ধন্যবাদ দিয়ে অন্য কাউকে বলুন (Berkeley, Cornell)।</p></li>
    <li><h3>প্রয়োজনীয় কাগজ দিন</h3><p>CV, ট্রান্সক্রিপ্ট, SOP/Motivation Letter-এর খসড়া, প্রোগ্রাম ও স্কলারশিপের তালিকা — শেষ তারিখসহ, সবচেয়ে আগেরটা উপরে — আর তাঁর সাথে করা কাজের ছোট সারাংশ (Cornell, UCLA)।</p></li>
    <li><h3>জমা দেওয়ার পদ্ধতি জানিয়ে দিন</h3><p>বেশিরভাগ পোর্টাল রেফারির ইমেইলে লিংক পাঠায়। তাঁর অফিসিয়াল (বিশ্ববিদ্যালয়ের) ইমেইল ঠিকানা দিন, আর জানিয়ে রাখুন কবে লিংক যাবে।</p></li>
    <li><h3>ভদ্রভাবে মনে করিয়ে দিন, তারপর ধন্যবাদ</h3><p>শেষ তারিখের ১–২ সপ্তাহ আগে একবার মনে করিয়ে দিন, কিন্তু বারবার চাপ দেবেন না। ফলাফল পেলে জানিয়ে ধন্যবাদ দিন (Cornell, UCLA)।</p></li>
  </ol>
  <h2>জরুরি সতর্কতা</h2>
  <ul>
    <li><b>নিজে চিঠি লিখে শিক্ষকের সই নেবেন না।</b> অনেক প্রোগ্রাম রেফারির অফিসিয়াল ইমেইল থেকে সরাসরি চিঠি চায়; নিজের লেখা ধরা পড়লে আবেদন বাতিল হতে পারে।</li>
    <li>আবেদন ফর্মে "চিঠি দেখার অধিকার ছেড়ে দেওয়া" (waive) অপশন থাকলে সাধারণত ছেড়ে দেওয়াই ভালো — কমিটি এমন চিঠিকে বেশি বিশ্বাসযোগ্য মনে করতে পারে (Harvard GSAS)।</li>
    <li>রেফারিদের সাথে আগেই কথা বলে নিন যে তাঁদের ইমেইলে লিংক যাবে — না জানলে স্প্যাম ফোল্ডারে পড়ে থাকতে পারে।</li>
  </ul>""",
        [("Cornell Graduate School — Requesting letters of recommendation", "https://gradschool.cornell.edu/inclusion/recruitment/prospective-students/requesting-letters-of-recommendation/"),
         ("UCLA — Asking your faculty for a letter of recommendation (PDF)", "https://grad.ucla.edu/asis/agep/advltrrec.pdf"),
         ("UC Berkeley — Preparing your application for graduate school", "https://grad.berkeley.edu/graduate-diversity/prospective-grad-students/preparing-your-application-for-graduate-school/"),
         ("Harvard GSAS — Right to inspect letters of recommendation", "https://gsas.harvard.edu/apply/degree-programs/completing-your-application/letters-recommendation/right-inspect-letters")],
        related_scholarships("রেফারেন্স লেটার লাগে এমন সরকারি স্কলারশিপ", lambda s_, r: r["provider_type"] == "government" and not s_.startswith("asia/bangladesh"), 15))


def proposal_body(updated):
    return _guide("proposal", "Research Proposal লেখা",
        "PhD আবেদন আর DAAD-এর মতো গবেষণা স্কলারশিপে Research Proposal সবচেয়ে গুরুত্বপূর্ণ কাগজ: কী গবেষণা করবেন, কেন, কীভাবে, আর কত সময়ে। মালয়েশিয়ার MIS-এর মতো কিছু স্কলারশিপ Master's by Research-এও এটা চায়।",
        """<h2>দৈর্ঘ্য</h2>
  <p>স্কলারশিপের ঘোষণাই আগে দেখুন। DAAD-এর ডক্টরাল ও রিসার্চ গ্রান্টে বিশেষ নির্দেশনা না থাকলে <b>সর্বোচ্চ ১০ পৃষ্ঠা</b>, আর সময়সূচি আলাদা পাতায়। MIS (মালয়েশিয়া) গবেষণা ডিগ্রির জন্য কমপক্ষে ১,০০০ শব্দ চায়। DAAD-এর একটি পুরোনো নির্দেশিকা বলে, সাধারণত প্রস্তাব ৪–১৫ পৃষ্ঠার হয়, আর ১,৫০০ শব্দের কমে পূর্ণাঙ্গ প্রস্তাব লেখা কঠিন।</p>
  <h2>কাঠামো</h2>
  <ol class="steps">
    <li><h3>শিরোনাম ও সারাংশ</h3><p>নির্দিষ্ট, বর্ণনামূলক শিরোনাম; ১৫০–২৫০ শব্দে পুরো প্রস্তাবের সারকথা।</p></li>
    <li><h3>গবেষণার ক্ষেত্র ও বর্তমান অবস্থা</h3><p>বিষয়টি নিয়ে এখন পর্যন্ত কী জানা আছে, কোন তত্ত্ব বা আগের কাজের উপর দাঁড়াবেন — DAAD এটা স্পষ্ট করে চায়।</p></li>
    <li><h3>গবেষণার ফাঁক ও প্রশ্ন</h3><p>কী জানা নেই, আর আপনার ২–৩টি নির্দিষ্ট গবেষণা প্রশ্ন বা লক্ষ্য।</p></li>
    <li><h3>পদ্ধতি (Methodology)</h3><p>ডেটা কোথা থেকে, কীভাবে সংগ্রহ ও বিশ্লেষণ করবেন, কোন যন্ত্র/সফটওয়্যার/ল্যাব লাগবে। DAAD বলে এটা খুব গুরুত্বপূর্ণ এবং প্রায়ই সবচেয়ে দীর্ঘ অংশ।</p></li>
    <li><h3>সময়সূচি</h3><p>টেবিল আকারে ধাপ আর প্রতিটির সময় — DAAD আলাদা পাতায় চায়।</p></li>
    <li><h3>প্রত্যাশিত ফল ও গুরুত্ব</h3><p>গবেষণা থেকে কী পাওয়া যাবে, বিজ্ঞান আর আপনার দেশের জন্য কেন গুরুত্বপূর্ণ।</p></li>
    <li><h3>তথ্যসূত্র</h3><p>যেসব কাজ উল্লেখ করেছেন তার পূর্ণ তালিকা, একটি নির্দিষ্ট রেফারেন্স স্টাইলে।</p></li>
  </ol>
  <h2>যা মনে রাখবেন</h2>
  <ul>
    <li>প্রস্তাব নিজে লিখুন। DAAD বলে প্রস্তাবটি আবেদনকারীর নিজের তৈরি এবং জার্মানির সম্ভাব্য সুপারভাইজারের সাথে আলোচনা করা হতে হবে।</li>
    <li>সম্ভাব্য সুপারভাইজারের সাম্প্রতিক কাজ পড়ে তাঁর গবেষণার সাথে মিল দেখান — <a href="/professors/">প্রফেসর সার্চ</a> আর <a href="/guides/professor-email/">প্রফেসরকে ইমেইল</a> গাইড দেখুন।</li>
    <li>যা করতে পারবেন না তার প্রতিশ্রুতি দেবেন না; সময় ও সম্পদের মধ্যে বাস্তবসম্মত প্রশ্ন বাছুন।</li>
    <li>বিজ্ঞান ও প্রকৌশলে অনেক সময় সুপারভাইজারের চলমান প্রজেক্টে যোগ দেওয়াই রীতি, সেখানে পূর্ণ প্রস্তাবের চেয়ে মিলটা বেশি গুরুত্বপূর্ণ; মানবিক ও সামাজিক বিজ্ঞানে পূর্ণাঙ্গ প্রস্তাব বেশি প্রত্যাশিত (UCL)।</li>
  </ul>""",
        [("DAAD — Doctoral Programmes in Germany (application requirements)", "https://www2.daad.de/deutschland/stipendium/datenbank/en/21148-scholarship-database/?detail=57135739"),
         ("DAAD — Research Grants in Germany", "https://www2.daad.de/deutschland/stipendium/datenbank/en/21148-scholarship-database/?detail=57742121"),
         ("DAAD — How to develop a research project and write a research proposal (PDF)", "https://static.daad.de/media/daad_de/der-daad/was-wir-tun/guideline_research_proposal_2015.pdf"),
         ("MoHE Malaysia — MIS 2026 guidelines (PDF)", "https://biasiswa.mohe.gov.my/INTER/doc/MIS/Guidelines%20MIS%202026.pdf"),
         ("UCL — Guidance on contacting potential supervisors (PDF)", "https://www.ucl.ac.uk/arts-humanities/sites/arts_humanities/files/2025-12/guidance_on_how_to_contact_potential_supervisors_for_phd%20(1).pdf")],
        related_scholarships("Research Proposal লাগতে পারে এমন PhD / গবেষণা স্কলারশিপ", lambda s_, r: bool(re.search(r"PhD|Postdoc", r["level"])), 15))


def prof_email_body(updated):
    skeleton = """Subject: Prospective PhD applicant — [your topic] ([intake, e.g. Fall 2027])

Dear Prof. [Surname],

[1–2 sentences] Who you are: degree, university, result.
[2–3 sentences] Which of their papers/projects you read and the specific
  link to your own interest or experience.
[1–2 sentences] What you would like to work on, and your relevant skill.
[1 sentence] Funding: the scholarship you are applying for (e.g. DAAD) or
  whether you need a funded position.
[1 sentence] Ask: are they taking new PhD students for [intake]?

CV attached (and a short proposal, if you have one).

Yours sincerely,
[Full name] · [university email] · [profile/Google Scholar link]"""
    return _guide("professor-email", "প্রফেসরকে ইমেইল করা",
        "PhD আর অনেক গবেষণা-মাস্টার্সে আবেদনের আগে সম্ভাব্য সুপারভাইজারের সাথে যোগাযোগ করতে হয় — DAAD-এর কিছু স্কলারশিপে সুপারভাইজারের সম্মতিপত্রও লাগে। ভালো ইমেইল ছোট, নির্দিষ্ট আর একজনের জন্যই লেখা।",
        f"""<h2>পাঠানোর আগে</h2>
  <ul>
    <li>ডিপার্টমেন্টের ওয়েবসাইট থেকে প্রফেসর খুঁজুন, দেখুন তিনি নতুন ছাত্র নিচ্ছেন কিনা, আর তাঁর সাম্প্রতিক ২–৩টি পেপার পড়ুন (Oxford, Cambridge)। শুরু করতে পারেন আমাদের <a href="/professors/">প্রফেসর সার্চ</a> থেকে।</li>
    <li>প্রতিটি ইমেইল আলাদা করে লিখুন। একই ইমেইল অনেককে পাঠালে সাধারণত কাজ হয় না (Cambridge)।</li>
    <li>সময় দিন: আবেদনের শেষ তারিখের অনেক আগে, সম্ভব হলে কয়েক মাস আগে যোগাযোগ করুন।</li>
  </ul>
  <h2>ইমেইলের কাঠামো</h2>
  <pre class="ooutput">{html.escape(skeleton)}</pre>
  <p class="meta">এটা কাঠামো মাত্র — নিজের ভাষায়, নিজের তথ্য দিয়ে লিখুন। ১৫০–২৫০ শব্দের মধ্যে রাখার চেষ্টা করুন।</p>
  <h2>যা করবেন, যা করবেন না</h2>
  <ul>
    <li>বিষয়ের লাইনে উদ্দেশ্য স্পষ্ট করুন, যেমন "Enquiry about potential PhD application" (Cambridge)।</li>
    <li>নাম, পদবি আর বানান দুবার মিলিয়ে নিন। "Dear Sir" নয়, "Dear Prof. [Surname]"।</li>
    <li>CV আর থাকলে ছোট প্রস্তাব সংযুক্ত করুন; ফাইল ছোট রাখুন আর পরিষ্কার নাম দিন (যেমন <em>Rahman_CV.pdf</em>) — বড় বা অনেক ফাইল স্প্যামে যেতে পারে।</li>
    <li>কীভাবে খরচ চালাবেন (কোন স্কলারশিপ, নাকি ফান্ডেড পজিশন খুঁজছেন) স্পষ্ট বলুন (Cambridge)।</li>
    <li>অনেকে উত্তর দেন না — এটা স্বাভাবিক। Edinburgh ৩–৪ সপ্তাহ অপেক্ষা করে তারপর একবার ভদ্রভাবে ফলো-আপ করতে বলে।</li>
    <li>না বললে ধন্যবাদ দিন, আর জিজ্ঞেস করতে পারেন অন্য কোনো সহকর্মী আপনার বিষয়ে আগ্রহী হতে পারেন কিনা।</li>
    <li>অনেক মাস্টার্স প্রোগ্রামে (বিশেষ করে ইউরোপের কোর্সভিত্তিক মাস্টার্সে) প্রফেসরকে ইমেইল করার দরকার নেই — প্রোগ্রামের নির্দেশনা দেখুন।</li>
  </ul>""",
        [("University of Cambridge BBSRC DTP — Contacting a potential PhD supervisor", "https://bbsrcdtp.lifesci.cam.ac.uk/contacting-potential-phd-supervisor-quick-guide"),
         ("University of Cambridge — Find a supervisor", "https://www.postgraduate.study.cam.ac.uk/apply/before/find-supervisor"),
         ("University of Oxford — Research project and supervisor", "https://www.ox.ac.uk/admissions/graduate/application-guide/starting-your-application/research-project-and-supervisor"),
         ("University of Edinburgh Business School — Find a supervisor", "https://www.business-school.ed.ac.uk/phd/find-a-supervisor"),
         ("UCL — Guidance on how to contact potential supervisors (PDF)", "https://www.ucl.ac.uk/arts-humanities/sites/arts_humanities/files/2025-12/guidance_on_how_to_contact_potential_supervisors_for_phd%20(1).pdf")],
        related_scholarships("সুপারভাইজারের সাথে যোগাযোগ কাজে লাগবে এমন PhD স্কলারশিপ", lambda s_, r: bool(re.search(r"PhD|Postdoc", r["level"])), 15))


# ---- Internal links -------------------------------------------------------------------------
VISA_IDS = {v["c"]: v["c"].lower().replace(" ", "-") for v in VISA}
TUITION_FREE = {"Germany", "Austria", "France", "Norway"}
LINK_CSS = """<style>
.rel{display:flex;flex-direction:column;gap:10px;max-width:820px}
.rel h2{font-size:20px;margin:6px 0 0}.rel ul{margin:0;padding-left:20px;display:flex;flex-direction:column;gap:4px}
.rel a{color:var(--accent)}.rel .tags{list-style:none;padding:0;flex-direction:row;flex-wrap:wrap;gap:8px}
.rel .tags a{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:4px 12px;text-decoration:none;background:var(--surface);font-size:14px}
</style>"""


def _rows_with_pages(pred=lambda slug, r: True):
    out = []
    for slug in COUNTRIES:
        for i, r in enumerate(load_rows(slug)):
            if (slug, i) in PAGES and pred(slug, r):
                out.append((slug, i, r))
    return out


def sch_link(slug, i, r, extra=True):
    meta = f' <span class="meta">· {html.escape(COUNTRIES[slug][0])} · {html.escape(r["level"])}</span>' if extra else ""
    return f'<li><a href="/scholarship/{PAGES[(slug, i)]}/">{html.escape(r["scholarship_name"])}</a>{meta}</li>'


def guide_links(country_en=None, level=""):
    """Guides that fit a country and level, most specific first."""
    g = []
    if country_en in VISA_IDS:
        g.append((f"/guides/visa/#{VISA_IDS[country_en]}", f"{country_en} স্টুডেন্ট ভিসা"))
    if country_en in VISA_IDS and next(v for v in VISA if v["c"] == country_en)["post"]:
        g.append(("/guides/post-study-work/", f"{country_en}-এ পড়া শেষে কাজ"))
    if country_en in VISA_IDS or country_en == "France":
        g.append(("/guides/part-time-work/", f"{country_en}-এ পড়ার সময় কাজ"))
    if country_en in TUITION_FREE:
        g.append(("/guides/tuition-free/", f"{country_en}-এ টিউশন ফি"))
    if re.search(r"PhD|Postdoc|MPhil", level):
        g += [("/guides/funded-phd/", "ফান্ডেড PhD (TA/RA)"), ("/guides/research-proposal/", "Research Proposal লেখা"), ("/guides/professor-email/", "প্রফেসরকে ইমেইল"), ("/professors/", "প্রফেসর সার্চ")]
    europe = country_en and any(s.startswith("europe/") and COUNTRIES[s][0] == country_en for s in COUNTRIES)
    g.append(("/guides/motivation-letter/", "Motivation Letter লেখা") if europe else ("/guides/sop/", "SOP লেখা"))
    g += [("/guides/cv/", "একাডেমিক CV"), ("/guides/lor/", "রেকমেন্ডেশন লেটার (LOR)"), ("/guides/interview/", "ইন্টারভিউর প্রস্তুতি"), ("/guides/english-tests/", "IELTS / TOEFL / Duolingo"), ("/guides/other-tests/", "GRE / GMAT / ভাষার পরীক্ষা"),
          ("/guides/documents/", "কাগজপত্র ও সত্যায়ন"), ("/tools/cgpa/", "CGPA রূপান্তর"), ("/tools/eligibility/", "যোগ্যতা যাচাই")]
    seen, out = set(), []
    for h, t in g:
        if h not in seen:
            seen.add(h)
            out.append(f'<li><a href="{h}">{t}</a></li>')
    return '<ul class="tags">' + "".join(out) + "</ul>"


def neighbours(slug):
    cont = slug.split("/")[0]
    items = "".join(f'<li><a href="/{s}/">{html.escape(COUNTRIES[s][2])}</a></li>' for s in COUNTRIES if s.startswith(cont + "/") and s != slug)
    return f'<h2>{CONTINENTS[cont][2]} অন্য দেশের স্কলারশিপ</h2><ul class="tags">{items}</ul>' if items else ""


def country_links(slug):
    name_en = COUNTRIES[slug][0]
    rows = _rows_with_pages(lambda s, r: s == slug)
    levels = " ".join(r["level"] for _, _, r in rows)
    lst = "".join(sch_link(s, i, r, extra=False) + "" for s, i, r in rows)
    return f"""<section class="rel">
{f'<h2>{html.escape(COUNTRIES[slug][2])} — সব স্কলারশিপের পেজ</h2><ul>{lst}</ul>' if lst else ""}
<h2>{html.escape(name_en)}-এ আবেদনের প্রস্তুতি</h2>{guide_links(name_en, levels)}
{neighbours(slug)}
</section>"""


def scholarship_links(slug, i, r):
    name_en = COUNTRIES[slug][0]
    lv = r["level"]
    key = "PhD" if re.search(r"PhD|Postdoc", lv) else "PG" if re.search(r"PG|Master|MS|MPhil", lv) else "UG"
    same_level = [x for x in _rows_with_pages(lambda s, o: s != slug and (key in o["level"] or (key == "PG" and "Master" in o["level"])))
                  if x[0].split("/")[0] == slug.split("/")[0]][:6]
    sl = "".join(sch_link(*x) for x in same_level)
    lvl_bn = {"PhD": "PhD / গবেষণা", "PG": "মাস্টার্স", "UG": "স্নাতক"}[key]
    return f"""<section class="rel">
<h2>এই স্কলারশিপের জন্য প্রস্তুতি</h2>{guide_links(name_en, lv)}
{f'<h2>{CONTINENTS[slug.split("/")[0]][2]} অন্য {lvl_bn} স্কলারশিপ</h2><ul>{sl}</ul>' if sl else ""}
{neighbours(slug)}
<p><a href="/deadlines/">সব স্কলারশিপের শেষ তারিখ</a> · <a href="/scholarships/">সব স্কলারশিপের তালিকা</a></p>
</section>"""


def related_scholarships(title, pred, limit=12):
    rows = _rows_with_pages(pred)[:limit]
    return f'<section class="rel"><h2>{title}</h2><ul>{"".join(sch_link(*x) for x in rows)}</ul></section>' if rows else ""


def scholarships_index_body(updated):
    parts = []
    for cont, (en, bn_name, bn_of) in CONTINENTS.items():
        blocks = []
        for slug in COUNTRIES:
            if not slug.startswith(cont + "/"):
                continue
            rows = _rows_with_pages(lambda s, r: s == slug)
            if rows:
                blocks.append(f'<h3><a href="/{slug}/">{html.escape(COUNTRIES[slug][0])}</a></h3><ul>{"".join(sch_link(s, i, r, extra=False) for s, i, r in rows)}</ul>')
        parts.append(f'<h2><a href="/{cont}/">{bn_of} স্কলারশিপ</a></h2>' + "".join(blocks))
    n = len(_rows_with_pages())
    return f"""<div class="wrap">
{nav()}
<nav class="crumbs"><a href="/">হোম</a></nav>
<header style="display:flex;flex-direction:column;gap:10px">
  <span class="eyebrow">সর্বশেষ যাচাই {CHECKED}</span>
  <h1>সব স্কলারশিপের তালিকা</h1>
  <p class="lede">{bn(n)}টি স্কলারশিপ, অঞ্চল আর দেশ অনুযায়ী সাজানো। ফিল্টার দিয়ে খুঁজতে <a href="/search/">স্কলারশিপ সার্চ</a>, শেষ তারিখ অনুযায়ী দেখতে <a href="/deadlines/">শেষ তারিখ সামনে</a>।</p>
</header>
<section class="rel idx">{"".join(parts)}</section>
{FOOTER}
</div>"""


def funded_phd_body(updated):
    return _guide("funded-phd", "ফান্ডেড PhD — TA, RA ও বেতনভুক্ত PhD",
        "স্কলারশিপ ছাড়াও PhD-র খরচ চালানোর সবচেয়ে বড় পথ হলো বিশ্ববিদ্যালয়ের নিজস্ব ফান্ডিং: যুক্তরাষ্ট্র-কানাডায় Teaching/Research Assistantship আর ন্যূনতম ফান্ডিং প্যাকেজ, আর উত্তর ইউরোপে PhD মানেই বেতনসহ চাকরি। অনেক ক্ষেত্রে আলাদা স্কলারশিপের আবেদন লাগে না — ভর্তির সাথেই ফান্ডিং আসে।",
        """<h2>শব্দগুলো চিনে নিন</h2>
  <div class="tbl-wrap"><table class="t">
    <tr><th>ধরন</th><th>কী পান</th><th>বদলে কী করতে হয়</th></tr>
    <tr><td><b>Teaching Assistantship (TA)</b></td><td>টিউশন মওকুফ + জীবনযাত্রার ভাতা (stipend)</td><td>স্নাতক কোর্সে ক্লাস/ল্যাব নেওয়া, খাতা দেখা</td></tr>
    <tr><td><b>Research Assistantship (RA)</b></td><td>টিউশন মওকুফ + ভাতা, সাধারণত প্রফেসরের গবেষণা অনুদান থেকে</td><td>প্রফেসরের প্রজেক্টে গবেষণা — প্রায়ই নিজের PhD-র কাজই</td></tr>
    <tr><td><b>Fellowship</b></td><td>ভাতা (কখনো টিউশনসহ)</td><td>সাধারণত কোনো কাজ লাগে না</td></tr>
    <tr><td><b>বেতনভুক্ত PhD পদ</b> (ইউরোপ)</td><td>মাসিক বেতন, ছুটি, পেনশন — কর্মচারী হিসেবে চুক্তি</td><td>গবেষণা, কখনো কিছু পড়ানো</td></tr>
  </table></div>
  <p class="meta">সংজ্ঞা: EducationUSA (U.S. Department of State)।</p>

  <h2>🇺🇸 যুক্তরাষ্ট্র</h2>
  <ul>
    <li>PhD-তে assistantship খুবই প্রচলিত; বিনিময়ে টিউশন মওকুফ আর ভাতা পাওয়া যায় (EducationUSA)।</li>
    <li>প্রতিযোগিতা বেশি; STEM আর গবেষণাভিত্তিক বিষয়ে ফান্ডিং বেশি।</li>
    <li>ভাতার পরিমাণ বিশ্ববিদ্যালয়ভেদে আলাদা — উদাহরণ: Rice University বলে তাদের ডক্টরাল ও থিসিস-মাস্টার্স শিক্ষার্থীরা প্রায়ই বছরে $23,400–$40,000 ভাতা পান।</li>
    <li>ডিপার্টমেন্টের প্রফেসররাই অনেক সময় ফান্ডিং কে পাবে ঠিক করেন — তাই আগে থেকে যোগাযোগ জরুরি (EducationUSA)।</li>
    <li>কিছু ফান্ডিংয়ের শেষ তারিখ শুরুর ১৮ মাস আগেও হতে পারে — আগেভাগে শুরু করুন।</li>
    <li>কোর্সভিত্তিক মাস্টার্সে ফান্ডিং কম; প্রথম বছরের বিদেশি শিক্ষার্থীরা অনেক সময় পান না।</li>
  </ul>

  <h2>🇨🇦 কানাডা — ন্যূনতম ফান্ডিং নীতি</h2>
  <p>অনেক কানাডিয়ান বিশ্ববিদ্যালয় PhD শিক্ষার্থীদের (বিদেশিসহ) একটা ন্যূনতম ফান্ডিংয়ের নিশ্চয়তা দেয়। উদাহরণ:</p>
  <div class="tbl-wrap"><table class="t fit">
    <tr><th>বিশ্ববিদ্যালয়</th><th>ন্যূনতম ফান্ডিং</th></tr>
    <tr><td>UBC (Vancouver)</td><td>সেপ্টেম্বর ২০২৬ থেকে প্রথম ৪ বছর বছরে CA$40,000; দেশি-বিদেশি সবার জন্য, সন্তোষজনক অগ্রগতি সাপেক্ষে</td></tr>
    <tr><td>University of Waterloo</td><td>বছরে CA$29,145 (১ মে ২০২৬ থেকে), ৪ বছর পর্যন্ত; বিদেশিরা অতিরিক্ত International Doctoral Student Award পান, যা প্রায় দেশি-বিদেশি টিউশনের পার্থক্য</td></tr>
    <tr><td>McGill — Biomedical Engineering (একটি ডিপার্টমেন্ট)</td><td>ভাতা বছরে CA$25,000; টিউশনসহ বিদেশি PhD1-এর মোট ন্যূনতম CA$44,163 (২০২৬–২৭)</td></tr>
  </table></div>
  <p class="meta">অঙ্কগুলো বিশ্ববিদ্যালয় বা ডিপার্টমেন্টের নির্দিষ্ট নীতি — আবেদনের আগে সেই প্রোগ্রামের পেজে মিলিয়ে নিন।</p>

  <h2>🇪🇺 ইউরোপ — PhD মানে চাকরি</h2>
  <ul>
    <li><b>সুইডেন:</b> ভর্তি হওয়া ডক্টরাল শিক্ষার্থীরা একই সাথে ছাত্র ও বিশ্ববিদ্যালয়ের কর্মচারী — মাসিক বেতন, ছুটি, পেনশন (Study in Sweden)।</li>
    <li><b>নেদারল্যান্ডস:</b> বেতন বিশ্ববিদ্যালয়ের সমষ্টিগত শ্রম চুক্তি (CAO) অনুযায়ী। উদাহরণ (একটি বিজ্ঞপ্তি): Radboud University-তে শুরু মাসে €3,059 গ্রস, চতুর্থ বছরে €3,881।</li>
    <li><b>নরওয়ে:</b> উদাহরণ (২০২৪-এর একটি NTNU বিজ্ঞপ্তি): বছরে গ্রস NOK 532,200 থেকে, বেতন থেকে ২% পেনশনে কাটা হয়।</li>
    <li><b>ডেনমার্ক:</b> বিশ্ববিদ্যালয়ের PhD পদে বেতন সরকারি AC চুক্তি অনুযায়ী; Industrial PhD-তে কোম্পানির চুক্তি অনুযায়ী (Study in Denmark)।</li>
    <li>এসব পদ চাকরির বিজ্ঞপ্তির মতো দেওয়া হয় — খুঁজুন ইউরোপীয় কমিশনের <a href="https://euraxess.ec.europa.eu/jobs/search" target="_blank" rel="noopener">EURAXESS Jobs</a> আর বিশ্ববিদ্যালয়ের "vacancies" পেজে।</li>
  </ul>

  <h2>কীভাবে এগোবেন</h2>
  <ol class="steps">
    <li><h3>বিষয় আর প্রফেসর ঠিক করুন</h3><p>আপনার আগ্রহের সাথে মেলে এমন ল্যাব খুঁজুন — <a href="/professors/">প্রফেসর সার্চ</a> দিয়ে শুরু করুন।</p></li>
    <li><h3>ফান্ডিং নিয়ে সরাসরি জিজ্ঞেস করুন</h3><p>ইমেইলে জানতে চান তিনি নতুন ছাত্র নিচ্ছেন কিনা আর RA ফান্ডিং আছে কিনা — দেখুন <a href="/guides/professor-email/">প্রফেসরকে ইমেইল</a>।</p></li>
    <li><h3>অফারে কী আছে মিলিয়ে নিন</h3><p>টিউশন পুরো মওকুফ কিনা, ভাতা কত ও কত বছর নিশ্চিত, স্বাস্থ্যবীমা আর বাধ্যতামূলক ফি কে দেবে, কাজের ঘণ্টা কত।</p></li>
    <li><h3>ভাতা দিয়ে জীবনযাত্রা চলবে কিনা হিসাব করুন</h3><p><a href="/tools/budget/">বাজেট ক্যালকুলেটর</a> দিয়ে শহরের খরচের সাথে মিলিয়ে দেখুন; ভিসার জন্যও এই অফার লেটার আর্থিক প্রমাণ হিসেবে কাজে লাগে।</p></li>
    <li><h3>ইউরোপের পদে চাকরির মতো আবেদন</h3><p>বিজ্ঞপ্তি অনুযায়ী CV, মোটিভেশন লেটার, রেফারেন্স — শেষ তারিখ কড়া, দেরিতে আবেদন নেওয়া হয় না।</p></li>
  </ol>""",
        [("EducationUSA — Graduate funding", "https://educationusa.state.gov/your-5-steps-us-study/finance-your-studies/graduate"),
         ("EducationUSA — Glossary", "https://educationusa.state.gov/experience-studying-usa/us-educational-system/glossary"),
         ("EducationUSA — Fully-funded doctoral programs", "https://educationusa.state.gov/scholarships/fully-funded-doctoral-programs"),
         ("UBC — Minimum funding policy for PhD students", "https://www.grad.ubc.ca/awards/minimum-funding-policy-phd-students"),
         ("University of Waterloo — Funding for research-based graduate programs", "https://uwaterloo.ca/future-graduate-students/funding/funding-research-based-graduate-programs"),
         ("McGill — Biomedical Engineering funding", "https://www.mcgill.ca/bbme/programs/funding"),
         ("Study in Sweden — PhD programmes", "https://studyinsweden.se/plan-your-studies/degree-programmes/phd-programmes/"),
         ("Study in Denmark — PhD and research", "https://studyindenmark.dk/study-options/what-can-i-study/phd-and-research"),
         ("EURAXESS — PhD position, Radboud University (salary example)", "https://euraxess.ec.europa.eu/worldwide/south-korea/news/phd-position-individual-dynamics-fatigue-nijmegen-netherlands")],
        related_scholarships("PhD স্কলারশিপও দেখুন", lambda s_, r: bool(re.search(r"PhD|Postdoc", r["level"])), 15))


def part_time_body(updated):
    rows = "".join(f'<tr><td><a href="/guides/visa/#{VISA_IDS[v["c"]]}">{v["bn"]}</a></td><td>{html.escape(v["work"])}</td></tr>' for v in VISA if v["work"])
    srcs = []
    for v in VISA:
        if v["work"]:
            srcs += [x for x in v["src"]]
    seen, uniq = set(), []
    for t, u in srcs:
        if u not in seen:
            seen.add(u)
            uniq.append((t, u))
    return _guide("part-time", "পড়ার সময় পার্ট-টাইম কাজ",
        "বেশিরভাগ দেশে স্টুডেন্ট ভিসায় সীমিত ঘণ্টা কাজ করা যায়। এখানে দেশভিত্তিক নিয়ম সরকারের অফিসিয়াল সূত্র থেকে — আর কিছু জরুরি সতর্কতা।",
        f"""<h2>দেশভিত্তিক কাজের সীমা</h2>
  <div class="tbl-wrap"><table class="t fit"><tr><th>দেশ</th><th>পড়ার সময় কাজের নিয়ম</th></tr>{rows}</table></div>
  <p class="meta">নিয়ম প্রায়ই বদলায়, আর কোর্সের ধরন (ফুল-টাইম, ভাষা কোর্স, গবেষণা) অনুযায়ী আলাদা হতে পারে। কাজ শুরুর আগে নিজের ভিসার শর্ত আর বিশ্ববিদ্যালয়ের ইন্টারন্যাশনাল অফিসে মিলিয়ে নিন।</p>
  <h2>জরুরি সতর্কতা</h2>
  <ul>
    <li><b>সীমার বেশি কাজ করবেন না।</b> ভিসার শর্ত ভাঙলে ভিসা বাতিল ও দেশে ফেরত পাঠানোর ঝুঁকি থাকে; পরে অন্য দেশের ভিসাতেও সমস্যা হতে পারে।</li>
    <li><b>পার্ট-টাইম আয় দিয়ে টিউশন চালানোর পরিকল্পনা করবেন না।</b> ভিসার আর্থিক প্রমাণ আলাদাভাবে দেখাতে হয় (<a href="/guides/visa/">ভিসা গাইড</a>), আর প্রথম কয়েক মাসে কাজ পাওয়া অনিশ্চিত।</li>
    <li>লিখিত চুক্তি নিন, বেতন ব্যাংকে নিন, ট্যাক্স নম্বর বা দেশের নিয়ম অনুযায়ী নিবন্ধন করুন। নগদে "অফ দ্য বুক" কাজ এড়িয়ে চলুন।</li>
    <li>ক্যাম্পাসের কাজ (লাইব্রেরি, ল্যাব, টিউটরিং) প্রায়ই সহজ শর্তে পাওয়া যায় আর পড়ার সাথে মেলে। PhD হলে দেখুন <a href="/guides/funded-phd/">TA/RA ফান্ডিং</a>।</li>
    <li>কাজ পেতে প্রায়ই স্থানীয় ভাষা লাগে (যেমন জার্মানি, জাপান, কোরিয়া, ফ্রান্স) — ভাষা শেখা শুরু করুন দেশে থাকতেই।</li>
  </ul>""", uniq,
        '<section class="rel"><h2>সম্পর্কিত</h2><ul class="tags"><li><a href="/tools/budget/">বাজেট ক্যালকুলেটর</a></li><li><a href="/guides/visa/">স্টুডেন্ট ভিসা</a></li><li><a href="/guides/tuition-free/">টিউশন-ফ্রি দেশ</a></li><li><a href="/guides/funded-phd/">ফান্ডেড PhD</a></li></ul></section>')


def interview_body(updated):
    return _guide("interview", "ভিসা ও স্কলারশিপ ইন্টারভিউ",
        "অনেক স্কলারশিপ (Chevening, GKS, DAAD-এর কিছু প্রোগ্রাম) চূড়ান্ত বাছাইয়ের আগে ইন্টারভিউ নেয়, আর যুক্তরাষ্ট্রের মতো দেশে ভিসার জন্য দূতাবাসে ইন্টারভিউ দিতে হয়। দুটোর প্রস্তুতি আলাদা।",
        """<h2>স্কলারশিপ ইন্টারভিউ</h2>
  <p>উদাহরণ হিসেবে Chevening-এর অফিসিয়াল নির্দেশনা — অন্য স্কলারশিপেও একই ধরনের প্রশ্ন আসে।</p>
  <ol class="steps">
    <li><h3>নিজের আবেদন আবার পড়ুন</h3><p>প্রবন্ধে যা লিখেছেন, ইন্টারভিউতে তার বাইরে নতুন উদাহরণসহ একই কথা বলতে পারতে হবে। মত বদলে থাকলে সেটা ব্যাখ্যা করুন।</p></li>
    <li><h3>প্রশ্নের মূল বিষয়গুলো</h3><p>নেতৃত্ব, অন্যকে প্রভাবিত করা, পেশাগত নেটওয়ার্ক, কোর্স ও বিশ্ববিদ্যালয় বাছাইয়ের কারণ, আর দেশে ফিরে আপনার প্রভাব — স্বল্প, মধ্য ও দীর্ঘমেয়াদি নির্দিষ্ট লক্ষ্য।</p></li>
    <li><h3>STAR কাঠামোয় উত্তর</h3><p>Situation, Task, Action, Result — "আমরা" নয়, <b>আপনি</b> কী করেছেন বলুন, আর ফল সংখ্যায় দেখান।</p></li>
    <li><h3>কোর্স ও দেশ নিয়ে পড়াশোনা</h3><p>কোন মডিউল কেন, একই রকম কোর্সের মধ্যে এটা কেন; আপনার দেশের অগ্রাধিকারের সাথে স্কলারশিপদাতা দেশের লক্ষ্যের মিল।</p></li>
    <li><h3>মক ইন্টারভিউ</h3><p>বন্ধু বা সহকর্মীর সাথে জোরে অনুশীলন করুন। মুখস্থ বা কপি করা উত্তর সহজে ধরা পড়ে — Chevening বলে "সঠিক উত্তর" বলে কিছু নেই, আপনার নিজের সত্যি উত্তরই চায়।</p></li>
    <li><h3>শেষে প্রশ্ন আর দিনের প্রস্তুতি</h3><p>প্যানেলকে জিজ্ঞেস করার মতো একটা ভাবনাপূর্ণ প্রশ্ন রাখুন; আগেভাগে পৌঁছান, আনুষ্ঠানিক পোশাক পরুন।</p></li>
  </ol>
  <h2>যুক্তরাষ্ট্রের স্টুডেন্ট ভিসা (F-1) — ঢাকা</h2>
  <p><b>সাথে নিন</b> (U.S. Embassy Dhaka):</p>
  <ul>
    <li>মূল Form I-20 (বিশ্ববিদ্যালয়ের সই করা), SEVIS ফি-র রসিদ</li>
    <li>DS-160 কনফার্মেশন পেজ (বারকোডসহ), অ্যাপয়েন্টমেন্ট লেটার, ফি-র রসিদ</li>
    <li>পাসপোর্ট — যুক্তরাষ্ট্রে থাকার সময়ের পরও অন্তত ৬ মাস মেয়াদ; আগের পাসপোর্টগুলোও আলাদা করে (স্টেপল না করে)</li>
    <li>অনলাইনে ছবি আপলোড না হলে একটা নিয়মমাফিক প্রিন্ট ছবি</li>
    <li>সহায়ক কাগজ: মার্কশিট/ট্রান্সক্রিপ্ট, পরীক্ষার স্কোর, ৩–১২ মাসের ব্যাংক স্টেটমেন্ট। দূতাবাস বলে এগুলো বাধ্যতামূলক নয় — সিদ্ধান্ত মূলত DS-160 আর আপনার উত্তরের উপর।</li>
  </ul>
  <p><b>যা জানা জরুরি:</b></p>
  <ul>
    <li>পড়ার পরিকল্পনা, খরচ কীভাবে চালাবেন আর বাংলাদেশের সাথে আপনার বন্ধন — নিজের ভাষায়, সংক্ষেপে বলতে পারুন।</li>
    <li>বন্ধু, আত্মীয় বা আইনজীবী সাথে ঢুকতে পারেন না।</li>
    <li><b>কোনো জাল কাগজ দেবেন না।</b> সন্দেহ হলে ভিসা প্রত্যাখ্যান আর স্থায়ী নিষেধাজ্ঞা হতে পারে। এজেন্ট যদি "ব্যাংক স্টেটমেন্ট বানিয়ে দেওয়ার" প্রস্তাব দেয়, সরে আসুন।</li>
  </ul>
  <p>অন্য দেশের ভিসায় কত টাকা দেখাতে হয়: <a href="/guides/visa/">স্টুডেন্ট ভিসা — দেশভিত্তিক</a>।</p>""",
        [("Chevening — How to succeed at your Chevening interview", "https://www.chevening.org/resource-hub/guidance/how-to-succeed-at-your-chevening-interview/"),
         ("Chevening — 5 questions to consider before your interview", "https://www.chevening.org/news/5-questions-to-consider-before-your-chevening-interview/"),
         ("Chevening — 5 tips from real Chevening interviewers", "https://www.chevening.org/news/5-tips-for-standing-out-in-your-interview-from-real-chevening-interviewers/"),
         ("U.S. Embassy in Bangladesh — Interview steps", "https://bd.usembassy.gov/interview-steps/"),
         ("U.S. Embassy in Bangladesh — Supporting documents", "https://bd.usembassy.gov/supporting-documents/"),
         ("U.S. Department of State — Student visa", "https://travel.state.gov/content/travel/en/us-visas/study/student-visa.html")],
        related_scholarships("ইন্টারভিউ হয় এমন কিছু স্কলারশিপ", lambda s_, r: r["provider_type"] == "government" and not s_.startswith("asia/bangladesh"), 12))


def student_file_body(updated):
    return _guide("student-file", "স্টুডেন্ট ফাইল ও বিদেশে টাকা পাঠানো",
        "বাংলাদেশ থেকে বিদেশে টিউশন ফি আর জীবনযাত্রার খরচ পাঠাতে হয় অনুমোদিত ডিলার (AD) ব্যাংকের মাধ্যমে — সাধারণত ব্যাংকে একটা \"স্টুডেন্ট ফাইল\" খুলে। নিয়ম বাংলাদেশ ব্যাংকের Foreign Exchange নির্দেশিকা ও সার্কুলারে।",
        """<h2>কী কী পাঠানো যায়</h2>
  <ul>
    <li><b>আবেদন, ভর্তি ও পরীক্ষার ফি:</b> AD ব্যাংক ছাড়তে পারে, তবে টাকা সরাসরি প্রতিষ্ঠানের কাছে যেতে হবে।</li>
    <li><b>টিউশন ও জীবনযাত্রার খরচ:</b> বিশ্ববিদ্যালয়ের দেওয়া খরচের হিসাব (বার্ষিক টিউশন, থাকা-খাওয়া, বীমা, আনুষঙ্গিক) অনুযায়ী।</li>
    <li><b>স্বাস্থ্যবীমা:</b> ভিসা বা ভর্তির জন্য বাধ্যতামূলক হলে।</li>
    <li><b>পেমেন্ট প্রতিষ্ঠান বা ব্লকড অ্যাকাউন্ট:</b> ভর্তির কাগজে নির্দিষ্ট পেমেন্ট প্রতিষ্ঠানের নাম থাকলে সেখানে পাঠানো যায়; ব্লকড অ্যাকাউন্টের টাকা পড়ার খরচেই ব্যবহার করতে হবে।</li>
  </ul>
  <h2>ব্যাংকে যা লাগে (সাধারণত)</h2>
  <ol class="steps">
    <li><h3>ভর্তির কাগজ ও খরচের হিসাব</h3><p>অফার/ভর্তির চিঠি আর প্রতিষ্ঠানের দেওয়া বার্ষিক খরচের হিসাব।</p></li>
    <li><h3>সত্যায়িত সনদ ও বৈধ পাসপোর্ট</h3><p>দেখুন <a href="/guides/documents/">কাগজপত্র ও সত্যায়ন</a>।</p></li>
    <li><h3>ব্যাংকের আবেদন ফর্ম</h3><p>ব্যাংক প্রতিটি শিক্ষার্থীর জন্য আলাদা ফাইল রাখে, যা বাংলাদেশ ব্যাংক পরিদর্শন করতে পারে।</p></li>
  </ol>
  <h2>জরুরি শর্ত</h2>
  <ul>
    <li>টাকা পাঠানোর এক বছরের মধ্যে বিদেশে যেতে হবে বলে ব্যাংক নিশ্চিত হবে।</li>
    <li><b>ভিসা প্রত্যাখ্যাত হলে</b> পাঠানো টাকা দেশে ফেরত আনতে হবে — ব্যাংক এ বিষয়ে আপনার কাছ থেকে অঙ্গীকারনামা নেবে। তাই ভিসার আগে বড় অঙ্ক পাঠানোর আগে প্রতিষ্ঠানের ফেরতের (refund) নিয়ম দেখে নিন।</li>
    <li>প্রতিষ্ঠান বা বিষয় বদলালে বা নতুন কোর্সে গেলে ব্যাংকের সাথে আগে কথা বলুন।</li>
    <li>হুন্ডি বা অনানুষ্ঠানিক পথে টাকা পাঠাবেন না — এটা অবৈধ, আর ভিসার আর্থিক প্রমাণ হিসেবেও গ্রহণযোগ্য হয় না।</li>
    <li>শিক্ষার ফি কার্ডে পরিশোধ নিয়ে বাংলাদেশ ব্যাংকের নতুন সার্কুলার আছে (আগস্ট ২০২৬) — কার্ডে দেওয়ার আগে নিজের ব্যাংকে সর্বশেষ সীমা জেনে নিন।</li>
  </ul>
  <p class="meta">ব্যাংকভেদে কাগজের তালিকা কিছুটা আলাদা হয়। ফাইল খোলার আগে নিজের ব্যাংকের Foreign Exchange / Student File ডেস্কে জিজ্ঞেস করুন।</p>""",
        [("Bangladesh Bank — FE Circular No. 37 (30 Sep 2025)", "https://www.bb.org.bd/mediaroom/circulars/fepd/sep302025fepd37e.pdf"),
         ("Bangladesh Bank — FE circular (10 Aug 2026)", "https://www.bb.org.bd/mediaroom/circulars/fepd/aug102026fepd-129e.pdf"),
         ("Bangladesh Bank — Guidelines for Foreign Exchange Transactions, Vol. 1, Chapter 11 (Private remittances)", "https://www.bb.org.bd/aboutus/regulationguideline/foreignexchange/feguidevol1/11.pdf")],
        '<section class="rel"><h2>সম্পর্কিত</h2><ul class="tags"><li><a href="/guides/visa/">ভিসায় কত টাকা দেখাতে হয়</a></li><li><a href="/tools/budget/">বাজেট ক্যালকুলেটর</a></li><li><a href="/guides/pre-departure/">যাওয়ার আগের চেকলিস্ট</a></li></ul></section>')


PRE_DEPARTURE = [
    ("কাগজপত্র", ["পাসপোর্টের মেয়াদ পুরো কোর্স + অন্তত ৬ মাস", "ভিসা / রেসিডেন্স পারমিটের কাগজ (যেমন I-20, CoE, ভর্তির চিঠি) হাতের ব্যাগে",
                   "I-20/CoE-তে নাম ও জন্মতারিখ পাসপোর্টের সাথে হুবহু মেলে কিনা দেখুন",
                   "মূল সনদ, মার্কশিট আর সত্যায়িত কপি", "স্কলারশিপ / ফান্ডিংয়ের চিঠি আর আর্থিক কাগজ",
                   "সব জরুরি কাগজের স্ক্যান কপি অনলাইনে (ইমেইল/ক্লাউডে)", "পাসপোর্ট সাইজ ছবি (কয়েক কপি)"]),
    ("টাকা ও ব্যাংক", ["স্টুডেন্ট ফাইলের মাধ্যমে টিউশন / ব্লকড অ্যাকাউন্টের টাকা পাঠানো হয়েছে", "আন্তর্জাতিক লেনদেন চালু ডেবিট/ক্রেডিট কার্ড",
                       "প্রথম কয়েক সপ্তাহের খরচের জন্য কিছু বৈদেশিক মুদ্রা (দেশের নিয়মিত সীমার মধ্যে)"]),
    ("স্বাস্থ্য", ["বাধ্যতামূলক স্বাস্থ্যবীমা চূড়ান্ত", "টিকার রেকর্ড আর প্রেসক্রিপশন (ইংরেজিতে), নিয়মিত ওষুধ কিছুদিনের মতো",
                   "ভিসার জন্য দেশ মেডিক্যাল পরীক্ষা চাইলে তা সম্পন্ন"]),
    ("যাত্রা ও পৌঁছানো", ["কবে পৌঁছাতে হবে বিশ্ববিদ্যালয়ে জেনে টিকিট — যুক্তরাষ্ট্রে I-20-র শুরুর ৩০ দিনের বেশি আগে ঢোকা যায় না",
                          "প্রথম রাতগুলোর থাকার ব্যবস্থা নিশ্চিত", "বিমানবন্দর থেকে যাতায়াতের পরিকল্পনা",
                          "ইন্টারন্যাশনাল অফিস / উপদেষ্টার নাম ও ফোন নম্বর", "হাতের ব্যাগে এক সেট কাপড় আর প্রয়োজনীয় জিনিস (লাগেজ দেরিতে এলে)",
                          "তরল ১০০ মিলির কম পাত্রে; লাগেজের ওজন সীমা এয়ারলাইনে মিলিয়ে নেওয়া"]),
    ("পৌঁছানোর পর প্রথম সপ্তাহ", ["বিশ্ববিদ্যালয়ে রিপোর্ট / ভর্তি নিশ্চিত", "দেশের নিয়মে ঠিকানা নিবন্ধন ও রেসিডেন্স পারমিট",
                                  "স্থানীয় সিম আর ব্যাংক অ্যাকাউন্ট", "বাংলাদেশ দূতাবাসের যোগাযোগ সংরক্ষণ", "ওরিয়েন্টেশনে অংশ নেওয়া"]),
]


def pre_departure_body(updated):
    sections = "".join(f'<h2>{t}</h2><ul class="chk">' + "".join(
        f'<li><label><input type="checkbox" data-k="{gi}-{ii}"> {html.escape(x)}</label></li>' for ii, x in enumerate(items)) + "</ul>"
        for gi, (t, items) in enumerate(PRE_DEPARTURE))
    total = sum(len(i) for _, i in PRE_DEPARTURE)
    return _guide("pre-departure", "যাওয়ার আগের চেকলিস্ট",
        "ভিসা পাওয়ার পর থেকে পৌঁছানোর প্রথম সপ্তাহ পর্যন্ত যা যা করতে হয়। টিক দিলে এই ব্রাউজারে মনে থাকবে — কোথাও পাঠানো হয় না।",
        f"""<style>.chk{{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:6px}}.chk label{{display:flex;gap:10px;align-items:flex-start;padding:8px 12px;background:var(--surface);border:1px solid var(--line);border-radius:8px;cursor:pointer}}
.chk input{{margin-top:5px;accent-color:var(--accent)}}.chk input:checked+*{{}}.chk label:has(input:checked){{color:var(--muted);text-decoration:line-through}}</style>
  <p class="warn"><b id="pd-n">০</b> / {bn(total)} সম্পন্ন · <button type="button" id="pd-reset" class="obtn" style="padding:4px 10px;font-size:13px">সব মুছুন</button></p>
  {sections}
  <p class="meta">প্রতিটি দেশ ও বিশ্ববিদ্যালয়ের নিজস্ব pre-departure তথ্য দেখুন — স্বাস্থ্যবীমা, আবহাওয়া, যাতায়াত, বাসা।</p>
  <script>
  (function(){{var K="hsi-predep",st={{}};try{{st=JSON.parse(localStorage.getItem(K)||"{{}}")}}catch(e){{}}
  var bx=document.querySelectorAll(".chk input"),n=document.getElementById("pd-n"),bn=function(x){{return String(x).replace(/\\d/g,function(c){{return "০১২৩৪৫৬৭৮৯"[c]}})}};
  function upd(){{var c=0;bx.forEach(function(b){{if(b.checked)c++}});n.textContent=bn(c)}}
  bx.forEach(function(b){{b.checked=!!st[b.dataset.k];b.addEventListener("change",function(){{st[b.dataset.k]=b.checked;try{{localStorage.setItem(K,JSON.stringify(st))}}catch(e){{}}upd()}})}});
  document.getElementById("pd-reset").onclick=function(){{st={{}};try{{localStorage.removeItem(K)}}catch(e){{}}bx.forEach(function(b){{b.checked=false}});upd()}};upd()}})();
  </script>""",
        [("EducationUSA — Gather pre-departure materials and documents", "https://educationusa.state.gov/your-5-steps-us-study/prepare-your-departure/graduate/gather-pre-departure-materials-and"),
         ("EducationUSA — Prepare for your departure", "https://educationusa.state.gov/your-5-steps-us-study/prepare-your-departure"),
         ("Study Australia — Preparing to travel", "https://www.studyaustralia.gov.au/en/plan-your-move/preparing-to-travel"),
         ("Study Australia — How to prepare for your flight", "https://www.studyaustralia.gov.au/en/tools-and-resources/tips-and-advice-for-students/how-to-prepare-for-your-flight-to-australia"),
         ("Bangladesh Bank — FE Circular No. 37 (student remittances)", "https://www.bb.org.bd/mediaroom/circulars/fepd/sep302025fepd37e.pdf")],
        '<section class="rel"><h2>সম্পর্কিত</h2><ul class="tags"><li><a href="/guides/student-file/">স্টুডেন্ট ফাইল ও টাকা পাঠানো</a></li><li><a href="/guides/visa/">স্টুডেন্ট ভিসা</a></li><li><a href="/guides/part-time-work/">পড়ার সময় কাজ</a></li><li><a href="/guides/documents/">কাগজপত্র ও সত্যায়ন</a></li></ul></section>')


def other_tests_body(updated):
    return _guide("other-tests", "GRE, GMAT, SAT ও ভাষার পরীক্ষা",
        "IELTS/TOEFL ছাড়াও কিছু প্রোগ্রাম আলাদা পরীক্ষা চায়: যুক্তরাষ্ট্রের অনেক গ্র্যাজুয়েট প্রোগ্রামে GRE বা GMAT, স্নাতকে SAT, আর জার্মান, জাপানি বা কোরিয়ান ভাষায় পড়লে সেই ভাষার সনদ। কোনটা লাগবে তা প্রোগ্রামের ভর্তির শর্তে দেখুন — অনেক প্রোগ্রাম এখন GRE/SAT ঐচ্ছিক রেখেছে।",
        """<h2>ভর্তির পরীক্ষা</h2>
  <div class="tbl-wrap"><table class="t fit">
    <tr><th>পরীক্ষা</th><th>কাদের জন্য</th><th>ফি ও পদ্ধতি</th></tr>
    <tr><td><b>GRE General</b><br><span class="meta">ETS</span></td><td>মাস্টার্স/PhD — বিশেষত যুক্তরাষ্ট্র, কিছু কানাডা ও ইউরোপ</td><td>সাধারণ ফি US$249 (১ আগস্ট ২০২৬ থেকে; আগের পেজে $220 দেখাতে পারে)। টেস্ট সেন্টারে বা বাসায় অনলাইনে (মানুষ পর্যবেক্ষক), সারা বছর।</td></tr>
    <tr><td><b>GMAT Focus</b><br><span class="meta">GMAC</span></td><td>MBA ও বিজনেস মাস্টার্স</td><td>ফি দেশভেদে আলাদা; যুক্তরাষ্ট্রে সেন্টারে US$275, অনলাইনে US$300। ৬০ দিনের বেশি আগে তারিখ বদলালে US$55 থেকে; না গেলে পুরো ফি বাতিল।</td></tr>
    <tr><td><b>SAT</b><br><span class="meta">College Board</span></td><td>যুক্তরাষ্ট্র ও কিছু অন্য দেশে স্নাতক ভর্তি</td><td>মূল ফি US$68 + আন্তর্জাতিক ফি US$43; দেরিতে নিবন্ধনে US$38। সামনের তারিখ: ৫ ডিসেম্বর ২০২৬ (নিবন্ধন ২০ নভেম্বর), ৬ মার্চ, ১ মে, ৫ জুন ২০২৭।</td></tr>
  </table></div>
  <h2>ভাষার পরীক্ষা — বাংলাদেশে</h2>
  <div class="tbl-wrap"><table class="t fit">
    <tr><th>ভাষা</th><th>পরীক্ষা ও কোথায়</th></tr>
    <tr><td><b>জার্মান</b></td><td><b>Goethe-Zertifikat</b> A1–C2 আর <b>TestDaF</b> (B2–C1, বছরে ৬টি নির্দিষ্ট তারিখ) — Goethe-Institut Bangladesh, ঢাকা। B1, B2, C1 ডিজিটালেও দেওয়া যায়। শুধু পরীক্ষার সনদই প্রমাণ; কোর্সে অংশগ্রহণের সনদ নয়। Goethe C2 থাকলে জার্মান বিশ্ববিদ্যালয়ে TestDaF লাগে না।</td></tr>
    <tr><td><b>জাপানি</b></td><td><b>JLPT</b> (N5–N1) — ঢাকায় আয়োজক Japanese Universities Alumni Association in Bangladesh (JUAAB); ২০২৬-এ ৫ জুলাই ও ৬ ডিসেম্বর। JASSO-র মতো স্কলারশিপে সাধারণত N2 চাওয়া হয়।</td></tr>
    <tr><td><b>কোরিয়ান</b></td><td><b>TOPIK</b> — ঢাকায় কোরিয়ান দূতাবাস আয়োজন করে, ভেন্যু পরীক্ষাভেদে আলাদা। সময়সূচি দূতাবাসের নোটিশ বোর্ডে।</td></tr>
  </table></div>
  <h2>পরামর্শ</h2>
  <ul>
    <li>আগে লক্ষ্য প্রোগ্রামগুলোর শর্ত দেখুন — GRE "optional" হলে ভালো স্কোর তবু কাজে লাগতে পারে, তবে বাধ্যতামূলক না হলে খরচ বাঁচাতে পারেন।</li>
    <li>স্কোর পাঠানোর সময় আর বৈধতার মেয়াদ (সাধারণত কয়েক বছর) দেখে পরীক্ষার তারিখ ঠিক করুন — আবেদনের শেষ তারিখের অন্তত ১–২ মাস আগে।</li>
    <li>জার্মানি, জাপান, কোরিয়ায় ইংরেজিতে পড়লেও পার্ট-টাইম কাজ আর দৈনন্দিন জীবনের জন্য স্থানীয় ভাষা খুব কাজে লাগে — দেখুন <a href="/guides/part-time-work/">পড়ার সময় কাজ</a>।</li>
    <li>ইংরেজি পরীক্ষার (IELTS, TOEFL, Duolingo, PTE) জন্য দেখুন <a href="/guides/english-tests/">ইংরেজি পরীক্ষার গাইড</a>।</li>
  </ul>
  <p class="meta">ফি আর তারিখ প্রায়ই বদলায় — নিবন্ধনের আগে নিচের অফিসিয়াল পেজে মিলিয়ে নিন।</p>""",
        [("ETS — GRE General Test fees", "https://www.ets.org/gre/test-takers/general-test/register/fees.html"),
         ("ETS — The GRE tests (at home and test centres)", "https://www.ets.org/gre.html"),
         ("mba.com — GMAT exam payment", "https://www.mba.com/exams/gmat-exam/register/exam-payment"),
         ("mba.com — GMAT fees, vouchers and fee waivers", "https://support.mba.com/hc/en-us/articles/6284241279771-GMAT-How-Much-Does-The-Exam-Cost"),
         ("College Board — SAT international fees", "https://satsuite.collegeboard.org/sat/registration/international-testing/fees"),
         ("College Board — SAT dates and deadlines", "https://satsuite.collegeboard.org/sat/dates-deadlines"),
         ("Goethe-Institut Bangladesh — German exams", "https://www.goethe.de/ins/bd/en/spr/prf.html"),
         ("Goethe-Institut Bangladesh — TestDaF", "https://www.goethe.de/ins/bd/en/m/spr/prf/testdaf.html"),
         ("JLPT — Overseas test site cities", "https://www.jlpt.jp/e/application/overseas_list.html"),
         ("Embassy of the Republic of Korea in Bangladesh — Notices (TOPIK)", "https://overseas.mofa.go.kr/bd-en/brd/m_2124/view.do?seq=760029")])


def fraud_body(updated):
    return _guide("fraud", "প্রতারণা থেকে সাবধান — এজেন্ট, ভুয়া ভর্তি ও ভিসা",
        "বিদেশে পড়ার আবেদনে ভুয়া ভর্তির চিঠি, জাল কাগজ আর \"গ্যারান্টি ভিসা\"-র প্রতারণা নতুন নয়। কানাডা সরকার ২০২৩ থেকে ভুয়া ভর্তির চিঠির ২,০০০-এর বেশি ঘটনা তদন্ত করেছে। মনে রাখুন: এজেন্ট কাগজ তৈরি করলেও আবেদনের সব তথ্যের দায় আপনার।",
        """<h2>🚩 এই লক্ষণ দেখলে সরে আসুন</h2>
  <ul>
    <li>ভর্তির চিঠি পাওয়ার <b>আগেই</b> ভিসার আবেদন করতে বলা, বা টাকার বিনিময়ে ভর্তির চিঠি "জোগাড়" করে দেওয়ার প্রস্তাব (IRCC)।</li>
    <li>টিউশন ফি বিশ্ববিদ্যালয়ের বদলে এজেন্টের অ্যাকাউন্টে দিতে বলা। এজেন্ট আপনার টাকা রাখবে না বা আপনার হয়ে পরিশোধ করবে না (British Council)।</li>
    <li>"১০০% ভিসা গ্যারান্টি" — ভিসার সিদ্ধান্ত শুধু দূতাবাস বা অভিবাসন দপ্তর নেয়, কোনো এজেন্ট নয়।</li>
    <li>ব্যাংক স্টেটমেন্ট, সনদ, অভিজ্ঞতার চিঠি "বানিয়ে দেওয়ার" প্রস্তাব। জাল কাগজ ধরা পড়লে ভিসা প্রত্যাখ্যান আর দীর্ঘ নিষেধাজ্ঞা হয় — কানাডায় ৫ বছর পর্যন্ত, যুক্তরাষ্ট্রে স্থায়ীও হতে পারে।</li>
    <li>পোর্টালের পাসওয়ার্ড বা ইমেইলের নিয়ন্ত্রণ এজেন্টের হাতে দিতে বলা — তাহলে বিশ্ববিদ্যালয়ের চিঠিপত্র আপনি দেখতেই পাবেন না।</li>
    <li>স্কলারশিপ "নিশ্চিত" করে দেওয়ার বিনিময়ে টাকা চাওয়া। সরকারি স্কলারশিপে আবেদন সাধারণত বিনামূল্যে, আর ফলাফল আসে স্কলারশিপদাতার অফিসিয়াল ইমেইল থেকে।</li>
  </ul>
  <h2>✅ নিজেকে রক্ষা করুন</h2>
  <ol class="steps">
    <li><h3>ভর্তির চিঠি সরাসরি নিন</h3><p>বিশ্ববিদ্যালয় যেন চিঠি সরাসরি আপনার ইমেইলে পাঠায়; সন্দেহ হলে বিশ্ববিদ্যালয়ের অফিসিয়াল ওয়েবসাইটের ঠিকানায় ইমেইল করে যাচাই করুন (IRCC)।</p></li>
    <li><h3>টাকা শুধু প্রতিষ্ঠানকে</h3><p>টিউশন সরাসরি বিশ্ববিদ্যালয়ে, বৈধ ব্যাংকিং পথে — দেখুন <a href="/guides/student-file/">স্টুডেন্ট ফাইল ও টাকা পাঠানো</a>।</p></li>
    <li><h3>নিজের অ্যাকাউন্ট নিজের হাতে</h3><p>আবেদন পোর্টাল, ভিসা অ্যাকাউন্ট আর ইমেইলের পাসওয়ার্ড কাউকে দেবেন না।</p></li>
    <li><h3>সব কাগজ নিজে পড়ুন</h3><p>জমা দেওয়ার আগে প্রতিটি কাগজ আর ফর্ম নিজে পড়ে নিশ্চিত হন যে সব তথ্য সত্য।</p></li>
    <li><h3>সন্দেহ হলে রিপোর্ট করুন</h3><p>যে দেশের ভিসা, তার অভিবাসন দপ্তর বা দূতাবাসে, আর বাংলাদেশে আইনশৃঙ্খলা বাহিনীতে।</p></li>
  </ol>
  <h2>এজেন্ট নিলে যা জিজ্ঞেস করবেন</h2>
  <p>এজেন্ট নেওয়া বাধ্যতামূলক নয় — বেশিরভাগ বিশ্ববিদ্যালয় আর স্কলারশিপে নিজেই অনলাইনে আবেদন করা যায়। নিলে British Council-এর পরামর্শ অনুযায়ী জিজ্ঞেস করুন:</p>
  <ul>
    <li>আপনি কীভাবে আয় করেন — বিশ্ববিদ্যালয় থেকে কমিশন পান কি? আমার কাছ থেকে কোন সেবার জন্য কত ফি?</li>
    <li>কোন কোন প্রতিষ্ঠানের সাথে আপনার অফিসিয়াল চুক্তি আছে? নির্দিষ্ট কোনোটা সুপারিশ করার জন্য বাড়তি প্রণোদনা পান কি?</li>
    <li>আপনার কাউন্সেলরের কোনো প্রশিক্ষণ বা সনদ আছে কি (যেমন British Council-এর সার্টিফায়েড কাউন্সেলর)?</li>
    <li>সেবায় অসন্তুষ্ট হলে অভিযোগের পদ্ধতি কী?</li>
    <li>আগে যাদের পাঠিয়েছেন, তাদের কারও সাথে কথা বলা যাবে কি?</li>
  </ul>""",
        [("Government of Canada (IRCC) — International student fraud", "https://www.canada.ca/en/immigration-refugees-citizenship/services/protect-fraud/study-permit-fraud.html"),
         ("Government of Canada — Genuine students impacted by fraud task force", "https://www.canada.ca/en/immigration-refugees-citizenship/corporate/transparency/committees/cimm-feb-28-2024/genuine-students-impacted-by-fraud-task-force.html"),
         ("British Council — Student and parent guide to choosing an education agent (PDF)", "https://www.britishcouncil.org/sites/default/files/student_and_parent_guide_to_choosing_an_education_agent.pdf"),
         ("U.S. Embassy in Bangladesh — Supporting documents", "https://bd.usembassy.gov/supporting-documents/")])


FAQ = [
    ("IELTS ছাড়া কি বিদেশে পড়া বা স্কলারশিপ পাওয়া সম্ভব?",
     'কিছু ক্ষেত্রে হ্যাঁ। অনেক বিশ্ববিদ্যালয় আগের ডিগ্রি ইংরেজি মাধ্যমে হলে বিশ্ববিদ্যালয়ের প্রত্যয়নপত্র (Medium of Instruction) মেনে নেয়, কেউ কেউ Duolingo বা TOEFL নেয়। যেমন Commonwealth Shared Scholarship নিজে IELTS চায় না, আর মালয়েশিয়ার MIS ইংরেজি মাধ্যমের ডিগ্রি গ্রহণ করে। আমাদের তালিকার যেসব স্কলারশিপে ছাড়ের পথ আছে: <a href="/guides/english-tests/">ইংরেজি পরীক্ষার গাইড</a>।'),
    ("CGPA কম হলে কি স্কলারশিপ পাওয়া যায়?",
     'অনেক স্কলারশিপে নির্দিষ্ট ন্যূনতম CGPA থাকে (যেমন MIS-এ মাস্টার্সের জন্য 3.00), অনেকগুলোতে স্পষ্ট সীমা নেই। <a href="/tools/eligibility/">যোগ্যতা যাচাই</a> টুলে নিজের CGPA দিয়ে দেখুন, আর জার্মানির জন্য <a href="/tools/cgpa/">CGPA রূপান্তর</a> করুন। কম ফলাফলের কারণ SOP-এ সংক্ষেপে ব্যাখ্যা করতে পারেন।'),
    ("পড়াশোনায় বিরতি (study gap) থাকলে কী হবে?",
     'নিয়ম প্রোগ্রামভেদে আলাদা। কিছু স্কলারশিপে সময়সীমা থাকে — যেমন DAAD EPOS-এ ব্যাচেলর ডিগ্রি ৬ বছরের বেশি পুরোনো হওয়া চলবে না, আবার কিছু (যেমন SI) কাজের অভিজ্ঞতাই চায়। বিরতিতে কী করেছেন (চাকরি, প্রশিক্ষণ) তা <a href="/guides/sop/">SOP</a> বা <a href="/guides/motivation-letter/">Motivation Letter</a>-এ পরিষ্কার করে লিখুন।'),
    ("বয়সের কোনো সীমা আছে কি?",
     'কিছু স্কলারশিপে আছে: যেমন Türkiye Scholarships-এ মাস্টার্সে ৩০-এর নিচে ও PhD-তে ৩৫-এর নিচে, France Eiffel-এ মাস্টার্সে ২৯ ও PhD-তে ৩৫, MIS-এ মাস্টার্সে ৪০ ও PhD-তে ৪৫। প্রতিটি স্কলারশিপ পেজের "শর্ত" ঘরে দেখুন, বা <a href="/tools/eligibility/">যোগ্যতা যাচাই</a> টুলে বয়স দিন।'),
    ("ব্যাংকে কত টাকা দেখাতে হয়?",
     'দেশভেদে আলাদা — যেমন জার্মানিতে ব্লকড অ্যাকাউন্টে বছরে অন্তত €11,904, অস্ট্রেলিয়ায় জীবনযাত্রার জন্য AUD 29,710 + কোর্স ফি। দেশভিত্তিক তালিকা <a href="/guides/visa/">স্টুডেন্ট ভিসা গাইডে</a>, আর মোট খরচের হিসাব <a href="/tools/budget/">বাজেট ক্যালকুলেটরে</a>। ফুল স্কলারশিপ বা ফান্ডিংয়ের চিঠি থাকলে সেটাও আর্থিক প্রমাণ হিসেবে গণ্য হতে পারে।'),
    ("বিনা টিউশনে বা পুরো খরচসহ পড়ার উপায় কী?",
     'তিনটি পথ: সরকারি ফুল স্কলারশিপ (<a href="/scholarships/">সব স্কলারশিপের তালিকা</a>), টিউশন-ফ্রি দেশ (<a href="/guides/tuition-free/">জার্মানি, নরওয়ে ইত্যাদি</a>), আর PhD-তে বিশ্ববিদ্যালয়ের ফান্ডিং — TA/RA বা বেতনভুক্ত PhD (<a href="/guides/funded-phd/">ফান্ডেড PhD গাইড</a>)।'),
    ("এজেন্ট ছাড়া কি নিজে আবেদন করা যায়?",
     'হ্যাঁ। বেশিরভাগ বিশ্ববিদ্যালয় আর সরকারি স্কলারশিপে নিজেই অনলাইনে আবেদন করা যায়, আর এই সাইটের প্রতিটি স্কলারশিপে অফিসিয়াল আবেদনের লিংক আছে। এজেন্ট নিলে আগে <a href="/guides/fraud/">প্রতারণা সতর্কতা</a> পড়ুন।'),
    ("পার্ট-টাইম কাজ করে কি পড়ার খরচ চালানো যায়?",
     'পুরো খরচ চালানোর পরিকল্পনা করা ঠিক নয়। কাজের ঘণ্টা সীমিত (যেমন যুক্তরাজ্যে টার্মে সপ্তাহে ২০ ঘণ্টা, ইতালিতে বছরে ১,০৪০ ঘণ্টা), আর ভিসার আর্থিক প্রমাণ আলাদাভাবে দেখাতে হয়। বিস্তারিত: <a href="/guides/part-time-work/">পড়ার সময় পার্ট-টাইম কাজ</a>।'),
    ("PhD-র জন্য কি আগে প্রফেসরের সাথে যোগাযোগ করতে হয়?",
     'অনেক দেশে হ্যাঁ — বিশেষ করে যুক্তরাজ্য, ইউরোপ, অস্ট্রেলিয়া আর যুক্তরাষ্ট্রে RA ফান্ডিংয়ের জন্য। DAAD-এর কিছু স্কলারশিপে সুপারভাইজারের সম্মতিপত্রও লাগে। দেখুন <a href="/guides/professor-email/">প্রফেসরকে ইমেইল</a> আর <a href="/professors/">প্রফেসর সার্চ</a>।'),
    ("স্বামী/স্ত্রী বা সন্তানকে কি সঙ্গে নেওয়া যায়?",
     'অনেক দেশে নির্ভরশীলদের ভিসা আছে, তবে শর্ত দেশ ও কোর্সভেদে আলাদা। যেমন যুক্তরাষ্ট্রে স্বামী/স্ত্রী ও সন্তানের নিজস্ব ভিসা আর আলাদা I-20 লাগে (EducationUSA)। আবেদনের আগে সেই দেশের অভিবাসন ওয়েবসাইটে নির্ভরশীলদের নিয়ম দেখুন।'),
    ("কোন কাগজ সত্যায়ন করতে হয়, কোথায়?",
     'সাধারণত সনদ ও মার্কশিট শিক্ষা বোর্ড/বিশ্ববিদ্যালয়, শিক্ষা মন্ত্রণালয় আর পররাষ্ট্র মন্ত্রণালয়ে (অথবা e-Apostille)। ধাপে ধাপে: <a href="/guides/documents/">কাগজপত্র ও সত্যায়ন</a>।'),
    ("এই সাইটের তথ্য কতটা নির্ভরযোগ্য, কবে আপডেট হয়?",
     'সব তথ্য সরকার, দূতাবাস, বিশ্ববিদ্যালয় বা স্কলারশিপদাতার অফিসিয়াল ওয়েবসাইট থেকে নেওয়া, প্রতিটির সাথে সূত্রের লিংক আছে। তালিকা প্রতি সপ্তাহে আপডেট হয়, আর মেয়াদ পেরোনো স্কলারশিপ সরিয়ে দেওয়া হয়। তবু আবেদনের আগে সূত্র লিংকে মিলিয়ে নিন। ভুল চোখে পড়লে জানান: <a href="mailto:higherstudyinfo30@gmail.com">higherstudyinfo30@gmail.com</a>।'),
]


def faq_body(updated):
    items = "".join(f'<details class="faq"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in FAQ]}
    script = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False).replace("</", "<\\/") + "</script>"
    return f"""<style>.faq{{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:12px 16px}}
.faq summary{{cursor:pointer;font-weight:600;font-size:17px}}.faq p{{margin:10px 0 0}}.faq a{{color:var(--accent)}}.faqs{{display:flex;flex-direction:column;gap:10px;max-width:820px}}</style>
<div class="wrap">
{nav("/guides/")}
<article class="prose" style="max-width:100%">
  <nav class="crumbs"><a href="/guides/">গাইড ও টুল</a></nav>
  <span class="eyebrow">প্রশ্নোত্তর</span>
  <h1>সচরাচর জিজ্ঞাসা (FAQ)</h1>
  <p class="lede" style="max-width:68ch">বিদেশে উচ্চশিক্ষা নিয়ে বাংলাদেশি শিক্ষার্থীদের সবচেয়ে বেশি প্রশ্নগুলো — উত্তরের সাথে বিস্তারিত গাইড আর অফিসিয়াল সূত্রের লিংক।</p>
  <div class="faqs">{items}</div>
</article>
{FOOTER}
</div>
{script}"""


def post_study_body(updated):
    rows = "".join(f'<tr><td><a href="/guides/visa/#{VISA_IDS[v["c"]]}">{v["bn"]}</a></td><td>{html.escape(v["post"])}</td></tr>' for v in VISA if v["post"])
    srcs, seen = [], set()
    for v in VISA:
        if v["post"]:
            for t, u in v["src"]:
                if u not in seen:
                    seen.add(u)
                    srcs.append((t, u))
    return _guide("post-study-work", "পড়া শেষে কাজের ভিসা — দেশভিত্তিক",
        "পড়া শেষ হলে অনেক দেশ চাকরি খুঁজতে বা কাজ করতে আলাদা ভিসা বা পারমিট দেয় — দেশ বাছাইয়ে এটা বড় বিষয়। এখানে প্রতিটি দেশের সরকারি সূত্রের তথ্য।",
        f"""<div class="tbl-wrap"><table class="t fit"><tr><th>দেশ</th><th>পড়া শেষে থাকার ও কাজের সুযোগ</th></tr>{rows}</table></div>
  <p class="meta">মালয়েশিয়ার জন্য অফিসিয়াল সূত্রে এমন ভিসার তথ্য পাইনি, তাই রাখা হয়নি। নিয়ম ঘন ঘন বদলায় — বিশেষ করে কানাডা, অস্ট্রেলিয়া আর যুক্তরাজ্যে। আবেদনের আগে সূত্র লিংকে মিলিয়ে নিন।</p>
  <h2>যা মনে রাখবেন</h2>
  <ul>
    <li>এসব ভিসার শর্ত অনেক সময় পড়ার শুরুতেই ঠিক হয় — যেমন কানাডায় প্রতিষ্ঠান PGWP-যোগ্য কিনা, যুক্তরাষ্ট্রে ডিগ্রি STEM তালিকায় কিনা। ভর্তির আগেই দেখে নিন।</li>
    <li>পুরো পড়ার সময় ফুল-টাইম স্ট্যাটাস আর ভিসার শর্ত (যেমন <a href="/guides/part-time-work/">কাজের ঘণ্টার সীমা</a>) মেনে চলুন — ভাঙলে পরে এই সুযোগ হারাতে পারেন।</li>
    <li>পাসপোর্টের মেয়াদ আগেই বাড়িয়ে নিন; কানাডায় PGWP পাসপোর্টের মেয়াদের বেশি দেওয়া হয় না।</li>
    <li>স্থানীয় ভাষা জানা চাকরির সুযোগ অনেক বাড়ায় — দেখুন <a href="/guides/other-tests/">ভাষার পরীক্ষা</a>।</li>
  </ul>""", srcs,
        '<section class="rel"><h2>সম্পর্কিত</h2><ul class="tags"><li><a href="/guides/visa/">স্টুডেন্ট ভিসা — দেশভিত্তিক</a></li><li><a href="/guides/part-time-work/">পড়ার সময় কাজ</a></li><li><a href="/guides/tuition-free/">টিউশন-ফ্রি দেশ</a></li><li><a href="/tools/budget/">বাজেট ক্যালকুলেটর</a></li></ul></section>')


SL_CSS = """<style>
.slbtn{font:inherit;font-weight:600;font-size:14px;cursor:pointer;border:1px solid var(--accent);color:var(--accent);background:var(--surface);border-radius:8px;padding:7px 12px}
.slbtn[aria-pressed="true"]{background:var(--accent);color:var(--surface)}
</style>"""


def shortlist_body(updated):
    script = """<script>
(function(){
  var K="hsi-shortlist",l=[];try{l=JSON.parse(localStorage.getItem(K)||"[]")}catch(e){}
  var esc=function(s){return String(s).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})};
  var bn=function(n){return String(n).replace(/\\d/g,function(d){return "০১২৩৪৫৬৭৮৯"[d]})};
  var t=new Date();t.setHours(0,0,0,0);
  var out=document.getElementById("sl"),cnt=document.getElementById("sl-n");
  function left(d){if(!d)return "";var x=Math.round((new Date(d+"T00:00:00")-t)/864e5);return x<0?"পেরিয়ে গেছে":x===0?"আজ শেষ":bn(x)+" দিন বাকি"}
  function draw(all){
    var rows=all.filter(function(r){return l.indexOf(r.id)>=0}).sort(function(a,b){return (a.d||"9999")<(b.d||"9999")?-1:1});
    var gone=l.filter(function(id){return !all.some(function(r){return r.id===id})}).length;
    cnt.textContent=bn(rows.length);
    if(!rows.length){out.innerHTML='<p class="empty">শর্টলিস্ট খালি। যেকোনো স্কলারশিপের পেজে “☆ শর্টলিস্টে রাখুন” চাপুন — শুরু করতে পারেন <a href="/scholarships/">সব স্কলারশিপের তালিকা</a> বা <a href="/tools/eligibility/">যোগ্যতা যাচাই</a> থেকে।</p>'+(gone?'<p class="meta">'+bn(gone)+'টি আগের সেভ করা স্কলারশিপ আর তালিকায় নেই (মেয়াদ পেরিয়েছে)।</p>':'');return}
    out.innerHTML='<div class="tbl-wrap"><table class="t"><tr><th>স্কলারশিপ</th><th>দেশ · লেভেল</th><th>সুবিধা</th><th>IELTS / English</th><th>শেষ তারিখ</th><th></th></tr>'+rows.map(function(r){
      return '<tr><td><a href="/scholarship/'+r.id+'/">'+esc(r.n)+'</a>'+(r.w?'<br><small class="meta">⏳ পরের রাউন্ডের অপেক্ষায়</small>':'')+'</td><td>'+esc(r.c)+' · '+esc(r.l)+'</td><td>'+esc(r.cov)+'</td><td>'+esc(r.e)+'</td><td>'+(r.d?esc(r.d)+'<br><small class="meta">'+left(r.d)+'</small>'+(r.ics?'<br><a href="/scholarship/'+r.id+'/deadline.ics" download>📅 .ics</a>':''):'<span class="meta">—</span>')+'</td><td><button type="button" class="obtn rm" data-id="'+r.id+'" style="padding:4px 10px;font-size:13px">সরান</button></td></tr>';
    }).join("")+'</table></div>'+(gone?'<p class="meta">'+bn(gone)+'টি সেভ করা স্কলারশিপ আর তালিকায় নেই (মেয়াদ পেরিয়েছে)।</p>':'');
    out.querySelectorAll(".rm").forEach(function(b){b.onclick=function(){l.splice(l.indexOf(b.dataset.id),1);try{localStorage.setItem(K,JSON.stringify(l))}catch(e){}draw(all)}});
  }
  fetch("/data/scholarships.json").then(function(r){return r.json()}).then(draw).catch(function(){out.innerHTML='<p class="empty">তালিকা লোড করা যায়নি। পেজটি আবার খুলুন।</p>'});
})();
</script>"""
    return f"""<div class="wrap">
{nav()}
<nav class="crumbs"><a href="/">হোম</a></nav>
<header style="display:flex;flex-direction:column;gap:10px">
  <span class="eyebrow">টুল</span>
  <h1>আমার শর্টলিস্ট (<span id="sl-n">০</span>)</h1>
  <p class="lede">যেসব স্কলারশিপ পেজে “☆ শর্টলিস্টে রাখুন” চেপেছেন, সেগুলো এখানে পাশাপাশি — শেষ তারিখ অনুযায়ী সাজানো। তালিকা শুধু এই ব্রাউজারে থাকে, কোথাও পাঠানো হয় না।</p>
</header>
<style>#sl a{{color:var(--accent)}}#sl td:first-child{{min-width:170px}}</style>
<section id="sl"><p class="empty">লোড হচ্ছে…</p></section>
<p class="meta">আবেদনের পরিকল্পনা করতে <a href="/tools/timeline/">টাইমলাইন প্ল্যানার</a> ব্যবহার করুন।</p>
{FOOTER}
</div>
{script}"""


TIMELINE = [  # (months before the application deadline, step, link)
    (12, "লক্ষ্য দেশ, প্রোগ্রাম আর স্কলারশিপ বাছাই; শর্ত মিলিয়ে নিন", "/tools/eligibility/"),
    (10, "IELTS/TOEFL বা GRE-র প্রস্তুতি শুরু; পরীক্ষার তারিখ বুক", "/guides/english-tests/"),
    (8, "PhD/গবেষণা হলে সম্ভাব্য সুপারভাইজারদের ইমেইল", "/guides/professor-email/"),
    (6, "পাসপোর্ট (মেয়াদ দেখে) আর সনদ সত্যায়নের কাজ শুরু", "/guides/documents/"),
    (4, "ইংরেজি/অন্যান্য পরীক্ষা দেওয়া শেষ — স্কোর পাঠানোর সময় রাখুন", "/guides/other-tests/"),
    (3, "রেফারিদের কাছে LOR চাওয়া (UCLA ২–৩ মাস আগে বলতে বলে)", "/guides/lor/"),
    (2, "SOP/Motivation Letter আর Research Proposal-এর খসড়া, অন্যকে দিয়ে পড়ানো", "/guides/sop/"),
    (1, "CV, স্ক্যান কপি, ফর্ম পূরণ; রেফারিদের মনে করিয়ে দেওয়া", "/guides/lor/"),
    (0, "আবেদন জমা — শেষ দিনের আগেই", "/deadlines/"),
]
AFTER = [  # (months before the course starts, step, link)
    (5, "ফলাফল/অফার এলে শর্ত মিলিয়ে গ্রহণ; স্কলারশিপ ইন্টারভিউর প্রস্তুতি", "/guides/interview/"),
    (4, "স্টুডেন্ট ফাইল খুলে টিউশন/ব্লকড অ্যাকাউন্টে টাকা পাঠানো", "/guides/student-file/"),
    (3, "ভিসার আবেদন ও ইন্টারভিউ", "/guides/visa/"),
    (1, "যাওয়ার আগের চেকলিস্ট — টিকিট, বীমা, থাকার জায়গা", "/guides/pre-departure/"),
]


def timeline_body(updated):
    data = json.dumps({"before": TIMELINE, "after": AFTER}, ensure_ascii=False)
    script = """<script>
(function(){
  var T=__T__,$=function(i){return document.getElementById(i)};
  var bn=function(n){return String(n).replace(/\\d/g,function(d){return "০১২৩৪৫৬৭৮৯"[d]})};
  var M=["জানুয়ারি","ফেব্রুয়ারি","মার্চ","এপ্রিল","মে","জুন","জুলাই","আগস্ট","সেপ্টেম্বর","অক্টোবর","নভেম্বর","ডিসেম্বর"];
  function sub(d,m){var x=new Date(d.getFullYear(),d.getMonth()-m,Math.min(d.getDate(),28));return x}
  function fmt(d){return M[d.getMonth()]+" "+bn(d.getFullYear())}
  var now=new Date();now.setDate(1);now.setHours(0,0,0,0);
  function li(d,s,h){var past=d<now;return '<li'+(past?' class="past"':'')+'><span class="when">'+fmt(d)+(past?' · দেরি হয়েছে — এখনই করুন':'')+'</span><a href="'+h+'">'+s+'</a></li>'}
  function run(){
    var dl=$("t-dl").value,st=$("t-start").value;
    if(!dl){$("t-out").innerHTML='<p class="empty">আবেদনের শেষ তারিখ দিন।</p>';return}
    var D=new Date(dl+"T00:00:00"),h='<h2>আবেদনের আগে</h2><ol class="tl">'+T.before.map(function(x){return li(sub(D,x[0]),x[1],x[2])}).join("")+'</ol>';
    if(st){var S=new Date(st+"-01T00:00:00");h+='<h2>অফার পাওয়ার পর</h2><ol class="tl">'+T.after.map(function(x){return li(sub(S,x[0]),x[1],x[2])}).join("")+'</ol>'}
    $("t-out").innerHTML=h;
  }
  ["t-dl","t-start"].forEach(function(i){$(i).addEventListener("input",run)});run();
})();
</script>""".replace("__T__", data)
    return f"""<style>.tl{{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:8px;border-left:3px solid var(--accent);padding-left:14px}}
.tl li{{display:flex;flex-direction:column;gap:2px}}.tl .when{{font-family:var(--mono);font-size:13px;color:var(--muted)}}.tl a{{color:var(--fg);font-weight:600}}
.tl li.past a{{color:var(--muted);font-weight:400}}</style>
<div class="wrap">
{nav("/guides/")}
<article class="prose" style="max-width:100%">
  <nav class="crumbs"><a href="/guides/">গাইড ও টুল</a></nav>
  <span class="eyebrow">টুল</span>
  <h1>আবেদনের টাইমলাইন প্ল্যানার</h1>
  <p class="lede" style="max-width:68ch">আপনার লক্ষ্য স্কলারশিপ বা প্রোগ্রামের শেষ তারিখ দিন — কোন মাসে কী করবেন, উল্টো দিক থেকে হিসাব করে দেখাবে। কোর্স শুরুর মাস দিলে অফারের পরের ধাপগুলোও দেখাবে। শেষ তারিখ খুঁজতে দেখুন <a href="/deadlines/">শেষ তারিখ সামনে</a>।</p>
  <div class="calc">
    <label>আবেদনের শেষ তারিখ<input id="t-dl" type="date"></label>
    <label>কোর্স শুরুর মাস (ঐচ্ছিক)<input id="t-start" type="month"></label>
  </div>
  <div id="t-out"></div>
  <p class="warn">সময়গুলো সাধারণ পরামর্শ — যেমন LOR-এর জন্য UCLA ২–৩ মাস আগে বলতে বলে, আর কিছু স্কলারশিপের শেষ তারিখ শুরুর ১৮ মাস আগেও হয় (EducationUSA)। নিজের প্রোগ্রাম, পরীক্ষার তারিখ আর ভিসার প্রসেসিং সময় অনুযায়ী সামঞ্জস্য করুন।</p>
</article>
{FOOTER}
</div>
{script}"""


def portals_body(updated):
    return _guide("application-portals", "দেশভিত্তিক আবেদন পোর্টাল",
        "অনেক দেশে বিশ্ববিদ্যালয়ে সরাসরি নয়, একটা কেন্দ্রীয় পোর্টাল দিয়ে আবেদন করতে হয়। কোন দেশে কোন পোর্টাল, ফি কত আর সময়সীমা কখন — অফিসিয়াল সূত্র থেকে।",
        """<div class="tbl-wrap"><table class="t fit">
    <tr><th>পোর্টাল</th><th>কোথায়, কাদের জন্য</th><th>ফি ও সময়</th></tr>
    <tr><td><b>uni-assist</b><br><span class="meta">জার্মানি</span></td><td>অনেক জার্মান বিশ্ববিদ্যালয় বিদেশি সনদ যাচাই uni-assist-কে দিয়ে করায়। কিছু বিশ্ববিদ্যালয় VPD পদ্ধতি ব্যবহার করে — uni-assist থেকে VPD নিয়ে তারপর নিজে বিশ্ববিদ্যালয়ে আবেদন করতে হয় (বেশি সময় রাখুন)।</td><td>প্রতি সেমিস্টারে প্রথম কোর্স €75, প্রতিটি অতিরিক্ত কোর্স €30 — কোর্সপ্রতি হিসাব, বিশ্ববিদ্যালয়প্রতি নয়; VPD-তেও একই ফি। কিছু বিশ্ববিদ্যালয় ফি নিজে দেয়।</td></tr>
    <tr><td><b>UCAS</b><br><span class="meta">যুক্তরাজ্য — স্নাতক</span></td><td>এক আবেদনে সর্বোচ্চ ৫টি পছন্দ (কনজারভেটরিতে ৬)। মাস্টার্স/PhD-তে সাধারণত বিশ্ববিদ্যালয়ে সরাসরি আবেদন।</td><td>২০২৭ চক্রে ফি £34.50। ১৫ অক্টোবর: Oxford, Cambridge ও বেশিরভাগ মেডিসিন/ডেন্টিস্ট্রি; ১৩ জানুয়ারি ২০২৭: বেশিরভাগ কোর্সের সমান বিবেচনার শেষ দিন; চূড়ান্ত শেষ ২৩ সেপ্টেম্বর ২০২৭।</td></tr>
    <tr><td><b>Common App</b><br><span class="meta">যুক্তরাষ্ট্র — স্নাতক</span></td><td>এক প্রোফাইল দিয়ে অনেক কলেজে আবেদন; প্রতিটি কলেজের নিজস্ব শেষ তারিখ, ফি ও শর্ত।</td><td>প্রয়োজনভিত্তিক Common App fee waiver বিদেশিরাও চাইতে পারেন, তবে কলেজভেদে গ্রহণ আলাদা (কেউ শুধু মার্কিন শিক্ষার্থীদের জন্য)। জমার সময় আপনার নিজের সময় অঞ্চলে রাত ১১:৫৯।</td></tr>
    <tr><td><b>Studielink</b><br><span class="meta">নেদারল্যান্ডস</span></td><td>প্রথমে Studielink-এ ভর্তির অনুরোধ, তারপর বিশ্ববিদ্যালয়ের নিজস্ব পোর্টালে কাগজ। বিদেশ থেকে DigiD ছাড়াই লগইন করা যায়। কিছু প্রতিষ্ঠান বিদেশিদের জন্য আলাদা পদ্ধতি ব্যবহার করে।</td><td>২০২৭–২৮-এর আবেদন ১ অক্টোবর ২০২৬ থেকে। Numerus fixus প্রোগ্রাম ১৫ জানুয়ারি, বাকিগুলো ১ মে (রাত ১১:৫৯) — তবে non-EU শিক্ষার্থীদের জন্য বিশ্ববিদ্যালয় প্রায়ই আগের শেষ তারিখ দেয়।</td></tr>
    <tr><td><b>Universitaly</b><br><span class="meta">ইতালি</span></td><td>ভিসার আগে প্রাক-নিবন্ধন (pre-enrolment); বিশ্ববিদ্যালয়ে আলাদাভাবে ভর্তির আবেদন।</td><td>দেখুন <a href="/guides/visa/#italy">ইতালির ভিসা</a>।</td></tr>
    <tr><td><b>Campus France (Études en France)</b><br><span class="meta">ফ্রান্স</span></td><td>অনেক দেশের শিক্ষার্থীদের জন্য ভর্তি ও ভিসা প্রক্রিয়া এক প্ল্যাটফর্মে।</td><td>দেখুন <a href="/guides/visa/#france">ফ্রান্সের ভিসা</a>।</td></tr>
  </table></div>
  <h2>যা মনে রাখবেন</h2>
  <ul>
    <li>পোর্টালের শেষ তারিখ আর বিশ্ববিদ্যালয়ের নিজের (বিশেষত বিদেশিদের) শেষ তারিখ আলাদা হতে পারে — দুটোই দেখুন, আর আগেরটা মানুন।</li>
    <li>স্কলারশিপের শেষ তারিখ প্রায়ই ভর্তির শেষ তারিখের আগে — দেখুন <a href="/deadlines/">শেষ তারিখ সামনে</a> আর <a href="/tools/timeline/">টাইমলাইন প্ল্যানার</a>।</li>
    <li>পোর্টালের অ্যাকাউন্ট নিজের ইমেইলে খুলুন, পাসওয়ার্ড কাউকে দেবেন না — দেখুন <a href="/guides/fraud/">প্রতারণা সতর্কতা</a>।</li>
    <li>ফি অনলাইনে দিতে আন্তর্জাতিক লেনদেন চালু কার্ড লাগে; বাংলাদেশ থেকে আবেদন ফি পাঠানোর নিয়ম দেখুন <a href="/guides/student-file/">স্টুডেন্ট ফাইল</a> গাইডে।</li>
  </ul>""",
        [("uni-assist — Handling fees", "https://www.uni-assist.de/en/how-to-apply/pay-all-fees/handling-fees/"),
         ("uni-assist — VPD (preliminary review documentation)", "https://www.uni-assist.de/en/tools/glossary-of-terms/description/term/vorpruefungsdokumentation-vpd-preliminary-review-documentation/"),
         ("UCAS — Application fee for the 2027 cycle", "https://www.ucas.com/faqs/what-is-the-application-fee-for-the-2027-cycle"),
         ("UCAS — Dates and deadlines", "https://www.ucas.com/applying/applying-to-university/dates-and-deadlines-for-uni-applications"),
         ("Common App — Fee waiver", "https://appsupport.commonapp.org/applicantsupport/s/article/What-do-I-need-to-know-about-the-Common-App-fee-waiver"),
         ("Common App — 2026–27 first-year requirements grid (PDF)", "https://content.commonapp.org/Files/ReqGrid.pdf"),
         ("Studielink — Make sure you are on time", "https://info.studielink.nl/en/how-to-use-studielink/make-sure-you-are-on-time"),
         ("Study in NL — How to apply", "https://www.studyinnl.org/plan-your-stay/how-to-apply"),
         ("Universitaly", "https://www.universitaly.it/"),
         ("Campus France — Student long-stay visa", "https://www.campusfrance.org/en/student-long-stay-visa")])


def cv_body(updated):
    skeleton = """[Full Name]
[City, Country] · [email] · [phone] · [LinkedIn / Google Scholar / GitHub]

EDUCATION
BSc in [Subject], [University], [Year]  — CGPA [x.xx/4.00]
  Thesis: "[Title]" — Supervisor: [Name]

RESEARCH EXPERIENCE
[Role], [Lab / Project], [Institution], [Month Year – Month Year]
  - What you did and what came of it (method, result, paper)

PUBLICATIONS & PRESENTATIONS
[Authors] ([Year]). [Title]. [Journal / Conference].

AWARDS & SCHOLARSHIPS
[Award], [Awarding body], [Year]

TEACHING / WORK EXPERIENCE  (relevant only)
SKILLS  (lab techniques, software, programming, languages with test scores)
REFERENCES  [Name, title, institution, official email] — or "Available on request\""""
    return _guide("cv", "একাডেমিক CV ও Europass CV",
        "মাস্টার্স, PhD আর স্কলারশিপের আবেদনে প্রায় সবসময় CV লাগে। চাকরির রিজিউমের চেয়ে একাডেমিক CV আলাদা: লক্ষ্য গবেষক ও শিক্ষার্থী হিসেবে আপনার পরিচয় তুলে ধরা। ইউরোপের অনেক আবেদনে Europass ফরম্যাট চাওয়া হয়।",
        f"""<h2>রিজিউম আর একাডেমিক CV-র পার্থক্য</h2>
  <ul>
    <li><b>দৈর্ঘ্য:</b> শুরুর পর্যায়ের রিজিউম সাধারণত ১ পৃষ্ঠা; CV প্রায়ই দুই বা আরও বেশি পৃষ্ঠা (Purdue OWL)।</li>
    <li><b>উদ্দেশ্য:</b> রিজিউম পেশাগত পরিচয় দেখায়; CV দেখায় গবেষণা, পড়ানো আর প্রকাশনা — একাডেমিক পরিচয়।</li>
    <li><b>কাঠামো নমনীয়:</b> নির্দিষ্ট কোনো ফরম্যাট নেই — অংশগুলো আবেদন অনুযায়ী সাজান (Berkeley), প্রতিটি অংশে সাম্প্রতিকতমটা আগে (Cornell)।</li>
  </ul>
  <h2>অংশগুলো (সাধারণ ক্রম)</h2>
  <ol class="steps">
    <li><h3>যোগাযোগ</h3><p>নাম, ইমেইল, ফোন, প্রাসঙ্গিক প্রোফাইল লিংক। ছবি, জন্মতারিখ, ধর্ম, বৈবাহিক অবস্থা সাধারণত লাগে না — প্রোগ্রাম বা দেশ চাইলে তবেই দিন।</p></li>
    <li><h3>শিক্ষা</h3><p>নতুন আবেদনকারীর জন্য সবার আগে (Berkeley): ডিগ্রি, বিশ্ববিদ্যালয়, সাল, CGPA, থিসিসের শিরোনাম ও সুপারভাইজার।</p></li>
    <li><h3>গবেষণা অভিজ্ঞতা</h3><p>প্রজেক্ট, আপনার ভূমিকা, পদ্ধতি আর ফল — সংখ্যা দিয়ে।</p></li>
    <li><h3>প্রকাশনা ও উপস্থাপনা</h3><p>জার্নাল, কনফারেন্স, পোস্টার — একটি নির্দিষ্ট রেফারেন্স স্টাইলে।</p></li>
    <li><h3>পুরস্কার ও স্কলারশিপ</h3><p>মেধাবৃত্তি, ডিনস লিস্ট, প্রতিযোগিতা।</p></li>
    <li><h3>পড়ানো ও প্রাসঙ্গিক কাজ</h3><p>TA, টিউটরিং, প্রাসঙ্গিক চাকরি। অপ্রাসঙ্গিক চাকরি আর স্কুলের অর্জন বাদ দিন (Purdue OWL)।</p></li>
    <li><h3>দক্ষতা ও ভাষা</h3><p>ল্যাব টেকনিক, সফটওয়্যার, প্রোগ্রামিং; ভাষার দক্ষতা পরীক্ষার স্কোরসহ।</p></li>
    <li><h3>রেফারেন্স</h3><p>নাম, পদবি, প্রতিষ্ঠান, অফিসিয়াল ইমেইল — দেখুন <a href="/guides/lor/">LOR গাইড</a>।</p></li>
  </ol>
  <h2>CV-র কাঠামো (ইংরেজিতে)</h2>
  <pre class="ooutput">{html.escape(skeleton)}</pre>
  <h2>Europass CV</h2>
  <ul>
    <li>ইউরোপীয় ইউনিয়নের বিনামূল্যের সেবা — কোনো লুকানো খরচ বা প্রিমিয়াম নেই।</li>
    <li>প্রোফাইল ছাড়াও CV বানানো যায়; প্রোফাইল থাকলে সংরক্ষিত তথ্য থেকে বিভিন্ন CV আর কভার লেটার বানানো সহজ। ২৯টি ভাষা আর কয়েকটি টেমপ্লেট।</li>
    <li>শুরু করুন <a href="https://europass.europa.eu/en" target="_blank" rel="noopener">europass.europa.eu</a>-তে "Create my Europass" চেপে।</li>
    <li>প্রোগ্রাম Europass চাইলে তবেই ব্যবহার করুন; নইলে উপরের একাডেমিক CV ফরম্যাট সাধারণত বেশি পরিষ্কার।</li>
  </ul>
  <h2>সাধারণ ভুল</h2>
  <ul>
    <li>সব আবেদনে একই CV — প্রোগ্রাম অনুযায়ী অংশের ক্রম আর জোর বদলান।</li>
    <li>দাবি কিন্তু প্রমাণ নেই — "hardworking" না লিখে কাজ আর ফল দেখান।</li>
    <li>SOP-এ যা বলেছেন তার সাথে CV-র তারিখ বা তথ্য না মেলা।</li>
    <li>PDF না করে Word ফাইল পাঠানো, বা ফাইলের নাম "CV final final.pdf" — "Rahman_CV.pdf" ধরনের নাম দিন।</li>
  </ul>""",
        [("Purdue OWL — Writing the curriculum vitae", "https://owl.purdue.edu/owl/job_search_writing/resumes_and_vitas/writing_the_cv.html"),
         ("Purdue OWL — Graduate school applications: process and materials", "https://owl.purdue.edu/owl/general_writing/graduate_school_applications/graduate_school_applications_overview/overview_process_and_materials.html"),
         ("UC Berkeley Career Engagement — The CV: elements", "https://career.berkeley.edu/grad-students-postdocs/academic-job-search/the-cv-part-2-elements/"),
         ("Cornell Graduate School — Resumes and CVs", "https://gradschool.cornell.edu/career-and-professional-development/pathways-to-success/prepare-for-your-career/take-action/resumes-and-cvs/"),
         ("Europass — The new Europass CV and cover letter tool", "https://europass.europa.eu/en/news/new-europass-cv-and-cover-letter-online-tool"),
         ("Europass — How to complete my Europass profile", "https://europass.europa.eu/en/how-complete-my-europass-profile")])
