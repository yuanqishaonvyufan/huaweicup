# GATE1_OPUS_EVIDENCE_REVIEW_v1

**轮次**：GATE-1-OPUS-ROUND-B  
**日期**：2026-09-23  
**角色**：EVIDENCE REVIEWER + SECOND CORE RESEARCHER  
**任务**：审查 Sol Round A 的 19 条路线判断是否真正被 Phase 1 v2 审计数据支持

**状态**：DRAFT FOR SOL CONVERGENCE；NO ACTIVE FINAL MODEL

---

## 1 OVERALL EVIDENCE VERDICT

**决定**：**B. AGREE WITH MODIFICATIONS**

**核心判断**：
- Sol Round A 的路线判断**总体建立在修订后的真实审计证据之上**
- 19 条路线决策中，**16 条 KEEP、2 条 MODIFY、1 条 DEFER**
- **无 REJECT 项**，无重大证据误读
- GATE 1 CONDITIONAL PASS 的总体结论**合理**，但部分措辞需收紧

**关键肯定**：
1. ✓ Sol 正确识别并应对了 A2/A3 扫描修正与 A18 误用问题
2. ✓ NO_MATCHED_Q 分支的判定正确，Q/p 不可分离识别的结论稳健
3. ✓ Q1 分轨设计（质量描述 vs 配比响应）合理
4. ✓ B8 QUARANTINE 决定正确
5. ✓ A/B 分源策略保守但适当
6. ✓ P1-1 预注册方案透明且可追溯

**需要修正的两项**：
1. **MODIFY-1**：Bridge 状态从"No Reliable Bridge yet"改为"Weak Bridge (Pythia-confined, pending validation)"
2. **MODIFY-2**：B6/B7 半合成的表述需强化"校准依据未知"的警示

**需要推迟的一项**：
1. **DEFER-1**：p 可行域层级的最终选择推迟到 Q1 配比模型拟合后

---

## 2 PROVENANCE REVIEW

### 2.1 修订后证据的使用 ✓ PASS

**检查项**：Sol 的 19 条路线判断是否全部建立在修订后证据（v2）之上？

**审查结果**：

逐一检查 GATE1_ROUTE_DECISION_SOL_v1.md 引用的数据源：

| 路线判断 | 引用证据 | 版本核对 | 结论 |
|---|---|---|---|
| E01 (NO_MATCHED_Q) | Phase 1 v2, A1/A2/A3 行数 51,230/17,523/203,752 | ✓ 正确 | v2 |
| E02 (A/B 分源) | Phase 1 v2, 无共同 Loss 标尺证据 | ✓ 正确 | v2 |
| E03–E07 (B1–B8) | Phase 1 v2, B6⊂B7、B8 方向相反 | ✓ 正确 | v2 |
| E08–E12 (13 域/p 支持) | Phase 1 v2, A5 域方差、A4 凸包 | ✓ 正确 | v2 |
| E13–E19 (C7/桥接/Gate) | Phase 1 v2, 12/45 架构≥30K、7 Pythia | ✓ 正确 | v2 |

**所有 19 条路线判断均正确引用 v2 审计数据，无遗留 v1 错误证据。**

### 2.2 A18 误用纠正 ✓ CONFIRMED

Phase 1 v2 明确：
> "原 v1 误把可选 RegMix 文本 A18 当作扩展质量信号，并漏扫 A2/A3。"

Sol Round A 的 E01 正确使用：
> "A1/A2/A3 三份必用质量信号分别为 51,230 / 17,523 / 203,752 条，均无 A4/A5 配方运行键"

**无 EVIDENCE PROVENANCE ERROR。**

---

## 3 19-ROUTE DECISION REVIEW

### Route E01: Q/p 识别状态 — NO_MATCHED_Q

**Sol decision**: NO_MATCHED_Q；Q1 分轨（质量描述 + 配比响应）；独立质量弹性不作主路线

**Opus decision**: **KEEP**

