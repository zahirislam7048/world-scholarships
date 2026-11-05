"""Build a country's scholarship preview page from data/<continent>/<country>/scholarships.csv.

Usage: python3 tools/build_preview.py <continent>/<country> <output.html> [YYYY-MM-DD]
"""
import csv
import datetime
import json
import pathlib
import re
import sys
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
ORDER = {"government": 0, "eu": 1, "consortium": 2, "public": 3, "private": 4, "international": 5}
# "<continent>/<country>" -> (English name, page title, heading). Order is display order.
CONTINENTS = {
    "asia": ("Asia", "এশিয়া", "এশিয়ার"),
    "gcc": ("GCC · Gulf", "GCC (উপসাগরীয় দেশ)", "GCC দেশগুলোর"),
    "europe": ("Europe", "ইউরোপ", "ইউরোপের"),
    "north-america": ("North America", "উত্তর আমেরিকা", "উত্তর আমেরিকার"),
    "latin-america": ("Latin America", "লাতিন আমেরিকা", "লাতিন আমেরিকার"),
    "oceania": ("Oceania", "ওশেনিয়া", "ওশেনিয়ার"),
    "africa": ("Africa", "আফ্রিকা", "আফ্রিকার"),
}
COUNTRIES = {
    "asia/bangladesh": ("Bangladesh", "বাংলাদেশ স্কলারশিপ তালিকা", "বাংলাদেশের স্কলারশিপ ও টিউশন ওয়েভার"),
    "asia/india": ("India", "ভারত স্কলারশিপ তালিকা", "ভারতের স্কলারশিপ"),
    "asia/china": ("China", "চীন স্কলারশিপ তালিকা", "চীনের স্কলারশিপ"),
    "asia/japan": ("Japan", "জাপান স্কলারশিপ তালিকা", "জাপানের স্কলারশিপ"),
    "asia/south-korea": ("South Korea", "দক্ষিণ কোরিয়া স্কলারশিপ তালিকা", "দক্ষিণ কোরিয়ার স্কলারশিপ"),
    "asia/singapore": ("Singapore", "সিঙ্গাপুর স্কলারশিপ তালিকা", "সিঙ্গাপুরের স্কলারশিপ"),
    "asia/hong-kong": ("Hong Kong", "হংকং স্কলারশিপ তালিকা", "হংকংয়ের স্কলারশিপ"),
    "asia/taiwan": ("Taiwan", "তাইওয়ান স্কলারশিপ তালিকা", "তাইওয়ানের স্কলারশিপ"),
    "asia/thailand": ("Thailand", "থাইল্যান্ড স্কলারশিপ তালিকা", "থাইল্যান্ডের স্কলারশিপ"),
    "asia/pakistan": ("Pakistan", "পাকিস্তান স্কলারশিপ তালিকা", "পাকিস্তানের স্কলারশিপ"),
    "asia/israel": ("Israel", "ইসরায়েল স্কলারশিপ তালিকা", "ইসরায়েলের স্কলারশিপ"),
    "asia/nepal": ("Nepal", "নেপাল স্কলারশিপ তালিকা", "নেপালের স্কলারশিপ"),
    "asia/malaysia": ("Malaysia", "মালয়েশিয়া স্কলারশিপ তালিকা", "মালয়েশিয়ার স্কলারশিপ"),
    "asia/indonesia": ("Indonesia", "ইন্দোনেশিয়া স্কলারশিপ তালিকা", "ইন্দোনেশিয়ার স্কলারশিপ"),
    "asia/brunei": ("Brunei", "ব্রুনাই স্কলারশিপ তালিকা", "ব্রুনাইয়ের স্কলারশিপ"),
    "gcc/saudi-arabia": ("Saudi Arabia", "সৌদি আরব স্কলারশিপ তালিকা", "সৌদি আরবের স্কলারশিপ"),
    "gcc/uae": ("United Arab Emirates", "সংযুক্ত আরব আমিরাত স্কলারশিপ তালিকা", "সংযুক্ত আরব আমিরাতের স্কলারশিপ"),
    "gcc/qatar": ("Qatar", "কাতার স্কলারশিপ তালিকা", "কাতারের স্কলারশিপ"),
    "gcc/kuwait": ("Kuwait", "কুয়েত স্কলারশিপ তালিকা", "কুয়েতের স্কলারশিপ"),
    "gcc/oman": ("Oman", "ওমান স্কলারশিপ তালিকা", "ওমানের স্কলারশিপ"),
    "gcc/bahrain": ("Bahrain", "বাহরাইন স্কলারশিপ তালিকা", "বাহরাইনের স্কলারশিপ"),
    "europe/italy": ("Italy", "ইতালি স্কলারশিপ তালিকা", "ইতালির স্কলারশিপ"),
    "europe/germany": ("Germany", "জার্মানি স্কলারশিপ তালিকা", "জার্মানির স্কলারশিপ"),
    "europe/united-kingdom": ("United Kingdom", "যুক্তরাজ্য স্কলারশিপ তালিকা", "যুক্তরাজ্যের স্কলারশিপ"),
    "europe/france": ("France", "ফ্রান্স স্কলারশিপ তালিকা", "ফ্রান্সের স্কলারশিপ"),
    "europe/sweden": ("Sweden", "সুইডেন স্কলারশিপ তালিকা", "সুইডেনের স্কলারশিপ"),
    "europe/switzerland": ("Switzerland", "সুইজারল্যান্ড স্কলারশিপ তালিকা", "সুইজারল্যান্ডের স্কলারশিপ"),
    "europe/netherlands": ("Netherlands", "নেদারল্যান্ডস স্কলারশিপ তালিকা", "নেদারল্যান্ডসের স্কলারশিপ"),
    "europe/belgium": ("Belgium", "বেলজিয়াম স্কলারশিপ তালিকা", "বেলজিয়ামের স্কলারশিপ"),
    "europe/finland": ("Finland", "ফিনল্যান্ড স্কলারশিপ তালিকা", "ফিনল্যান্ডের স্কলারশিপ"),
    "europe/austria": ("Austria", "অস্ট্রিয়া স্কলারশিপ তালিকা", "অস্ট্রিয়ার স্কলারশিপ"),
    "europe/denmark": ("Denmark", "ডেনমার্ক স্কলারশিপ তালিকা", "ডেনমার্কের স্কলারশিপ"),
    "europe/norway": ("Norway", "নরওয়ে স্কলারশিপ তালিকা", "নরওয়ের স্কলারশিপ"),
    "europe/latvia": ("Latvia", "লাটভিয়া স্কলারশিপ তালিকা", "লাটভিয়ার স্কলারশিপ"),
    "europe/slovakia": ("Slovakia", "স্লোভাকিয়া স্কলারশিপ তালিকা", "স্লোভাকিয়ার স্কলারশিপ"),
    "europe/turkiye": ("Türkiye", "তুরস্ক স্কলারশিপ তালিকা", "তুরস্কের স্কলারশিপ"),
    "europe/hungary": ("Hungary", "হাঙ্গেরি স্কলারশিপ তালিকা", "হাঙ্গেরির স্কলারশিপ"),
    "europe/ireland": ("Ireland", "আয়ারল্যান্ড স্কলারশিপ তালিকা", "আয়ারল্যান্ডের স্কলারশিপ"),
    "europe/erasmus-mundus": ("European Union", "Erasmus Mundus স্কলারশিপ", "Erasmus Mundus Joint Masters স্কলারশিপ"),
    "north-america/usa": ("United States", "যুক্তরাষ্ট্র স্কলারশিপ তালিকা", "যুক্তরাষ্ট্রের স্কলারশিপ"),
    "north-america/canada": ("Canada", "কানাডা স্কলারশিপ তালিকা", "কানাডার স্কলারশিপ"),
    "latin-america/brazil": ("Brazil", "ব্রাজিল স্কলারশিপ তালিকা", "ব্রাজিলের স্কলারশিপ"),
    "latin-america/colombia": ("Colombia", "কলম্বিয়া স্কলারশিপ তালিকা", "কলম্বিয়ার স্কলারশিপ"),
    "oceania/australia": ("Australia", "অস্ট্রেলিয়া স্কলারশিপ তালিকা", "অস্ট্রেলিয়ার স্কলারশিপ"),
    "oceania/new-zealand": ("New Zealand", "নিউজিল্যান্ড স্কলারশিপ তালিকা", "নিউজিল্যান্ডের স্কলারশিপ"),
    "africa/mauritius": ("Mauritius", "মরিশাস স্কলারশিপ তালিকা", "মরিশাসের স্কলারশিপ"),
    "africa/nigeria": ("Nigeria", "নাইজেরিয়া স্কলারশিপ তালিকা", "নাইজেরিয়ার স্কলারশিপ"),
}


