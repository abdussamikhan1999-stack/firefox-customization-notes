# Firefox & Friends Customization Notes

Notes distilled from `/FFFCG/` (Firefox & Friends Customization General,
4chan `/g/`-style) — `user.js` privacy/performance tweaks, `userChrome.css`
UI theming, and Firefox-derivative browsers.

See [LINKS.md](LINKS.md) for the full raw link list, organized by section,
and [applied-profile/](applied-profile/) for an actual, working config
built from these links and tested against a real Firefox — not just a
summary of what's out there.

## The two config files this general revolves around

- **`user.js`** — drops into your Firefox profile folder and overrides
  `about:config` preferences at every startup (privacy, telemetry, security,
  performance knobs). This is what Betterfox/arkenfox and the hardening
  guide below all produce.
- **`userChrome.css`** / **`userContent.css`** — CSS that restyles Firefox's
  own UI (`userChrome.css`) or web page rendering (`userContent.css`).
  Needs `toolkit.legacyUserProfileCustomizations.stylesheets` enabled first.
  This is what the CSS-hacks repos below produce.

## `user.js` privacy/perf configs — pick one, don't combine blindly

- **Betterfox** — "law of diminishing returns / minimum effective dose"
  philosophy: privacy + performance + decluttering, deliberately *not*
  maximalist, explicitly trying to avoid breaking sites. Already integrated
  into several forks below (Zen, Waterfox, Floorp ship Betterfox-derived
  defaults). The lower-friction choice if you just want "better defaults,"
  not a hardening project.
- **arkenfox/user.js** — the more thorough hardening baseline; philosophy is
  user choice over one-size-fits-all — ships **overrides you're expected to
  apply on top**, since full hardening breaks some sites by design. Pair
  with uBlock Origin. The wiki's own framing: fewer than 10 common overrides
  fix ~99% of breakage people hit.
- **brainfucksec's 2026 hardening guide** — a step-by-step walkthrough
  (not a drop-in file) covering: dedicated hardening profile, switching to a
  non-tracking search engine, disabling telemetry/studies/crash reports,
  DNS prefetch/geolocation/WebRTC leak prevention, strict Enhanced Tracking
  Protection (Total Cookie Protection), DoH via Mullvad/AdGuard, Resist
  Fingerprinting (RFP), and clear-on-exit. Its own explicit warning: **don't
  blindly copy-paste config you don't understand** — same spirit as
  arkenfox's "expect to need overrides."

**Practical note**: these three overlap heavily and are not meant to be
stacked — arkenfox + Betterfox both touching the same prefs will fight each
other. Pick one baseline (Betterfox for low-friction, arkenfox if you want
maximum hardening and are willing to debug breakage) and layer the
hardening-guide's *concepts* (DoH provider choice, RFP, etc.) on top rather
than pasting all three.

## `userChrome.css` / theming resources

- **userchrome.org** — the reference/teaching site: what userChrome.css is,
  how to set up the stylesheet file, autoconfig scripting, plus community
  recipe-sharing. Start here if you've never touched this before.
- **firefoxcss-store** (github.io) — a gallery/store of ready-made themes.
- **MrOtherGuy/firefox-csshacks** — the deep well: 1,300+ commits of
  modular, self-contained tab/button/toolbar style snippets meant to be
  `@import`ed individually (not copy-pasted) so updates don't clobber your
  customizations.
- **ran-sama/firefox-preferences** and **zapSNH/zapsCoolPhotonTheme** —
  more specific preference lists / a themed style pack, respectively;
  narrower in scope than firefox-csshacks.
- **OP's own userChrome.css / userContent.css** (shorl.com links) — this
  particular thread's maintainer sharing their current personal config as a
  concrete example to fork from.

## Gecko-based Firefox forks — what actually differentiates them

- **LibreWolf** — the "privacy hardening, pre-applied" choice: ships with
  uBlock Origin built in, DRM removed, telemetry stripped, privacy search
  defaults (DuckDuckGo/Searx) — basically "arkenfox-style hardening without
  you doing the hardening yourself." Tracks Firefox's stable release
  closely.