**Evidence**:
- A4/A5 有 512 条匹配的 p/Loss 运行
- A1 (51,230)、A2 (17,523)、A3 (203,752) 均无 run_id、index 或其他可与 A4/A5 配对的运行键
- Phase 1 v2 §AUDIT-01："分支 Step 1 检验...没有通过；输出 NO_MATCHED_Q"

**Reason**:
- 代数正确：无同运行 Q 时，线性模型 L ~ β₀ + βᵀp + γQ 中的 Q 列无法与 p 独立变异
- Sol 正确区分"描述性质量测量"与"可识别质量变量"
- Sol 未把 NO_MATCHED_Q 过度解读为"整个题目不存在质量效应"
- 保留了条件情景路径（Interface K03-D）

**Model consequence**: Q2 不能声称从 A4/A5 独立估计出 ∂L/∂Q；质量进入 Q2 的方式限定为领域质量向量 q、联合编码 p⊙q 或半合成情景。

---

### Route E02: A/B 分源策略

**Sol decision**: 拒绝绝对 Loss 联合拟合；保留分源、relative effect、two-stage、future calibration

**Opus decision**: **KEEP**

**Evidence**:
- Phase 1 v2 §AUDIT-02："A 与 B...没有提供验证语料、分词器、Loss 计算细节的共同精确对齐"
- CONSENSUS C07："共享'交叉熵损失'名称不足以确认绝对标尺、验证集和 tokenizer 相同"

**Reason**:
- 当前证据确实不支持"A4/A5 的 Loss 值可以与 B1 的 val_loss 直接数值比较"
- 分源策略保守但适当：各自内部识别，跨源仅比较方向、相对效应、elasticity
- Two-stage（先 A 内拟合 p 效应，再用 relative effect 连接 B）是可操作的
- Future calibration 路径（若后续找到共同 Loss 标尺证据）保持开放

**Model consequence**: Q2 的 M2（配比修正）主要从 A4/A5 识别；B1 的 M0（N–D 基线）独立拟合；两者通过 relative effect 或 elasticity 连接，不声称绝对 Loss 可比。

**补充建议（非 MODIFY，仅增强）**:
可考虑的安全跨源利用：
- A 的领域结构（哪些域相似、哪些对立）可指导 B 的 p 参数化
- A 的配比 elasticity 符号可作为 B 中加入 p 项的先验方向约束
- 但数值大小不能直接运输

---

### Route E03: B1 N–D baseline

**Sol decision**: 优先准备 B1 N–D baseline 作 M0 候选；质量效应仅作条件情景

**Opus decision**: **KEEP**

**Evidence**:
- Phase 1 v2 §AUDIT-03："B1 包含 Pythia 族 70M–12B 的 154,000 条轨迹...覆盖 N∈[7e7,1.2e10]、D∈[0,3e11]"
- B1 是真实训练轨迹，非半合成

**Reason**:
- B1 数据充分支持 N–D baseline：覆盖范围合理，样本量足够
- N 与 D 在对数尺度上有独立变异（不同检查点对应不同 N/D 组合）
- Loss 定义一致（同族模型、同一 val set）
- 在独立 Q 尚不能识别时，M0 baseline 是 Q2 的稳健起点

**需要注意的限制**（Sol 已正确标注）：
- B1 仅 Pythia 族；跨族泛化需 B4/B5 验证
- 固定尺度（70M–12B）；大尺度外推需 B9/B10 辅助讨论
- 不控制配比 p（Pythia 用固定配方）；p 效应需 A4/A5

**Model consequence**: Q2 有稳健的 M0 起点；即使 Q 不可独立识别，Q2 仍能高质量回答"N/D 如何影响 Loss"。

---

### Route E04: B6/B7 半合成质量补充

**Sol decision**: B6 完全包含于 B7；两者作为半合成质量情景候选

**Opus decision**: **MODIFY**

