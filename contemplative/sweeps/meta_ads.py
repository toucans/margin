#!/usr/bin/env python3
"""Meta Ad Library (Graph API ads_archive) — CLI and MCP stdio server.

One file, stdlib only, no dependencies: the vendor API plus code we own.
Token is read from ~/.config/margin/meta.env (never from the repo).

  CLI:  meta_ads.py search "grey area drinking" --countries DK,GB --limit 50
  MCP:  meta_ads.py mcp          (registered as the `meta` server)
"""
import json, os, sys, urllib.parse, urllib.request, urllib.error, pathlib

GRAPH = "https://graph.facebook.com/v21.0/ads_archive"
ENV = pathlib.Path.home() / ".config" / "margin" / "meta.env"

FIELDS = [
    "id", "page_id", "page_name", "ad_delivery_start_time", "ad_delivery_stop_time",
    "ad_creative_bodies", "ad_creative_link_titles", "ad_creative_link_captions",
    "ad_creative_link_descriptions", "ad_snapshot_url", "publisher_platforms",
    "eu_total_reach", "target_ages", "target_gender", "target_locations", "languages",
]


def token():
    t = os.environ.get("META_ADS_TOKEN")
    if t:
        return t
    if ENV.exists():
        for line in ENV.read_text().splitlines():
            line = line.strip()
            if line.startswith("META_ADS_TOKEN="):
                return line.split("=", 1)[1].strip()
    raise SystemExit(f"no META_ADS_TOKEN in env or {ENV}")


def search(search_terms, countries=("DK",), search_type="KEYWORD_EXACT_PHRASE",
           ad_type="ALL", limit=50, fields=None, date_min=None, max_pages=20):
    """Page through ads_archive. Returns a list of ad dicts."""
    params = {
        "search_terms": search_terms,
        "ad_reached_countries": json.dumps(list(countries)),
        "ad_type": ad_type,
        "search_type": search_type,
        "fields": ",".join(fields or FIELDS),
        "limit": str(min(limit, 100)),
        "access_token": token(),
    }
    if date_min:
        params["ad_delivery_date_min"] = date_min
    url = GRAPH + "?" + urllib.parse.urlencode(params)
    out = []
    for _ in range(max_pages):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                body = json.load(r)
        except urllib.error.HTTPError as e:
            detail = json.load(e).get("error", {}).get("message", str(e))
            raise SystemExit(f"graph error: {detail}")
        out.extend(body.get("data", []))
        nxt = body.get("paging", {}).get("next")
        if not nxt or len(out) >= limit:
            break
        url = nxt
    return out[:limit]


def exchange(short_token=None):
    """Trade a short-lived user token for a ~60-day one.

    Refuses to write an empty or error response over a working token — the
    failure mode that cost us the original once.
    """
    import urllib.parse
    cfg = {}
    for line in ENV.read_text().splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.split("=", 1); cfg[k.strip()] = v.strip()
    app_id, secret = cfg.get("META_APP_ID"), cfg.get("META_APP_SECRET")
    if not (app_id and secret):
        raise SystemExit("META_APP_ID and META_APP_SECRET must be in " + str(ENV))
    q = urllib.parse.urlencode({
        "grant_type": "fb_exchange_token", "client_id": app_id,
        "client_secret": secret, "fb_exchange_token": short_token or token()})
    try:
        with urllib.request.urlopen(
                "https://graph.facebook.com/v21.0/oauth/access_token?" + q, timeout=30) as r:
            body = json.load(r)
    except urllib.error.HTTPError as e:
        raise SystemExit("exchange refused: " +
                         json.load(e).get("error", {}).get("message", str(e)))
    new = body.get("access_token")
    if not new or len(new) < 50:
        raise SystemExit("refusing to write a short/empty token; env left untouched")
    cfg["META_ADS_TOKEN"] = new
    ENV.write_text("# Meta Graph API token for the Ad Library (ads_archive).\n"
                   "# Kept outside the repo on purpose: never commit this.\n"
                   + "".join(f"{k}={v}\n" for k, v in cfg.items()))
    ENV.chmod(0o600)
    print(f"token replaced; expires_in={body.get('expires_in')}")


