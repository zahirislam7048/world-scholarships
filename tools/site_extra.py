"""Site-wide navigation and the cross-country pages: deadlines, search, about, privacy."""
import html
import json

from build_preview import CONTINENTS, COUNTRIES, load_rows

NAV_CSS = """<style>
.topnav{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:8px 20px;padding-block:14px;border-bottom:1px solid var(--line)}
.topnav .brand{font-family:var(--display);font-weight:700;font-size:18px;color:var(--fg);text-decoration:none}
.topnav .links{display:flex;flex-wrap:wrap;gap:4px 18px}
.topnav .links a{color:var(--muted);text-decoration:none;font-size:15px}
.topnav .links a:hover,.topnav .links a[aria-current]{color:var(--accent)}
.sitefoot{font-size:13px;color:var(--muted);border-top:1px solid var(--line);padding-top:14px}
.sitefoot a{color:var(--muted)}
a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
</style>"""

NAV_ITEMS = [("/deadlines/", "শেষ তারিখ সামনে"), ("/search/", "সব স্কলারশিপ খুঁজুন"), ("/guides/", "গাইড ও টুল"), ("/about/", "আমাদের সম্পর্কে")]


def nav(current=""):
    cur = ' aria-current="page"'
    links = "".join(f'<a href="{href}"{cur if href == current else ""}>{label}</a>' for href, label in NAV_ITEMS)
    return f'<nav class="topnav" aria-label="মেনু"><a class="brand" href="/">Higher Study Info</a><span class="links">{links}</span></nav>'


EMAIL = "higherstudyinfo30@gmail.com"
PHONE_DISPLAY = "+880 1644-842785"
PHONE_TEL = "+8801644842785"
CONTACT_HTML = (f'<ul><li>ইমেইল: <a href="mailto:{EMAIL}">{EMAIL}</a></li>'
                f'<li>ফোন: <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li></ul>')

CHECKED = ""  # set by build_site.main from data/LAST_CHECKED
GUIDES_CHECKED = "2026-11-04"  # when the guide and tool figures were last verified
PRIVACY_EFFECTIVE = "2026-11-04"

FOOTER = ('<footer class="sitefoot"><a href="/about/">আমাদের সম্পর্কে</a> · <a href="/privacy/">Privacy Policy</a>'
          f' · যোগাযোগ: <a href="mailto:{EMAIL}">{EMAIL}</a>'
          ' · তথ্য অফিসিয়াল সূত্র থেকে, প্রতি সপ্তাহে আপডেট হয়</footer>')

BN_MONTHS = ["জানুয়ারি", "ফেব্রুয়ারি", "মার্চ", "এপ্রিল", "মে", "জুন", "জুলাই", "আগস্ট", "সেপ্টেম্বর", "অক্টোবর", "নভেম্বর", "ডিসেম্বর"]
BN_DIGITS = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")


def bn(n):
    return str(n).translate(BN_DIGITS)


def all_rows():
    out = []
    for slug, (name_en, title, heading) in COUNTRIES.items():
        cont = slug.split("/")[0]
        for r in load_rows(slug):
            out.append({**r, "slug": slug, "section": cont, "section_bn": CONTINENTS[cont][1]})
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
  <span class="what"><a href="{html.escape(apply)}" target="_blank" rel="noopener">{html.escape(r["scholarship_name"])}</a>
  <span>{html.escape(name_en)} · {html.escape(r["provider"])} · {html.escape(r["level"])} · <a href="/{r["slug"]}/">বিস্তারিত</a></span></span>
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
  <p class="lede">যেসব স্কলারশিপের শেষ তারিখ জানা আছে, সেগুলো তারিখ অনুযায়ী সাজানো। নাম চাপলে আবেদনের পেজ খুলবে। ১৪ দিনের কম বাকি থাকলে লাল চিহ্ন দেখাবে। শেষ তারিখ নেই এমন স্কলারশিপ দেখতে <a href="/search/">সব স্কলারশিপ খুঁজুন</a>।</p>
