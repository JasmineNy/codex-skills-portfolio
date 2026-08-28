# Official English Translation

> Skill ID: `official-english-translation` · Category: 企业内容与品牌传播

## 功能说明

把中文宣传材料本地化为正式对外英文，并通过术语库、品牌语气和 QA 清单控制质量。

## 适合解决的问题

当用户请求与上述功能范围匹配的任务时，Codex 可读取本目录的 `SKILL.md`，按照其中的输入、步骤、质量控制和输出规范执行。

## 使用方法

1. 将本目录复制到 Codex 的个人或项目 Skill 目录。
2. 在对话中使用 `$official-english-translation` 显式调用，或让 Codex 根据 description 自动匹配。
3. 如本 Skill 含 `references/`、`scripts/` 或 `assets/`，请保留相对目录结构。

## 源文件

- [`agents/openai.yaml`](./agents/openai.yaml)
- [`references/company-profile.md`](./references/company-profile.md)
- [`references/company-terminology.tsv`](./references/company-terminology.tsv)
- [`references/official-english-style.md`](./references/official-english-style.md)
- [`references/official-translation-style-samples.md`](./references/official-translation-style-samples.md)
- [`references/translation-qa-checklist.md`](./references/translation-qa-checklist.md)
- [`scripts/__pycache__/glossary_check.cpython-312.pyc`](./scripts/__pycache__/glossary_check.cpython-312.pyc)
- [`scripts/glossary_check.py`](./scripts/glossary_check.py)
- [`SKILL.md`](./SKILL.md)

## 公开版说明

公司简介、术语表和案例已替换为适合公开展示的模板，不包含内部公司内容。
