# CHANGELOG

按时间倒序排列。每条记录写明日期、版本、涉及章节和改动内容。英译章节末尾注明据中文本哪一版译出。

## 2026-11-19　英译起步：目录、封面、人名表与第一批样稿

据中文本《景》（ny83427/jing）当前版本译出。目录结构与中文本一致。

- `README.md`：说明英文版目录与中文版的对应关系、全书结构、翻译进度与版本约定。
- `working/toc.md`：书名 *Luminous*、副标题（含备选）、三部（*Alaha* / *Messiah* / *Wind*）、十二卷、六十六章及尾声、附录十篇、后记的中英对照，以及文件命名规则。
- `working/names.md`：人名、地名、官职、教内称谓、时间表达的英译表；★ 号五处待作者拍板。
- `working/translation-notes.md`：译法通则（KJV 底本、景教译名、双关处理、军中称谓）与待定事项。
- 封面：`tools/cover/make_covers.py` 由中文本封面模板生成英文版，`cover/Main.jpg` 与 `cover/Vol1.jpg`–`Vol3.jpg`（1680×2380），源图在 `cover/source/`。字体用 Cinzel、Cormorant Garamond、Noto Sans Syriac（npm @fontsource）。
- `images/`：复制中文本序章所用景教碑图片两张。
- 正文（`text/`），均为 v0.1：
  - 序章 `000-Prologue-Unearthed.md`（据中文 v0.2）。
  - 第一至第二十章 `001`–`020`（第一卷至第四卷），英译样稿。
  - 附录一至十 `089`–`098`；附录二碑文对照沿用 `duizhao` 两栏表格，为全书碑文题记的英译底本；附录九改为与英文通行圣经译名（KJV 及汉语文理、委办本）对照。
  - 后记 `099-Afterword.md`（据中文 v0.5）。
- 已知待核：附录三与附录九的 Deeg 书名不一致，照中文原样保留，见 `working/translation-notes.md`。
