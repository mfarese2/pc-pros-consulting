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

# The hosted page gets a fuller search title; the preview keeps the short name.
SITE = "https://pcprosconsulting.com/"
page = page.replace(
    "<title>PC Pros Consulting</title>",
    "<title>PC Pros Consulting | IT Consulting for New and Growing Businesses in Massachusetts</title>",
    1,
)

out = ROOT / "docs"
out.mkdir(exist_ok=True)
(out / "index.html").write_text(page, encoding="utf-8")
(out / ".nojekyll").write_text("", encoding="utf-8")
(out / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n", encoding="utf-8")
(out / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    f"  <url><loc>{SITE}</loc></url>\n"
    "</urlset>\n",
    encoding="utf-8",
)
# docs/CNAME holds the custom domain GitHub Pages serves; build.py leaves it alone.
print("Wrote", out / "index.html", "plus robots.txt and sitemap.xml")
