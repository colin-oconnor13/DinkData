# Change log — shared Pickleball app

Newest first.

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
