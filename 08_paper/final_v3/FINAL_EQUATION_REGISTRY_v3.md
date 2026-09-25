# 最终公式登记

## 式（1）
- equation_id: E01
- number: 1
- question: 1
- formula: u_{ij}=\widehat F_{j,T}(x_{ij}),\qquad \mathrm{DQ0}_i=\frac{1}{5}\sum_{j=1}^{5}{u_{ij}}.
- rendered_parts: ['u_{ij}=\\widehat F_{j,T}(x_{ij}),\\qquad \\mathrm{DQ0}_i=\\frac{1}{5}\\sum_{j=1}^{5}{u_{ij}}.']
- symbol_definitions: 全文符号表及公式前后定义
- units: N十亿参数，D十亿token；Q4分数0—100；其他见符号表
- source_model: Q1_MODEL_SPEC_v1 / fixed diagnostic definitions
- paper_section: 5.1 二十二项综合评分与五维解释性画像
- assumptions: 固定参考及局部欧氏配比关联；非质量因果效应

## 式（2）
- equation_id: E02
- number: 2
- question: 1
- formula: \overline u_{dj}=\frac{1}{|I_{dj}|}\sum_{i\in I_{dj}}{u_{ij}},\qquad I_{dj}=\{i\in I_d:u_{ij}\text{有效}\}.
- rendered_parts: ['\\overline u_{dj}=\\frac{1}{|I_{dj}|}\\sum_{i\\in I_{dj}}{u_{ij}},\\qquad I_{dj}=\\{i\\in I_d:u_{ij}\\text{有效}\\}.']
- symbol_definitions: 全文符号表及公式前后定义
- units: N十亿参数，D十亿token；Q4分数0—100；其他见符号表
- source_model: Q1_MODEL_SPEC_v1 / fixed diagnostic definitions
- paper_section: 5.1 二十二项综合评分与五维解释性画像
- assumptions: 固定参考及局部欧氏配比关联；非质量因果效应

## 式（3）
- equation_id: E03
- number: 3
- question: 1
- formula: C_{jk,d}(\tau)=\frac{1}{n_d}\sum_{i\in I_d}{\mathbf 1\{(v_{ij}\ge\tau,\ v_{ik}\le1-\tau)\ \mathrm{or}\ (v_{ik}\ge\tau,\ v_{ij}\le1-\tau)\}}.
- rendered_parts: ['C_{jk,d}(\\tau)=\\frac{1}{n_d}\\sum_{i\\in I_d}{J_{ijk}}', 'J_{ijk}=\\mathbf1\\{(v_{ij}\\ge\\tau,\\ v_{ik}\\le1-\\tau)', '\\mathrm{or}\\ (v_{ik}\\ge\\tau,\\ v_{ij}\\le1-\\tau)\\}']
- symbol_definitions: 全文符号表及公式前后定义
- units: N十亿参数，D十亿token；Q4分数0—100；其他见符号表
- source_model: Q1_MODEL_SPEC_v1 / fixed diagnostic definitions
- paper_section: 5.2 区分语义冲突与统计分歧
- assumptions: 固定参考及局部欧氏配比关联；非质量因果效应

## 式（4）
- equation_id: E04
- number: 4
- question: 1
- formula: H^{\mathsf T}H=I_{16},\quad H^{\mathsf T}\mathbf1=0,\quad z=H^{\mathsf T}(p-\overline p),\quad \widehat L_m(p)=a_m+\beta_m^{\mathsf T}z.
- rendered_parts: ['H^{\\mathsf T}H=I_{16},\\quad H^{\\mathsf T}\\mathbf1=0,\\quad z=H^{\\mathsf T}(p-\\overline p)', '\\widehat L_m(p)=a_m+\\beta_m^{\\mathsf T}z']
- symbol_definitions: 全文符号表及公式前后定义
- units: N十亿参数，D十亿token；Q4分数0—100；其他见符号表
- source_model: Q1_MODEL_SPEC_v1 / fixed diagnostic definitions
- paper_section: 5.3 单纯形约束下的配比响应
- assumptions: 固定参考及局部欧氏配比关联；非质量因果效应

