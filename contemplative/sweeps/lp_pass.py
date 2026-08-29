#!/usr/bin/env python3
"""§4 second pass: fetch each unique destination and read H1, page type, price.

Verbatim only — the H1 is recorded as written, never summarised.
"""
import json, sys, re, html, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"}
PRICE = re.compile(r"(?:US)?[$£€]\s?\d[\d,.]*(?:\s?(?:per|/)\s?(?:mo|month))?|"
                   r"\b\d[\d.,]*\s?(?:kr|DKK|EUR|USD|GBP)\b", re.I)

def classify(t):
    """Order matters: the strongest commercial signal wins. Nav-bar and footer
    links say 'book a call' on nearly every coaching site, so an application
    verdict needs the phrase repeatedly or in a form."""
    tl = t.lower()
    def n(p):
        return len(re.findall(p, tl))
    if n(r"(add to cart|proceed to checkout|complete (your )?purchase|"
          r"stripe\.com|checkout\.|buy now)") >= 1:
        return "direct_checkout"
    if n(r"(wistia|vimeo\.com/video|youtube\.com/embed|<video)") >= 1 and \
       n(r"(watch|video|training|masterclass)") >= 2:
        return "vsl"
    if n(r"(<form|typeform|jotform|gravityform|application)") >= 1 and \
       n(r"(apply now|application|qualify|book a call|discovery call|"
         r"strategy (call|session))") >= 2:
        return "application_form"
    if n(r"(circle\.so|skool\.com|mighty ?networks|discord\.gg|"
          r"join the community|private group)") >= 1:
        return "community"
    if n(r"(enter your email|free (guide|ebook|pdf|download|training|"
          r"masterclass|workshop)|waitlist|subscribe|newsletter)") >= 1:
        return "optin"
    if n(r"(apply now|book a call|discovery call)") >= 1:
        return "application_form"
    return "unknown"

def h1_of(t):
    m = re.search(r"<h1[^>]*>(.*?)</h1>", t, re.S | re.I)
    if not m:
        m = re.search(r"<title[^>]*>(.*?)</title>", t, re.S | re.I)
    if not m:
        return None
    return html.unescape(re.sub(r"<[^>]+>", " ", m.group(1))).strip()[:220] or None

def one(url):
    u = url if url.startswith("http") else "https://" + url
    try:
        req = urllib.request.Request(u, headers=UA)
        with urllib.request.urlopen(req, timeout=25) as r:
            final = r.geturl()
            t = r.read(600_000).decode("utf8", "replace")
    except Exception as e:  # noqa: BLE001
        return {"destination_url": url, "error": str(e)[:70],
                "lp_h1": None, "lp_page_type": None, "price_visible": None}
    prices = PRICE.findall(t)
    return {"destination_url": url, "final_url": final, "lp_h1": h1_of(t),
            "lp_page_type": classify(t),
            "price_visible": prices[0].strip() if prices else "gated"}

if __name__ == "__main__":
    urls = [u.strip() for u in open(sys.argv[1]) if u.strip()]
    with ThreadPoolExecutor(max_workers=10) as ex:
        out = list(ex.map(one, urls))
    json.dump(out, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
    ok = sum(1 for o in out if o.get("lp_h1"))
    print(f"{len(out)} urls, {ok} with an H1 -> {sys.argv[2]}")
