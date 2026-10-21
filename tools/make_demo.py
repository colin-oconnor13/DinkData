#!/usr/bin/env python3
"""Generate data/demo.json: made-up matches for the app's demo mode (?demo=1).

Everyone in it is fictional. It is deterministic (fixed seed), so re-running gives the same
file. A few patterns are built in so every part of the app has something to show:

- the demo player improves faster than their rating catches up (beats expectations early);
- one tournament partner with real chemistry, one partnership that underperforms;
- a nemesis pair and a favourite opponent in the league;
- weekly ladder leagues (single games to 11) and tournaments (best of 3).

The app shifts every date so the newest match lands near today, so the demo never looks stale.

    python tools/make_demo.py
"""
import io, json, math, os, random
from datetime import date, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "demo.json")
rng = random.Random(20261021)
S = 0.45                      # rating gap scale of the win curve (a 0.25 edge wins ~78%)

FIRST = ["Avery", "Blake", "Casey", "Dana", "Ellis", "Finley", "Gray", "Harper", "Indy", "Jamie",
         "Kendall", "Lane", "Marlow", "Noel", "Oakley", "Parker", "Quinn", "Reese", "Sage", "Tatum",
         "Rowan", "Shay", "Teagan", "Wren", "Arden", "Bellamy", "Corin", "Darcy", "Emery", "Frankie"]
LAST = ["Ashdown", "Brightwater", "Calloway", "Dunmore", "Everly", "Fairbank", "Glenholm", "Hollis",
        "Ingram", "Juniper", "Kestrel", "Larkspur", "Merriwether", "Northcott", "Oakhurst", "Pennington",
        "Quarry", "Rookwood", "Stillwell", "Thistledown", "Underhill", "Vale", "Whitlock", "Yardley"]


class Player:
    def __init__(self, pid, name, skill):
        self.id, self.name, self.skill = pid, name, skill
        self.rating = round(skill + rng.gauss(0, 0.12), 3)


def make_people(n):
    names, out = set(), []
    while len(out) < n:
        nm = f"{rng.choice(FIRST)} {rng.choice(LAST)}"
        if nm in names:
            continue
        names.add(nm)
        out.append(Player(9100000000 + len(out) * 137 + 11, nm, round(rng.uniform(3.05, 4.35), 3)))
    return out


people = make_people(64)
ME = Player(9099990001, "Demo Player", 3.38)
ME.rating = 3.31
by_name = {p.name: p for p in people}

# Named roles (picked from the pool so they look like everyone else).
chem, steady, clash = people[0], people[1], people[2]          # tournament partners
chem.skill, steady.skill, clash.skill = 3.62, 3.55, 3.70
nemesis = (people[3], people[4])                                 # beat me more than they should
nemesis[0].skill, nemesis[1].skill = 3.50, 3.48
favourite = people[5]                                            # I beat them more than I should
favourite.skill = 3.66
BONUS_PARTNER = {chem.id: 0.14, clash.id: -0.12}
BONUS_OPP = {nemesis[0].id: -0.09, nemesis[1].id: -0.09, favourite.id: 0.10}
for p in (chem, steady, clash, *nemesis, favourite):
    p.rating = round(p.skill + rng.gauss(0, 0.06), 3)

START, END = date(2025, 4, 1), date(2026, 10, 14)
SPAN = (END - START).days


def my_skill(d):
    t = (d - START).days / SPAN
    return 3.38 + 0.36 * t + 0.04 * math.sin(t * 9)


def p_win(edge):
    return 1 / (1 + 10 ** (-edge / S))


def game_scores(p_team):
    """One game to 11 (win by 2) given our chance of winning it; returns (ours, theirs)."""
    won = rng.random() < p_team
    gap = max(0.6, rng.gauss(4.2 + 9 * abs(p_team - 0.5), 2.3))
    lose = max(0, round(11 - gap))
    if lose >= 10:                                   # deuce: 12-10, now and then 13-11
        lose = 10 + (rng.random() < 0.25)
    win = 11 if lose <= 9 else lose + 2
    return (win, lose) if won else (lose, win)


def update(players, share, exp_share, k=0.15):
    """DUPR-style: ratings move on the share of points won vs the share the ratings expected, so a
    close loss to a stronger team can still raise a rating (and a scrappy win can lower it)."""
    imp = round(k * (share - exp_share) * rng.uniform(0.8, 1.2), 4)
    for p in players:
        p.rating = round(p.rating + imp, 4)
    return imp


matches, mid = [], 7000001


