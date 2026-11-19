"""Generate the English covers of LUMINOUS from the Chinese cover template.

Usage (from this folder):
    npm i @fontsource/cinzel @fontsource/cormorant-garamond   # once
    python3 make_covers.py            # writes ../../cover/source/*.png and ../../cover/*.jpg

The artwork (dusk sky, sun, lotus cross, the calligraphic 景, the caravan) is taken
unchanged from final_main.html, the Chinese edition's cover; only the lettering differs.
"""
import pathlib, re
from playwright.sync_api import sync_playwright
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SUBTITLE = "A Novel of the Church of the East in Tang China"
BYLINE = "LAO TIE &amp; CLAUDE"

COVERS = {
    "Main": None,
    "Vol1": ("BOOK ONE", "ALAHA", "755 – 765"),
    "Vol2": ("BOOK TWO", "MESSIAH", "765 – 818"),
    "Vol3": ("BOOK THREE", "WIND", "818 – 850"),
}

CSS = """
<link rel="stylesheet" href="node_modules/@fontsource/cinzel/500.css">
<link rel="stylesheet" href="node_modules/@fontsource/cinzel/700.css">
<link rel="stylesheet" href="node_modules/@fontsource/cormorant-garamond/500-italic.css">
<style>
.en-title{position:absolute;left:0;right:0;top:170px;text-align:center;font-family:"Cinzel";font-weight:700;
 font-size:184px;letter-spacing:34px;padding-left:34px;color:#f7dcae;text-shadow:0 3px 14px rgba(0,0,0,.45)}
.en-rule{position:absolute;left:560px;right:560px;top:420px;height:2px;background:linear-gradient(90deg,rgba(247,220,174,0),#e8c99a,rgba(247,220,174,0))}
.en-sub{position:absolute;left:0;right:0;top:446px;text-align:center;font-family:"Cormorant Garamond";font-style:italic;
 font-weight:500;font-size:58px;letter-spacing:1px;color:#efd2a2;text-shadow:0 2px 8px rgba(0,0,0,.4)}
.en-book{position:absolute;left:0;right:0;top:396px;text-align:center;font-family:"Cinzel";font-weight:500;color:#f7dcae;
 text-shadow:0 2px 10px rgba(0,0,0,.4)}
.en-book .k{display:block;font-size:44px;letter-spacing:18px;padding-left:18px}
.en-book .n{display:block;font-size:104px;font-weight:700;letter-spacing:26px;padding-left:26px;margin-top:8px}
.en-book .y{display:block;font-size:38px;letter-spacing:10px;margin-top:6px;opacity:.85}
.en-vol .en-title{top:96px;font-size:128px;letter-spacing:26px;padding-left:26px}
.en-vol .en-rule{top:282px}
.en-vol .en-book{top:312px}
.en-vol .en-sub{top:2096px;font-size:44px}
.en-by{position:absolute;left:0;right:0;bottom:170px;text-align:center;font-family:"Cinzel";font-weight:500;font-size:46px;
 letter-spacing:16px;padding-left:16px;color:#e8c99a;text-shadow:0 2px 8px rgba(0,0,0,.35)}
.en-vol .en-by{bottom:150px}
</style>
"""


def build(name, book):
    src = (HERE / "final_main.html").read_text(encoding="utf-8")
    # drop the Chinese byline and its style block
    src = re.sub(r'<style>\.author2.*?</style><div class="author2">.*?</div>', "", src, flags=re.S)
    src = src.replace("</head>", CSS + "</head>", 1)
    if book is None:
        text = (f'<div class="en-title">LUMINOUS</div><div class="en-rule"></div>'
                f'<div class="en-sub">{SUBTITLE}</div><div class="en-by">{BYLINE}</div>')
        src = src.replace('<div class="page">', '<div class="page">', 1)
    else:
        k, n, y = book
        text = (f'<div class="en-title">LUMINOUS</div><div class="en-rule"></div>'
                f'<div class="en-book"><span class="k">{k}</span><span class="n">{n}</span><span class="y">{y}</span></div>'
                f'<div class="en-sub">{SUBTITLE}</div><div class="en-by">{BYLINE}</div>')
        src = src.replace('<div class="page">', '<div class="page en-vol">', 1)
    src = src.replace("</div></body>", text + "</div></body>")
    out = HERE / f"en_{name}.html"
    out.write_text(src, encoding="utf-8")
    return out


def main():
    (ROOT / "cover" / "source").mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1680, "height": 2380})
        for name, book in COVERS.items():
            html = build(name, book)
            pg.goto(html.as_uri())
            pg.wait_for_timeout(600)
            png = ROOT / "cover" / "source" / f"{name}.png"
            pg.screenshot(path=str(png))
            im = Image.open(png).convert("RGB")
            im.save(ROOT / "cover" / f"{name}.jpg", quality=88)
            print("wrote", name)
        b.close()


if __name__ == "__main__":
    main()