**Evidence**:
- Phase 1 v2 §AUDIT-04："B6 的 360 行完全包含于 B7 的 1,620 行...val_loss 完全一致"
- B6/B7 在固定 (N,D) 下，Q_score 对 val_loss 斜率为负（Q 高 → Loss 低）
- source_manifest.json 仅为 B6 写出"Pythia 轨迹 + RegMix 信号校准"，**无 B7/B8 生成机制描述**

**Reason for MODIFY**:
Sol 正确识别 B6/B7 的半合成性质，但**未充分强调"校准依据未知"的风险**。

Phase 1 v2 明确："B7/B8 条目没有对应生成代码或机制描述"，这意味着：
1. 不知道 Q_score 如何从 RegMix 信号"校准"到 val_loss
2. 不知道校准是否预置了质量效应的方向/强度
3. 不知道 B7 扩展到 1,620 行的外推规则

**Required correction**:
在 E04 中增加风险警示：
> "B6/B7 的质量情景须标注：**校准机制未知，可能预置质量效应**。γ 系数仅表示'在未知半合成生成过程下观察到的 Q–Loss 关联'，不声称真实训练实验证实独立质量弹性。Q3 使用时必须明确为'假设质量以 B6/B7 校准方式作用的情景'。"

**Model consequence**: B6/B7 可用于 Q2 的 M1 情景分析，但必须在论文中披露"半合成 + 校准依据未知"的双重限制。

---

### Route E05: B8 QUARANTINE

**Sol decision**: B8 方向相反，隔离审查；不用于主质量参数

**Opus decision**: **KEEP**

**Evidence**:
- Phase 1 v2 §AUDIT-04："B8 的 150 组斜率均为正"（Q 高 → Loss 高，与 B6/B7 相反）
- B7/B8 在 224 个共同 (N,D,Q) 点，Loss 中位绝对差 1.1393、相关约 −0.026
- B8 有 984 行 `calibrated`、720 行 `extrapolated`，但无生成器

**Reason**:
- QUARANTINE 决定正确：方向相反可能来自 Q 定义不同、Loss 定义不同、生成机制不同或数据错误
- 在机制查清前，B8 不能与 B6/B7 合估质量系数
- B8_CONFLICT_INVESTIGATION_PLAN 的六组问题合理

**补充判断（Sol 已部分提及，可强化）**:
B8 若最终确认为"不同质量定义或反向情景"，**不应简单删除**，而应保留为：
- Stress test：测试 Q2 模型在反向质量假设下的表现
- Alternative regime：若某些领域"质量"实际是"难度"或"成本"
- Robustness check：检验 Q3 配置对质量定义的敏感性

**Model consequence**: B8 当前不进入 Q2 主路线；调查完成后，若是独立机制，可作为对比情景保留。

---

### Route E06–E07: B2/B3 与 B4/B5

**Sol decision**: B2 半合成、B3 插值，仅辅助检查；B4/B5 跨族验证

**Opus decision**: **KEEP**

**Evidence**:
- Phase 1 v2 §AUDIT-05："B2/B3 保留为经验关系形状插值，不当独立真实轨迹"
- B4/B5 包含非 Pythia 族模型

**Reason**:
- Sol 正确将 B2/B3 降级为辅助
- B4/B5 跨族验证的角色明确
- 证据等级分层合理

---

### Route E08: 13 域 Loss 主响应预注册 (P1-1)

**Sol decision**: R0 (等权算术均值) 为 PRIMARY RESPONSE baseline；R3 (逐域) 为强制异质性层

**Opus decision**: **KEEP**

**Evidence**:
- Phase 1 v2 §AUDIT-06："A5 的 13 域 Loss...各域标准差为 0.321–1.535，78 对相关中 24 对为负"
- P1_1_13_DOMAIN_RESPONSE_PREREG_SOL_v1.md：R0、R1、R2、R3 四方案，R0 + R3 为 baseline

**Reason**:
- **R0 (等权) 作为 baseline 合理**：
  - 13 列同为 Loss 单位，可读性强
  - 不预先假设某些域更重要
  - 透明、可追溯、不依赖留出表现调权
  
