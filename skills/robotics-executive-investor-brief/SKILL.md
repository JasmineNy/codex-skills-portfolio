---
name: "投资人管理层汇报材料"
description: Use to create concise Chinese executive or investor-facing robotics business briefs, board updates, management presentations, investment narratives, strategic memos, and decision papers with market, traction, GTM, differentiation, risks, and asks.
---

# 投资人管理层汇报材料

## Skill 名称
投资人 / 管理层汇报材料 Skill

## 适用场景
用于生成管理层决策简报、投资人沟通材料、董事会更新、战略备忘录或融资叙事草稿。

## 输入字段模板
```text
汇报主题：
目标读者：管理层 / 投资人 / 董事会 / 合作伙伴
核心问题：
产品/场景：
地区：
已有数据：
期望动作：决策 / 争取资源 / 对外沟通 / 融资支持
```

## 分析框架
| 模块 | 分析要点 |
|---|---|
| 一句话结论 | 要读者记住的核心判断 |
| 为什么现在 | 市场窗口、技术拐点、客户变化、竞争变化 |
| 我们凭什么 | 产品、团队、数据、客户、成本、生态 |
| 商业化路径 | 场景、客户、GTM、收入模式、里程碑 |
| 风险 | 技术、交付、市场、监管、资金 |
| Ask | 需要批准的资源、决策或下一步 |

## 输出格式
```markdown
## Executive Summary
| 问题 | 结论 |

## Key Messages
1. ...
2. ...
3. ...

## Evidence & Assumptions
| 论点 | 证据 | 假设/缺口 |

## Commercialization Plan
| 阶段 | 目标 | 指标 |

## Risks & Mitigation
## Ask / Decision Needed
```

## 质量检查标准
- 开头必须能在 60 秒内讲清结论。
- 每个关键论点有证据或明确假设。
- 对投资人突出市场、差异化、规模化路径；对管理层突出取舍、资源和风险。
- 明确需要读者做什么决策。

## 可复用 prompt
```text
请作为机器人公司战略/产品市场负责人，为以下主题生成管理层/投资人汇报材料草稿。要求结论先行、信息密度高、商业决策导向，包含核心判断、证据与假设、商业化路径、风险缓释和明确 Ask。中文商务语境。

输入：
{输入字段}
```

## 示例输入
```text
汇报主题：是否将康养陪伴作为 2026 年重点场景
目标读者：管理层
核心问题：是否投入产品和销售资源
产品/场景：人形机器人康养陪伴与巡房
```

## 示例输出
```markdown
## Executive Summary
| 问题 | 结论 |
|---|---|
| 是否作为重点场景 | 建议作为中期探索场景，不作为近期收入主战场 |
| 主要原因 | 需求真实但付费方、责任边界和稳定性要求仍需验证 |
```
