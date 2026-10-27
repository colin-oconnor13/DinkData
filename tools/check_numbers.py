#!/usr/bin/env python3
"""Regression check for the app's numbers.

Loads the real app on the demo data (?demo=1) in headless Chrome/Edge, reads the key figures
off the page (record, KPIs, Matchup Strength, Close Games, streaks, Partner/Opponent Index with
its Signals, Repeat Meetings, events) and compares them with tests/demo_snapshot.json. Any change
to the maths shows up as a diff, so a change is either intended (update the snapshot) or a bug.

    python tools/check_numbers.py            # compare; exit code 1 if anything changed
    python tools/check_numbers.py --update   # accept the current numbers as the new snapshot

Dates are replaced by placeholders, since demo mode moves the dates to end yesterday.
"""
import argparse, json, os, re, socket, subprocess, sys, time, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _cdp  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAP = os.path.join(ROOT, "tests", "demo_snapshot.json")

TEXT = r"(s=>{const e=document.querySelector(s);return e?e.innerText.replace(/\s+/g,' ').trim():null})"
READ = {  # name -> [tab to open or None, JS returning text]
    "match count": [None, "document.getElementById('fCount').textContent"],
    "record strip": [None, TEXT + "('#wlStrip')"],
    "overview KPIs": [None, TEXT + "('#kpis')"],
    "matchup strength": ["analysis", TEXT + "('#bdTable')"],
    "close games": ["analysis", TEXT + "('#cgTable')"],
    "streaks": ["analysis", TEXT + "('#stkKpis')"],
    "streak situations": ["analysis", TEXT + "('#stkTable')"],
    "performance by event": ["analysis", TEXT + "('#evTable')"],
    "partner index": ["people:partner", TEXT + "('#pxTable')"],
    "partner index hint": ["people:partner", "document.getElementById('pxHint').textContent"],
    "partner repeat meetings": ["people:partner", TEXT + "('#rptTable')"],
    "partner list": ["people:partner", TEXT + "('#pplTable')"],
    "opponent index": ["people:opp", TEXT + "('#pxTable')"],
    "opponent index hint": ["people:opp", "document.getElementById('pxHint').textContent"],
    "opponent repeat meetings": ["people:opp", TEXT + "('#rptTable')"],
    "opponent list": ["people:opp", TEXT + "('#pplTable')"],
    "matchup model note": ["people:partner", "document.getElementById('pxModel').textContent"],
}
DATES = [(re.compile(r"\b20\d\d-\d\d-\d\d\b"), "<date>"),
         (re.compile(r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2}, 20\d\d\b"), "<date>"),
         (re.compile(r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) '\d\d\b"), "<month>"),
         (re.compile(r"\b\d+[dwmy] ago\b|\btoday\b|\byesterday\b"), "<ago>")]


def scrub(v):
    if not isinstance(v, str): return v
    for rx, rep in DATES: v = rx.sub(rep, v)
    return v


def free_port():
    s = socket.socket(); s.bind(("127.0.0.1", 0)); p = s.getsockname()[1]; s.close(); return p


def collect():
    port = free_port()
    srv = subprocess.Popen([sys.executable, os.path.join(ROOT, "tools", "serve_local.py"), "--port", str(port)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    proc = profile = None
    try:
        for _ in range(50):
            try: urllib.request.urlopen(f"http://127.0.0.1:{port}/"); break
            except Exception: time.sleep(0.2)
        proc, page, profile = _cdp.launch(free_port())
        page.send("Page.enable")
        page.send("Page.addScriptToEvaluateOnNewDocument", source="window.__errs=[];addEventListener('error',e=>__errs.push(e.message));")
        page.send("Emulation.setDeviceMetricsOverride", width=1280, height=900, deviceScaleFactor=1, mobile=False)
        page.send("Page.navigate", url=f"http://localhost:{port}/?demo=1")
        page.wait("document.getElementById('kpis')&&document.getElementById('kpis').children.length")
        page.js("document.querySelectorAll('#zoom [data-z=\"all\"]').forEach(b=>b.click())")
        out, where = {}, None
        for name, (tab, expr) in READ.items():
            if tab != where:
                if tab:
                    t, _, mode = tab.partition(":")
                    page.js(f"document.querySelector('[data-tab={t}]').click()")
                    if mode: page.js(f"(document.querySelector('[data-p=\"{mode}\"]')||{{click(){{}}}}).click()")
                    time.sleep(0.5)
                where = tab
            out[name] = scrub(page.js(expr))
        out["page errors"] = page.js("window.__errs")
        return out
    finally:
        if proc: _cdp.close(proc, profile)
        srv.kill()


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--update", action="store_true", help="write the current numbers as the new snapshot")
    a = ap.parse_args()
    now = collect()
    if now["page errors"]:
        print("Page errors:", now["page errors"]); sys.exit(1)
    if a.update or not os.path.exists(SNAP):
        os.makedirs(os.path.dirname(SNAP), exist_ok=True)
        json.dump(now, open(SNAP, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"Snapshot written: {SNAP} ({len(now)} readings)"); return
    old = json.load(open(SNAP, encoding="utf-8"))
    changed = [k for k in sorted(set(old) | set(now)) if old.get(k) != now.get(k)]
    if not changed:
        print(f"OK: all {len(now)} readings match the snapshot."); return
    for k in changed:
        print(f"\nCHANGED: {k}\n  was: {old.get(k)}\n  now: {now.get(k)}")
    print(f"\n{len(changed)} of {len(now)} readings changed. If intended: python tools/check_numbers.py --update")
    sys.exit(1)


if __name__ == "__main__":
    main()