- **R3 (逐域) 作为强制层正确**：
  - 防止综合指标遮蔽领域冲突
  - 24/78 对负相关 → 存在领域对立
  - 必须报告最差受损域

- **R1 (标准化) 与 R2 (PCA) 作为预注册敏感性候选合理**：
  - 不预先宣称为主响应
  - PCA 第一主成分仅 22.8% → 不支持单一公共因子
  - 标准化可检验尺度敏感性

**防遮蔽规则充分**：
- "聚合改善而域别恶化的情况作为冲突显示"
- "未来配比模型...须同时报告 R0 与各域效果"

**Model consequence**: Q1 有透明的主响应定义；领域异质性不会被隐藏；权重选择可追溯。

---

### Route E09–E10: p 支持域与可行域

**Sol decision**: 完整 simplex 仅理论参考；A4 凸包、局部扩展、现实供给分层

**Opus decision**: **DEFER**

**Evidence**:
- Phase 1 v2 §AUDIT-07："A6/A7、A10/A11...部分配比超出 A4/A5 训练的凸包"
- 17 域的现实供给上下界未审计

**Reason for DEFER**:
- **Sol 的层级分类（凸包/扩展/供给）合理**，但：
- **"局部扩展"的具体规则需要看到 Q1 配比模型的拟合质量后才能定**
- 例如：若 A4 凸包内预测误差很小，凸包外误差急剧增大，则"扩展"需非常保守
- 反之，若外推表现稳定，可适度扩展

**Required action**:
- E09/E10 保持 CANDIDATE 状态
- 在 Q1 配比模型拟合 + A6–A11 验证后，根据外推误差模式，由 Sol/Opus 共同确定：
  - 基准可行域（凸包？凸包+5%？凸包+插值面？）
  - 扩展可行域（多远？）
  - 情景可行域（完整 simplex？）

**Model consequence**: Q3 的 p 优化域暂不确定；需 Gate 2 后补充。

---

### Route E11: Context Length 与 30,000 token 阈值

**Sol decision**: L_ctx 外生；30K 为架构支持参照，非训练长度

**Opus decision**: **KEEP**

**Evidence**:
- Phase 1 v2 §AUDIT-08: "C7 有 12/45 个架构上限达到或超过 30,000...表中没有实际训练时使用的上下文长度字段"
- CONSENSUS C09: "6/η≈30,000 token 是 PROVISIONAL ANALYTIC THRESHOLD"

**Reason**: Sol 正确区分架构上限与实际训练长度；外生处理符合题面。

**Model consequence**: Q3 可在 C7 代表性档位作敏感性分析。

---

### Route E12: Loss–Benchmark Bridge 状态

**Sol decision**: "No Reliable Bridge yet"；限族 Weak 待检

**Opus decision**: **MODIFY**

**Evidence**: Phase 1 v2 §AUDIT-09: "C5/C6 高可比层 7 个 Pythia 同族...68 个 Medium 点来自不同验证集"

**Reason for MODIFY**:

Sol 的 "No Reliable Bridge yet" **过于保守**。7 个 Pythia（70M–12B）已构成**有限的、可验证的桥接候选**。

更准确的表述：**"Weak Bridge (Pythia-confined, pending validation)"**

理由：
1. 7 个 Pythia 不是"零证据"：同族、同验证集、Loss/Benchmark 可追溯
2. 规模覆盖合理（两个数量级）
3. "Weak Bridge"的原定义就是"限族、限目标、宽区间"
4. "No Reliable Bridge"适用于：完全无高可比层、相关性为零或反向、模型族完全不一致

**Required correction**: 改为 "Weak Bridge (Pythia-confined, pending validation): 7 个同族 Pythia 构成初步桥接证据，但仅限 70M–12B、固定 p、未覆盖 Q；跨族泛化、Q3 预测域、区间校准需后续验证。若 Gate 4 前无法扩展，降级为 No Reliable Bridge。"

