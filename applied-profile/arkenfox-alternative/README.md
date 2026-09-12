# arkenfox alternative

The main `applied-profile/` folder ships Betterfox's `user.js`. The
top-level repo's own notes are explicit that Betterfox and arkenfox
shouldn't be *stacked* — they touch overlapping preferences and will
fight each other — so this is a documented **alternative**, not an
addition: pick one baseline, not both.

## `user.js` here — real, current, and checked

This is [arkenfox/user.js](https://github.com/arkenfox/user.js)'s actual
current file (v144, fetched directly, not retyped), 182 `user_pref` lines.

Verified the same way as Betterfox's file in the parent folder: dropped
it into a fresh profile, ran real Firefox against it, and checked the
written `prefs.js` afterward. 114 of arkenfox's 182 preference names
appear there with matching values (including
`privacy.resistFingerprinting.block_mozAddonManager = true` and
`browser.cache.disk.enable = false`, both arkenfox-specific) — real
confirmation the file was read and applied, not just present on disk.
(The remaining ~68 don't necessarily indicate anything wrong — some
overrides only take effect under conditions arkenfox's own file
comments describe, e.g. depending on other prefs or Firefox version
specifics; this wasn't chased further than the "does it demonstrably
work at all" question this comparison is for.)

## Betterfox vs. arkenfox — the actual tradeoff, not just an opinion

Both were verified working in this repo. The choice between them is
about how much you're willing to debug:

- **Betterfox** (in the parent folder) explicitly optimizes for not
  breaking sites — a smaller, more conservative preference set.
- **arkenfox** is the more thorough hardening baseline, and says so
  itself in its own header comment: read the whole wiki first, expect to
  need a `user-overrides.js` on top, expect some site breakage as a
  normal/expected outcome, not a bug.

If you're not sure, Betterfox in the parent folder is the lower-effort
starting point; come here specifically if you've decided you want
arkenfox's more aggressive posture and are willing to debug the fallout.

## Install

Same mechanism as the parent folder's `user.js` — copy this file to your
profile folder as `user.js`, restart Firefox. This one doesn't ship a
`userChrome.css`; use the parent folder's if you also want the UI
density change (it's independent of which `user.js` you pick).