</header>
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
        "u": f'/{r["slug"]}/', "el": r.get("eligibility", ""),
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
    }).sort(function(a,b){return (a.d&&a.d>=today?a.d:"9999")<(b.d&&b.d>=today?b.d:"9999")?-1:1});
    cnt.textContent=bn(rows.length)+"টি স্কলারশিপ";
    if(!rows.length){out.innerHTML='<p class="empty">কিছু পাওয়া যায়নি। অন্য শব্দ দিয়ে খুঁজুন বা ফিল্টার সরান।</p>';return}
    out.innerHTML=rows.map(function(r){
      var info=r.a===r.src;
      return '<article class="res"><span class="where">'+esc(r.c)+'</span><h3>'+esc(r.n)+'</h3>'+
        '<p>'+esc(r.p)+' · '+esc(r.l)+'</p>'+
        (r.cov?'<p><b>সুবিধা:</b> '+esc(r.cov)+'</p>':'')+
        (r.e?'<p><b>IELTS / English:</b> '+esc(r.e)+'</p>':'')+
        (r.d&&r.d>=today?'<p><b>শেষ তারিখ:</b> '+esc(r.d)+'</p>':'')+
        '<div class="row"><a class="apply'+(info?' info':'')+'" href="'+esc(r.a)+'" target="_blank" rel="noopener">'+(info?'আবেদনের তথ্য ↗':'আবেদন করুন ↗')+'</a><a class="more" href="'+r.u+'">দেশের পেজ</a></div></article>';
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
{FOOTER}
</div>
{script}"""


def about_body(updated):
    total = len(all_rows())
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
</style>"""

GUIDES = [
    ("/guides/documents/", "📄 কাগজপত্র ও সত্যায়ন", "বাংলাদেশ থেকে আবেদনের জন্য সার্টিফিকেট সত্যায়ন, e-Apostille আর পুলিশ ক্লিয়ারেন্স — ধাপে ধাপে।"),
    ("/guides/english-tests/", "🗣️ IELTS, TOEFL, Duolingo, PTE", "বাংলাদেশে ফি, কোথায় বুক করবেন, আর কোন স্কলারশিপে IELTS ছাড়ের পথ আছে।"),
    ("/tools/cgpa/", "🧮 CGPA রূপান্তর", "বাংলাদেশের CGPA থেকে জার্মান গ্রেড (Bavarian formula) আর গ্রেড-ব্যান্ড।"),
    ("/guides/visa/", "🛂 স্টুডেন্ট ভিসা — দেশভিত্তিক", "৯টি দেশে কত টাকা দেখাতে হয়, পড়ার সময় কাজ, ভিসা ফি — অফিসিয়াল সূত্রে।"),
    ("/guides/tuition-free/", "💶 টিউশন-ফ্রি ও কম খরচের দেশ", "জার্মানি, অস্ট্রিয়া, ফ্রান্স, নরওয়ে — EU-র বাইরের শিক্ষার্থীদের টিউশন।"),
    ("/tools/budget/", "💰 বাজেট ক্যালকুলেটর", "প্রথম বছরের আনুমানিক খরচ আর ভিসার জন্য কত দেখাতে হবে — টাকায়।"),
    ("/guides/sop/", "✍️ Statement of Purpose (SOP)", "কাঠামো, দৈর্ঘ্য, কী করবেন না — আর নিজের তথ্য দিয়ে আউটলাইন বানানোর টুল।"),
    ("/guides/motivation-letter/", "📝 Motivation Letter", "DAAD, Erasmus Mundus-এর মতো ইউরোপীয় আবেদনের জন্য — প্রশ্ন, কাঠামো আর আউটলাইন টুল।"),
]


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
        f'<tr><td>{html.escape(COUNTRIES[r["slug"]][0])}</td><td><a href="/{r["slug"]}/">{html.escape(r["scholarship_name"])}</a></td>'
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
     "post": "", "fee": "",
     "apply": ("German Embassy Dhaka — Study visa", "https://dhaka.diplo.de/bd-en/service/2685884-2685884"),
     "src": [("German Embassy Dhaka — Study visa checklist (June 2026)", "https://dhaka.diplo.de/resource/blob/2685888/1826aadb06dfc6b0224e91583b6836cb/p-01-checklist-students-data.pdf"),
             ("DAAD — Side jobs", "https://www.daad.de/en/studying-in-germany/work-career/side-jobs/")]},
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
     "post": "", "fee": "ভিসা (MRV) ফি $185 + SEVIS I-901 ফি $350",
     "apply": ("U.S. Embassy Dhaka", "https://bd.usembassy.gov/"),
     "src": [("travel.state.gov — Student visa", "https://travel.state.gov/content/travel/en/us-visas/study/student-visa.html"),
             ("ICE — I-901 SEVIS fee", "https://www.ice.gov/sevis/i901"),
             ("Study in the States — Working in the US", "https://studyinthestates.dhs.gov/students/work/working-in-the-united-states")]},
    {"c": "Canada", "bn": "কানাডা", "visa": "Study permit",
     "funds": "একক আবেদনকারী: জীবনযাত্রার জন্য CAD 22,895 (1 Sep 2025 থেকে) + প্রথম বছরের টিউশন + যাতায়াত",
     "work": "ক্যাম্পাসের বাইরে টার্মে সপ্তাহে 24 ঘণ্টা; নির্ধারিত ছুটিতে সীমাহীন",
     "post": "", "fee": "",
     "apply": ("IRCC — Study permit", "https://www.canada.ca/en/immigration-refugees-citizenship/services/study-canada/study-permit/get-documents.html"),
     "src": [("IRCC — International students (CIMM, Apr 2026)", "https://www.canada.ca/en/immigration-refugees-citizenship/corporate/transparency/committees/cimm-apr-22-2026/international-students.html"),
             ("IRCC — Work off campus", "https://www.canada.ca/en/immigration-refugees-citizenship/services/study-canada/work/work-off-campus.html")]},
    {"c": "Australia", "bn": "অস্ট্রেলিয়া", "visa": "Student visa (subclass 500)",
     "funds": "AUD 29,710 (12 মাসের জীবনযাত্রা) + প্রথম 12 মাসের কোর্স ফি + যাতায়াত; অথবা বার্ষিক আয় অন্তত AUD 60,000",
     "work": "", "post": "", "fee": "",
     "apply": ("Home Affairs — Student visa", "https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing/changes-to-student-visa-application-rules-500-590"),
     "src": [("Study Australia — Change to evidence of financial capacity", "https://www.studyaustralia.gov.au/en_in/tools-and-resources/news/change-to-evidence-of-financial-capacity-for-student-visas"),
             ("Home Affairs — Financial capacity evidence", "https://immi.homeaffairs.gov.au/help-text/evidence/Pages/et-h0185.aspx")]},
    {"c": "Italy", "bn": "ইতালি", "visa": "Study visa (type D)",
     "funds": "বছরে €10,179.85 (মাসে প্রায় €848) — কিছু কনস্যুলেট ফেরার খরচও (প্রায় €500) চায়",
     "work": "", "post": "", "fee": "",
     "apply": ("Universitaly — pre-enrolment", "https://www.universitaly.it/"),
     "src": [("Italian Consulate — Study visa checklist 2026/2027", "https://consdubai.esteri.it/wp-content/uploads/2026/05/StudyVisa_2026_2027.pdf")]},
    {"c": "Japan", "bn": "জাপান", "visa": "Student (College Student)",
     "funds": "",
     "work": "অনুমতি নিয়ে সপ্তাহে 28 ঘণ্টা (দীর্ঘ ছুটিতে দিনে 8 ঘণ্টা); অনুমতি বিমানবন্দরেই নেওয়া যায়",
     "post": "", "fee": "",
     "apply": ("Study in Japan — Part-time work", "https://www.studyinjapan.go.jp/en/work-in-japan/part-time-jobs/"),
     "src": [("Study in Japan — Part-time work", "https://www.studyinjapan.go.jp/en/work-in-japan/part-time-jobs/")]},
    {"c": "South Korea", "bn": "দক্ষিণ কোরিয়া", "visa": "D-2 student visa",
     "funds": "মাসে অন্তত KRW 900,000 × 6 মাস = প্রায় KRW 5,400,000",
     "work": "অনুমতি নিয়ে স্নাতকে সপ্তাহে 30, স্নাতকোত্তরে 35 ঘণ্টা (সূত্রভেদে আলাদা — বিশ্ববিদ্যালয়ে জেনে নিন); সাধারণত কোরিয়ান ভাষার দক্ষতা লাগে",
     "post": "", "fee": "",
     "apply": ("Study in Korea — Visa and stay", "https://www.studyinkorea.go.kr/ko/plan/visaAndStay.do"),
     "src": [("Study in Korea — Residence and stay", "https://www.studyinkorea.go.kr/ko/life/residenceAndStayInfo.do")]},
    {"c": "Malaysia", "bn": "মালয়েশিয়া", "visa": "Student Pass (EMGS-এর মাধ্যমে)",
     "funds": "",
     "work": "অনুমোদিত জায়গায় সপ্তাহে 20 ঘণ্টা — EMGS বলে শুধু 7 দিনের বেশি ছুটিতে, Immigration বলে পড়ার সময়েও; প্রতিষ্ঠানে জেনে নিন",
     "post": "", "fee": "Student Pass RM60/বছর + ভিসা ফি (দেশভেদে, সর্বোচ্চ RM50) + EMGS প্রসেসিং ফি",
     "apply": ("EMGS — Student Pass", "https://visa.educationmalaysia.gov.my/"),
     "src": [("Immigration Malaysia — Student Pass", "https://www.imi.gov.my/index.php/en/main-services/pass/student-pass/"),
             ("EMGS — FAQ", "https://educationmalaysia.gov.my/get-in-touch/faq")]},
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
        fields = [("prog", "প্রোগ্রাম, বিশ্ববিদ্যালয় ও দেশ", "e.g. MSc Water Management, University of X, Germany"),
                  ("why", "কেন এই বিষয় — কী থেকে আগ্রহ শুরু", "e.g. flood work in my district ..."),
                  ("exp", "আগের পড়া/কাজের অভিজ্ঞতা, যা এই প্রোগ্রামে কাজে লাগবে", "e.g. 2 years at ..., project on ..."),
                  ("fit", "কেন এই প্রোগ্রাম, বিশ্ববিদ্যালয় ও দেশ", "e.g. modules on ..., partner institutes ..."),
                  ("back", "দেশে ফিরে কীভাবে কাজে লাগাবেন", "e.g. apply ... at my department / ministry")]
        order = [("Motivation", "What draws you to this field and why now: {why}."),
                 ("Background", "Studies and work that prepared you, and how: {exp}."),
                 ("Choice", "Why {prog} — the programme, the university and the country: {fit}."),
                 ("Goals during the stay", "What you want to learn or achieve while studying there."),
                 ("After the degree", "How you will use the qualification, especially back home: {back}.")]
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
