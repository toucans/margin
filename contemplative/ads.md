# Ad evidence

**An ad running three months is profitable.** Nobody subsidises a loser that
long, and no other public source separates who is making money from who is
merely posting. This is the check a problem framing passes before it is
believed.

Record per ad: the first line of the hook, the landing page headline, the price
where shown, delivery start and stop, and — where the EU exposes it — targeting
and reach. Targeting is advertisers naming the buyer with their own money,
which settles by observation what `vocabulary.md` can only count.

---

## Google — wired

The Ads Transparency Center is public and needs no login. There is no official
API for commercial ads; the only official feed is a BigQuery set limited to
political ones. Access is through Apify, added as an MCP server at user scope:

    claude mcp add --transport http --scope user apify https://mcp.apify.com

OAuth on first use — run `/mcp` and authenticate. `search-actors` finds the
Transparency Center scrapers, `call-actor` runs them. Runs consume Apify
credits.

## Meta — pending

**Waiting on ID review. Add the Ad Library API once it clears.**

Worth the wait. Outside the EU the API returns political and social-issue ads
only. DSA Article 39 forces every large platform to expose *all* ads served in
the EU — creative, advertiser, run dates, targeting parameters, aggregate reach
— kept a year past the last impression. That coverage is EU and UK only, so it
is available here and not to most people asking this question.

Graph API `ads_archive`. `ad_delivery_start_time` and `ad_delivery_stop_time`
carry the longevity. `ad_reached_countries` to DK plus the larger EU markets,
`ad_type` to all. Verify field names against the docs.

**Test first:** whether keyword search behaves the same for non-political EU
ads. If it doesn't, enumerate by advertiser page — the list of players falls out
of the Google pass anyway.

## Where it lands

Pull to plain JSON, index it as a corpus beside `hormozi`, query it through the
`rag` server. A rented index (Foreplay, AdSpy, BigSpy) answers one question and
keeps the answer; this one goes on answering.

## Findings

None yet.
