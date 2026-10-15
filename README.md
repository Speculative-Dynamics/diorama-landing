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
hash. If you edit either, recompute the hash or the browser will block it.
