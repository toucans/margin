#!/usr/bin/env python3
import json, html
D = json.load(open("report_data.json"))
MAX = 280

def esc(s): return html.escape(s or "")

blocks = []
for c in D:
    rows = []
    for it in c["items"]:
        w = min(100, it["days"] / MAX * 100)
        live = "live" if it["days"] >= 90 else ""
        rows.append(f'''<li class="rec">
  <div class="rec-h"><span class="adv">{esc(it["adv"])}</span>
    <span class="meta"><span class="ctry">{esc(it["countries"])}</span>
    {'<span class="var">'+str(it["variants"])+' variants</span>' if it["variants"]>1 else ''}
    <span class="lp">{esc(it["lp"]).replace("_"," ")}</span></span></div>
  <div class="bar"><span class="fill {live}" style="width:{w:.1f}%"></span><b class="d">{it["days"]}d</b></div>
  <blockquote class="hook">{esc(it["hook"])}</blockquote>
</li>''')
    blocks.append(f'''<section class="cluster" id="{c["id"]}">
  <header class="ch"><span class="cid">{c["id"]}</span>
    <h2>{esc(c["label"])}</h2>
    <span class="count">{c["advertisers"]} advertisers past triage · {len(c["items"])} on framing</span></header>
  <ol class="recs">{"".join(rows)}</ol>
</section>''')

COVER = [("DK",8854,18188),("DE",8535,16464),("NL",8251,16124),
         ("GB",11621,18889),("US",10208,18316),("AU",9937,18121)]
cov = "".join(f'<div class="cc"><b>{k}</b><span>{a:,}</span><i>{b:,}</i></div>' for k,a,b in COVER)

