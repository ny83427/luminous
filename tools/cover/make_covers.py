"""Generate the English covers of LUMINOUS from the Chinese cover template.

Usage (from this folder):
    npm i @fontsource/cinzel @fontsource/cormorant-garamond   # once
    python3 make_covers.py            # writes ../../cover/source/*.png and ../../cover/*.jpg

The artwork is taken unchanged from the Chinese edition's cover designs
(jing/工具/封面设计): final_main.html for the main cover, and final_p1/p2/p3.html for the
three book covers (dusk and caravan / night sky and star road / red sun and palace roofs).
Only the lettering differs: the Chinese vertical label 第一部 阿罗诃 etc. becomes an English
label in the same top-left position and colour, and LUMINOUS and the byline go at the foot.
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
    "Vol1": ("final_p1.html", "BOOK ONE", "ALAHA", "755 – 765"),
    "Vol2": ("final_p2.html", "BOOK TWO", "MESSIAH", "765 – 818"),
    "Vol3": ("final_p3.html", "BOOK THREE", "WIND", "818 – 850"),
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


VOL_CSS = """
<link rel="stylesheet" href="node_modules/@fontsource/cinzel/500.css">
<link rel="stylesheet" href="node_modules/@fontsource/cinzel/700.css">
<link rel="stylesheet" href="node_modules/@fontsource/cormorant-garamond/500-italic.css">
<style>
.en-part{position:absolute;left:170px;top:190px;font-family:"Cinzel";color:var(--c);text-shadow:0 2px 10px rgba(0,0,0,.35)}
.en-part .k{display:block;font-size:40px;font-weight:500;letter-spacing:14px}
.en-part .n{display:block;font-size:86px;font-weight:700;letter-spacing:14px;margin-top:6px;line-height:1}
.en-part .r{display:block;width:120px;height:2px;background:var(--c);opacity:.7;margin:22px 0 16px}
.en-part .y{display:block;font-size:34px;font-weight:500;letter-spacing:8px;opacity:.85}
.en-foot{position:absolute;left:0;right:0;bottom:140px;text-align:center;color:var(--a);text-shadow:0 2px 8px rgba(0,0,0,.35)}
.en-foot .t{display:block;font-family:"Cinzel";font-weight:700;font-size:64px;letter-spacing:22px;padding-left:22px}
.en-foot .s{display:block;font-family:"Cormorant Garamond";font-style:italic;font-weight:500;font-size:38px;margin-top:6px}
.en-foot .b{display:block;font-family:"Cinzel";font-weight:500;font-size:34px;letter-spacing:12px;padding-left:12px;margin-top:14px;opacity:.9}
</style>
"""


def build_vol(name, spec):
    tpl, k, n, y = spec
    src = (HERE / tpl).read_text(encoding="utf-8")
    part_c = re.search(r'\.part\{[^}]*?color:(#[0-9a-fA-F]{6})', src).group(1)
    auth_c = re.search(r'\.author2\{[^}]*?color:(#[0-9a-fA-F]{6})', src).group(1)
    src = re.sub(r'<div class="author2">.*?</div><div class="part">.*?</div>', "", src, flags=re.S)
    src = src.replace("</head>", VOL_CSS + "</head>", 1)
    text = (f'<div class="en-part" style="--c:{part_c}"><span class="k">{k}</span><span class="n">{n}</span>'
            f'<span class="r"></span><span class="y">{y}</span></div>'
            f'<div class="en-foot" style="--a:{auth_c}"><span class="t">LUMINOUS</span>'
            f'<span class="s">{SUBTITLE}</span><span class="b">{BYLINE}</span></div>')
    src = re.sub(r'(</div>\s*</body>)', text + r'\1', src, count=1)
    out = HERE / f"en_{name}.html"
    out.write_text(src, encoding="utf-8")
    return out


def build(name, book):
    if book is not None:
        return build_vol(name, book)
    src = (HERE / "final_main.html").read_text(encoding="utf-8")
    src = re.sub(r'<style>\.author2.*?</style><div class="author2">.*?</div>', "", src, flags=re.S)
    src = src.replace("</head>", CSS + "</head>", 1)
    text = (f'<div class="en-title">LUMINOUS</div><div class="en-rule"></div>'
            f'<div class="en-sub">{SUBTITLE}</div><div class="en-by">{BYLINE}</div>')
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
        # three-book mockup (after the Chinese edition's 封面/Mockup.jpg); uses the Vol covers just written
        mp = b.new_page(viewport={"width": 1600, "height": 1000}, device_scale_factor=2)
        mp.goto((HERE / "mockup.html").as_uri())
        mp.wait_for_timeout(800)
        png = ROOT / "cover" / "source" / "Mockup.png"
        mp.screenshot(path=str(png))
        Image.open(png).convert("RGB").save(ROOT / "cover" / "Mockup.jpg", quality=88)
        print("wrote Mockup")
        b.close()


if __name__ == "__main__":
    main()
