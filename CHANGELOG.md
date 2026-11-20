# CHANGELOG

按时间倒序排列。每条记录写明日期、版本、涉及章节和改动内容。英译章节末尾注明据中文本哪一版译出。

## 2026-11-19　网页不显示仓库链接

- 与中文版网站一致：首页页脚去掉 GitHub 仓库链接。章节页只显示版本号和字数，不显示最后修改时间（此前已如此，核对无误）。

## 2026-11-19　合集效果图改为立体

- 作者反馈英文版合集图不像立体的书。`tools/cover/mockup.html` 改用 CSS 3D：每本书是一个有厚度的盒子（封面、书脊、切口、书顶），整体侧转 34°，书脊朝向观者，每本各自取景，与中文版合集图的立体效果一致。
- 重新生成 `cover/Mockup.jpg`，并重新嵌入预告片作缩略图；网站随之更新。

## 2026-11-19　预告片放慢

- 作者反馈每个画面停留太短，字幕来不及看清。各场景时长由 4.0/4.2/4.0/4.0/4.2/3.8/3.4/5.0 秒延长为 6.0/5.8/6.0/6.0/6.4/5.6/5.2/7.0 秒，全片由 32.6 秒变为 48 秒。
- 场景之间的淡入淡出放慢（0.5/0.45 秒 → 0.9/0.8 秒，片尾淡出 0.9 → 1.6 秒）；字幕淡入不短于 1 秒，并在场景结束前约 0.9 秒才开始淡出。
- 配乐按新的场景起点整体对齐（`sound.py` 中的 `OLD_T`/`NEW_T` 映射），音型与配器不变。
- 修正：含“·”、引号或省略号的英文字幕原先按中文字距排，词间空得过大，已改按英文排。
- 合集图仍嵌为视频缩略图；网站首页预告片时长说明改为 48 秒。

## 2026-11-19　三部合集效果图；预告片缩略图

- 新增 `cover/Mockup.jpg`（3200×2000）与 `cover/source/Mockup.png`：仿中文版 `封面/Mockup.jpg`，暗赭底上并排三本书，各带书脊（LUMINOUS / I · ALAHA 等 / LAO TIE & CLAUDE），封面用新的三部封面。设计源文件 `tools/cover/mockup.html`，由 `make_covers.py` 一并生成。
- 网站：首页目录下方加合集图（同中文版）；封面页加合集图；首页预告片的封面（poster）改为合集图。
- 预告片：把合集图作为封面图（attached_pic）嵌入 `trailer/Luminous_trailer.mp4`，在文件管理器和播放器里显示为缩略图；视频内容不变。

## 2026-11-19　三部封面改按中文版各自的设计

- 原先英文版三部封面都套用了主封面的画面（落日、驼队），只换了文字。现改为分别以中文版 `final_p1.html`（暮色落日与驼队）、`final_p2.html`（深蓝夜空与星路）、`final_p3.html`（朱红大日、十字与宫殿屋脊）为底图，画面与中文版完全一致。
- 文字处理：中文竖排的“第一部 阿罗诃”等改为同一位置（左上）的英文部名（BOOK ONE / ALAHA / 755 – 765），颜色沿用中文版各部的部名颜色；底部为 LUMINOUS、副标题与署名，颜色沿用中文版署名颜色。
- 更新 `tools/cover/make_covers.py`、`cover/Vol1–3.jpg` 与 `cover/source/Vol1–3.png`，网站 `docs/` 重新生成。

## 2026-11-19　全书译完；英文预告片；阅读网站

- 正文：第二十一章至第六十六章 `021`–`066`（第五卷至第十二卷）及尾声 `067-Epilogue-The-Steppe.md` 译出，均为 v0.1，章末注明据中文哪一版。一卷一次提交。
- 第五十七、五十九章英文章名改回与 `working/toc.md` 一致（*As Far as the Edict Reaches*、*Packing*）。
- 早先章节的小修：第十四、十五章 “Master Yisi” 统一为 “Master Yi”；第十四章版本行格式统一；第十六章 “Dragon Queen” 改为 “Purple-Robed Dragon King”；第五十四章一处笔误。
- `working/names.md` 新增第七节（第二十一章以后的人名、地名、称谓）；`working/translation-notes.md` 新增第七节，列出中文原文里请作者核对的几处。
- 预告片：`tools/trailer/trailer.py`、`sound.py` 由中文版改写，画面与配乐不变，字幕改英文（Cardo 字体），碑面仍刻中文碑文；输出 `trailer/Luminous_trailer.mp4`（32.6 秒，约 28 MB）。
- 阅读网站：`tools/site/build_site.py`、`style.css`、`app.js` 由中文版改写——同样的版式、目录、日夜间、字号、朗读（改用英文语音）、已读标记与续读；字体 EB Garamond / Cormorant Garamond。生成到 `docs/`，含预告片与封面页。与中文版一样，网页上不显示各章碑文题记与章末附注。

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
