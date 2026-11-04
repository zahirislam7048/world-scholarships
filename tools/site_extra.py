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

NAV_ITEMS = [("/deadlines/", "শেষ তারিখ সামনে"), ("/search/", "সব স্কলারশিপ খুঁজুন"), ("/about/", "আমাদের সম্পর্কে")]


def nav(current=""):
    cur = ' aria-current="page"'
    links = "".join(f'<a href="{href}"{cur if href == current else ""}>{label}</a>' for href, label in NAV_ITEMS)
    return f'<nav class="topnav" aria-label="মেনু"><a class="brand" href="/">Higher Study Info</a><span class="links">{links}</span></nav>'


FOOTER = ('<footer class="sitefoot"><a href="/about/">আমাদের সম্পর্কে</a> · <a href="/privacy/">Privacy Policy</a>'
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
  <span class="eyebrow">সব দেশ · সর্বশেষ আপডেট {updated}</span>
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
  <span class="eyebrow">সব দেশ · সর্বশেষ আপডেট {updated}</span>
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
  <p>প্রতি সপ্তাহে তালিকা আপডেট হয়: নতুন বিজ্ঞপ্তি যোগ হয়, মেয়াদ শেষ হওয়া স্কলারশিপ বাদ যায়, আর নতুন দেশ যোগ হয়। সর্বশেষ আপডেট: {updated}।</p>
  <h2>আমরা কারা নই</h2>
  <p>Higher Study Info কোনো সরকার, বিশ্ববিদ্যালয় বা স্কলারশিপ প্রদানকারী প্রতিষ্ঠানের অংশ নয়, আর আবেদন গ্রহণ করে না। আবেদন সবসময় সংশ্লিষ্ট প্রতিষ্ঠানের অফিসিয়াল সাইটে করতে হয়। কেউ এই সাইটের নামে টাকা চাইলে তা প্রতারণা।</p>
  <p><a href="/privacy/">Privacy Policy</a></p>
</article>
{FOOTER}
</div>"""


def privacy_body(updated):
    return f"""<div class="wrap">
{nav()}
<article class="prose">
  <span class="eyebrow">Higher Study Info · কার্যকর: {updated}</span>
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
  <h2>পরিবর্তন</h2>
  <p>এই নীতিতে পরিবর্তন হলে এই পেজে তারিখসহ আপডেট করা হবে।</p>
</article>
{FOOTER}
</div>"""
