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

**`userChrome.css` — only partially verified.** This environment has no
display server (no Xvfb), and Firefox's headless mode renders web page
*content* only — it never constructs the actual browser chrome (toolbar,
tabs) that this file restyles, so there is no way to visually confirm it
looks right from here. What *was* verified: `user.js` already sets
`toolkit.legacyUserProfileCustomizations.stylesheets = true` (confirmed
present in the written `prefs.js`, so you don't need to enable this
yourself), and running Firefox with the stylesheet file in place
(`<profile>/chrome/userChrome.css`) produced a clean exit (code 0), no
stderr output, and no crash-report files — so it's not obviously broken —
but "doesn't crash" is a much weaker claim than "renders correctly."
**Actually look at your toolbar after installing this** rather than
trusting that it's right sight-unseen.

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
