"""Minimal Chrome DevTools Protocol client (standard library only), used by check_numbers.py."""
import base64, json, os, shutil, socket, struct, subprocess, tempfile, time, urllib.request

CHROMES = [os.environ.get("CHROME", ""),
           r"C:\Program Files\Google\Chrome\Application\chrome.exe",
           r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
           "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
           "/usr/bin/google-chrome", "/usr/bin/chromium"]


class Page:
    def __init__(self, ws_url):
        host_port, path = ws_url[len("ws://"):].split("/", 1)
        host, port = host_port.split(":")
        self.s = socket.create_connection((host, int(port)))
        key = base64.b64encode(os.urandom(16)).decode()
        self.s.sendall((f"GET /{path} HTTP/1.1\r\nHost: {host_port}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n"
                        f"Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n").encode())
        buf = b""
        while b"\r\n\r\n" not in buf:
            buf += self.s.recv(4096)
        self.rest, self.n = buf.split(b"\r\n\r\n", 1)[1], 0

    def _recv(self, k):
        while len(self.rest) < k:
            self.rest += self.s.recv(65536)
        out, self.rest = self.rest[:k], self.rest[k:]
        return out

    def _frame(self):
        b1, b2 = self._recv(2)
        ln = b2 & 0x7F
        if ln == 126: ln = struct.unpack(">H", self._recv(2))[0]
        elif ln == 127: ln = struct.unpack(">Q", self._recv(8))[0]
        return b1 & 0x0F, self._recv(ln)

    def send(self, method, **params):
        self.n += 1
        data = json.dumps({"id": self.n, "method": method, "params": params}).encode()
        ln = len(data)
        hdr = bytes([0x81]) + (bytes([0x80 | ln]) if ln < 126 else bytes([0x80 | 126]) + struct.pack(">H", ln) if ln < 65536
                               else bytes([0x80 | 127]) + struct.pack(">Q", ln))
        mask = os.urandom(4)
        self.s.sendall(hdr + mask + bytes(c ^ mask[i % 4] for i, c in enumerate(data)))
        while True:
            op, payload = self._frame()
            if op != 1: continue
            msg = json.loads(payload)
            if msg.get("id") == self.n:
                if "error" in msg: raise RuntimeError(msg["error"])
                return msg.get("result", {})

    def js(self, expr):
        r = self.send("Runtime.evaluate", expression=expr, awaitPromise=True, returnByValue=True)
        if "exceptionDetails" in r: raise RuntimeError(r["exceptionDetails"])
        return r["result"].get("value")

    def wait(self, expr, secs=20):
        for _ in range(int(secs * 5)):
            try:
                if self.js(expr): return True
            except RuntimeError:
                pass
            time.sleep(0.2)
        raise TimeoutError(expr)


def launch(port=9341):
    exe = next((c for c in CHROMES if c and os.path.exists(c)), None)
    if not exe: raise SystemExit("Chrome or Edge not found; set CHROME to its path.")
    profile = tempfile.mkdtemp(prefix="dinkdata-check-")
    proc = subprocess.Popen([exe, "--headless=new", "--disable-gpu", f"--remote-debugging-port={port}",
                             f"--user-data-dir={profile}", "about:blank"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(75):
        try:
            tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list"))
            page = next(t for t in tabs if t["type"] == "page")
            return proc, Page(page["webSocketDebuggerUrl"]), profile
        except Exception:
            time.sleep(0.2)
    proc.kill(); raise RuntimeError("browser did not start")


def close(proc, profile):
    proc.kill()
    try: proc.wait(5)
    except Exception: pass
    shutil.rmtree(profile, ignore_errors=True)