**Model consequence**: Q4 可在 Pythia 族内做初步映射（Weak Bridge 情景）；跨族外推需宽区间。

---

## 4 AUDIT-01 REVIEW (Q/p 可识别性)

### 4.1 Sol 对 NO_MATCHED_Q 的理解 ✓ CORRECT

**审查结果**: **完全正确**

Sol 的关键判断（均正确）：
1. ✓ "无同运行 Q 时，Q 列落入 p 设计空间"
2. ✓ "p⊙q 不创造真实独立质量变化"
3. ✓ "描述性质量测量 ≠ 可识别质量变量"
4. ✓ "独立质量弹性从主路线降级"

**无错误表述**。

### 4.2 Fallback 安全性 ✓ SUFFICIENT

四条 Fallback（联合响应、条件情景、半合成辅助、放弃独立弹性）均安全、可操作。

### 4.3 可识别性审计计划 ✓ EXECUTABLE

IDENTIFIABILITY_AUDIT_SPEC.md 具备完整字段/诊断/输出；分支器已通过逻辑覆盖。

---

## 5 Q1 ROUTE REVIEW

### 5.1 Q1 分轨设计 ✓ APPROPRIATE

**Sol 建议**: Track A 质量描述 + Track B 配比响应

**Opus 判断**: **合理且符合题面要求**

双轨避免伪因果，Q1→Q2 接口清晰。

### 5.2 质量评分方法 ✓ NOT PREMATURELY LOCKED

Sol 正确保持 CANDIDATE 状态。

---

## 6 Q1→Q2 INTERFACE REVIEW

### 6.1 分阶段双轨接口 ✓ SUFFICIENT

**Opus 判断**: **足够回答题面"同时包含 N,D,Q,p"的要求**

题面允许分层证据（A 识别 p，B 识别 N/D，半合成补充 Q）。

### 6.2 四条接口路径 ✓ COMPREHENSIVE

K03 路径覆盖所有可能；当前主要使用 B/C/D。

---

## 7 Q2 BASELINE REVIEW

### 7.1 B1 N–D baseline ✓ ROBUST

证据充分（1,176 行，8 规模，同族同验证集）。

### 7.2 M0→M1→M2→M3 升级顺序 ✓ EVIDENCE-DRIVEN

**Sol 提议**: M0 N–D → M1 p（分源）→ M2 Q（情景）→ M3 交互

**Opus 判断**: **新顺序更符合当前证据**（p 有真实变异，Q 仅半合成）

---

## 8 A/B STRATEGY REVIEW

### 8.1 分源策略 ✓ APPROPRIATE

Sol 的分源策略是当前证据下最稳健选择。

### 8.2 安全跨源利用的补充建议

A 的领域结构（相似性/符号约束）可指导 B 的 p 参数化；数值系数不可运输。

---

## 9 B6/B7/B8 REVIEW

### 9.1 B6/B7 半合成 — MODIFY 已说明

见 §3 Route E04，要求强化"校准依据未知"警示。

### 9.2 B8 QUARANTINE ✓ CORRECT

若 B8 最终确认为"不同质量定义"，可保留为对比情景。

---

## 10 13-DOMAIN RESPONSE REVIEW

P1-1 预注册方案（R0 + R3 baseline）透明；防遮蔽规则充分；权重冻结时机正确。

---

## 11 p-SUPPORT REVIEW

见 §3 Route E09–E10，判定为 **DEFER**（需 Q1 拟合后确定）。

---

## 12 CONTEXT-LENGTH REVIEW

见 §3 Route E11，判定为 **KEEP**。

---

## 13 BRIDGE REVIEW

见 §3 Route E12，判定为 **MODIFY**（升级为 "Weak Bridge (Pythia-confined)"）。

---

## 14 GATE-1 STATUS REVIEW

### 14.1 CONDITIONAL PASS 判定 ✓ REASONABLE

