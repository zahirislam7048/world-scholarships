"""Build a country's scholarship preview page from data/<continent>/<country>/scholarships.csv.

Usage: python3 tools/build_preview.py <continent>/<country> <output.html> [YYYY-MM-DD]
"""
import csv
import datetime
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ORDER = {"government": 0, "eu": 1, "consortium": 2, "public": 3, "private": 4, "international": 5}
# "<continent>/<country>" -> (English name, page title, heading). Order is display order.
CONTINENTS = {"asia": ("Asia", "এশিয়া", "এশিয়ার"), "europe": ("Europe", "ইউরোপ", "ইউরোপের")}
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
    "asia/saudi-arabia": ("Saudi Arabia", "সৌদি আরব স্কলারশিপ তালিকা", "সৌদি আরবের স্কলারশিপ"),
    "asia/uae": ("United Arab Emirates", "সংযুক্ত আরব আমিরাত স্কলারশিপ তালিকা", "সংযুক্ত আরব আমিরাতের স্কলারশিপ"),
    "asia/qatar": ("Qatar", "কাতার স্কলারশিপ তালিকা", "কাতারের স্কলারশিপ"),
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
    "europe/erasmus-mundus": ("European Union", "Erasmus Mundus স্কলারশিপ", "Erasmus Mundus Joint Masters স্কলারশিপ"),
}


def load_rows(slug):
    rows = list(csv.DictReader(open(ROOT / "data" / slug / "scholarships.csv", encoding="utf-8")))
    rows.sort(key=lambda r: (ORDER.get(r["provider_type"], 9), r.get("deadline") or "9999"))
    return rows


def render(slug, updated):
    name_en, title, heading = COUNTRIES[slug]
    html = (ROOT / "tools" / "preview_template.html").read_text(encoding="utf-8")
    for key, val in {"__TITLE__": title, "__COUNTRY_EN__": name_en, "__HEADING__": heading,
                     "__SLUG__": slug, "__UPDATED__": updated}.items():
        html = html.replace(key, val)
    return html.replace("__DATA__", json.dumps(load_rows(slug), ensure_ascii=False).replace("</", "<\\/"))


if __name__ == "__main__":
    slug, out = sys.argv[1], sys.argv[2]
    updated = sys.argv[3] if len(sys.argv) > 3 else datetime.date.today().isoformat()
    pathlib.Path(out).write_text(render(slug, updated), encoding="utf-8")
    print(f"{slug}: {len(load_rows(slug))} records -> {out}")
