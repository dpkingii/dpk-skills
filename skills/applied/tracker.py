#!/usr/bin/env python3
"""Read and append rows in the Job Applications sheet through its Apps Script web app.

  tracker.py peek URL          print the title metadata of a job page
  tracker.py find TERM...      print rows matching a company name or link
  tracker.py append            append rows from a JSON array on stdin
"""
import difflib
import html
import json
import re
import subprocess
import sys
from pathlib import Path

CONFIG = Path.home() / ".config" / "job-tracker" / "config.json"


def call(action, **fields):
    config = json.loads(CONFIG.read_text())
    payload = json.dumps({"secret": config["secret"], "action": action, **fields})
    # -L turns the POST into the GET that Apps Script's redirect expects, so -X POST must stay out.
    result = subprocess.run(
        ["curl", "-sSL", "--max-time", "60", "-H", "Content-Type: text/plain",
         "--data-binary", "@-", config["url"]],
        input=payload, capture_output=True, text=True,
    )
    try:
        body = json.loads(result.stdout)
    except json.JSONDecodeError:
        sys.exit(f"Unexpected response: {result.stderr or result.stdout[:300]}")
    if not body.get("ok"):
        sys.exit(f"Tracker error: {body.get('error')}")
    return body


def to_script_rows(rows):
    # The deployed script still appends [company, role, status, date, link], so
    # date and link are sent in the status and date slots to fill the 4-column sheet.
    return [{"company": r["company"], "role": r["role"], "status": r["date"], "date": r.get("link", "")} for r in rows]


def normalize(text):
    return re.sub(r"[^a-z0-9]", "", text.lower())


def bare_link(link):
    path, _, query = link.partition("?")
    # Some boards (Greenhouse embeds) identify the job only in the query, so strip tracking params instead of the whole query.
    kept = [q for q in query.split("&") if q and not q.startswith(("jr_id=", "utm_"))]
    return (path.rstrip("/") + ("?" + "&".join(kept) if kept else "")).lower()


def matches(term, company, link):
    if term.startswith("http"):
        return bool(link) and bare_link(term) == bare_link(link)
    term, company = normalize(term), normalize(company)
    return term in company or difflib.SequenceMatcher(None, term, company).ratio() >= 0.8


def find(terms):
    rows = call("list")["rows"]
    for number, row in enumerate(rows, start=1):
        company, role, date, link = (row + [""] * 4)[:4]
        if number > 1 and company and any(matches(t, company, link) for t in terms):
            print(f"row {number} | {company} | {role} | {date} | {link}")


def peek(url):
    result = subprocess.run(
        ["curl", "-sSL", "--max-time", "20", "-A", "Mozilla/5.0",
         "-w", "\n%{url_effective}", url],
        capture_output=True, text=True, errors="replace",
    )
    page, _, final_url = result.stdout.rpartition("\n")

    def first(pattern):
        match = re.search(pattern, page, re.IGNORECASE | re.DOTALL)
        return " ".join(html.unescape(match.group(1)).split())[:300] if match else ""

    print(json.dumps({
        "final_url": final_url,
        "title": first(r"<title[^>]*>(.*?)</title>"),
        "og_title": first(r"<meta[^>]+property=[\"']og:title[\"'][^>]+content=[\"'](.*?)[\"']"),
        "og_site_name": first(r"<meta[^>]+property=[\"']og:site_name[\"'][^>]+content=[\"'](.*?)[\"']"),
    }, indent=2))


def main():
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command == "peek" and len(sys.argv) == 3:
        peek(sys.argv[2])
    elif command == "find" and len(sys.argv) > 2:
        find(sys.argv[2:])
    elif command == "append":
        print(json.dumps(call("append", rows=to_script_rows(json.load(sys.stdin)))))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
