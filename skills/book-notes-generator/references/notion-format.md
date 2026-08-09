# Notion Format

## Contents

1. Destination discovery
2. Page structure
3. Nested toggle pattern
4. Property handling
5. Preview and verification

## Destination discovery

1. Search for the user's book database and fetch its data source schema.
2. Search inside it for the current reading-note template and the same book title.
3. Fetch the template and one recently approved note to learn current structure and style.
4. Create a new page by duplicating the template when duplication is available.
5. Keep existing pages unchanged unless the user asks to update or replace them.

Do not hard-code a database ID, template page ID, option name, or property list. The workspace may change.

## Page structure

Preserve the template's visual system. The validated baseline is:

```text
📚 Book Name
└─ 💜 全书总结
   ├─ 📘 三句话概括这本书
   └─ ✅ 行动
└─ 📝 全书架构
   └─ Level 1 toggle
      └─ Level 2 bold toggle
         └─ Level 3 toggle
            ├─ supporting text
            └─ optional Level 4 action-example toggle
└─ ✏️ 特别概念
└─ 🔗 知识连接
```

Use 3–7 Level 1 toggles. Color them consistently with the current template. Keep the knowledge map inside `全书架构`; do not add a duplicate flat outline elsewhere.

## Nested toggle pattern

Use Notion enhanced Markdown nesting:

```markdown
<details color="blue_bg">
<summary>短语式主题</summary>
	<details>
	<summary>**明确的核心洞察**</summary>
		<details>
		<summary>简短解释标题</summary>
			正文解释。**最重要的一句可以加粗。**
			<details>
			<summary>行动示例｜具体动作</summary>
				步骤、公式或示例。
			</details>
		</details>
	</details>
</details>
```

Validate actual nesting after writing. Visual indentation in source text alone is insufficient evidence.

## Property handling

- Map source metadata only to properties that exist in the fetched schema.
- Use an existing select or multi-select option when it matches. Ask before creating a materially new taxonomy.
- Leave formulas and rollups untouched.
- Set a reading status only when the user's meaning is clear; processing a file does not prove the user personally finished reading it.
- Use `电子书` or the current equivalent when the source is an EPUB/PDF and the schema supports it.
- Do not invent author, dates, rating, ISBN, cover, or tags.

## Preview and verification

When the user requests a format preview, create a real Notion page or a small section in a duplicated template. Include at least one complete Level 1 → Level 2 → Level 3 chain and, for practical books, one Level 4 action example. Return the Notion link and wait for approval.

For the final page:

1. Fetch it after all writes.
2. Confirm the title and applicable properties.
3. Confirm all template sections were addressed.
4. Confirm toggles nest one level at a time.
5. Confirm Level 2 titles are bold.
6. Confirm practical details, special concepts, and genuine page links survived.
7. Fix discrepancies before returning the link.