## 式（5）
- equation_id: E05
- number: 5
- question: 1
- formula: R_0(p)=\frac{1}{13}\sum_{m=1}^{13}{\widehat L_m(p)},\qquad R_3(p)=(\widehat L_1(p),\ldots,\widehat L_{13}(p)).
- rendered_parts: ['R_0(p)=\\frac{1}{13}\\sum_{m=1}^{13}{\\widehat L_m(p)},\\qquad R_3(p)=(\\widehat L_1(p),\\ldots,\\widehat L_{13}(p)).']
- symbol_definitions: 全文符号表及公式前后定义
- units: N十亿参数，D十亿token；Q4分数0—100；其他见符号表
- source_model: Q1_MODEL_SPEC_v1 / fixed diagnostic definitions
- paper_section: 5.3 单纯形约束下的配比响应
- assumptions: 固定参考及局部欧氏配比关联；非质量因果效应

## 式（6）
- equation_id: E06
- number: 6
- question: 2
- formula: L_B(N,D)=L_\infty+A N^{-\alpha}+B D^{-\beta}.
- rendered_parts: ['L_B(N,D)=L_\\infty+A N^{-\\alpha}+B D^{-\\beta}.']
- symbol_definitions: 全文符号表及公式前后定义
- units: N十亿参数，D十亿token；Q4分数0—100；其他见符号表
- source_model: Q2_ROUND5_SPEC_v1
- paper_section: 6.1 来源内估计与参数含义
- assumptions: 来源内加性幂律；质量与运输仅条件情景

## 式（7）
- equation_id: E07
- number: 7
- question: 2
- formula: \widehat L_B=1.68979756+0.35398032N^{-0.33997658}+1.24030558D^{-0.27987813}.
- rendered_parts: ['\\widehat L_B=1.68979756+0.35398032N^{-0.33997658}+1.24030558D^{-0.27987813}.']
- symbol_definitions: 全文符号表及公式前后定义
- units: N十亿参数，D十亿token；Q4分数0—100；其他见符号表
- source_model: Q2_ROUND5_SPEC_v1
- paper_section: 6.1 来源内估计与参数含义
- assumptions: 来源内加性幂律；质量与运输仅条件情景

## 式（8）
- equation_id: E08
- number: 8
- question: 2
- formula: \frac{\partial L_B}{\partial N}=-\frac{\alpha U}{N},\quad \frac{\partial L_B}{\partial D}=-\frac{\beta V}{D},\quad \varepsilon_N=-\frac{\alpha U}{L_B},\quad \varepsilon_D=-\frac{\beta V}{L_B}.
- rendered_parts: ['\\frac{\\partial L_B}{\\partial N}=-\\frac{\\alpha U}{N},\\quad\\frac{\\partial L_B}{\\partial D}=-\\frac{\\beta V}{D}', '\\varepsilon_N=-\\frac{\\alpha U}{L_B},\\quad\\varepsilon_D=-\\frac{\\beta V}{L_B}']
- symbol_definitions: 全文符号表及公式前后定义
- units: N十亿参数，D十亿token；Q4分数0—100；其他见符号表
- source_model: Q2_ROUND5_SPEC_v1
- paper_section: 6.3 边际效用 弹性与规模替代
- assumptions: 来源内加性幂律；质量与运输仅条件情景

## 式（9）
- equation_id: E09
- number: 9
- question: 2
- formula: \frac{d\log D}{d\log N}=-\frac{\alpha U}{\beta V},\qquad D_{\rm new}=\left(\frac{B}{L_{\rm old}-L_\infty-A N_{\rm new}^{-\alpha}}\right)^{1/\beta}.
- rendered_parts: ['\\frac{d\\log D}{d\\log N}=-\\frac{\\alpha U}{\\beta V}', 'D_{\\rm new}=\\left(\\frac{B}{L_{\\rm old}-L_\\infty-A N_{\\rm new}^{-\\alpha}}\\right)^{1/\\beta}']
- symbol_definitions: 全文符号表及公式前后定义
- units: N十亿参数，D十亿token；Q4分数0—100；其他见符号表
- source_model: Q2_ROUND5_SPEC_v1
- paper_section: 6.3 边际效用 弹性与规模替代
- assumptions: 来源内加性幂律；质量与运输仅条件情景

