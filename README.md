# AI Skills

知识库相关的 Codex Skills 合集，主要用于 AI、内容创作、个人知识管理和效率提升。

当前优先发布可用的 MVP，再根据真实使用反馈持续完善。

## Skills

| Skill | 功能 | 状态 |
|---|---|---|
| [Book Notes Generator](skills/book-notes-generator/) | 通读完整书籍，生成渐进式 Notion 或 PDF 读书笔记 | v0.1 Beta |

## 安装 Book Notes Generator

克隆仓库：

```bash
git clone https://github.com/yuqishan163-cloud/knowledge-base.git
```

复制 Skill 到 Codex：

```bash
cp -R knowledge-base/skills/book-notes-generator ~/.codex/skills/
```

重新打开 Codex 后即可使用。

PDF 输出需要 Python 3.10+ 和 ReportLab：

```bash
python3 -m pip install -r knowledge-base/skills/book-notes-generator/requirements.txt
```

Notion 输出需要安装并连接 Notion 插件，并授予目标书单库的访问权限。

## Book Notes Generator

这个 Skill 支持 EPUB、PDF、TXT 和 Markdown，可以：

- 通读完整书籍，避免只根据目录或简介总结
- 使用 Progressive Summarization（渐进式归纳）组织内容
- 根据理论型、实用型、案例型和反思型书籍调整笔记深度
- 为实用书保留步骤、公式、清单和行动示例
- 使用现有 Notion 书单库模板，生成多层折叠笔记
- 生成带大纲、层级符号和中文字体的 PDF 笔记
- 只在联系真实有用时添加知识连接

### 使用示例

```text
使用 $book-notes-generator 通读这本 EPUB，生成渐进式 Notion 读书笔记。
```

```text
使用 $book-notes-generator 阅读这本 PDF，生成一份适合复习的 PDF 笔记。
```

```text
先在 Notion 中创建一小段可折叠预览，我确认后再完成整本书。
```

### 笔记结构

Notion 使用逐层折叠：知识地图 → 核心洞察 → 支持信息 → 可选行动示例。

PDF 只给第一层编号，后续使用符号：

```text
1 第一主题
◆ 核心洞察
  • 支持信息
    → 行动示例
```

演示文件见 [examples/book-notes-generator/demo-note.md](examples/book-notes-generator/demo-note.md)。

### 中文字体

PDF 脚本会自动寻找 macOS 的 STHeiti 或 Linux 的 Noto Sans CJK。也可以通过 `--regular-font` 和 `--bold-font` 手动指定字体。

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

AI Skills is a growing collection of Codex Skills for AI, content creation, personal knowledge management, and productivity. Book Notes Generator reads complete books and turns them into reusable progressive-summary notes for Notion or PDF.

## License

[MIT](LICENSE)
