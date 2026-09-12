#!/usr/bin/env python3
"""
Verifies userChrome.css actually applies to Firefox's real browser chrome
— headlessly, with no display server (no Xvfb) required.

Firefox's `--screenshot` flag only renders web page *content*; it never
constructs the actual browser chrome (toolbar, tabs) that userChrome.css
restyles, so a screenshot can't prove this file does anything. Instead,
this launches Firefox with Marionette (its own automation protocol) and
`-remote-allow-system-access`, switches Marionette into "chrome" context
(normally reserved for testing Firefox itself, not web content), and reads
back the *computed* CSS values on real chrome elements — proof the
stylesheet was actually applied by the browser's real style engine, not
just a text file that exists.

Runs the comparison twice with the same profile and the same user.js:
once with userChrome.css present, once with it removed, to isolate that
specific file as the cause of the change rather than assuming it.

Usage: python3 verify_userchrome.py
(no dependencies beyond a `firefox` binary on PATH; stdlib only)
"""
import json
import os
import shutil
import socket
import subprocess
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
MARIONETTE_PORT = 2828

# computed-style checks that compact_proton.css specifically sets;
# comparing against Firefox's own defaults (not asserted, measured
# fresh each run) is what makes this a real before/after, not a guess
# at what "stock Firefox" looks like.
CHECKS = [
    (
        "--toolbarbutton-inner-padding on :root",
        "return getComputedStyle(document.documentElement)"
        ".getPropertyValue('--toolbarbutton-inner-padding');",
    ),
    (
        ".tab-close-button width",
        "var el = document.querySelector('.tab-close-button');"
        "return el ? getComputedStyle(el).width : 'ELEMENT NOT FOUND';",
    ),
]


def marionette_send(sock, msg_id, name, params):
    payload = json.dumps([0, msg_id, name, params])
    sock.sendall(f"{len(payload)}:{payload}".encode())


def marionette_recv(sock):
    buf = b""
    while b":" not in buf:
        buf += sock.recv(1)
    length_str, rest = buf.split(b":", 1)
    length = int(length_str)
    while len(rest) < length:
        rest += sock.recv(4096)
    return json.loads(rest.decode())


def run_checks_against_profile(profile_dir):
    proc = subprocess.Popen(
        [
            "firefox", "--headless", "--no-remote", "--profile", profile_dir,
            "--marionette", "--new-instance", "-remote-allow-system-access",
        ],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        time.sleep(4)  # give Firefox time to start and open the Marionette port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect(("127.0.0.1", MARIONETTE_PORT))
        s.recv(4096)  # discard the initial handshake

        marionette_send(s, 1, "WebDriver:NewSession", {})
        marionette_recv(s)

        marionette_send(s, 2, "Marionette:SetContext", {"value": "chrome"})
        set_context_resp = marionette_recv(s)
        if set_context_resp[2] is not None:
            raise RuntimeError(f"Could not switch to chrome context: {set_context_resp[2]}")

        results = {}
        for i, (label, script) in enumerate(CHECKS, start=3):
            marionette_send(s, i, "WebDriver:ExecuteScript", {"script": script, "args": []})
            resp = marionette_recv(s)
            results[label] = resp[3]["value"] if resp[2] is None else f"ERROR: {resp[2]}"

        s.close()
        return results
    finally:
        proc.terminate()
        proc.wait(timeout=10)


def main():
    with tempfile.TemporaryDirectory() as profile_dir:
        shutil.copy(os.path.join(HERE, "user.js"), os.path.join(profile_dir, "user.js"))
        chrome_dir = os.path.join(profile_dir, "chrome")
        os.makedirs(chrome_dir, exist_ok=True)
        userchrome_path = os.path.join(chrome_dir, "userChrome.css")

        print("Checking WITHOUT userChrome.css (baseline)...")
        without = run_checks_against_profile(profile_dir)

        shutil.copy(os.path.join(HERE, "userChrome.css"), userchrome_path)
        print("Checking WITH userChrome.css...")
        with_ = run_checks_against_profile(profile_dir)

    print(f"\n{'Check':<40} {'Without userChrome.css':<25} {'With userChrome.css'}")
    print("-" * 95)
    changed_count = 0
    for label in without:
        b, a = without[label], with_.get(label, "(missing)")
        changed = b != a
        changed_count += changed
        print(f"{label:<40} {b!r:<25} {a!r}{'  <-- changed' if changed else ''}")

    print(f"\n{changed_count}/{len(without)} checks changed — this is the real, measured "
          f"effect of userChrome.css on Firefox's actual browser chrome.")


if __name__ == "__main__":
    main()
