"""Writes index.html and smartthings-callback.html with their CSP hashes.

Run from this folder: python3 build.py .
Icons come from the app repo: swift scripts/app_icon.swift <dir> 64 180 512
"""
import base64, hashlib, sys
out = sys.argv[1]

def sha(s):
    return "sha256-" + base64.b64encode(hashlib.sha256(s.encode()).digest()).decode()

def page(title, style, body, script=None, robots="noindex, nofollow"):
    csp = f"default-src 'none'; img-src 'self'; style-src '{sha(style)}'; base-uri 'none'; form-action 'none'"
    if script is not None:
        csp = f"default-src 'none'; img-src 'self'; script-src '{sha(script)}'; style-src '{sha(style)}'; base-uri 'none'; form-action 'none'"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="{csp}">
<meta name="referrer" content="no-referrer">
<meta name="robots" content="{robots}">
<link rel="icon" type="image/png" href="favicon.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<title>{title}</title>
<style>{style}</style>
</head>
<body>
{body}{'' if script is None else f'<script>{script}</script>'}
</body>
</html>
"""

base = """
  :root { color-scheme: dark; }
  body {
    margin: 0;
    min-height: 100vh;
    display: grid;
    place-items: center;
    padding: 24px;
    box-sizing: border-box;
    background: #09090B;
    color: #F4F4F6;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", system-ui, sans-serif;
    text-align: center;
  }
  main { max-width: 420px; }
  h1 { font-size: 22px; font-weight: 600; margin: 0 0 10px; }
  p { color: #A8A8B0; font-size: 15px; line-height: 1.5; margin: 0; }
  a { color: #D6D6DC; }
"""

callback_script = """
  // SmartThings only redirects to https pages, so this page hands the
  // sign-in result to the Diorama app. It forwards only the OAuth "code",
  // "state" and "error" values, checked against strict patterns, to a
  // fixed app address. Nothing is stored or sent anywhere else.
  (function () {
    var allowed = { code: /^[A-Za-z0-9._~-]{1,512}$/, state: /^[A-Za-z0-9-]{1,128}$/, error: /^[a-z_]{1,64}$/ };
    var incoming = new URLSearchParams(window.location.search);
    var outgoing = new URLSearchParams();
    Object.keys(allowed).forEach(function (name) {
      var value = incoming.get(name);
      if (value !== null && allowed[name].test(value)) outgoing.set(name, value);
    });
    // Keep the one-time code out of the address bar and browser history.
    window.history.replaceState(null, "", window.location.pathname);

    if (!outgoing.has("state") || (!outgoing.has("code") && !outgoing.has("error"))) {
      document.getElementById("title").textContent = "Nothing to do here";
      document.getElementById("message").textContent = "This page finishes signing in to SmartThings from the Diorama app.";
      return;
    }
    var target = "diorama://smartthings/callback?" + outgoing.toString();
    document.getElementById("open").setAttribute("href", target);
    window.location.replace(target);
  })();
"""
callback_body = """<main>
  <h1 id="title">Returning to Diorama…</h1>
  <p id="message">If nothing happens, <a id="open" href="#">tap here to open the app</a>.</p>
</main>
"""
open(f"{out}/smartthings-callback.html", "w").write(page("Returning to Diorama", base, callback_body, callback_script))

index_style = base + """  .icon { width: 112px; height: 112px; border-radius: 25px; margin-bottom: 18px; box-shadow: 0 12px 40px rgba(255, 176, 97, 0.18); }
  small { display: block; margin-top: 18px; color: #6E6E76; font-size: 13px; }
"""
index_body = """<main>
  <img class="icon" src="icon.png" width="112" height="112" alt="">
  <h1>Diorama</h1>
  <p>A miniature of one room on an iPhone: tap the lights, the lamp, the speaker and the air conditioner right where they sit.</p>
  <small>A personal app. Not available on the App Store.</small>
</main>
"""
open(f"{out}/index.html", "w").write(page("Diorama", index_style, index_body))
print("written")
