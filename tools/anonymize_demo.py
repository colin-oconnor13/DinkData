#!/usr/bin/env python3
"""Turn a real synced data.json into data/demo.json for the app's demo mode (?demo=1).

    python tools/anonymize_demo.py path/to/data.json

Keeps what makes the demo feel real (scores, results, the order and rhythm of matches, who
played with and against whom, each player's rating trend) and removes what points to real
people:

- every player (including the owner, shown as "Demo Player") gets a fictional name and id,
  the same one each time they appear, so partner/opponent stats still work;
- every event and venue gets a fictional name, keeping its type (tournament / league, as the
  app's eventType() reads it) and its skill level (3.0 / 3.5 / 4.0 ...);
- each player's ratings move by a small fixed amount (within +/-0.04), so they don't match
  anyone's real DUPR while their trend and the expected-results maths stay intact;
- match ids are renumbered. (The app moves the dates so the newest match is yesterday.)

Deterministic: the same input gives the same output.
"""
import io, json, os, random, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "demo.json")
rng = random.Random(4242)

FIRST = ["Avery", "Blake", "Casey", "Dana", "Ellis", "Finley", "Gray", "Harper", "Indy", "Jamie",
         "Kendall", "Lane", "Marlow", "Noel", "Oakley", "Parker", "Quinn", "Reese", "Sage", "Tatum",
         "Rowan", "Shay", "Teagan", "Wren", "Arden", "Bellamy", "Corin", "Darcy", "Emery", "Frankie",
         "Hollis", "Jules", "Kit", "Logan", "Morgan", "Remy", "Robin", "Skyler", "Toby", "Val"]
LAST = ["Ashdown", "Brightwater", "Calloway", "Dunmore", "Everly", "Fairbank", "Glenholm", "Hartwell",
        "Ingram", "Juniper", "Kestrel", "Larkspur", "Merriwether", "Northcott", "Oakhurst", "Pennington",
        "Quarry", "Rookwood", "Stillwell", "Thistledown", "Underhill", "Vale", "Whitlock", "Yardley",
        "Ambrose", "Birchall", "Cresswell", "Dovecote", "Elmsworth", "Foxley", "Greystone", "Hazelwood"]
PLACES = ["Lakeside", "Riverside", "Maple Grove", "Prairie View", "Harbor", "Cedar Ridge", "Northside",
          "Willow Creek", "Pine Hollow", "Sunset", "Granite Falls", "Meadowbrook"]
T_KINDS = ["Open", "Classic", "Shootout", "Championship", "Paddle Festival"]
L_KINDS = ["Ladder League", "Night League", "Round Robin League", "Indoor League", "Doubles League"]
TOURNEY = re.compile(r"tournament|festival|open|championship|state games|classic|shootout", re.I)


def main(src):
    d = json.load(io.open(src, encoding="utf-8"))
    me_id = d["player"]["id"]
    ms = sorted(d["matches"], key=lambda m: (m["date"], m["matchId"]))

    # Fictional names / ids / rating offsets, assigned in order of first appearance. Any fictional
    # first or last name that a real player in the source also has is left out, so none overlap.
    real_words = {w.lower() for m in ms for p in [m.get("partner"), *(m.get("opponents") or [])]
                  if p and p.get("name") for w in p["name"].split()} | {w.lower() for w in (d["player"].get("name") or "").split()}
    names = [f"{a} {b}" for a in FIRST for b in LAST if a.lower() not in real_words and b.lower() not in real_words]
    rng.shuffle(names)
    people = {me_id: {"name": "Demo Player", "id": 9099990001, "off": round(rng.uniform(-0.04, 0.04), 3)}}
    def person(pid):
        if pid not in people:
            people[pid] = {"name": names[len(people)], "id": 9100000000 + len(people) * 137 + 11,
                           "off": round(rng.uniform(-0.04, 0.04), 3)}
        return people[pid]
    shift = lambda v, off: None if v is None else round(float(v) + off, 4)

    # Fictional events, keeping type and level.
    events, used = {}, set()
    def event(raw):
        if raw not in events:
            lvl = (re.search(r"([2-5]\.[05])", raw or "") or [None, None])[1]
            while True:
                place = rng.choice(PLACES)
                if TOURNEY.search(raw or ""):
                    nm = f"{place} {rng.choice(['Spring', 'Summer', 'Fall', 'Winter'])} {rng.choice(T_KINDS)}" + \
                         (f" - Mens Doubles Skill: ({lvl})" if lvl else "")
                else:
                    nm = f"{place} {rng.choice(L_KINDS)}" + (f" {lvl}" if lvl else "")
                if nm not in used:
                    used.add(nm); events[raw] = (nm, f"{place} Pickleball Courts"); break
        return events[raw]

    out, mid = [], 7000001
    me = people[me_id]
    for m in ms:
        nm, venue = event(m.get("event") or m.get("venue") or "")
        def anon(p):
            if not p:
                return None
            q = person(p["id"])
            return {"id": q["id"], "name": q["name"], "ratingThen": shift(p.get("ratingThen"), q["off"]),
                    "ratingPre": shift(p.get("ratingPre"), q["off"]), "ratingNow": shift(p.get("ratingNow"), q["off"])}
        out.append({"matchId": mid, "date": m["date"], "event": nm, "venue": venue, "format": m.get("format") or "DOUBLES",
                    "confirmed": True, "winner": m.get("winner"), "scores": m.get("scores") or [], "oppScores": m.get("oppScores") or [],
                    "partner": anon(m.get("partner")), "opponents": [anon(o) for o in m.get("opponents") or []],
                    "preRating": shift(m.get("preRating"), me["off"]), "impact": m.get("impact"),
                    "postRating": shift(m.get("postRating"), me["off"])})
        mid += rng.randint(3, 40)

    cur = d["player"].get("currentDoubles")
    data = {"player": {"id": me["id"], "name": me["name"], "currentDoubles": shift(cur, me["off"])},
            "generated": d.get("generated"), "syncedAt": d.get("syncedAt"), "demo": True, "matches": out}
    text = json.dumps(data, ensure_ascii=False, indent=1)
    # Safety net: no real name or id from the source may survive.
    real = {str(me_id)} | {str(p["id"]) for m in ms for p in [m.get("partner"), *(m.get("opponents") or [])] if p}
    real |= {p["name"] for m in ms for p in [m.get("partner"), *(m.get("opponents") or [])] if p and p.get("name")}
    real |= {d["player"].get("name") or "", *(m.get("event") or "" for m in ms), *(m.get("venue") or "" for m in ms)}
    leaks = [r for r in real if r and len(r) > 3 and r in text]
    assert not leaks, f"real values left in demo.json: {leaks[:5]}"
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(text)
    print(f"Wrote {OUT}: {len(out)} matches, {len(people)} players, {len(events)} events renamed; no real names/ids left.")


if __name__ == "__main__":
    main(sys.argv[1])
