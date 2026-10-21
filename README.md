# Pickleball — your DUPR history, analysed

A free web app that turns your DUPR match history into something you can learn from: how you do
by event, partner and opponent; who you play best and worst with **compared with what the
ratings expected**; your form over time; close games; streaks and bounce-back.

**Open the app:** <https://colin-oconnor13.github.io/PickleballStats/>

## Getting started (about two minutes)

1. Open the app and tap **Set up the Sync bookmark**.
2. Add the bookmark:
   - **Computer:** drag the **🔄 Sync to Pickleball** button to your bookmarks bar.
   - **Phone:** you need a *second* bookmark just for syncing; your normal bookmark of the app
     stays. Tap **📌 Set up on this phone**: a setup-only page at its own address, titled
     "PB Sync", so Chrome's ☆ makes a new, already-named bookmark. Tap **📋 Copy code**,
     bookmark that page (⋮ → ☆), tap **Edit** and replace its URL with the code.
3. Log in at <https://dashboard.dupr.com> as usual (2FA included) and run the bookmark there.
   On a phone, type **PB Sync** in the address bar and tap the bookmark suggestion.
4. A panel on the DUPR page shows progress, then the app opens. Tap **Save**.

Sync again whenever you've played. Tested on Android in Chrome and Edge; iPhone Safari should
work but hasn't been tested.

## Viewing other players

- Open another player's profile on dashboard.dupr.com and run the bookmark there: it asks
  whether to sync **their** matches (view only) or yours.
- On your own sync you can also choose **Me + my 14 most recent people**.
- Switch between yourself and them with the **👁 Viewing** bar at the top, which also removes
  them. They're kept in this browser only, like your own data.

## Your privacy

- The sync runs **in your own browser**, using the DUPR login you already have. Your password
  and 2FA code are never seen by this app.
- Your matches are saved **only in that browser**. They aren't sent to this site, to the person
  who shared it, or anywhere else. The site is a static page; its host only sees a visit.
- Each device keeps its own copy. To move to another device or keep a backup:
  **Filters → ⚙ Clean up data → Your data → Export my data**, then **Import data** on the other
  device. **Delete my data from this browser** removes everything.

## What you'll see

- **Overview:** headline numbers for any filter (year, event type, level, event, partner),
  performance by event, rating by event.
- **Analysis:** rating over time, rolling 20-match form, performance by date and by matchup
  strength, close games & deciders, streaks & bounce-back, and the full match log.
- **Opponents & Partners:** the Partner / Opponent Index (expected vs actual results), ranked
  lists with your DUPR change per match, and patterns: you vs your partner's rating, balanced vs
  lopsided opponents, repeat meetings.

Anyone or anything with fewer than 4 matches is shown separately as a small sample.

## How "expected" works

Expected win % = `1 / (1 + 10^(−Δ / S))`, where Δ is (your DUPR + partner's) / 2 minus the
opponents' average, everyone's rating going into the match. S is fitted to **your own** matches.
**Wins vs expected** = actual wins − expected wins; **Signal** says whether that gap is bigger than
chance, weighing your points (margin vs expected) as well as your wins, with an arrow for the
direction. Strong means beyond chance even allowing for how many people the table lists (about
3.3× for 45 people, never below 2×); Some is 2× or more; Leaning is 1–2× (a direction only);
otherwise Could be luck.

## Good to know

This app uses the same internal API as DUPR's own dashboard, from your browser while you're
logged in. It isn't an official DUPR product, and DUPR could change that API at any time.

---

## For developers

Static site, no build. `site.json` is the only per-copy setting: `storage` (`"browser"` here;
`"github"` commits synced data to a repo instead), the Sync bookmark's `app` address, and an
optional pinned DUPR player. After editing `site.json` or `tools/sync_bookmarklet.js`, run
`python tools/build_bookmarklet.py`. `python tools/serve_local.py` runs a copy on localhost that
saves to the git-ignored `local/` folder.

Based on [kyeill/pickleball](https://github.com/kyeill/pickleball); the win-probability curve
comes from [DaRubberDuckieee/pickleball-dupr-predictor](https://github.com/DaRubberDuckieee/pickleball-dupr-predictor).