def is_watch(r):
    """A recurring programme whose next round is not announced yet: shown with a badge, not counted."""
    return r.get("session_year", "").startswith("Next round")


def load_rows(slug):
    rows = list(csv.DictReader(open(ROOT / "data" / slug / "scholarships.csv", encoding="utf-8")))
    rows.sort(key=lambda r: (is_watch(r), ORDER.get(r["provider_type"], 9), r.get("deadline") or "9999"))
    return rows


def page_slugs():
    """(country slug, row index) -> URL slug of that scholarship's own page, unique across the site."""
    out, seen = {}, set()
    for slug in COUNTRIES:
        for i, r in enumerate(load_rows(slug)):
            name = unicodedata.normalize("NFKD", r["scholarship_name"]).encode("ascii", "ignore").decode().lower()
            base = re.sub(r"[^a-z0-9]+", "-", f"{name} {slug.split('/')[1]}").strip("-")[:90].strip("-")
            s, n = base, 2
            while s in seen:
                s, n = f"{base}-{n}", n + 1
            seen.add(s)
            out[(slug, i)] = s
    return out


def render(slug, updated, pages=None):
    name_en, title, heading = COUNTRIES[slug]
    html = (ROOT / "tools" / "preview_template.html").read_text(encoding="utf-8")
    for key, val in {"__TITLE__": title, "__COUNTRY_EN__": name_en, "__HEADING__": heading,
                     "__SLUG__": slug, "__UPDATED__": updated}.items():
        html = html.replace(key, val)
    rows = load_rows(slug)
    if pages:
        rows = [{**r, "page": f"/scholarship/{pages[(slug, i)]}/"} if (slug, i) in pages else r for i, r in enumerate(rows)]
    return html.replace("__DATA__", json.dumps(rows, ensure_ascii=False).replace("</", "<\\/"))


if __name__ == "__main__":
    slug, out = sys.argv[1], sys.argv[2]
    updated = sys.argv[3] if len(sys.argv) > 3 else datetime.date.today().isoformat()
    pathlib.Path(out).write_text(render(slug, updated), encoding="utf-8")
    print(f"{slug}: {len(load_rows(slug))} records -> {out}")
