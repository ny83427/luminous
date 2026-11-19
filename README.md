# Luminous

*A Novel of the Church of the East in Tang China* — the English edition of 景 (https://github.com/ny83427/jing), by Lao Tie and Claude.

景教在唐朝的沉浮。本仓库是长篇历史小说《景》的英译版，书名 *Luminous*。中文原版见 `ny83427/jing`。

## 目录结构（与 jing 一一对应）

| Luminous | jing | 内容 |
|---|---|---|
| `text/` | `正文/` | 英译正文，一章一个文件。文件名格式「三位序号-Vol卷号-Ch章号-英文章名.md」，序号与中文版相同：序章 000，尾声 067，附录 089–098，后记 099。 |
| `working/` | `工作文件/` | 翻译工作文件：`toc.md`（书名、三部、卷名、章名中英对照）、`names.md`（人名地名术语英译表）、`translation-notes.md`（译法通则与待作者决定的问题）。 |
| `references/` | `参考资料/` | 参考资料。中文原始资料留在 jing，不重复存放；英译附录一至五已涵盖其内容。 |
| `cover/` | `封面/` | 英文版封面：总封面 `Main.jpg`，三部封面 `Vol1–3.jpg`；`cover/source/` 是 PNG 原图（1680×2380）。 |
| `tools/cover/` | `工具/封面设计/` | 封面生成脚本 `make_covers.py`，在中文版 `final_main.html` 的画面上换成英文字。 |
| `images/` | `图片/` | 正文插图（与中文版相同）。 |
| `docs/` | `docs/` | 预留给阅读网站（尚未生成）。 |
| `CHANGELOG.md` | `修改记录.md` | 每一版改了什么，按时间倒序。 |

## 全书结构

LUMINOUS — three books, twelve volumes, sixty-six chapters.

- Prologue: Unearthed
- **Book One: ALAHA** (the book of Yisi, 755–765): Vol. 1 Guo Ziyi · Vol. 2 Li Guangbi · Vol. 3 The Pamir Road · Vol. 4 Xiangji Temple · Vol. 5 Chang'an · Vol. 6 The Shuofang Army
- **Book Two: MESSIAH** (the book of Jingjing, 765–818): Vol. 7 A-Lian · Vol. 8 The Daqin Monastery · Vol. 9 The Translation Hall
- **Book Three: WIND** (the book of the believers, 818–850): Vol. 10 Huichang · Vol. 11 Jade Gate · Vol. 12 Baghdad
- Epilogue: The Steppe
- Appendices 1–10 · Afterword

逐章英文章名见 `working/toc.md`。

## 翻译进度

- 已译（英译初稿/样稿 v0.1）：序章、第 1–20 章、附录一至十、后记。
- 待译：第 21–66 章、尾声。

## 版本约定

与中文版相同：

- 每章文末一行标注版本号、最后修改时间（美国中部时间）和状态；英译版另注明所据的中文版本，如 `v0.1 (translated from Chinese v0.5)`。
- 中文版某章改版后，英译跟着重译或修订，版本号加 0.1。
- 每次提交都在提交说明和 `CHANGELOG.md` 里写明改了哪些章、改了什么、为什么改。
