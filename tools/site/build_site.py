#!/usr/bin/env python3
"""Build the GitHub Pages reading site for LUMINOUS from text/*.md into docs/.

Adapted from the Chinese edition's jing/工具/build_site.py (same layout and behaviour,
English interface). Run from the repository root:

    python3 tools/site/build_site.py

Re-run after any change to text/, then commit docs/.
"""
import hashlib
import html
import re
import shutil
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent.parent
HERE = Path(__file__).resolve().parent
SRC = ROOT / "text"
OUT = ROOT / "docs"
COVER = ROOT / "cover"
FIG = ROOT / "images"
TRAILER = ROOT / "trailer" / "Luminous_trailer.mp4"

# As in the Chinese site (author's decision, 2026-11-09): the stele epigraph at the head of
# each chapter and the end-of-chapter notes stay in the Markdown but are not shown on the web.
SHOW_EPIGRAPH = False
SHOW_CHAPTER_NOTES = False

BOOKS = {"Book One": ("p1", "Vol1", "ALAHA"), "Book Two": ("p2", "Vol2", "MESSIAH"), "Book Three": ("p3", "Vol3", "WIND")}


def parse(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    part = vol = title = None
    body_start = 0
    for i, ln in enumerate(lines):
        if ln.startswith("#"):
            h = ln.lstrip("#").strip()
            if re.match(r"Book (One|Two|Three)\b", h):
                part = h
            elif re.match(r"Volume \w+", h) and ln.startswith("# "):
                vol = h
            elif title is None:
                title = h
            else:
                break
            body_start = i + 1
        elif ln.strip():
            break
    body = "\n".join(lines[body_start:])
    version = ""
    m = re.search(r"\n---\s*\n\s*\*\*Version\*\*(.+)$", body, re.S)
    if m:
        v = re.sub(r"\*\*(.+?)\*\*", r"\1", "Version" + m.group(1)).strip()
        v = re.sub(r"\s*Last modified.*?（美国中部时间）", "", v)
        v = re.sub(r"\s*Status\s+\S+", "", v).strip()
        version = v.replace("　", " ")
        body = body[: m.start()]
    words = len(re.findall(r"[A-Za-z0-9’'\-]+", re.sub(r"!\[[^\]]*\]\([^)]*\)|<[^>]+>", " ", body)))
    return dict(part=part, vol=vol, title=title, body=body, version=version, words=words)


def short(title):
    """'Chapter 12　Wolves' -> 'Wolves' for prev/next links."""
    return re.sub(r"^(Chapter \d+|Appendix \d+)\s*", "", title).strip() or title


ASSET_V = hashlib.md5((HERE / "style.css").read_bytes() + (HERE / "app.js").read_bytes()).hexdigest()[:8]


def page(title, content, extra_head="", body_class=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#f3ecdc">
<title>{html.escape(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=EB+Garamond:ital,wght@0,400;0,600;1,400&family=Noto+Serif+SC:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css?v={ASSET_V}">
<link rel="icon" href="img/icon.png">
{extra_head}
</head>
<body class="{body_class}">
<script>try{{if(localStorage.getItem('lum-dark')==='1')document.body.classList.add('dark');var fs=localStorage.getItem('lum-fs');if(fs)document.documentElement.style.setProperty('--fs',fs+'px');}}catch(e){{}}</script>
{content}
<script src="app.js?v={ASSET_V}"></script>
</body>
</html>
"""


def main():
    chapters = []
    cur_part = cur_vol = None
    for f in sorted(SRC.glob("*.md")):
        d = parse(f)
        if d["part"]:
            cur_part = d["part"]
        if d["vol"]:
            cur_vol = d["vol"]
        num = f.name[:3]
        d["num"], d["slug"] = num, f"{num}.html"
        if num == "000" or num >= "067":
            d["group_part"] = d["group_vol"] = None
        else:
            d["group_part"], d["group_vol"] = cur_part, cur_vol
        chapters.append(d)

    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "img" / "fig").mkdir(parents=True)
    for p in COVER.glob("*.jpg"):
        shutil.copy(p, OUT / "img" / p.name)
    shutil.copy(HERE / "icon.png", OUT / "img" / "icon.png")
    shutil.copy(HERE / "style.css", OUT / "style.css")
    shutil.copy(HERE / "app.js", OUT / "app.js")
    (OUT / ".nojekyll").write_text("")
    for p in FIG.iterdir():
        if p.is_file():
            shutil.copy(p, OUT / "img" / "fig" / p.name)
    if TRAILER.exists():
        shutil.copy(TRAILER, OUT / "trailer.mp4")

    md = markdown.Markdown(extensions=["extra"])
    total = sum(c["words"] for c in chapters)

    for i, c in enumerate(chapters):
        md.reset()
        body_html = md.convert(c["body"])
        if not SHOW_EPIGRAPH:
            body_html = re.sub(r"\A\s*<blockquote>.*?</blockquote>\s*", "", body_html, count=1, flags=re.S)
        if not SHOW_CHAPTER_NOTES and c["num"] <= "067":
            body_html = re.sub(r"<hr\s*/?>\s*<p>(<strong>)?Notes?[:：.].*\Z", "", body_html, flags=re.S)
        body_html = body_html.replace('src="../images/', 'src="img/fig/')
        body_html = re.sub(r'<p><img alt="([^"]*)" src="([^"]+)" ?/?></p>',
                           r'<figure class="fig"><a href="\2" target="_blank"><img src="\2" alt="\1" loading="lazy"></a><figcaption>\1</figcaption></figure>',
                           body_html)
        prev_c = chapters[i - 1] if i > 0 else None
        next_c = chapters[i + 1] if i + 1 < len(chapters) else None
        crumbs = " · ".join(x for x in (c["group_part"], c["group_vol"]) if x).replace("　", " ")
        nav = '<nav class="pn">'
        nav += f'<a href="{prev_c["slug"]}" rel="prev">← {html.escape(short(prev_c["title"]))}</a>' if prev_c else "<span></span>"
        nav += '<a href="index.html#toc" class="up">Contents</a>'
        nav += f'<a href="{next_c["slug"]}" rel="next">{html.escape(short(next_c["title"]))} →</a>' if next_c else "<span></span>"
        nav += "</nav>"
        head_part = f'<div class="part-title">{html.escape(c["part"])}</div>' if c["part"] else ""
        vol_title = f'<div class="vol-title">{html.escape(c["vol"])}</div>' if c["vol"] else ""
        content = f"""
<header class="bar">
  <a href="index.html" class="brand">Luminous</a>
  <span class="crumb">{html.escape(crumbs)}</span>
  <span class="tools"><button id="tts-btn" title="Read aloud" hidden>▶ Listen</button><button data-act="smaller" title="Smaller text">A−</button><button data-act="bigger" title="Larger text">A＋</button><button data-act="dark" title="Light / dark">◐</button></span>
</header>
<main class="reader" data-slug="{c['slug']}" data-title="{html.escape(c['title'])}">
  {head_part}
  {vol_title}
  <h1>{html.escape(c['title'])}</h1>
  <article>
{body_html}
  </article>
  <p class="ver">{html.escape(c['version'])} · about {c['words']:,} words</p>
  {nav}
</main>
<div id="tts-bar" class="tts-bar" hidden>
  <button data-tts="prev" title="Previous paragraph">⏮</button>
  <button data-tts="toggle" class="tts-main" title="Play / pause">❚❚</button>
  <button data-tts="next" title="Next paragraph">⏭</button>
  <button data-tts="stop" title="Stop">■</button>
  <label>Speed<select data-tts="rate"><option value="0.8">0.8×</option><option value="1" selected>1.0×</option><option value="1.2">1.2×</option><option value="1.5">1.5×</option><option value="1.8">1.8×</option></select></label>
  <label class="tts-voice">Voice<select data-tts="voice"></select></label>
  <label class="tts-auto"><input type="checkbox" data-tts="auto" checked>Continue to next chapter</label>
  <span class="tts-tip">While listening, tap any paragraph to read from there</span>
</div>
"""
        extra = (f'<link rel="prev" href="{prev_c["slug"]}">' if prev_c else "") + (f'<link rel="next" href="{next_c["slug"]}">' if next_c else "")
        (OUT / c["slug"]).write_text(page(f"{c['title']} | Luminous".replace("　", " "), content, extra), encoding="utf-8")

    # contents
    toc, apps, tails = [], [], []
    last_part = last_vol = None
    open_vol = False

    def li(c):
        t = c["title"].replace("Epilogue　", "Epilogue · ").replace("　", " ")
        lab = ""
        m = re.match(r"(Chapter \d+)\s+(.*)", t)
        if m:
            lab, t = m.group(1).replace("Chapter ", ""), m.group(2)
        lab_html = f'<b>{lab}</b>' if lab else ""
        return f'<li><a href="{c["slug"]}">{lab_html}<span class="t">{html.escape(t)}</span></a><span class="n">{c["words"]:,}</span></li>'

    for c in chapters:
        if c["group_part"] and c["group_part"] != last_part:
            if open_vol:
                toc.append("</ol></section>")
                open_vol = False
            key = re.match(r"Book \w+", c["group_part"]).group(0)
            pid, _, big = BOOKS[key]
            toc.append(f'<h2 class="toc-part" id="{pid}">{html.escape(key)}<span>{big}</span></h2>')
            last_part = c["group_part"]
        if c["group_vol"] != last_vol:
            if open_vol:
                toc.append("</ol></section>")
                open_vol = False
            if c["group_vol"]:
                toc.append(f'<section class="toc-vol"><h3>{html.escape(c["group_vol"].replace("　", " · "))}</h3><ol>')
                open_vol = True
            last_vol = c["group_vol"]
        if not c["group_vol"] and c["num"] != "000":
            (apps if "089" <= c["num"] <= "098" else tails).append(c)
            continue
        toc.append(li(c) if open_vol else f'<ol class="toc-single">{li(c)}</ol>')
    if open_vol:
        toc.append("</ol></section>")
    toc.append('<div class="toc-gap"></div><div class="toc-extra">')
    toc.append('<section class="toc-vol toc-tail"><h3>Epilogue · Afterword</h3><ol>')
    toc += [li(c) for c in tails]
    toc.append("</ol></section>")
    toc.append('<section class="toc-vol toc-app"><h3>Appendices</h3><ol>')
    for c in apps:
        lab, _, rest = c["title"].partition("　")
        toc.append(f'<li><a href="{c["slug"]}"><b>{html.escape(lab.replace("Appendix ", ""))}</b><span class="t">{html.escape(rest or lab)}</span></a><span class="n">{c["words"]:,}</span></li>')
    toc.append("</ol></section></div>")

    index = f"""
<header class="bar">
  <a href="index.html" class="brand">Luminous</a>
  <span class="crumb">English edition · first draft</span>
  <span class="tools"><a href="gallery.html">Covers</a><a href="https://ny83427.github.io/jing/" title="中文版">中文</a><button data-act="dark" title="Light / dark">◐</button></span>
</header>
<main class="home">
  <section class="hero">
    <img src="img/Main.jpg" alt="Luminous — cover" class="cover-main">
    <div class="hero-text">
      <h1 class="big">Luminous</h1>
      <p class="subtitle">A Novel of the Church of the East in Tang China</p>
      <p class="by">Lao Tie &amp; Claude</p>
      <p class="blurb">In 1623, outside the walls of Xi'an, workmen dig up a Tang stele with rotted hemp cloth still clinging to its face. The Jesuit fathers read the inscription and claim the men on it as their brothers, not knowing that the Western church had long ago branded them heretics. The stone holds some seventeen hundred characters. It cannot hold the people behind them: a monk who scouted the road for Guo Ziyi, a son who translated scripture and raised the stele, and a grandson-in-the-faith who buried it with his own hands.</p>
      <p class="stat">Three books · twelve volumes · sixty-six chapters, with prologue, epilogue, afterword and ten appendices · about {round(total / 1000):,} thousand words · translated from the Chinese 《景》</p>
      <p class="cta"><a href="000.html" class="btn">Begin with the Prologue</a><a href="#" class="btn ghost" id="resume" hidden>Continue reading</a></p>
    </div>
  </section>
  <section class="trailer">
    <video src="trailer.mp4" poster="img/Mockup.jpg" controls preload="none" playsinline></video>
    <p>Trailer · 48 seconds</p>
  </section>
  <section class="vols">
    <a href="#p1"><img src="img/Vol1.jpg" alt="Book One"><span>Book One · Alaha</span></a>
    <a href="#p2"><img src="img/Vol2.jpg" alt="Book Two"><span>Book Two · Messiah</span></a>
    <a href="#p3"><img src="img/Vol3.jpg" alt="Book Three"><span>Book Three · Wind</span></a>
  </section>
  <section class="toc" id="toc">
    <h2 class="toc-head">Contents</h2>
    {''.join(toc)}
  </section>
  <section class="mock">
    <img src="img/Mockup.jpg" alt="The three books">
  </section>
  <footer class="foot">English edition, first draft · <a href="https://github.com/ny83427/luminous">source</a> · <a href="https://ny83427.github.io/jing/">中文版《景》</a></footer>
</main>
"""
    (OUT / "index.html").write_text(page("Luminous | Lao Tie & Claude", index), encoding="utf-8")

    items = [("Main", "Cover"), ("Vol1", "Book One · Alaha"), ("Vol2", "Book Two · Messiah"), ("Vol3", "Book Three · Wind"), ("Mockup", "The three books")]
    g = "".join(f'<figure class="{"wide" if k == "Mockup" else ""}"><a href="img/{k}.jpg"><img src="img/{k}.jpg" alt="{t}" loading="lazy"></a><figcaption>{t}</figcaption></figure>' for k, t in items)
    gallery = f"""
<header class="bar">
  <a href="index.html" class="brand">Luminous</a>
  <span class="crumb">Covers</span>
  <span class="tools"><a href="index.html#toc">Contents</a><button data-act="dark" title="Light / dark">◐</button></span>
</header>
<main class="gallery">{g}</main>
"""
    (OUT / "gallery.html").write_text(page("Covers | Luminous", gallery), encoding="utf-8")
    print(f"built {len(chapters)} pages, {total:,} words")


if __name__ == "__main__":
    main()
