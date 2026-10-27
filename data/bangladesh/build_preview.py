"""Build the scholarship preview page from scholarships.csv.

Usage: python3 build_preview.py <output.html> [YYYY-MM-DD]
"""
import csv
import datetime
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
ORDER = {"government": 0, "public": 1, "private": 2, "international": 3}

rows = list(csv.DictReader(open(HERE / "scholarships.csv", encoding="utf-8")))
rows.sort(key=lambda r: ORDER[r["provider_type"]])
updated = sys.argv[2] if len(sys.argv) > 2 else datetime.date.today().isoformat()
html = (HERE / "preview_template.html").read_text(encoding="utf-8")
html = html.replace("__DATA__", json.dumps(rows, ensure_ascii=False).replace("</", "<\\/"))
html = html.replace("__UPDATED__", updated)
pathlib.Path(sys.argv[1]).write_text(html, encoding="utf-8")
print(f"{len(rows)} records -> {sys.argv[1]}")
