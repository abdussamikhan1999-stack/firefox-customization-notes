# Applied Firefox profile

Unlike the rest of this repo (which documents *links to* configuration
resources), this folder is an actual, working config — pulled directly
from the real upstream projects, dropped into a real Firefox profile, and
tested with the real `firefox` binary (v150.0) in this environment.

## What's here

- **`user.js`** — the real, current combined file from
  [yokoffing/Betterfox](https://github.com/yokoffing/Betterfox) (fetched
  directly, not retyped/summarized). Combines Betterfox's Fastfox
  (performance), Securefox (privacy/tracking), Peskyfox (UI decluttering),
  and Smoothfox (scrolling) modules into one file.
- **`userChrome.css`** — [MrOtherGuy/firefox-csshacks](https://github.com/MrOtherGuy/firefox-csshacks)'
  `compact_proton.css`, fetched directly (MPL 2.0, attribution preserved
  in the file's own header comment). Restores a more compact UI density
  than Firefox's default Proton spacing.

## What was actually verified, and how

**`user.js` — verified, not assumed.** Created a fresh Firefox profile,
dropped this file in as `<profile>/user.js`, and ran the real `firefox`
binary against it (`firefox --headless --profile <dir> ... about:support`).
A first attempt tried to confirm this via a screenshot of `about:support`,
but that page populates its tables asynchronously with JavaScript after
the initial paint, so the screenshot came back with every table empty —
worth noting as a dead end rather than silently dropping it, since it
looked like a plausible failure at first glance. The real proof came from
checking the profile's own `prefs.js`, which Firefox writes out on clean
shutdown reflecting every currently-active preference: it contained
`browser.contentblocking.category = "strict"`,
`network.http.max-connections = 1800`, and
`privacy.globalprivacycontrol.enabled = true` — the exact values from
`user.js`, not Firefox's own defaults (stock Firefox ships
`network.http.max-connections` at 900, for instance). That confirms the
preferences were genuinely read and applied by a real Firefox process,
not just written to a text file and hoped for.

**`userChrome.css` — also genuinely verified, via a different route.**
This environment has no display server (no Xvfb), and Firefox's normal
`--screenshot` flag only renders web page *content* — it never constructs
actual browser chrome, so that route was a dead end for this file
specifically. Instead, `verify_userchrome.py` (in this folder) launches
Firefox with `--marionette -remote-allow-system-access`, switches
Marionette (Firefox's own automation protocol) into **chrome context**
— normally reserved for testing Firefox itself, not web pages — and reads
back the real *computed* CSS values on actual chrome elements. Run twice,
with the same profile and same `user.js`, once with `userChrome.css`
present and once with it removed, to isolate that file specifically as
the cause rather than assuming:

| Check | Without `userChrome.css` | With `userChrome.css` |
|---|---|---|
| `--toolbarbutton-inner-padding` on `:root` | `8px` | `6px` |
| `.tab-close-button` width | `18px` | `20px` |

Both values match `compact_proton.css`'s explicit rules exactly (it sets
`--toolbarbutton-inner-padding: 6px !important` and
`.tab-close-button { width: 20px !important; }`). Reran the whole
comparison a second time and got identical numbers both times — this is
a real, reproducible measurement of the file's effect on Firefox's actual
style engine, not a guess based on "it didn't crash." Run it yourself
with `python3 verify_userchrome.py` (stdlib only, needs `firefox` on
`PATH`).

## Alternative: arkenfox instead of Betterfox

See [arkenfox-alternative/](arkenfox-alternative/) if you want arkenfox's
more thorough (and more work to live with) hardening baseline instead of
Betterfox's `user.js` above — **don't use both together**, they touch
overlapping preferences and will conflict. That folder documents the
actual tradeoff and was verified the same way this one was.

## Install

1. Open `about:profiles` in Firefox, find your profile's folder ("Open
   Directory" / "Root Directory"), or create a new profile if you'd
   rather not touch your daily one first.
2. Copy `user.js` into that profile folder directly (next to the
   existing `prefs.js`).
3. Create a `chrome` folder inside the profile folder if it doesn't
   exist, and copy `userChrome.css` into it as `chrome/userChrome.css`.
4. Fully restart Firefox (not just reload a tab — `user.js` is only read
   at startup).
5. Check `about:support`'s "Important Modified Preferences" table to
   confirm the Betterfox prefs took effect (this is the same check
   described above, just done visually instead of via `prefs.js`).
