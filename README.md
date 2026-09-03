# AI Skills

知识库相关的 Codex Skills 合集，主要用于 AI、内容创作、个人知识管理和效率提升。

当前优先发布可用的 MVP，再根据真实使用反馈持续完善。

## Skills

| Skill | 功能 | 状态 |
|---|---|---|
| [Yuqi Book Notes](skills/yuqi-book-notes/) | 通读完整书籍，生成渐进式 Notion 或 PDF 读书笔记 | v0.1 Beta |
| [Yuqi Class Notes](skills/yuqi-class-notes/) | 将完整课程整理为独立文章与经过验证的 PDF 笔记 | v0.1 Beta |

## 安装 Skills

克隆仓库：

```bash
git clone https://github.com/yuqishan163-cloud/knowledge-base.git
```

复制 Skill 到 Codex：

```bash
cp -R knowledge-base/skills/yuqi-book-notes ~/.codex/skills/
cp -R knowledge-base/skills/yuqi-class-notes ~/.codex/skills/
```

重新打开 Codex 后即可使用。

PDF 输出需要 Python 3.10+ 和 ReportLab：

```bash
python3 -m pip install -r knowledge-base/skills/yuqi-book-notes/requirements.txt
```

Notion 输出需要安装并连接 Notion 插件，并授予目标书单库的访问权限。

## Yuqi Book Notes

这个 Skill 支持 EPUB、PDF、TXT 和 Markdown，可以：

- 通读完整书籍，避免只根据目录或简介总结
- 使用 Progressive Summarization（渐进式归纳）组织内容
- 根据理论型、实用型、案例型和反思型书籍调整笔记深度
- 为实用书保留步骤、公式、清单和行动示例
- 使用现有 Notion 书单库模板，生成多层折叠笔记
- 先交付完整 Markdown 笔记，用户确认后才生成 PDF
- PDF 用大标题、加粗结论、普通正文和引用块区分四层，核心结论优先使用原文
- Notion 只在联系真实有用时添加知识连接；PDF 不单设概念、个人行动和知识连接板块

### 使用示例

```text
使用 $yuqi-book-notes 通读这本 EPUB，生成渐进式 Notion 读书笔记。
```

```text
使用 $yuqi-book-notes 阅读这本书，先给我完整 Markdown 笔记审批，确认后再生成 PDF。
```

```text
先在 Notion 中创建一小段可折叠预览，我确认后再完成整本书。
```

### 笔记结构

Notion 使用逐层折叠：知识地图 → 核心洞察 → 支持信息 → 可选行动示例。

PDF 使用四种格式，第四层按书的类型选择，整体优先有用的行动示例：

```markdown
## 1. 第一主题

**优先使用原书句子的核心结论。**

普通正文解释论证、机制和适用条件。

> 行动示例、原书案例或关键细节。
```

实用书优先保留步骤、公式和可执行的行动示例；概念型书优先使用原书案例或关键细节，混合型书按观点选择。不强行给每个观点添加第四层，也不另设个人行动计划。加粗摘句会与原文核对，避免将拼接、改写的句子冒充原文；归纳时不套用 AI 味的平衡句式。

完整 Markdown 审批是 PDF 流程的必要步骤，格式预览不能代替内容审批。确认后只调整排版；内容如有实质性变更，需重新审批。Notion 的模板、折叠、行动、特别概念和知识连接流程保持不变。

演示文件见 [examples/yuqi-book-notes/demo-note.md](examples/yuqi-book-notes/demo-note.md)。

### 中文字体

PDF 默认使用 macOS 的宋体正文与黑体标题，也会尝试可用的中文备用字体。可以通过 `--regular-font` 和 `--bold-font` 指定字体文件；TTC 字体集合可用 `--regular-font-index` 和 `--bold-font-index` 选择字形。字体嵌入后仍需核对文字并逐页检查排版。

## 隐私与版权

- 仓库不包含书籍文件、提取后的原文、个人 Notion 数据或测试输出。
- 请确保你有权处理输入书籍。
- 分享笔记前请确认当地版权规则，并优先分享转化后的原创表达。

## 已知限制

- 扫描版 PDF 可能需要额外 OCR。
- 超长或结构异常的书籍需要分批读取并检查覆盖率。
- Notion 模板结构因用户而异，写入前需要读取当前数据库和模板。
- 金融、医疗、法律和软件等时效性内容需要额外核验。

## English

AI Skills is a growing collection of Codex Skills for AI, content creation, personal knowledge management, and productivity. Yuqi Book Notes reads complete books and turns them into reusable progressive-summary notes for Notion or PDF. Yuqi Class Notes turns complete classes into independent articles and verified PDF notes.

## License

[MIT](LICENSE)
