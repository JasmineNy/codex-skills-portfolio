# 求职软件四件套

> Skill ID: `job-application-kit` · Category: 求职决策与申请

## 功能说明

生成岗位结论、BOSS 分段话术、一次发全版、已读未回跟进和简历选择建议。

## 适合解决的问题

当用户请求与上述功能范围匹配的任务时，Codex 可读取本目录的 `SKILL.md`，按照其中的输入、步骤、质量控制和输出规范执行。

## 使用方法

1. 将本目录复制到 Codex 的个人或项目 Skill 目录。
2. 在对话中使用 `$job-application-kit` 显式调用，或让 Codex 根据 description 自动匹配。
3. 如本 Skill 含 `references/`、`scripts/` 或 `assets/`，请保留相对目录结构。

## 源文件

- [`agents/openai.yaml`](./agents/openai.yaml)
- [`assets/fontconfig-job-kit.conf`](./assets/fontconfig-job-kit.conf)
- [`references/asset-catalog.md`](./references/asset-catalog.md)
- [`references/four-part-method.md`](./references/four-part-method.md)
- [`references/resume-catalog.md`](./references/resume-catalog.md)
- [`references/source-map.md`](./references/source-map.md)
- [`scripts/__pycache__/render_resume_assets.cpython-312.pyc`](./scripts/__pycache__/render_resume_assets.cpython-312.pyc)
- [`scripts/__pycache__/validate_kit.cpython-312.pyc`](./scripts/__pycache__/validate_kit.cpython-312.pyc)
- [`scripts/render_resume_assets.py`](./scripts/render_resume_assets.py)
- [`scripts/validate_kit.py`](./scripts/validate_kit.py)
- [`SKILL.md`](./SKILL.md)

## 公开版说明

公开版使用候选人资料和简历路径占位符，不包含真实个人履历数据。