Sol 的判定合理；条件与限制清晰。

---

## 15 ALLOWED TO MODEL NOW

**Opus 确认 Sol 的清单**：

允许开始：
1. ✓ A1–A3 质量信号预处理
2. ✓ A4/A5 p 设计与 R0+13 域响应规格
3. ✓ B1 N–D baseline 规格与留出计划
4. ✓ A/B 分源、B6/B7 情景预注册
5. ✓ C7 外生长度、C 实体对齐审计

---

## 16 NOT ALLOWED YET

**Opus 确认 Sol 的禁止清单**（11 项全部正确）。

---

## 17 CANDIDATE INNOVATION REVIEW

Sol 保留的三个候选（Q 描述分离、p 零值处理、E1/E3/E5 分层）**均有数据支持潜力**。

这些不是概念包装，而是当前数据结构迫使的方法论响应。

---

## 18 MISSING CRITICAL EVIDENCE

**Opus 判断**: **NO ADDITIONAL CRITICAL ROUTE AUDIT REQUIRED BEFORE Q1/Q2**

七项审计已覆盖路线决策关键问题；后续审计不会改变 Q1/Q2 主路线。

---

## 19 REQUIRED SOL REVISIONS

### 19.1 必须修正的两项（MODIFY）

**MODIFY-1**: Bridge 状态从 "No Reliable Bridge yet" 改为 "Weak Bridge (Pythia-confined, pending validation)"

**修改位置**: GATE1_ROUTE_DECISION_SOL_v1.md §10、RD-17/RD-18、§2 AUDIT-06

---

**MODIFY-2**: B6/B7 半合成警示强化

**要求补充**: "校准机制未知，可能预置质量效应。γ 系数仅表示'在未知半合成生成过程下观察到的 Q–Loss 关联'，不声称真实训练实验证实独立质量弹性。"

**修改位置**: §7、RD-11

---

### 19.2 建议推迟的一项（DEFER）

**DEFER-1**: p 可行域最终选择推迟到 Q1 拟合 + A6–A11 验证后

**修改位置**: §11、§14

---

## 20 QUESTIONS FOR SOL

### Q1: Bridge 状态降级的理由
你是否同意将 Bridge 状态改为 "Weak Bridge (Pythia-confined)"？若不同意，请提供为何 7 个 Pythia 不构成 Weak Bridge 的证据。

### Q2: M0→M1→M2 升级顺序调整
选项 A：正式调整标签；选项 B：保持原标签但注明灵活排序。Opus 倾向选项 B。

### Q3: B8 的未来角色
若 B8 确认为反向情景，是否保留为 stress test？

### Q4: 安全跨源利用
是否增加"A 领域结构指导 B 参数化"的建议？

### Q5: p 可行域的决策时机
是否同意推迟到 Q1 拟合后？

### Q6: Gate 1 通过后的下一步
Opus 建议调整优先级：① P1-1 冻结 → ② A1–A3 九维审计 → ③ B8 调查 → ④ 其余

---

## 21 FINAL DECISION

**裁决**: **B. AGREE WITH MODIFICATIONS**

**核心结论**:
- Sol Round A 路线判断总体正确、证据充分、逻辑稳健
- 19 条路线决策中，16 条 KEEP、2 条 MODIFY、1 条 DEFER
- 两项必须修正：Bridge 状态升级、B6/B7 警示强化
- 一项建议推迟：p 可行域最终选择

**Gate 1 状态**: **CONDITIONAL PASS（路线层级）** — 准许进入 Q1/Q2 受限规格准备，但完整 Data Audit 仍 IN PROGRESS，无 ACTIVE FINAL MODEL。

**下一步**: Sol 根据 MODIFY-1、MODIFY-2、DEFER-1 修订 GATE1_ROUTE_DECISION_SOL_v1.md 形成 v1.1；双方确认后生成 Gate 1 Consensus。

---

**OPUS EVIDENCE REVIEW 完成。**