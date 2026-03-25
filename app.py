"""
Minimal single-file Flask app for Cloudera AI (CDSW) Applications.
HTML is embedded below; no templates directory required.

Port resolution (first match wins):
  1. CDSW_APP_PORT — set by Cloudera when the Application runs
  2. DEFAULT_CDSW_APP_PORT — optional env var for local/dev fallback
  3. 8090 — built-in default if neither is set
"""

import os

from flask import Flask, Response

# Built-in default when neither CDSW_APP_PORT nor DEFAULT_CDSW_APP_PORT is set
_BUILTIN_DEFAULT_PORT = 8090

# Override via DEFAULT_CDSW_APP_PORT env (e.g. local dev) or edit _BUILTIN_DEFAULT_PORT above
DEFAULT_CDSW_APP_PORT = int(
    os.environ.get("DEFAULT_CDSW_APP_PORT", str(_BUILTIN_DEFAULT_PORT))
)


def _listen_port() -> int:
    raw = os.environ.get("CDSW_APP_PORT")
    if raw is not None and raw.strip() != "":
        return int(raw)
    return DEFAULT_CDSW_APP_PORT


INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Singleton Flask</title>
  <style>
    :root { font-family: system-ui, sans-serif; line-height: 1.5; }
    body { margin: 2rem; max-width: 40rem; }
    code { background: #f4f4f5; padding: 0.15em 0.4em; border-radius: 4px; }
  </style>
</head>
<body>
  <h1>Singleton Flask</h1>
  <p>All logic lives in <code>app.py</code>. Port comes from
    <code>CDSW_APP_PORT</code> when set; otherwise
    <code>DEFAULT_CDSW_APP_PORT</code> or <code>8090</code>.</p>
</body>
</html>
"""

app = Flask(__name__)


@app.get("/")
def index() -> Response:
    return Response(INDEX_HTML, mimetype="text/html; charset=utf-8")


@app.get("/health")
def health() -> Response:
    return Response("ok", mimetype="text/plain; charset=utf-8")


if __name__ == "__main__":
    port = _listen_port()
    app.run(host="0.0.0.0", port=port, debug=False)