## 式（10）
- equation_id: E10
- number: 10
- question: 2
- formula: L_s(N,D,Q,p)=L_B(N,D)-h_Q(Q-Q_0)+k_s(N)\Delta L_A(p),\quad h_Q=\lambda\,0.3619952862.
- rendered_parts: ['L_s(N,D,Q,p)=L_B(N,D)-h_Q(Q-Q_0)+k_s(N)\\Delta L_A(p),\\quad h_Q=\\lambda\\,0.3619952862.']
- symbol_definitions: 全文符号表及公式前后定义
- units: N十亿参数，D十亿token；Q4分数0—100；其他见符号表
- source_model: Q2_ROUND5_SPEC_v1
- paper_section: 6.4 广义质量与配比项的条件解释
- assumptions: 来源内加性幂律；质量与运输仅条件情景

## 式（11）
- equation_id: E11
- number: 11
- question: 2
- formula: \frac{d\log N}{dQ}=-\frac{h_Q}{\alpha U},\quad \frac{d\log D}{dQ}=-\frac{h_Q}{\beta V},\quad N_{\rm new}=\left(\frac{A}{U+h_Q\Delta Q}\right)^{1/\alpha}.
- rendered_parts: ['\\frac{d\\log N}{dQ}=-\\frac{h_Q}{\\alpha U},\\quad \\frac{d\\log D}{dQ}=-\\frac{h_Q}{\\beta V},\\quad N_{\\rm new}=\\left(\\frac{A}{U+h_Q\\Delta Q}\\right)^{1/\\alpha}.']
- symbol_definitions: 全文符号表及公式前后定义
- units: N十亿参数，D十亿token；Q4分数0—100；其他见符号表
- source_model: Q2_ROUND5_SPEC_v1
- paper_section: 6.4 广义质量与配比项的条件解释
- assumptions: 来源内加性幂律；质量与运输仅条件情景

## 式（12）
- equation_id: E12
- number: 12
- question: 2
- formula: \Delta\widehat L_m=\delta\,(e_i-e_j)^{\mathsf T}H\beta_m,\qquad \mathbf1^{\mathsf T}(e_i-e_j)=0.
- rendered_parts: ['\\Delta\\widehat L_m=\\delta\\,(e_i-e_j)^{\\mathsf T}H\\beta_m,\\qquad \\mathbf1^{\\mathsf T}(e_i-e_j)=0.']
- symbol_definitions: 全文符号表及公式前后定义
- units: N十亿参数，D十亿token；Q4分数0—100；其他见符号表
- source_model: Q2_ROUND5_SPEC_v1
- paper_section: 6.4 广义质量与配比项的条件解释
- assumptions: 来源内加性幂律；质量与运输仅条件情景

## 式（13）
- equation_id: E13
- number: 13
- question: 3
- formula: C_{\rm used}=10^{18}(6+\eta L_{\rm ctx})ND+10^9D\,[g(Q)-g(Q_0)]_+\le C.
- rendered_parts: ['C_{\\rm used}=10^{18}(6+\\eta L_{\\rm ctx})ND+10^9D\\,[g(Q)-g(Q_0)]_+\\le C.']
- symbol_definitions: 全文符号表及公式前后定义
- units: N十亿参数，D十亿token；Q4分数0—100；其他见符号表
- source_model: Q3_MODEL_SPEC_v1 / Q3_COST_MODEL_v1
- paper_section: 7.1 统一单位的算力代理
- assumptions: 题设成本、外生上下文、统计支持域；预算可闲置

## 式（14）
- equation_id: E14
- number: 14
- question: 3
- formula: g_{\rm exp}(Q)=10^7e^{6Q},\quad g_{\rm pow}(Q)=5\times10^9Q^4,\quad g_{\rm log}(Q)=2\times10^9\log(1+10Q).
- rendered_parts: ['g_{\\rm exp}(Q)=10^7e^{6Q},\\quad g_{\\rm pow}(Q)=5\\times10^9Q^4,\\quad g_{\\rm log}(Q)=2\\times10^9\\log(1+10Q).']
- symbol_definitions: 全文符号表及公式前后定义
- units: N十亿参数，D十亿token；Q4分数0—100；其他见符号表
- source_model: Q3_MODEL_SPEC_v1 / Q3_COST_MODEL_v1
- paper_section: 7.1 统一单位的算力代理
- assumptions: 题设成本、外生上下文、统计支持域；预算可闲置

