# Pickleball — your DUPR history, analysed

A free web app that turns your DUPR match history into something you can learn from: how you do
by event, partner and opponent; who you play best and worst with **compared with what the
ratings expected**; your form over time; close games; streaks and bounce-back.

**Open the app:** <https://colin-oconnor13.github.io/PickleballStats/>

## Getting started (about two minutes)

1. Open the app and tap **Set up the Sync bookmark**.
2. Add the bookmark:
   - **Computer:** drag the **🔄 Sync to Pickleball** button to your bookmarks bar.
   - **Phone:** tap **📋 Copy bookmark code**, bookmark any page, edit that bookmark, name it
     **PB Sync** and paste the code over its address.
3. Log in at <https://dashboard.dupr.com> as usual (2FA included) and run the bookmark there.
   On a phone, type **PB Sync** in the address bar and tap the bookmark suggestion.
4. A panel on the DUPR page shows progress, then the app opens. Tap **Save**.

Sync again whenever you've played. On Android, use **Chrome** to sync: Edge doesn't run
bookmarks like this one. iPhone Safari should work but hasn't been tested.

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
chance (Strong over 2×, Some 1–2×, otherwise Noise).

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
