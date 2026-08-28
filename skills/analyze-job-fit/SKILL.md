---
name: analyze-job-fit
description: Analyze a pasted job description against a verified candidate profile, calculate a conservative job-fit score, identify capability gaps and hard requirements, draft a natural Chinese job-platform greeting, and recommend the best primary and backup resumes from a configured local resume library.
---

# 岗位匹配与简历推荐

## Purpose

Turn a pasted JD into an evidence-based application decision. Use only verified personal facts, distinguish direct evidence from transferable capability, and recommend existing resumes without editing them unless the user separately requests resume revision.

## Required References

1. Read [references/source-map.md](references/source-map.md) completely before analyzing any JD.
2. Read the current master profile and ability map identified there. Read the case bank only when the JD requires evidence beyond those two files.
3. Read [references/resume-catalog.md](references/resume-catalog.md) completely before recommending resumes.
4. Open the most relevant candidate resumes when their positioning is insufficient to choose a primary and backup confidently.

Do not browse the web or add company research unless the user explicitly requests it. Analyze the supplied JD as written.

## Workflow

### 1. Normalize the JD

- Extract the company, role, location, seniority, core responsibilities, required experience, domain background, skills/tools, result ownership, management expectations, and explicit hard requirements.
- Separate `必须/硬性/required` conditions from `优先/preferred/加分` conditions.
- Treat repeated requirements, first-listed responsibilities, and explicit business outcomes as higher emphasis.
- Mark unclear or absent JD information as `未说明`; do not infer it from the company name.

### 2. Build the Evidence Matrix

Map every material JD requirement to verified evidence and assign exactly one status:

| Status | Coefficient | Use when |
| --- | ---: | --- |
| 强匹配 | 1.0 | Direct, recent evidence demonstrates the same capability and comparable scope. |
| 部分匹配 | 0.7 | Direct evidence exists but differs in scope, depth, ownership, product, or result. |
| 可迁移 | 0.4 | Adjacent evidence supports transfer, but the exact requirement has not been demonstrated. |
| 明显缺口 | 0 | Verified facts show the capability or condition is absent or materially insufficient. |
| 信息待确认 | 0 | Available personal evidence cannot establish the requirement. |

- Cite concise, concrete evidence: role, action, scope, metric, and outcome where available.
- Never turn team outcomes into sole personal ownership.
- Never treat materials, training, or activity delivery as proof of revenue, conversion, or customer adoption.
- Keep `信息待确认` separate from `明显缺口`; ask for missing facts only when they could materially change the decision.

### 3. Calculate the Score

Use these four categories and fixed total weights:

| Category | Weight |
| --- | ---: |
| 核心职责 | 40 |
| 行业与相关经验 | 25 |
| 专业能力、方法和工具 | 20 |
| 结果责任与管理要求 | 15 |

Within each category, distribute its weight across the extracted requirements. Use equal weights by default; increase the weight of explicit must-haves or repeatedly emphasized requirements and disclose the adjustment. Keep the category total unchanged.

Calculate each category subtotal as `requirement weight × status coefficient`, then sum and round to the nearest whole number. Show all four subtotals so the score is auditable. Treat missing personal evidence conservatively; do not award assumed points.

Apply these verdicts:

- `80–100`：优先投递
- `70–79`：建议投递并定向优化
- `60–69`：谨慎投递
- `<60`：暂不建议

### 4. Apply Hard-Requirement Controls

- List education, years, language, location, travel, certification, work authorization, and other explicitly mandatory conditions separately.
- If verified facts clearly fail any non-negotiable hard requirement, cap the final score at `59` and explain the cap.
- If a hard requirement is unknown, do not cap the score. Mark the application recommendation `需确认硬门槛后执行` and name the missing fact.
- Do not treat a preferred qualification as a hard gate.
- Show both the pre-cap score and capped final score whenever a cap applies.

### 5. Identify Advantages and Gaps

- Select the three advantages with the greatest JD weight and strongest evidence.
- Select the three gaps most likely to affect screening or interview performance.
- For every gap, label it as `硬门槛`, `核心能力`, `行业知识`, or `证据表达` and give one realistic mitigation action.
- Do not disguise a true gap as an advantage. Distinguish a learnable knowledge gap from missing ownership or missing results.

### 6. Draft the Greeting

Write one Chinese greeting suitable for Boss直聘 or a similar platform:

- Keep it between `80–120` Chinese characters including punctuation; target about `100`.
- Use a warm, natural, conversational tone rather than a formal cover letter.
- Mention the exact role, the two strongest relevant capabilities, one verified quantified result when natural, and interest in further communication.
- Prefer `您好，我关注到贵司的……岗位` over generic enthusiasm.
- Avoid empty adjectives, keyword stacking, private phone numbers, unverified claims, and any claim that turns client-service experience into direct employment.
- Count or re-check the length before returning it. Revise if it falls outside the range.

### 7. Recommend Resumes

- Choose one `主选` and one `备选` from the canonical catalog.
- Rank by JD narrative alignment, evidence prominence, role-title fit, relevant keywords, and risk of distracting content—not by filename similarity alone.
- Return each resume as a clickable Markdown link using its absolute local path.
- Explain the primary/backup difference in one or two sentences each.
- Give up to three JD-specific edits for the primary resume, but do not modify the file in this workflow.
- If no existing resume is adequately aligned, still name the closest primary resume and explicitly recommend creating a new targeted version.

## Fixed Output Format

Use this order and keep the answer decision-oriented:

```markdown
# 岗位匹配结论

**公司 / 岗位：** …  
**最终匹配度：** XX/100（如封顶，同时写原始分）  
**投递建议：** 优先投递 / 建议投递并定向优化 / 谨慎投递 / 暂不建议  
**一句话判断：** …

## 评分拆解

| 维度 | 权重 | 得分 | 判断 |
| --- | ---: | ---: | --- |
| 核心职责 | 40 | … | … |
| 行业与相关经验 | 25 | … | … |
| 专业能力、方法和工具 | 20 | … | … |
| 结果责任与管理要求 | 15 | … | … |

## JD—能力—证据—差距矩阵

| JD要求 | 重要性 | 匹配状态 | 个人证据 | 差距或风险 |
| --- | --- | --- | --- | --- |

## 硬性门槛

| 门槛 | 当前判断 | 对结论的影响 |
| --- | --- | --- |

## 三项核心优势

1. …
2. …
3. …

## 三项关键差距

1. **差距类型｜差距：** …；**建议：** …
2. …
3. …

## 打招呼话术

> …

## 简历推荐

**主选：** [文件名](/absolute/path)  
推荐理由：…

**备选：** [文件名](/absolute/path)  
适用差异：…

**投递前建议调整：**
1. …
2. …
3. …
```

Omit no section. If the JD lacks a company name, location, or hard requirement, write `未说明` rather than asking by default. Ask a concise follow-up only when the JD itself is too incomplete to identify the role's core work.

## Fact and Language Guardrails

- Preserve the candidate's verified employer/client relationship; do not turn client-service experience into direct employment.
- Use only conservative figures and attribution rules from the configured master profile.
- Do not claim completed robot pilots, customer payment, scaled deployment, revenue, or win-rate results without verified evidence.
- Do not inflate public-cloud depth, SaaS customer-success ownership, pricing authority, direct people management, SQL/BI implementation depth, or English fluency.
- Use `参与`, `协同推动`, `作为业务产品负责人`, or `负责业务设计` when those accurately reflect ownership.
- Write concise Chinese business language. Prefer evidence and tradeoffs over encouragement.
