# Change log — shared Pickleball app

Newest first.

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
