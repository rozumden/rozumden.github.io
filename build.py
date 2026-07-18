#!/usr/bin/env python3
"""Static site generator for rozumden.github.io.

Reads all page content from ``site.yml`` and renders ``index.html`` from the
template below. The rendered page is intentionally identical in look to the
hand-written original; the point is that content now lives in one structured
file instead of ~1100 lines of copy-pasted HTML.

Usage:
    python3 build.py            # regenerate index.html
    python3 build.py --check    # verify referenced media exist, don't write

Adding a publication is just a new entry under ``publications:`` in site.yml
(see the README). Hover animations are handled by CSS (.one:hover .two), so
there is no per-paper JavaScript to copy anymore.
"""

from __future__ import annotations

import html
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit(
        "This script needs PyYAML. Install it with:\n"
        "    python3 -m pip install pyyaml"
    )

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "site.yml"
OUT_FILE = ROOT / "index.html"
IMAGES_DIR = ROOT / "images"

VIDEO_EXTS = {".mp4", ".m4v", ".mov", ".webm"}


# --------------------------------------------------------------------------- #
# Rendering helpers
# --------------------------------------------------------------------------- #
def image_cell(pub: dict, warnings: list[str]) -> str:
    """Render the left-hand thumbnail cell for a publication.

    A publication may have just a static ``image`` or, additionally, a
    ``hover`` media file (video or gif/image) shown on mouse-over. The
    fade-in/out is pure CSS via the .one/.two classes.
    """
    image = pub["image"]
    hover = pub.get("hover")
    _check_media(image, warnings)

    if not hover:
        return (
            '        <div>\n'
            f"          <img src='images/{image}' width=\"160\">\n"
            '        </div>'
        )

    _check_media(hover, warnings)
    ext = Path(hover).suffix.lower()
    if ext in VIDEO_EXTS:
        overlay = (
            '<video width=100% muted autoplay loop>\n'
            f'          <source src="images/{hover}" type="video/mp4">\n'
            '          Your browser does not support the video tag.\n'
            '          </video>'
        )
    else:
        overlay = f'<img width=100% src="images/{hover}">'

    return (
        '        <div class="one">\n'
        f'          <div class="two">{overlay}</div>\n'
        f"          <img src='images/{image}' width=\"160\">\n"
        '        </div>'
    )


def links_line(links: list[dict]) -> str:
    """Render the ' / '-separated list of links under a publication."""
    parts = [f'<a href="{l["href"]}">{l["text"]}</a>' for l in links]
    return "\n        ".join(
        part + (" /" if i < len(parts) - 1 else "") for i, part in enumerate(parts)
    )


def render_publication(pub: dict, warnings: list[str]) -> str:
    bg = ' bgcolor="#ffffd0"' if pub.get("highlight") else ""
    award = ""
    if pub.get("award"):
        award = f' &nbsp <font color="red"><strong>{pub["award"]}</strong></font>'

    return f"""    <tr{bg}>
      <td style="padding:20px;width:25%;vertical-align:middle">
{image_cell(pub, warnings)}
      </td>
      <td style="padding:20px;width:75%;vertical-align:middle">
        <a href="{pub['url']}">
          <span class="papertitle">{pub['title']}</span>
        </a>
        <br>
        {pub['authors']}
        <br>
        <em>{pub['venue']}</em>, {pub['year']}{award}
        <br>
        {links_line(pub['links'])}
        <p></p>
        <p>{pub['abstract']}</p>
      </td>
    </tr>"""


def render_news(news: list[dict]) -> str:
    items = "\n".join(
        f"                  <li><strong>{n['date']}</strong>: {n['text']}</li>"
        for n in news
    )
    return f"""            <tr>
              <td style="padding:20px;width:100%;vertical-align:middle">
                <h2>News</h2>
                <ul>
{items}
                </ul>
              </td>
            </tr>
"""


def render_list_section(title: str, items: list[str]) -> str:
    lis = "\n".join(f"                  <li>{item}</li>" for item in items)
    return f"""            <tr>
              <td style="padding:20px;width:100%;vertical-align:middle">
                <h2>{title}</h2>
                <ul>
{lis}
                </ul>
              </td>
            </tr>"""


def _check_media(name: str, warnings: list[str]) -> None:
    if not (IMAGES_DIR / name).exists():
        warnings.append(f"missing media: images/{name}")


