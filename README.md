# Diorama landing

Static pages for the Diorama app, served by GitHub Pages at
https://speculative-dynamics.github.io/diorama-landing/.

- `index.html`: a one-screen page about the app.
- `smartthings-callback.html`: the redirect page registered with SmartThings.
  Samsung only redirects to https pages, so this page forwards the sign-in
  result (`code`, `state` or `error`, each checked against a strict pattern)
  to `diorama://smartthings/callback`. It stores nothing and removes the
  one-time code from the address bar.

Both pages pin their inline style and script with a Content Security Policy
hash, so edit them in `build.py` and run `python3 build.py .` to rewrite the
pages with fresh hashes.

`icon.png`, `apple-touch-icon.png` and `favicon.png` are the app icon at 512,
180 and 64 pixels, drawn by `scripts/app_icon.swift` in the Diorama app repo.
