# 来源、匹配与使用说明

## 书目快照

- 来源：[HackerBooks](https://hackerbooks.org/#/)，作者 roansh / Rohit Shinde。
- [原站 About](https://hackerbooks.org/#/about) · [HN 发布说明](https://news.ycombinator.com/item?id=50326821)。
- 快照日期：2026-11-02；书目 15,766 个；原站主题 32 个。
- 原站汇总 Hacker News 评论，并使用 Open Library 进行作品匹配与元数据补全。本项目不是独立人工精选的 15,766 本推荐书单。
- 保留作品 ID、原始条目标题、作者、出版年份、主题和热度字段；不保证原站的匹配、分类和版本信息均正确。
- `u` 是提及该书的不同评论者人数；`ru` 是原站识别为推荐的不同评论者人数。两者不等于评分，且本项目未重审评论立场。
- 本项目对原站 32 个主题增加 9 个浏览大类，单书允许多类；不按分类重复计算总条目数量。

## 中文书名

- 先保留常用中文名和已匹配的中文条目名，再按作品 ID 查询 Open Library 的中文版本。查询共覆盖 14,999 个条目，获得 142 个含中文标题的版本候选；明显乱码、英文影印版标签等不直接采用。
- 目前 common 563 条、wiki 191 条、edition 140 条、edited 389 条、machine 14457 条、retained 26 条。
- `edition` 表示同作品中文版本的书目名称，`cn_source` 保留版本链接；仍需留意来源元数据误配及地区版本差异。
- `edited` 是结合内容与术语校订的参考译名，不代表正式出版名。具体对照见 `data/title-edits.txt`，改动记录见 `data/title-review-report.json`。
- 无法核实的名字保留原名以便辨认，详情中说明参考译名；不再提供按译名状态筛选，也不在书卡显示状态标签。
- 出版资料例证：[力量训练基础](https://search.worldcat.org/title/1020336574)、[JavaScript语言精粹](https://phei.com.cn/module/goods/wssd_content.jsp?bookid=33817)、[JavaScript权威指南](https://www.oreilly.com.cn/index.php?func=book&isbn=978-7-111-67722-2)。[Crafting Interpreters 官方内容](https://craftinginterpreters.com/) 用于确认解释器语境；“动手实现解释器”是本页参考译名。
- 数据中的 `t` 是源站条目标题，未声称一定是首次原版书名；`a` 是源站作者列表。原始书名和作品 ID 保持不变。
- Accelerando 原站年份 1900 与出版记录不符，依据[出版社页面](https://www.penguinrandomhouse.com/books/294259/accelerando-by-charles-stross/)修正为 2005，原值保存在 `source_y`。

## 封面

- 原站封面编号：13,983 个条目。
- 对 1,783 个原站缺失封面编号的条目，以 Open Library 作品 ID 作精确检索，补充 473 个关联版本的封面编号。
- 合计 14,456 个条目有关联封面编号，其余 1,310 个暂无编号。关联编号不保证外部图片服务始终可用。
- 首选原站封面服务 `covers.hackerbooks.org`；图片加载失败时，尝试 [Open Library Covers API](https://openlibrary.org/dev/docs/api/covers)；仍失败时显示标注“暂无封面”的排版占位图。
- 图片按浏览需要联网加载，没有批量打包下载出版封面。图像可能为外文版，不能据此推断具体中文 ISBN 或版次。
- 详情中保留 [Open Library](https://openlibrary.org/) 的作品入口。

## 项目身份

侧栏底部以“项目开发者”展示 PassionYoungz 的公开头像、署名及社交链接，参考个人蒸馏项目的开发者名片；页首不作个人书架署名。头像仅作项目身份展示；书本图标为本项目的 SVG 标识。

## 项目宣传封面

`docs/assets/cover.png` 是为本项目使用 imagegen 生成的宣传素材，画面使用虚构的无书名装帧，不作为任何书目的真实封面。

提示词与生成方式见 [`branding/cover-prompt.txt`](branding/cover-prompt.txt)。页面预览截图内的出版物封面仍属于各自权利人。

## 授权范围

仓库 MIT License 覆盖本项目原创代码。第三方元数据、评论、出版封面、商标及截图内的第三方图像，不因被展示或引用而转为本项目的 MIT 授权；请遵循各来源的权利与条款。

本项目提供书目发现与来源导航，不提供书籍正文下载。
