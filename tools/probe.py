"""What a Danish webshop tells you about itself before you ever contact it.

Fetches the front page (and /handelsbetingelser-ish pages), and reports the
platform, the tracking stack, the consent layer and the commercial terms that
feed straight into the offer.
"""
import gzip, re, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

UA = {"User-Agent": "Mozilla/5.0 (compatible; margin-research/1.0; +mailto:7derpy@gmail.com)",
      "Accept-Encoding": "gzip"}

PLATFORM = [
    ("Shopify",     r"cdn\.shopify\.com|Shopify\.theme|shopify-features"),
    ("WooCommerce", r"woocommerce|wp-content/plugins/woocommerce"),
    ("Magento",     r"mage/|Magento_|static/version\d+"),
    ("DanDomain",   r"dandomain|shop\d+\.dandomain"),
    ("Smartweb",    r"smartweb|hostedshop"),
    ("Shoporama",   r"shoporama"),
    ("Salesforce",  r"demandware|salesforce commerce"),
    ("Centra",      r"centra\.com|centraapi"),
]
TRACKING = [
    ("GA4",            r"gtag/js\?id=G-|google-analytics\.com/g/collect"),
    ("GTM web",        r"googletagmanager\.com/gtm\.js|GTM-[A-Z0-9]{5,}"),
    ("Meta pixel",     r"connect\.facebook\.net/[a-z_]+/fbevents\.js|fbq\("),
    ("Google Ads",     r"googleadservices|/pagead/conversion|AW-\d{9,}"),
    ("Klaviyo",        r"klaviyo\.com|static\.klaviyo"),
    ("TikTok",         r"analytics\.tiktok\.com"),
    ("Pinterest",      r"pintrk\("),
    ("Hotjar/Clarity", r"hotjar\.com|clarity\.ms"),
    ("Trustpilot",     r"trustpilot\.com/bootstrap|widget\.trustpilot"),
]
CONSENT = [
    ("Cookiebot",           r"consent\.cookiebot\.com|Cookiebot"),
    ("Cookie Information",  r"policy\.app\.cookieinformation\.com|cookieinformation"),
    ("CookieYes",           r"cookieyes"),
    ("Usercentrics",        r"usercentrics"),
    ("Consent Mode v2",     r"ad_user_data|ad_personalization"),
]
TERMS = [
    ("free shipping DKK",  r"[Ff]ri(?:t)? fragt[^.<]{0,40}?(\d{2,4})\s*(?:,-|kr)"),
    ("return window days", r"(\d{1,3})\s*dages?\s*(?:retur|fortrydelse|returret)"),
]


def get(url, timeout=20):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read()
        final = r.geturl()
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    return raw.decode("utf-8", "replace"), final


def sgtm(html, host):
    """Server-side GTM shows up as a first-party collect endpoint."""
    hits = re.findall(r'https?://([a-z0-9.-]*\.?%s)/[a-z]{1,12}(?:/|\?)' %
                      re.escape(host.split(".", 1)[-1]), html)
    for h in set(hits):
        if re.search(r"\b(gtm|sgtm|tag|track|ss|server|analytics|data|metrics)\b", h):
            return h
    if re.search(r"googletagmanager\.com/gtag/js.*?&?transport_url|transport_url", html):
        return "transport_url set"
    return None


def probe(domain):
    host = domain.replace("https://", "").replace("http://", "").strip("/")
    out = {"domain": host}
    try:
        html, final = get("https://" + host)
    except Exception as e:
        return {**out, "error": type(e).__name__}
    blob = html
    # terms usually live on a separate page
    for path in ("handelsbetingelser", "levering", "returret", "kundeservice"):
        try:
            more, _ = get(f"https://{host}/{path}", timeout=12)
            blob += more
        except Exception:
            pass

    def found(table, text):
        return [n for n, pat in table if re.search(pat, text, re.I)]

    out["platform"] = ", ".join(found(PLATFORM, html)) or "?"
    out["tracking"] = found(TRACKING, html)
    out["consent"] = found(CONSENT, html)
    out["sgtm"] = sgtm(html, host) or "-"
    for label, pat in TERMS:
        m = re.search(pat, blob)
        out[label] = m.group(1) if m else "-"
    out["bytes"] = len(blob)
    return out


doms = sys.argv[1:] or ["coolshop.dk", "proshop.dk", "cykelpartner.dk",
                        "nicehair.dk", "lampeguru.dk", "med24.dk"]
with ThreadPoolExecutor(max_workers=6) as ex:
    for r in ex.map(probe, doms):
        if "error" in r:
            print(f"{r['domain']:20s} ERROR {r['error']}")
            continue
        print(f"\n=== {r['domain']} ===  platform={r['platform']}")
        print(f"   tracking : {', '.join(r['tracking']) or '-'}")
        print(f"   consent  : {', '.join(r['consent']) or '-'}")
        print(f"   sGTM     : {r['sgtm']}")
        print(f"   fri fragt: {r['free shipping DKK']} kr    returret: {r['return window days']} dage")