## 式（15）
- equation_id: E15
- number: 15
- question: 3
- formula: \mathcal L=L_B+\mu(kND-c),\qquad \alpha A N^{-\alpha}=\beta B D^{-\beta},\quad \mu\ge0,\quad \mu(kND-c)=0.
- rendered_parts: ['\\mathcal L=L_B+\\mu(kND-c),\\qquad \\alpha A N^{-\\alpha}=\\beta B D^{-\\beta},\\quad \\mu\\ge0,\\quad \\mu(kND-c)=0.']
- symbol_definitions: 全文符号表及公式前后定义
- units: N十亿参数，D十亿token；Q4分数0—100；其他见符号表
- source_model: Q3_MODEL_SPEC_v1 / Q3_COST_MODEL_v1
- paper_section: 7.2 解析最优配置与结构转移
- assumptions: 题设成本、外生上下文、统计支持域；预算可闲置

## 式（16）
- equation_id: E16
- number: 16
- question: 3
- formula: N_0=\left(\frac{\alpha A}{\beta B}\right)^{1/(\alpha+\beta)}K^{\beta/(\alpha+\beta)},\quad N^*=\operatorname{clip}\!\left(N_0,\max(N_{\min},K/D_{\max}),\min(N_{\max},K/D_{\min})\right),\quad D^*=K/N^*.
- rendered_parts: ['N_0=\\left(\\frac{\\alpha A}{\\beta B}\\right)^{1/(\\alpha+\\beta)}K^{\\beta/(\\alpha+\\beta)}', 'a_N=\\max(N_{\\min},K/D_{\\max}),\\quad b_N=\\min(N_{\\max},K/D_{\\min})', 'N^*=\\operatorname{clip}(N_0,a_N,b_N),\\qquad D^*=K/N^*']
- symbol_definitions: 全文符号表及公式前后定义
- units: N十亿参数，D十亿token；Q4分数0—100；其他见符号表
- source_model: Q3_MODEL_SPEC_v1 / Q3_COST_MODEL_v1
- paper_section: 7.2 解析最优配置与结构转移
- assumptions: 题设成本、外生上下文、统计支持域；预算可闲置

## 式（17）
- equation_id: E17
- number: 17
- question: 3
- formula: -\alpha A N^{-\alpha}+\beta B\left(\frac{kN+r}{c}\right)^\beta\frac{kN}{kN+r}=0.
- rendered_parts: ['-\\alpha A N^{-\\alpha}+\\beta B\\left(\\frac{kN+r}{c}\\right)^\\beta\\frac{kN}{kN+r}=0.']
- symbol_definitions: 全文符号表及公式前后定义
- units: N十亿参数，D十亿token；Q4分数0—100；其他见符号表
- source_model: Q3_MODEL_SPEC_v1 / Q3_COST_MODEL_v1
- paper_section: 7.3 质量成本选择与投入门槛
- assumptions: 题设成本、外生上下文、统计支持域；预算可闲置

## 式（18）
- equation_id: E18
- number: 18
- question: 3
- formula: h_{\rm crit}(c)=\inf_{Q>Q_0}\frac{L_{ND}^*(c,Q)-L_{ND}^*(c,Q_0)}{Q-Q_0}.
- rendered_parts: ['h_{\\rm crit}(c)=\\inf_{Q>Q_0}\\frac{L_{ND}^*(c,Q)-L_{ND}^*(c,Q_0)}{Q-Q_0}.']
- symbol_definitions: 全文符号表及公式前后定义
- units: N十亿参数，D十亿token；Q4分数0—100；其他见符号表
- source_model: Q3_MODEL_SPEC_v1 / Q3_COST_MODEL_v1
- paper_section: 7.3 质量成本选择与投入门槛
- assumptions: 题设成本、外生上下文、统计支持域；预算可闲置

## 式（19）
- equation_id: E19
- number: 19
- question: 3
- formula: \frac{C_{\rm attn}}{C_{\rm train}}=\frac{\eta L_{\rm ctx}}{6},\qquad L_{\rm crit}=\frac{6}{\eta}=30000.
- rendered_parts: ['\\frac{C_{\\rm attn}}{C_{\\rm train}}=\\frac{\\eta L_{\\rm ctx}}{6},\\qquad L_{\\rm crit}=\\frac{6}{\\eta}=30000.']
- symbol_definitions: 全文符号表及公式前后定义
- units: N十亿参数，D十亿token；Q4分数0—100；其他见符号表
- source_model: Q3_MODEL_SPEC_v1 / Q3_COST_MODEL_v1
- paper_section: 7.5 上下文成本与解析交点
- assumptions: 题设成本、外生上下文、统计支持域；预算可闲置