# --------------------------------------------------------------------------- #
# Page template
# --------------------------------------------------------------------------- #
def render_page(data: dict, warnings: list[str]) -> str:
    site = data["site"]
    bio = "\n".join(f"                <p>{p}</p>" for p in data["bio"])
    links = data["header_links"]
    links_html = " &nbsp;/&nbsp;\n                  ".join(
        f'<a href="{l["href"]}">{l["text"]}</a>' for l in links
    )

    news_block = ""
    if data.get("news"):
        news_html = render_news(data["news"])
        if not data.get("show_news", False):
            news_block = f"             <!--\n{news_html}            -->\n"
        else:
            news_block = news_html

    pubs = "\n\n".join(render_publication(p, warnings) for p in data["publications"])

    supervising = render_list_section("Supervising", data["supervising"])
    reviewing = render_list_section("Reviewing", data["reviewing"])
    teaching = data["teaching"]

    return f"""<!DOCTYPE HTML>
<html lang="en">
  <head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={site['ga_id']}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());

      gtag('config', '{site['ga_id']}');
    </script>

    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">

    <title>{site['title']}</title>

    <meta name="author" content="{site['author']}">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="shortcut icon" href="images/favicon/favicon.ico" type="image/x-icon">
    <link rel="stylesheet" type="text/css" href="stylesheet.css">

    <!-- This file is GENERATED by build.py from site.yml. Do not edit by hand. -->
  </head>

  <body>
    <table style="width:100%;max-width:800px;border:0px;border-spacing:0px;border-collapse:separate;margin-right:auto;margin-left:auto;"><tbody>
      <tr style="padding:0px">
        <td style="padding:0px">
          <table style="width:100%;border:0px;border-spacing:0px;border-collapse:separate;margin-right:auto;margin-left:auto;"><tbody>
            <tr style="padding:0px">
              <td style="padding:2.5%;width:63%;vertical-align:middle">
                <p class="name" style="text-align: center;">
                  {site['name']}
                </p>
                <p><small>{site['name_note']}</small></p>
{bio}
                <p style="text-align:center">
                  {links_html}
                </p>
              </td>
              <td style="padding:2.5%;width:40%;max-width:40%">
                <a href="images/{site['photo']}"><img style="width:100%;max-width:100%;object-fit: cover; border-radius: 50%;" alt="profile photo" src="images/{site['photo']}" class="hoverZoomLink"></a>
              </td>
            </tr>
          </tbody></table>
          <table style="width:100%;border:0px;border-spacing:0px;border-collapse:separate;margin-right:auto;margin-left:auto;"><tbody>
{news_block}
            <tr>
              <td style="padding:20px;width:100%;vertical-align:middle">
                <h2>Research</h2>
                <p>
                </p>
              </td>
            </tr>

          </tbody></table>
          <table style="width:100%;border:0px;border-spacing:0px;border-collapse:separate;margin-right:auto;margin-left:auto;"><tbody>

{pubs}

    <!-- FINISH PUBLICATIONS -->
          </tbody></table>


          <table style="width:100%;border:0px;border-spacing:0px;border-collapse:separate;margin-right:auto;margin-left:auto;"><tbody>
{supervising}

{reviewing}

          </tbody></table>
          <table style="width:100%;border:0px;border-spacing:0px;border-collapse:separate;margin-right:auto;margin-left:auto;"><tbody>


          <table width="100%" align="center" border="0" cellspacing="0" cellpadding="20"><tbody>
            <tr>
              <td>
                <h2>Teaching</h2>
              </td>
            </tr>
          </tbody></table>
          <table width="100%" align="center" border="0" cellpadding="20"><tbody>

            <tr>
              <td style="padding:20px;width:25%;vertical-align:middle"><img src="images/{teaching['image']}" width="160"></td>
              <td width="75%" valign="center">
                {teaching['html']}
              </td>
            </tr>

          </tbody></table>
          <table style="width:100%;border:0px;border-spacing:0px;border-collapse:separate;margin-right:auto;margin-left:auto;"><tbody>
            <tr>
              <td style="padding:0px">
                <br>
                <p style="text-align:right;font-size:small;">
                  Adapted from <a href="https://github.com/jonbarron/jonbarron_website">here</a>.
                </p>
              </td>
            </tr>
          </tbody></table>

        </td>
      </tr>
    </table>
  </body>
</html>
"""


def main() -> int:
    check_only = "--check" in sys.argv
    data = yaml.safe_load(DATA_FILE.read_text())
    warnings: list[str] = []
    page = render_page(data, warnings)

    for w in dict.fromkeys(warnings):  # dedupe, keep order
        print(f"  warning: {w}", file=sys.stderr)

    n = len(data["publications"])
    if check_only:
        print(f"Checked {n} publications. {len(set(warnings))} warning(s).")
        return 1 if warnings else 0

    OUT_FILE.write_text(page)
    print(f"Wrote {OUT_FILE.name} ({n} publications, {len(set(warnings))} warning(s)).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
