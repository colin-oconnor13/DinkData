# Change log — shared Pickleball app

Newest first.

## 2026-10-29 — People: names link to DUPR profiles
- Player names on the People tab (partner/opponent list, the detail table, the people table, small
  samples, opponent pairs) open the player's DUPR profile in a new tab (`duprA`). Clicking a name
  doesn't select or expand its row. Plain text in the demo (made-up ids). SW cache rj-v103.
- tools/check_numbers.py: "4mo ago" style relative dates are normalised too, so the snapshot
  doesn't drift as the demo's dates move.

## 2026-10-27 — Highlights for other players with a full history
- Viewing another player now shows the Upsets / Notable results and the all-time range, unless
  their history was cut off at 150 matches (`HL_PARTIAL`: the `capped` flag from a "me + recent
  people" sync, or exactly 150 matches). Under 150 is everything they've played; over 150 came
  from a sync on their own DUPR page. Root `data-hl="off"` hides the cards. SW cache rj-v102.
- Header pill links to DUPR (dashboard before a sync, your player page after); the computer
  set-up step links to dashboard.dupr.com.

## 2026-10-27 — UX review 3: plain words everywhere (branch review-b2)
- **One "why" for every Signal** (`explain()`): the partner-row template (what happened / vs
  expected / could it be luck) now backs every How-sure pill, on hover (360 px box, any
  `[data-why]`) and on tap (bubble). Builder numbers (z, cut-offs) only with `?debug=1`.
- **No half-wins:** `about()` / `woeTxt()`: "about 3–4", "+3"; Last session has no pill ("You won 6,
  a great night"); tournaments "about 1 win"; Expected W–L whole. Percentages whole (`pct`).
- **Plain columns:** Matches, Games, Points won, Score vs expected, Rating change per match, How
  sure. Matchup bands named in words (cut-offs in tap text). "Given up" → Upset losses; DUPR at
  the time / Hindsight → Ratings then / now; "Worth watching" → "Leaning one way".
- **Copy:** Overview tiles, record line, playing-at sentence (1 decimal), Upsets card; Trends
  captions (form, tournaments, streaks, "When you play best" splits, rating goal admits a wide
  range); People index title/hint/footnotes (model note moved to the Guide, linked); match rows
  ("57% chance to win", event name only, "Oct 26"); sync messages (raw errors behind "details").
- **Guide:** new lead; Form and Signal passages fixed (they contradicted the app); Margin,
  Playing at, How sure, Ratings then / now rewritten.

## 2026-10-27 — UX review batch 2 (branch review-b2)
- **A · Last session** card opens the Overview: record vs what the ratings expected (with Signal),
  DUPR move, partners, the session's upset / given-up match, then 3 match rows + All N. Replaces
  "Latest matches" and the Latest chips in the record strip.
- **B · One partner list** (`renderPL`) replaces Standouts and Partner chemistry: wins vs expected
  with a ±2 SD luck range, grouped by Signal (2+ / Worth watching 1–2 / Too early, which shows 3 +
  Show more); tap for points, DUPR and the matches. The Partners / Opponents switch is a sticky bar
  at the top of the People tab (default Partners) and drives every card there.
- **C · Phone set-up** (?bm=1) is one step at a time with a progress bar and a new **Test it here**
  step. PB Sync run on any Dink Data page (it has #bmPage) fires `pbsync-test` instead of the
  "open DUPR" alert; sync.js rebuilt.
- **D · Four tabs:** Overview · Trends · People · Matches. Guide opens from **?** in the header (with
  Back). Highlights folded in: all-time range under the rating chart; Upset index + Notable results
  at the bottom of the Overview (the "Worth a look" teaser is gone); Matches gains Upsets ▲ / Given
  up ▼ chips (F.wl 'UP' / 'GU').
- **E · One Period** (All time · 12 mo · 60 days · Custom… with year shortcuts and a date range) at
  the top of the filter bar, part of `pass`. Gone: the Year filter, both Last-60-days switches,
  Highlights' own switch; the record strip follows the Period, not the chart zoom. Period counts as
  a filter (gold outline, ✕ Clear) but doesn't open the Filters panel.
- Partner list rows explain themselves in three plain lines, whole numbers only (tap to open; on
  desktop also a 360 px hover box): what happened vs what the ratings expected ("about 4–5"),
  whether the scores agree, and whether it could still be luck (with about how many more matches
  would tell). Card header, group and empty-list text rewritten to match.
- Guide text updated. SW cache rj-v99.

## 2026-10-27 — Chemistry: "Worth watching" group (branch review-all)
- Partner chemistry now has three groups by how far the result sits from 0 in luck units (SE):
  2+ = coloured with ▲/▼ (as before); 1–2 = **Worth watching** (faint colour, Leaning ●○○, with a
  note that about 1 in 3 partners land there by chance); under 1 = Too early to tell (grey).
  Legend gains a "Worth watching" swatch. SW cache rj-v98.

## 2026-10-27 — Active filter can't be missed (branch review-all)
Filters apply on every tab, and one set by tapping an event row was easy to miss (empty Partner
Index, short match list).
- When a filter is set or changed, the Filters panel opens. The bar gets a gold outline, the summary
  is shown in bold, and a **✕ Clear** button sits in the header, so it's visible even when collapsed.
- Empty Index or partner lists name the filter (or the 60-day switch) and offer ✕ Clear filters or Show all time
  (`emptyWhy`).
- SW cache rj-v97.

## 2026-10-27 — UX review fixes (batch 1, branch review-all)
From two UX reviews (the first on the live site, the second on this branch).
- **Trust:** Signal words Clear ●●● / Likely ●●○ / Leaning ●○○ / Too early ○○○; "vs expected"
  numbers coloured only at Likely or Clear (`woeCls`); 0.000 changes uncoloured; on phones the
  Signal is a full-width line under the name (`td.sigcell`); predictor inputs fit; card labels don't
  break at dashes. Chemistry rows whose luck range crosses 0 are grey, no arrow, grouped under
  "Too early to tell". Standouts name someone only at Clear.
- **First run:** with no data, only the welcome card and the open set-up steps (`.nodata`); no
  Sync now until the first sync. One name, **PB Sync**, everywhere (incl. the on-DUPR panel).
- **Freshness:** header shows "Colin · synced 2 days ago"; stale banner after 7 days (was 21).
- **Overview:** "played like a 3.61–4.56 player (your DUPR is 3.61)" leads with the range; What
  to work on is one line when nothing clears, otherwise an action; Latest matches compact (no
  date / event line), 3 rows + "All N"; tile copy rewritten; matches per month moved to Form.
- **Trends:** Form "Playing at" compared with your DUPR; Tournament results after Event Matches;
  Performance by Event has W–L vs expected; Performance by Date shows 6 days + "Show all"; rating
  goal is a range of months, at the bottom; recent rating changes read "±"; no gender aside.
- **Highlights:** hint no longer styled as a card; Peak and Current merge when equal.
- **Theme / a11y:** phones follow the system theme; light-theme lime / gold / loss darkened to
  ≥ 4.5:1; tabs have role=tab + aria-selected; W/L chips are buttons; 44 px targets on touch;
  reduced motion also stops smooth scrolling; touch wording ("Tap") on touch screens.
- **Sync:** your own account with new matches gets one step ("8 new matches · Oct 26 · 6–2 ·
  +0.086 → See your last session"); other cases keep the careful three-button wording.
- Snapshot updated (wording, labels, the new event column). SW rj-v96.

## 2026-10-27 — review build: every mock-up from the stats/coaching review (branch review-all)
Built from the approved mock-up gallery; reviewed locally on Colin's Oct 26 export before publishing.
- **Value retired** (option A): gone from the Overview, event / date / people tables and Form;
  Context shows Avg opponent + Expected win %; people rank by Wins vs expected by default.
- **Opponent-strength buckets removed**; Matchup Strength adds Expected win %, Wins vs expected and
  DUPR change / match (Pts%, Value, Opponent columns dropped there).
- **Record strip:** the expected record and a tick for the expected win %.
- **Close Games:** Expected win % + Wins vs expected (each game carries its match's win chance).
- **Upsets:** under 40% / over 60% win chance; "Wins above expected" (underdog matches) replaces Net.
- **Partner chemistry:** margin vs expected with ±2 SE luck range (was raw margin vs your overall).
- **Standouts:** ranked by the evidence score with the Signal pill; "Nobody stands out yet" < |z| 2.
- **Performance by Date:** nights under 6 matches greyed and tagged "few matches".
- **Playing at** (`playingAt`): rating your last 20 results were worth, as a dashed line with a
  luck band (clipped) on Rating Over Time, and the default Form metric. Matches per month below
  the chart. Rating dots are ▲/▼ shapes as well as colours.
- **Tournament results** card (record, expected, played at, DUPR change), **rating-adjusted splits**
  (match number in a day, days off, playing up / at / down, partner rated above / below, venue),
  **What to work on** (only |z| ≥ 2, else the biggest lean and how many more matches would tell),
  **opponent pairs** (3+ meetings).
- **Index:** Effect (DUPR) column with likely range (empirical Bayes, `effectsOf`); when results
  don't spread beyond luck the effect reads "0.00 · within luck". A robustness line: matches with
  someone whose rating has since moved 0.3+, and which labels change without them (†).
- Guide: Playing at and Effect (DUPR) added, Value removed, Trends description updated.
- Regression snapshot updated for these intended changes. SW rj-v95.

## 2026-10-27 — viewing dropdown sorted
- The 👁 Viewing dropdown lists My matches first, then viewed players alphabetically by name
  (first name first, case-insensitive) instead of in the order they were synced. SW rj-v94.

## 2026-10-27 — numbers regression check; exact Signal tails; smaller fixes
- **`tools/check_numbers.py`** (+ `tools/_cdp.py`, `tests/demo_snapshot.json`): loads the real app
  on the demo in headless Chrome/Edge and compares 18 readings (record, KPIs, Matchup Strength,
  Close Games, streaks, Index tables + hints, Repeat Meetings, lists, events) with the snapshot.
- **Exact wins surprise** (`winsZ`): Poisson-binomial mid-p tail turned into z, instead of the
  normal approximation, which overstated small samples (4 wins in 4 even matches: 2.00 → 1.86).
  Checked against an independent Python version to 4 decimals. Snapshot change: a few 4-match
  opponent rows move Leaning → Could be luck.
- **S shrinkage:** the fitted S is pulled toward 0.48 with a weight of 40 matches.
- **Unconfirmed matches** sit out the model and the Signal and are marked in the match log.
- **Viewed players** synced via "Me + recent people" (150-match cap) are labelled "based on their
  last 150 DUPR matches" in the viewing bar (`capped`, set on new syncs).
- **Demo banner** says ratings are shifted a little to anonymise. SW rj-v93.

## 2026-10-27 — fixes from the stats/coaching review (checked on real data)
Checked against Colin's Oct 26 export before and after (241 matches → 238 doubles).
- **Ratings going into the match everywhere** (`diff = diffPre`, `oppThen` / `partnerThen` from
  `ratingPre`): post-match ratings contain the result. Matchup Strength "Favored" was 83%, really
  55%; "Underdog" 30% → 37%. Also Value's schedule term, Avg opponent, buckets, match-log ratings.
- **Hindsight basis** (was "DUPR now"): your rating then + everyone else's current rating; it used
  to apply your *current* rating to every old match. Toggle reads "DUPR at the time / Hindsight".
- **Signal on one baseline:** expected margin is fitted through zero (`MODEL.a = 0`), so the margin
  half compares against the ratings like the wins half (it measured "vs your usual margin").
- **Signal table:** the Strong cutoff counts every row, not just the name-search matches; a line
  says what luck alone gives ("about 14 of these 45 … Leaning or stronger, about 2.0 … Some").
- **Best / Worst tags** only when |z| ≥ 2 (all 6 partner tags were luck), with ↑/↓.
- **Repeat Meetings** counts a match once per row (151 matches were counted twice).
- **Streaks** use DUPR's processing order, like the current-streak teaser (they disagreed: L1 vs
  W2); the hint gives the typical longest streak by chance (~W6 / L7).
- **Singles excluded** (`M` is doubles only): 3 singles were in the record, Win %, Close Games.
- **Rally scoring:** games to 21 are scaled to 21 for Margin.
- **Late-entered matches** (`CHART_LATE`) sit out the S fit and the Signal.
- **Rating went up** (one name everywhere; was Rating rose / Beat exp.) leaves 0.000 changes out.
- **Predictor** keys players by DUPR id (two people with one name no longer collapse).
- **Guide:** tab names (Form is on Trends), every view that ignores the filters, doubles only,
  Strong/Some no longer overclaim, Margin is an average of games with ±5-point game noise, Points
  won is pooled, Hindsight explained; removed "your rating may be about to follow".
- Not changed yet (decisions pending): opponent-strength buckets, Value. SW rj-v92.

## 2026-10-26 — record strip follows the Rating Over Time zoom
- The strip's W–L and win % now cover the filtered matches inside the Rating Over Time zoom
  window (3M / 6M / 1Y / All / a year), labelled "Record · last 3 months" etc., and redraw when
  the zoom changes (`renderWL`, `WL_LIST`). Phones open that chart on 3M, so the strip does too.
  The Latest chips are unchanged. SW rj-v91.

## 2026-10-26 — Overview record strip
- Picked from mock-ups (option B, with the latest day instead of the last 10): a full-width strip
  at the top of Your performance (`#wlStrip`): **W – L** large in green/red and a win % bar, both
  following the filters, plus **Latest · <date>**: W/L chips for the latest day's matches (the
  same matches as Latest matches, unfiltered, in processing order) with the day's record; tapping
  them scrolls to Latest matches.
- Win % moved out of the Results group (the strip carries it): Results is now Points won +
  Margin; Context is Value + Avg opponent. SW rj-v90.

## 2026-10-26 — Rating Over Time no longer drops recent days
- Reported: a viewed player (Troy, 324 matches) had months of recent days missing from Rating
  Over Time while Form showed them. Cause: the chart leaves out days whose matches are all
  "late" (rated after later-dated ones), and `ORDER` bridges every break in the rating chain
  (DUPR restating a rating) with the closest continuation; one wrong jump ahead made weeks of
  normal matches look late. Reproduced on real data with 4 restated ratings: 10 of 30 days hidden.
- The chart now uses `CHART_LATE`: exact links only, a backwards link taken only when it is the
  only one, and late only if rated after a match dated over a week later. Same test: all 30 days
  drawn; clean data unchanged. `LATE` / the 📅 offer in Clean up are unchanged.
- The 150-match cap on "Me + recent people" already keeps the *most recent* 150 (history comes
  newest-first); players synced from their own DUPR page aren't capped. SW rj-v89.

## 2026-10-21 — moved to colin-oconnor13.github.io/DinkData
- Repo renamed PickleballStats → **DinkData**; `site.json` app URL, README links, the Sync
  bookmark loader and `sync.js` now point at `/DinkData/`. GitHub doesn't redirect Pages sites on
  a rename, so a separate tiny repo named **PickleballStats** serves a redirect: every old path,
  query and #fragment forwards to the same place here (sync hand-offs, ?demo, ?bm keep working),
  and its `sync.js` loads this one, so existing PB Sync bookmarks keep working unchanged.
  localStorage / IndexedDB are per origin (colin-oconnor13.github.io), so visitors keep their data.
  Home-screen installs of the old URL should be reinstalled. SW rj-v88.

## 2026-10-21 — demo uses real, anonymised matches
- `data/demo.json` is now Colin's 234 synced matches run through **`tools/anonymize_demo.py`**:
  every player gets a fictional name and id (consistently, so partner/opponent stats hold; no
  fictional first/last name matches a real player's), events and venues get fictional names that
  keep tournament/league type and skill level, each player's ratings shift by a fixed ±0.04, match
  ids are renumbered; scores, results and order are kept. The script refuses to write if any real
  name, id, event or venue string survives. `tools/make_demo.py` (synthetic data) removed.

## 2026-10-21 — demo mode with made-up data
- PBStats is retired; this shared copy is the one app now (changes no longer ported).
- **👀 See a demo first** on the welcome card opens `?demo=1`: the full app on `data/demo.json`,
  ~190 matches of fictional players over ~18 months (ladder leagues + tournaments) from
  `tools/make_demo.py` (fixed seed). Built-in patterns so every view has something to show: the
  player outgrows their rating, a chemistry partner and a weak partnership, a nemesis pair and a
  favourite opponent, deuce games, best-of-3 tournament matches, and DUPR-style score-based rating
  moves (some losses raise the rating). Dates shift so the newest match is yesterday.
- The demo never reads or writes the visitor's data: no viewed players, saved edits ignored,
  `save()` no-op, Clean-up (export/import/delete) hidden, idpill "Demo data", a banner with
  **Set up with my DUPR →** (`?setup=1` opens the sync card) and **Exit demo**.
- `serve_local.py` serves the committed `data/demo.json` (other `/data/` files stay local). SW rj-v87.

## 2026-10-20 — renamed Dink Data, new logo
- App name **Dink Data**, tagline *your DUPR history, analysed* (header, tab title, home-screen
  name, manifest, welcome card, setup page, the bookmark button and the on-DUPR sync panel
  "🔄 Sync to Dink Data"). Repo names and URLs unchanged.
- New logo (picked from mock-ups): a lime pickleball whose holes become a rising trend line, the
  last point larger. `favicon.svg`, the header SVG, and `icons/icon-192/512.png` (dark tile, mark
  inside the maskable safe zone) were re-rendered. SW rj-v86.

## 2026-10-20 — setup page: steps for your browser
- The bookmark helper's steps were Chrome-only. It now guesses the browser from the user agent
  (Edge → `edge`; iOS Safari → `safari`; Android Chrome/Brave → `chrome`; anything else,
  incl. Chrome on iOS and Samsung Internet → `other`) and shows that set of steps 2–5, with
  pills to switch. Edge uses Favorites wording; Safari uses Share → Add Bookmark, then
  Bookmarks → Edit, and runs from Bookmarks. Edge/Safari menu wording is best-effort and
  untested on devices; a note says menus vary by version.
- The desktop-site tip is on the setup page too, and Safari's is worded as "the menu button
  next to the web address (aA or ⋯)" since the icon differs across iOS versions. The phone
  panel and Sync-now tip no longer assume Chrome's ☆ suggestion. SW rj-v85.

## 2026-10-20 — phone tip: use the desktop site if DUPR sends you to its app
- Tester feedback: logging in at dashboard.dupr.com on a phone with the DUPR app took them into
  the app. DUPR's mobile site runs a Branch "Journeys" redirect (`window.top.location` to
  `mydupr-alternate.app.link/…?__branch_flow_type=viewapp`), which hands off to the app, and it
  doesn't fire on every visit. The **On a phone** panel now has a "DUPR keeps sending you to its
  app?" tip: switch the DUPR tab to the desktop site (Chrome/Brave ⋮ → Desktop site; Edge … →
  View desktop site; Safari aA → Request Desktop Website), log in, run PB Sync. Not yet
  confirmed by the tester. SW rj-v84.

## 2026-10-20 — clearer first-time setup; iPhone + DUPR app; no Edge warning
- **Setup section redesigned:** a bigger "First time on this device?" heading and two panels with
  drawn icons, **On a computer** (Ctrl/⌘+Shift+B, drag the button, sync) and **On a phone**
  (why a second bookmark, **📌 Set up on this phone**, how to sync). Side by side on wide
  screens; stacked on phones with the phone panel first.
- **DUPR app installed:** iPhones open every tapped dashboard.dupr.com link in the app except
  `/session` (DUPR's apple-app-site-association), so on iOS **Sync now** opens `/session`, with a
  note that DUPR's "page not found" there is expected (the bookmark runs on any DUPR page).
  Android (Chrome, Edge, Brave) stays in the browser, so it keeps the home page. The Sync-now
  tip and the setup page add a fallback: type dashboard.dupr.com in the address bar. Running
  PB Sync on the `/session` page is not yet confirmed on an iPhone.
- **Edge works:** removed the "use Chrome, Edge won't run bookmarks" text (app, setup page,
  READMEs). SW rj-v83.

## 2026-10-20 — bookmark helper is its own simple page
- `?bm=1` no longer shows the whole app with a note (it wasn't obvious it was a different page).
  The `bm-only` class is set before first paint and hides everything but `#bmPage`: a single
  "Make your PB Sync bookmark" card with 4 steps (Copy code → ⋮ ☆ → Edit → paste as URL), how to
  run it on DUPR, and Back to the app. The page title is "PB Sync", so the new bookmark arrives
  already named. The app's sync card now just has **📌 Set up on this phone** for phones. SW rj-v82.

## 2026-10-20 — short loader bookmark (phone sync did nothing)
- On Chrome for Android the pasted bookmark was cut off at ~2,000 of its 9,100 characters, so it
  was a syntax error and nothing ran. `build_bookmarklet.py` now writes **`sync.js`** (the
  bookmarklet source with site.json values) and the published bookmark is a ~300-char loader
  that adds `<site>/sync.js?<time>` to the DUPR page, with an alert if it can't load. dashboard.dupr.com
  sends no Content-Security-Policy, so the script is allowed. Sync fixes now reach users without
  re-making the bookmark. Old long bookmarks keep working. `serve_local.py` still inlines the
  full code (an https page may refuse http://localhost scripts). SW rj-v81.

## 2026-10-20 — ported from PBStats: phone setup via a bookmark helper page
- Phone setup now starts with **📌 Open bookmark helper** (the app at `?bm=1`), so the ☆ makes a
  new bookmark to turn into PB Sync instead of editing your normal bookmark of the app. SW rj-v80.

## 2026-10-20 — ported from PBStats: Standouts colours
- Toughest partner / Nemesis are always red and only name someone below expected; otherwise the
  tile says "Nobody" (and the same for Best / Favourite above expected). SW rj-v79.

## 2026-10-20 — ported from PBStats: Signal uses points too; Leaning ↑/↓
- Signal now weighs points (margin vs expected) as well as wins, without double-counting.
- New **Leaning ↑/↓** label for a direction that's still within luck; arrows on every pill;
  the tap text explains the numbers behind each label. SW rj-v78.

## 2026-10-20 — ported from PBStats: sync-link hardening, stricter Signal, tap-to-explain
- Recent players bundled in a sync link are stored only after you choose Save / Open app / Keep.
- Signal allows for how many people a table tests (Strong ≈ 3.3× for 45 people; Some ≥ 2×).
- Phones: tap anything with hover text to read it; table cards show column explanations (ⓘ).
- Also brings over everything else PBStats added since 2026-10-11 (see its LOG). SW rj-v77.

## 2026-10-11 — "How to read this" guide tab
- New 4th tab (**Guide** on mobile): a plain-language explainer of the three views, filters,
  every metric, the expected-vs-actual idea, the reliability signals and small-sample rules, the
  charts, and viewing other players. Static and data-free, so it works before a first sync.

## 2026-10-11 — plainer wording, no GitHub terms shown
- Jargon removed from visible text (Your performance, Recent rating changes, "DUPR change",
  "Expected…", "Could be luck" signal) and the Partner Index note rewritten in plain English.
- No "GitHub" wording appears anywhere a visitor can see it (data is kept in their browser).

## 2026-10-11 — easier mobile sync
- **Sync now** button (header, sync card, stale banner) opens dashboard.dupr.com and copies the
  "PB Sync" keyword with a reminder, so syncing after setup is nearly one tap.
- Phone bookmark setup is now 3 numbered visual step cards instead of a paragraph.
- Rating Over Time gains 3M / 6M / 1Y range pills (phones default to 3M).

## 2026-10-11 — view other players
- Run the Sync bookmark on another player's DUPR page to view their stats, or choose
  "Me + my 14 most recent people" on your own sync. Their data stays in this browser only
  (IndexedDB); a 👁 Viewing bar switches between you and them, and removes them.

## 2026-10-11 — first shared release
Shared copy of the maintainer's personal app, with browser storage: each visitor's synced
matches stay in their own browser (localStorage `pb-data-v1`), with Export / Import / Delete in
the Clean up panel and a welcome card on first visit. The Sync bookmark syncs whoever is logged
in to DUPR. Features: Overview / Analysis / Opponents & Partners tabs, Partner / Opponent Index
from a win curve fitted to each player's own matches, form, close games, streaks, repeat
meetings, phone layout and a phone-friendly bookmark (same-tab handoff in the URL fragment).
