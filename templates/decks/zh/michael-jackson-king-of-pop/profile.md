# 流行音乐之王模板（中文）

## 模板文件

`template.pptx`

## 概述

14 页、16:9 的人物传记 / 致敬套牒，以迈克尔·杰克逊为例。视觉体系是深色聚光灯 + 金色的「King of Pop」气质：整屏封面、编号内容页、生平时间线、数据卡、专辑柱状图、荣誉墙、光与影、谢幕与遗产。由中英对照原版拆分而来的纯中文版（英文版见 `en/michael-jackson-king-of-pop`）。

当用户想做一份有仪式感的中文人物 deck（名人传记、致敬、品牌 / 人物档案、文化回顾）时，用它作为起点。

## 结构

- 页面尺寸 10.00 x 5.62 英寸（16:9）。页数 14。版式 11 套。含 1 个专辑柱状图。
- 字体：正文 PingFang SC；运行页眉用 Courier New（等宽）；数字与装饰用 Arial / Arial Black。

## 适合

- 名人传记、致敬片、人物 / 品牌档案。
- 文化回顾、生平时间线、一个人物的「高光与争议」。

## 复用规则

- 保留节奏：整屏封面 → 编号内容页 → 时间线 → 数据 → 荣誉 → 光与影 → 谢幕与遗产。
- 复用深色 + 金色的聚光灯视觉，替换成用户的人物、数据与图片。
- CJK 字体沿用 PingFang SC，避免中文豆腐块。

## Agent 提示

1. 构建前先跑 `scripts/inspect_template.py templates/decks/zh/michael-jackson-king-of-pop/template.pptx`。
2. 用 `deckkit.open_template()` 基于本套牒构建；源构建脚本在 `_sources/michael-jackson-king-of-pop/`（含中英对照原版与 `build_mj_mono.py`）。
3. 把模板当作视觉系统，而非内容来源。
