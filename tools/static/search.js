/* Site-wide search box: loads /data/search-index.json on first use and shows matches as you type. */
(function () {
  var box = document.querySelector(".gsearch input"), list = document.querySelector(".gsearch ul");
  if (!box || !list) return;
  var idx = null, sel = -1, items = [];
  var en = document.documentElement.lang === "en";
  var KIND = en ? { s: "Scholarship", c: "Country", g: "Guide", t: "Tool", h: "List", p: "Professor", o: "Opportunity" }
                : { s: "স্কলারশিপ", c: "দেশ", g: "গাইড", t: "টুল", h: "তালিকা", p: "প্রফেসর", o: "সুযোগ" };
  function load(cb) {
    if (idx) return cb();
    fetch(en ? "/data/search-index-en.json" : "/data/search-index.json").then(function (r) { return r.json(); }).then(function (d) { idx = d; cb(); }).catch(function () { idx = []; cb(); });
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function score(e, words) {
    var hay = (e.t + " " + (e.k || "")).toLowerCase(), t = e.t.toLowerCase(), sc = 0;
    for (var i = 0; i < words.length; i++) {
      var p = hay.indexOf(words[i]); if (p < 0) return -1;
      sc += t.indexOf(words[i]) === 0 ? 6 : t.indexOf(words[i]) >= 0 ? 4 : 1;
    }
    return sc + ({ c: 3, t: 2, h: 2, g: 2, s: 1, o: 1, p: 0 }[e.y] || 0);
  }
  function render() {
    var q = box.value.trim().toLowerCase();
    if (q.length < 2) { list.hidden = true; return; }
    var words = q.split(/\s+/);
    items = idx.map(function (e) { return [score(e, words), e]; }).filter(function (x) { return x[0] >= 0; })
               .sort(function (a, b) { return b[0] - a[0]; }).slice(0, 8).map(function (x) { return x[1]; });
    sel = -1;
    var all = '<li class="all"><a href="/search/?q=' + encodeURIComponent(box.value.trim()) + '">' + (en ? "Search all scholarships for “" : "সব স্কলারশিপে খুঁজুন: “") + esc(box.value.trim()) + "” →</a></li>";
    list.innerHTML = (items.length ? items.map(function (e) {
      return '<li><a href="' + e.u + '"><span class="k">' + KIND[e.y] + "</span>" + esc(e.t) + (e.d ? '<small>' + esc(e.d) + "</small>" : "") + "</a></li>";
    }).join("") : '<li class="none">' + (en ? "No direct match" : "সরাসরি কিছু মেলেনি") + "</li>") + all;
    list.hidden = false;
  }
  box.addEventListener("focus", function () { load(function () {}); });
  box.addEventListener("input", function () { load(render); });
  box.addEventListener("keydown", function (ev) {
    var links = list.querySelectorAll("a");
    if (ev.key === "ArrowDown" || ev.key === "ArrowUp") {
      ev.preventDefault(); if (!links.length) return;
      sel = (sel + (ev.key === "ArrowDown" ? 1 : -1) + links.length) % links.length;
      links.forEach(function (a, i) { a.classList.toggle("on", i === sel); });
    } else if (ev.key === "Enter") {
      ev.preventDefault();
      var a = sel >= 0 ? links[sel] : (items.length ? links[0] : null);
      location.href = a ? a.getAttribute("href") : "/search/?q=" + encodeURIComponent(box.value.trim());
    } else if (ev.key === "Escape") { list.hidden = true; }
  });
  document.addEventListener("click", function (ev) { if (!ev.target.closest(".gsearch")) list.hidden = true; });
})();