HTML = f'''<title>Who Pays to Name the Problem</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=Public+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap">
<style>
:root{{--paper:#F6F7F5;--card:#FFFFFF;--ink:#131C19;--ink2:#3E4A45;--muted:#6C7A74;
 --rule:#DCE3DF;--pine:#1D6B4C;--pine-soft:#CFE3D8;--clay:#9C5230;--clay-soft:#F0DFD5;}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--paper:#0D1412;--card:#141D1A;
 --ink:#E7EDE9;--ink2:#B4C1BB;--muted:#84978E;--rule:#26332E;--pine:#5FC594;--pine-soft:#1E3A2E;--clay:#D08A5F;--clay-soft:#3A2820;}}}}
:root[data-theme="dark"]{{--paper:#0D1412;--card:#141D1A;--ink:#E7EDE9;--ink2:#B4C1BB;
 --muted:#84978E;--rule:#26332E;--pine:#5FC594;--pine-soft:#1E3A2E;--clay:#D08A5F;--clay-soft:#3A2820;}}
*{{box-sizing:border-box}}
body{{background:var(--paper);color:var(--ink);font:400 16px/1.6 "Public Sans",system-ui,sans-serif;margin:0}}
.wrap{{max-width:920px;margin:0 auto;padding:56px 24px 96px;display:flex;flex-direction:column;gap:44px}}
.eyebrow{{font:500 11px/1 "JetBrains Mono",ui-monospace,monospace;letter-spacing:.14em;
 text-transform:uppercase;color:var(--muted)}}
h1{{font:600 clamp(34px,5.5vw,52px)/1.05 "Fraunces",Georgia,serif;margin:14px 0 0;
 letter-spacing:-.02em;text-wrap:balance}}
.sub{{color:var(--ink2);font-size:18px;max-width:62ch;margin:16px 0 0}}
h2{{font:600 22px/1.25 "Fraunces",Georgia,serif;margin:0;letter-spacing:-.01em}}
h3{{font:600 15px/1.3 "Public Sans",sans-serif;margin:0 0 10px;letter-spacing:-.005em}}
.verdict{{background:var(--card);border:1px solid var(--rule);border-left:3px solid var(--pine);
 padding:22px 26px;display:flex;flex-direction:column;gap:8px}}
.verdict p{{margin:0;color:var(--ink2)}} .verdict strong{{color:var(--ink)}}
.covgrid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(108px,1fr));gap:1px;
 background:var(--rule);border:1px solid var(--rule)}}
.cc{{background:var(--card);padding:14px 16px;display:flex;flex-direction:column;gap:3px}}
.cc b{{font:500 13px/1 "JetBrains Mono",monospace;letter-spacing:.08em;color:var(--muted)}}
.cc span{{font:500 20px/1 "Public Sans",sans-serif;font-variant-numeric:tabular-nums;color:var(--pine)}}
.cc i{{font:400 12px/1 "JetBrains Mono",monospace;font-style:normal;color:var(--muted);
 font-variant-numeric:tabular-nums}}
.legend{{display:flex;gap:20px;flex-wrap:wrap;font-size:13px;color:var(--muted);align-items:center}}
.key{{display:inline-flex;align-items:center;gap:7px}}
.sw{{width:22px;height:8px;background:var(--pine-soft);display:inline-block}}
.sw.on{{background:var(--pine)}}
.cluster{{display:flex;flex-direction:column;gap:16px}}
.ch{{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;
 border-bottom:1px solid var(--rule);padding-bottom:10px}}
.cid{{font:500 12px/1 "JetBrains Mono",monospace;color:var(--paper);background:var(--ink);
 padding:5px 7px;letter-spacing:.06em}}
.count{{margin-left:auto;font:400 12px/1 "JetBrains Mono",monospace;color:var(--muted)}}
.recs{{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:20px}}
.rec-h{{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;margin-bottom:7px}}
.adv{{font-weight:600;font-size:15px}}
.meta{{margin-left:auto;display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}}
.ctry,.var,.lp{{font:400 11px/1 "JetBrains Mono",monospace;color:var(--muted);letter-spacing:.04em}}
.var{{color:var(--clay)}}
.bar{{position:relative;height:10px;background:var(--rule);display:flex;align-items:center}}
.fill{{display:block;height:100%;background:var(--pine-soft)}}
.fill.live{{background:var(--pine)}}
.bar .d{{position:absolute;right:0;top:-19px;font:500 11px/1 "JetBrains Mono",monospace;
 color:var(--muted);font-variant-numeric:tabular-nums}}
.bar::after{{content:"";position:absolute;left:32.1%;top:-3px;bottom:-3px;width:1px;background:var(--ink);opacity:.35}}
.hook{{margin:11px 0 0;padding-left:14px;border-left:2px solid var(--rule);
 font:400 13.5px/1.55 "JetBrains Mono",ui-monospace,monospace;color:var(--ink2);
 max-width:78ch;overflow-wrap:anywhere}}
.finding{{background:var(--card);border:1px solid var(--rule);padding:20px 24px}}
.finding p{{margin:0;color:var(--ink2);max-width:66ch}}
.findings{{display:flex;flex-direction:column;gap:14px}}
.caveat{{border-left:3px solid var(--clay);background:var(--clay-soft)}}
.caveat h3{{color:var(--clay)}}
.caveat p{{color:var(--ink2)}}
footer{{border-top:1px solid var(--rule);padding-top:18px;font:400 12.5px/1.6 "JetBrains Mono",monospace;color:var(--muted)}}
a{{color:var(--pine)}}
@media(max-width:560px){{.meta{{margin-left:0;width:100%}}.count{{margin-left:0}}}}
</style>
<div class="wrap">
<header>
  <div class="eyebrow">Meta Ad Library sweep · 29 Aug 2026</div>
  <h1>Who pays to name the problem</h1>
  <p class="sub">291 keyword queries across eight framings and six countries, active and
  inactive. 163,508 ads returned. What survives is the copy someone has paid to keep
  running — the only public evidence that separates a live market from a loud one.</p>
</header>

<div class="verdict">
  <div class="eyebrow">§0.1 — resolved</div>
  <p><strong>API, not the web UI — and the API was not the constraint.</strong>
  The brief expected commercial ads to be keyword-searchable only inside the EU, leaving
  DK/DE/NL to carry the study. That proved wrong: <strong>ad_type=ALL returned commercial
  ads in all six countries</strong>, with targeting everywhere and EU reach on EU rows.
  Text is returned verbatim. Every hook below is quoted exactly as it ran.</p>
  <p>Google is out of scope as the brief predicted — its Transparency Center is
  advertiser-keyed, and no advertiser list was assumed here.</p>
</div>

<section>
  <h3>Coverage — ads returned per country</h3>
  <div class="covgrid">{cov}</div>
  <p class="eyebrow" style="margin-top:10px">green = active pass · grey = inactive pass · no country returned nothing</p>
</section>

<section>
  <h3>The ledger</h3>
  <p style="color:var(--ink2);margin:0 0 14px;max-width:66ch">Bars are the longest single
  creative run, after dropping everything under 45 days and everything whose hook only
  contained the keyword. The line at 90 days is the brief's own threshold: an ad running
  three months is being paid for because it works.</p>
  <div class="legend">
    <span class="key"><i class="sw on"></i> 90 days or more — profitable</span>
    <span class="key"><i class="sw"></i> 45–89 days — surviving, unproven</span>
  </div>
</section>

{"".join(blocks)}

<section class="findings">
  <h3>What the sweep says</h3>
  <div class="finding"><p><strong>C2 is the live market, not C1.</strong> “Can’t switch
  off” is the deepest cluster by a distance — 41 advertisers past triage, with runs of 191,
  160, 159 and 151 days. The 2 a.m. decision has almost nobody selling against it. The
  framing you lead with is the one nobody has priced; the money is next door.</p></div>
  <div class="finding"><p><strong>The control held.</strong> Sarah Rusbatch ran one
  creative 123 days in Britain and Australia at once, into a gated application. C5 was
  the brief’s built-in check — it returned a working lane, so a thin cluster elsewhere is
  a real reading rather than a coverage artifact.</p></div>
  <div class="finding"><p><strong>A worked lane gets industrialised.</strong> Four
  separate pages — Mindful Drinking Community, Dr. Alex Morgan, Alcohol Free Daily and
  Ask Dr. Whitmore — run the same hook into the same destination, calmio.ai, across five
  countries for 60–68 days. One operator wearing four faces.</p></div>
  <div class="finding"><p><strong>C3 is empty, and the emptiness is real.</strong> One
  advertiser survived across all six countries. Compulsive checking is a symptom people
  recognise and will not buy a cure for on its own.</p></div>
  <div class="finding"><p><strong>Nobody sells the mechanism.</strong> Rusbatch sells
  drinking by promising <em>switching off</em>; Rewired Woman sells burnout to
  <em>executive women</em>, seven variants over five countries. The buyer is reached
  through the habit or the role — never through the mechanism.</p></div>
  <div class="finding caveat"><h3>Read the price column as unread</h3><p>The API exposes
  only the display domain, so the landing-page pass reads each domain’s root rather than
  the creative’s true destination, and the price regex mistakes stray “$1” strings for
  prices. Variant counts are copy-hash groupings, not Meta’s own collation_count.
  Recovering real destination URLs needs a pass through the UI scraper.</p></div>
</section>

<footer>291 queries · 0 query errors · 163,508 ads · 1,823 past triage · 548 on framing ·
122 advertisers<br>Raw CSV and the sweep scripts live in <code>contemplative/sweeps/</code>.</footer>
</div>'''
open("report.html","w").write(HTML)
print("wrote report.html", len(HTML), "bytes")
