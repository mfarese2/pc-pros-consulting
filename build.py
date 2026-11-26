"""Build the GitHub Pages version of the site.

index.html is the source page (also published as the claude.ai preview, which
adds its own <html>/<head> wrapper). This script wraps it into a complete HTML
document and writes it to docs/index.html, which GitHub Pages serves.

Run:  python3 build.py
"""
from pathlib import Path

ROOT = Path(__file__).parent
src = (ROOT / "index.html").read_text(encoding="utf-8")

split = src.index("</style>") + len("</style>")
head, body = src[:split], src[split:].lstrip("\n")

# The claude.ai preview supplies these base rules; a normal host does not.
base = """<style>
:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
body{margin:0}
img{max-width:100%}
[hidden]{display:none!important}
</style>"""

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{base}
{head}
</head>
<body>
{body}</body>
</html>
"""

out = ROOT / "docs"
out.mkdir(exist_ok=True)
(out / "index.html").write_text(page, encoding="utf-8")
(out / ".nojekyll").write_text("", encoding="utf-8")
print("Wrote", out / "index.html")
