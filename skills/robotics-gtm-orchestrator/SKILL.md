---
name: "机器人GTM总控"
description: Use when a user asks for robotics company GTM, product marketing, commercialization, market research, competitor analysis, scenario analysis, customer research, ROI, solution packaging, or executive/investor business reports, especially for humanoid robots or embodied AI. This is the master skill that selects and combines the robotics GTM sub-skills into a complete Chinese business report.
---

# 机器人GTM总控

## Skill 名称
机器人公司 GTM / 产品市场 / 商业化分析总控 Skill

## 适用场景
当用户输入一个研究任务，但没有明确指定要做市场调研、竞品、ROI、GTM、客户拜访或汇报材料时，先用本 Skill 判断应调用哪些子 Skill，并组合成完整报告结构。

## 输入字段模板
```text
研究主题/场景：
目标客户/用户：
产品形态：
地区/市场：
报告用途：内部决策 / 客户沟通 / 投资人材料 / 产品规划 / 销售支持
时间范围：
已有资料：
输出深度：快评 / 标准报告 / 深度报告
特殊要求：
```

## 子 Skill 路由
| 用户意图 | 应调用 Skill |
|---|---|
| 判断场景机会、市场空间、落地优先级 | robotics-scenario-market-research |
| 分析机器人厂商、产品、方案、价格、渠道 | robotics-competitor-analysis |
| 拆客户需求、痛点、采购链、使用流程 | robotics-customer-painpoints |
| 设计进入市场路径、销售动作、渠道、试点 | robotics-gtm-strategy |
| 算商业模式、ROI、回本周期、价格策略 | robotics-business-model-roi |
| 定产品定位、差异化、价值主张 | robotics-positioning-differentiation |
| 生成完整行业/场景报告 | robotics-industry-report |
| 准备客户拜访、账户研究、提问清单 | robotics-customer-visit-research |
| 包装解决方案、客户材料、方案框架 | robotics-solution-packaging |
| 输出管理层/投资人简报 | robotics-executive-investor-brief |

## 分析框架
1. 先识别：场景、客户、产品、地区、报告用途、决策对象。
2. 判断缺口：数据不足时标注“需进一步验证”，不要编造精确数字。
3. 选择 2-5 个子 Skill，按用途组合。
4. 报告结论先行，给出 3-5 条可执行建议。
5. 所有商业判断都写明假设、风险和验证动作。

## 输出格式
```markdown
# 标题
## 一页结论
| 判断 | 结论 | 依据 | 置信度 |

## 任务拆解与采用的分析模块
| 模块 | 目的 | 产出 |

## 核心分析
按子 Skill 组合输出。

## 建议行动
| 优先级 | 动作 | 负责人/对象 | 时间 | 验证指标 |

## 假设、风险与数据缺口
| 项目 | 当前假设 | 风险 | 验证方式 |
```

## 质量检查标准
- 是否回答了报告用途，而不是泛泛介绍行业。
- 是否有明确优先级、商业建议和下一步动作。
- 是否区分事实、判断、假设和“需进一步验证”。
- 是否包含目标客户、购买链、商业化路径、ROI 或竞品中的关键项。
- 是否避免空话，如“前景广阔”“持续赋能”，除非有具体含义。

## 可复用 prompt
```text
你是人形机器人公司的 GTM / 产品市场 / 商业化分析负责人。请根据以下任务，先判断需要调用哪些分析模块，再输出一份中文商业报告。要求结论先行、多用表格、面向决策、明确假设和数据缺口，不确定内容标注“需进一步验证”。

任务信息：
{粘贴输入字段}
```

## 示例输入
```text
研究主题/场景：商业综合体安防巡检
目标客户/用户：购物中心物业和安保部门
产品形态：轮式/人形巡检机器人
地区/市场：中国一线城市
报告用途：内部决策
输出深度：标准报告
```

## 示例输出
```markdown
## 一页结论
| 判断 | 结论 | 依据 | 置信度 |
|---|---|---|---|
| 是否值得进入 | 建议以试点方式进入，不宜大规模铺开 | 客户有降本和数字化诉求，但复杂场景稳定性和安保责任边界需验证 | 中 |
| 优先客户 | 头部商管集团、标杆购物中心 | 连锁复制价值高，具备预算和展示诉求 | 中 |

## 建议行动
| 优先级 | 动作 | 验证指标 |
|---|---|---|
| P0 | 找 3 家商管客户做访谈 | 明确夜间巡检、异常上报、联动安保的真实付费意愿 |
| P1 | 设计 8 周试点包 | 试点转商用率、人工替代比例、异常识别准确率 |
```