- **Waterfox** — built-in ad blocking + **Oblivious HTTP relay DNS**
  (separates your identity from your DNS queries — a step beyond plain
  DoH), tree-style tabs, full telemetry removal, independent (non-Mozilla)
  funding model.
- **Floorp** — the productivity/power-user fork: Workspaces (tab groups
  bound to Firefox containers, so separate cookie jars per context),
  **Split View** (up to 4 pages in one window), pinnable Web Panels
  (sidebar mini-browser for any site). Closer to an "Arc browser for
  Firefox" pitch than a pure privacy fork.
- **Zen Browser** — (site itself still 403s automated fetches; verified via
  independent reviews instead — [OMG Ubuntu](https://www.omgubuntu.co.uk/2025/08/zen-browser-is-what-mozilla-firefox-should-be),
  [XDA Developers](https://www.xda-developers.com/this-firefox-fork-fixed-every-complaint-i-had-with-mozilla/))
  positions itself similarly to Floorp — vertical tabs by default,
  **Workspaces** (each keeps its own session state and cookies, not just a
  tab-grouping label), **Split View** (2–4 tabs in a binary-tree grid — a
  wide screen can genuinely drive a full 4-tab layout), plus Compact Mode
  and "Glance" link previews. Open-source (MPL 2.0), same rendering engine
  as Firefox — the novelty is entirely the interface/workflow layer, not a
  new engine. Reviews as of mid-2025/2026 still describe it as beta
  software, worth knowing before treating it as daily-driver-stable.
- **GNU IceCat** (gnu.org/software/gnuzilla) — the FSF's fully-free-software
  Firefox rebuild (strips anything non-free, including some codecs/DRM
  hooks); the "software freedom purist" option, at some functionality cost.
- **SeaMonkey** — the continuation of the old Mozilla Application Suite
  (browser + mail/news client + IRC + composer bundled together) — for
  people who specifically want the pre-Firefox all-in-one suite model.
- **K-Meleon** — a lightweight, Windows-only, non-XUL Gecko browser aimed
  at minimal resource usage on older/weaker hardware.
- **IronFox** (Android) — a fork of Divested Computing Group's Mull
  Browser (itself Firefox-based), AGPL-3.0, privacy/security-focused,
  distributed via F-Droid/Accrescent/Obtainium rather than the Play Store.
- **Fennec F-Droid** — the F-Droid-distributed, non-Google-Play build of
  Firefox for Android (Fennec was Firefox mobile's old codename) — useful
  specifically if you want Firefox mobile without any Google Play
  Services/Play Store dependency.
- **"male-poon" FreeBSD forum thread** — reads like a joke/shitpost
  reference to **Pale Moon** (an older independent Firefox fork, itself
  somewhat controversial in its community) rather than a real separate
  browser; treat as thread humor, not a genuine recommendation, unless you
  open it and find otherwise.

## Picking a fork

- Want hardened privacy with zero manual config → **LibreWolf**.
- Want a power-user/productivity layout (workspaces, split view) → **Floorp**
  or **Zen Browser** — compare the two directly, they're going after the
  same audience.
- Want DNS-level privacy specifically → **Waterfox**'s Oblivious HTTP relay
  is a distinctive feature none of the others mention.
- Want free-software purism over convenience → **GNU IceCat**.
- Want Android specifically, outside the Play Store → **IronFox** or
  **Fennec F-Droid**.
- Just want stock Firefox with better defaults, no fork commitment → skip
  forks entirely, apply **Betterfox**'s `user.js` to regular Firefox.

## Sharing configs

The thread's go-to pastebins for posting `user.js`/`userChrome.css`
snippets: **rentry.co**, **bin.disroot.org**, **share.riseup.net** — all
chosen specifically because they don't require an account to post (unlike
GitHub gists), lowering friction for quick config-sharing.