def status():
    import time
    t = token()
    q = urllib.parse.urlencode({"input_token": t, "access_token": t})
    with urllib.request.urlopen(
            "https://graph.facebook.com/v21.0/debug_token?" + q, timeout=30) as r:
        d = json.load(r)["data"]
    exp = d.get("expires_at")
    print(f"valid={d.get('is_valid')} scopes={d.get('scopes')} "
          f"hours_left={round((exp - time.time()) / 3600, 1) if exp else 'never'}")


# ---------------------------------------------------------------- MCP server

TOOLS = [{
    "name": "ads_archive_search",
    "description": (
        "Search the Meta Ad Library (Graph API ads_archive) for ads by keyword. "
        "Returns creative text, run dates, platforms, targeting (age/gender/location) "
        "and EU reach. ad_type=ALL covers commercial ads. Use "
        "KEYWORD_EXACT_PHRASE for framing matches — KEYWORD_UNORDERED matches loosely "
        "and returns unrelated ads."),
    "inputSchema": {
        "type": "object",
        "properties": {
            "search_terms": {"type": "string", "description": "Keyword or phrase."},
            "countries": {"type": "array", "items": {"type": "string"},
                          "description": "ISO-2 codes, e.g. ['DK','GB']. UK is GB."},
            "search_type": {"type": "string",
                            "enum": ["KEYWORD_EXACT_PHRASE", "KEYWORD_UNORDERED"]},
            "ad_type": {"type": "string",
                        "enum": ["ALL", "POLITICAL_AND_ISSUE_ADS"]},
            "limit": {"type": "integer", "description": "Max ads (paged). Default 50."},
            "date_min": {"type": "string",
                         "description": "Only ads delivered on/after YYYY-MM-DD."},
        },
        "required": ["search_terms"],
    },
}]


def rpc(msg):
    m, mid = msg.get("method"), msg.get("id")
    if m == "initialize":
        return {"protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "meta-ads", "version": "1.0.0"}}
    if m == "tools/list":
        return {"tools": TOOLS}
    if m == "tools/call":
        a = msg.get("params", {}).get("arguments", {}) or {}
        rows = search(a["search_terms"],
                      countries=a.get("countries", ["DK"]),
                      search_type=a.get("search_type", "KEYWORD_EXACT_PHRASE"),
                      ad_type=a.get("ad_type", "ALL"),
                      limit=int(a.get("limit", 50)),
                      date_min=a.get("date_min"))
        return {"content": [{"type": "text",
                             "text": json.dumps(rows, ensure_ascii=False, indent=1)}]}
    raise ValueError(f"unknown method {m}")


def serve():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        if "id" not in msg:          # notification: no reply
            continue
        try:
            res = {"jsonrpc": "2.0", "id": msg["id"], "result": rpc(msg)}
        except Exception as e:       # noqa: BLE001 - report upstream, keep serving
            res = {"jsonrpc": "2.0", "id": msg["id"],
                   "error": {"code": -32000, "message": str(e)}}
        sys.stdout.write(json.dumps(res, ensure_ascii=False) + "\n")
        sys.stdout.flush()


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "mcp":
        return serve()
    if len(sys.argv) > 1 and sys.argv[1] == "exchange":
        return exchange(sys.argv[2] if len(sys.argv) > 2 else None)
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        return status()
    if len(sys.argv) > 2 and sys.argv[1] == "search":
        args = sys.argv[3:]
        def opt(name, default=None):
            return args[args.index(name) + 1] if name in args else default
        rows = search(sys.argv[2],
                      countries=opt("--countries", "DK").split(","),
                      search_type=opt("--search-type", "KEYWORD_EXACT_PHRASE"),
                      limit=int(opt("--limit", "50")),
                      date_min=opt("--date-min"))
        json.dump(rows, sys.stdout, ensure_ascii=False, indent=1)
        return
    raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