def play(d, event, venue, partner, opps, best_of):
    global mid
    my_true = my_skill(d)
    team_true = (my_true + partner.skill) / 2 + BONUS_PARTNER.get(partner.id, 0) + sum(BONUS_OPP.get(o.id, 0) for o in opps) / 2
    opp_true = sum(o.skill for o in opps) / 2
    p_game = p_win(team_true - opp_true)
    sc, oc = [], []
    if best_of == 1:
        a, b = game_scores(p_game); sc, oc = [a], [b]
    else:
        w = l = 0
        while w < 2 and l < 2:
            a, b = game_scores(p_game); sc.append(a); oc.append(b)
            w, l = w + (a > b), l + (b > a)
    won = sum(a > b for a, b in zip(sc, oc)) > len(sc) / 2
    pre = {p.id: p.rating for p in (ME, partner, *opps)}
    exp = p_win((ME.rating + partner.rating) / 2 - (opps[0].rating + opps[1].rating) / 2)
    share, exp_share = sum(sc) / (sum(sc) + sum(oc)), 0.5 + (exp - 0.5) * 0.42
    my_imp = update([ME, partner], share, exp_share)
    update(list(opps), 1 - share, 1 - exp_share)
    info = lambda p: {"id": p.id, "name": p.name, "ratingThen": round(p.rating, 3), "ratingPre": round(pre[p.id], 4), "ratingNow": None, "_p": p}
    matches.append({"matchId": mid, "date": d.isoformat(), "event": event, "venue": venue, "format": "DOUBLES",
                    "confirmed": True, "winner": won, "scores": sc, "oppScores": oc,
                    "partner": info(partner), "opponents": [info(o) for o in opps],
                    "preRating": round(pre[ME.id], 4), "impact": round(my_imp, 5), "postRating": round(ME.rating, 4)})
    mid += rng.randint(3, 40)


# ---- schedule: ladder league seasons (Tuesdays) + tournaments ----
SEASONS = [("Riverside Spring Ladder League 3.5", date(2025, 4, 8), date(2025, 6, 24)),
           ("Riverside Fall Ladder League 3.5", date(2025, 9, 9), date(2025, 11, 18)),
           ("Northside Indoor Winter League 3.5", date(2026, 1, 6), date(2026, 3, 24)),
           ("Riverside Spring Ladder League 4.0", date(2026, 4, 7), date(2026, 6, 23)),
           ("Riverside Fall Ladder League 4.0", date(2026, 9, 8), date(2026, 10, 13))]
TOURNEYS = [("Lakeside Spring Open - Mens Doubles Skill: (3.5) Age: (Any)", date(2025, 5, 17), steady),
            ("Prairie Summer Classic - Mens Doubles Skill: (3.5)", date(2025, 7, 12), chem),
            ("Harbor Dink Shootout - Mens Doubles Skill: (3.5)", date(2025, 8, 23), clash),
            ("Maple Leaf Fall Open - Mens Doubles Skill: (3.5) Age: (Any)", date(2025, 10, 11), chem),
            ("Frostbite Indoor Classic - Mens Doubles Skill: (3.5)", date(2026, 2, 7), steady),
            ("Lakeside Spring Open - Mens Doubles Skill: (4.0) Age: (Any)", date(2026, 5, 16), chem),
            ("Sunset Paddle Festival - Mens Doubles Skill: (4.0)", date(2026, 6, 13), clash),
            ("Prairie Summer Classic - Mens Doubles Skill: (4.0)", date(2026, 7, 18), chem),
            ("Harbor Dink Shootout - Mens Doubles Skill: (4.0)", date(2026, 8, 22), steady),
            ("Maple Leaf Fall Open - Mens Doubles Skill: (4.0) Age: (Any)", date(2026, 10, 3), chem)]

league_pool = [p for p in people[6:] if abs(p.skill - 3.6) < 0.45] + list(nemesis) + [favourite]
days = {}
for name, a, b in SEASONS:
    d = a
    while d <= b:
        if rng.random() < 0.8:
            days.setdefault(d, []).append(("league", name))
        d += timedelta(days=7)
for name, d, partner in TOURNEYS:
    days.setdefault(d, []).append(("tourney", name, partner))

for d in sorted(days):
    for ev in days[d]:
        if ev[0] == "league":
            for _ in range(rng.choice((3, 3, 4))):
                if rng.random() < 0.12:
                    opps = list(nemesis)
                else:
                    opps = rng.sample(league_pool, 2)
                    if rng.random() < 0.10 and favourite not in opps:
                        opps[0] = favourite
                partner = rng.choice([p for p in league_pool if p not in opps and p not in nemesis])
                play(d, ev[1], "Riverside Courts, Lakeside" if "Riverside" in ev[1] else "Northside Rec Center, Lakeside", partner, opps, 1)
        else:
            lvl = 3.5 if "(3.5)" in ev[1] else 4.0
            field = [p for p in people[6:] if abs(p.skill - (lvl + 0.1)) < 0.4]
            for _ in range(rng.choice((4, 5, 5, 6))):
                play(d, ev[1], "Lakeside Pickleball Center", ev[2], rng.sample(field, 2), 3)

# Everyone's current rating, and the payload in the app's data.json shape.
for m in matches:
    for o in [m["partner"], *m["opponents"]]:
        o["ratingNow"] = round(o.pop("_p").rating, 3)
data = {"player": {"id": ME.id, "name": ME.name, "currentDoubles": round(ME.rating, 3)},
        "generated": "2026-10-15", "syncedAt": "2026-10-15T12:00:00.000Z", "demo": True, "matches": matches}
io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(data, ensure_ascii=False, indent=1))
wins = sum(m["winner"] for m in matches)
print(f"Wrote {OUT}: {len(matches)} matches, {wins}-{len(matches) - wins}, "
      f"rating {matches[0]['preRating']:.3f} -> {ME.rating:.3f}")