## 式（20）
- equation_id: E20
- number: 20
- question: 4
- formula: y_i=\frac{1}{6}\sum_{k=1}^{6}{b_{ik}},\qquad F_t=Q_{0.90}\{y_i:t-28\text{天}<t_i\le t\}.
- rendered_parts: ['y_i=\\frac{1}{6}\\sum_{k=1}^{6}{b_{ik}},\\qquad F_t=Q_{0.90}\\{y_i:t-28\\text{天}<t_i\\le t\\}.']
- symbol_definitions: 全文符号表及公式前后定义
- units: N十亿参数，D十亿token；Q4分数0—100；其他见符号表
- source_model: Q4_FRONTIER_MODEL_SPEC_v1
- paper_section: 8.1 同口径能力与研究样本
- assumptions: 同口径评测群体；描述性回归；趋势与条件扩散

## 式（21）
- equation_id: E21
- number: 21
- question: 4
- formula: y_i=a+\theta_N\log N_i+\gamma t_i+\delta_{\mathrm{type}(i)}+\xi_{\mathrm{family}(i)}+\epsilon_i.
- rendered_parts: ['y_i=a+\\theta_N\\log N_i+\\gamma t_i+\\delta_{\\mathrm{type}(i)}+\\xi_{\\mathrm{family}(i)}+\\epsilon_i.']
- symbol_definitions: 全文符号表及公式前后定义
- units: N十亿参数，D十亿token；Q4分数0—100；其他见符号表
- source_model: Q4_FRONTIER_MODEL_SPEC_v1
- paper_section: 8.3 参数规模关联与剩余性能分量
- assumptions: 同口径评测群体；描述性回归；趋势与条件扩散

## 式（22）
- equation_id: E22
- number: 22
- question: 4
- formula: \Delta F=\Delta S+\Delta R,\qquad \pi_N=\frac{\Delta S}{\Delta F},\quad \pi_R=1-\pi_N.
- rendered_parts: ['\\Delta F=\\Delta S+\\Delta R,\\qquad \\pi_N=\\frac{\\Delta S}{\\Delta F},\\quad \\pi_R=1-\\pi_N.']
- symbol_definitions: 全文符号表及公式前后定义
- units: N十亿参数，D十亿token；Q4分数0—100；其他见符号表
- source_model: Q4_FRONTIER_MODEL_SPEC_v1
- paper_section: 8.3 参数规模关联与剩余性能分量
- assumptions: 同口径评测群体；描述性回归；趋势与条件扩散

## 式（23）
- equation_id: E23
- number: 23
- question: 4
- formula: z_t=\log\frac{F_t/100}{1-F_t/100}=a_F+b_Ft+e_t,\qquad \widehat F_{t+h}=\frac{100}{1+\exp[-(\widehat a_F+\widehat b_F(t+h))]}.
- rendered_parts: ['z_t=\\log\\frac{F_t/100}{1-F_t/100}=a_F+b_Ft+e_t', '\\widehat F_{t+h}=\\frac{100}{1+\\exp[-(\\widehat a_F+\\widehat b_F(t+h))]}']
- symbol_definitions: 全文符号表及公式前后定义
- units: N十亿参数，D十亿token；Q4分数0—100；其他见符号表
- source_model: Q4_FRONTIER_MODEL_SPEC_v1
- paper_section: 8.4 动态模型与短期限验证
- assumptions: 同口径评测群体；描述性回归；趋势与条件扩散

## 式（24）
- equation_id: E24
- number: 24
- question: 4
- formula: \widehat F_\rho(h)=\operatorname{clip}\{U(h)-(1-\rho)\theta_N g_{\rm ref}h,0,100\},\quad \rho\in\{1,0.5,0\}.
- rendered_parts: ['\\widehat F_\\rho(h)=\\operatorname{clip}\\{U(h)-(1-\\rho)\\theta_N g_{\\rm ref}h,0,100\\},\\quad \\rho\\in\\{1,0.5,0\\}.']
- symbol_definitions: 全文符号表及公式前后定义
- units: N十亿参数，D十亿token；Q4分数0—100；其他见符号表
- source_model: 03_models/paper_repair/Q4_REPAIR_PREFIT_SPEC_v1.md
- paper_section: 8.5 日期明确的预测与三类不确定性
- assumptions: 外生正增长参考、训练D固定、C≈6ND；参数关联系数仅作情景敏感性，不识别真实效应