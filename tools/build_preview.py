"""Build a country's scholarship preview page from data/<slug>/scholarships.csv.

Usage: python3 tools/build_preview.py <slug> <output.html> [YYYY-MM-DD]
"""
import csv
import datetime
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ORDER = {"government": 0, "eu": 1, "consortium": 2, "public": 3, "private": 4, "international": 5}
# slug -> (English name, page title, heading)
COUNTRIES = {
    "bangladesh": ("Bangladesh", "বাংলাদেশ স্কলারশিপ তালিকা", "বাংলাদেশের স্কলারশিপ ও টিউশন ওয়েভার"),
    "italy": ("Italy", "ইতালি স্কলারশিপ তালিকা", "ইতালির স্কলারশিপ"),
    "erasmus-mundus": ("European Union", "Erasmus Mundus স্কলারশিপ", "Erasmus Mundus Joint Masters স্কলারশিপ"),
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
