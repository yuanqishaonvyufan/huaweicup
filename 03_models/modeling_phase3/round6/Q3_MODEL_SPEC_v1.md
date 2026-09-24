# Q3 optimization specification v1 — R6-SPEC-001

FROZEN BEFORE OPTIMIZATION。CP1必须commit/push/远端核验后才运行。Q1/Q2不重训；Q4不启动。继承Q3_COST_MODEL_v1成本、G3已冻结Q2参数和支持；正式模型为“支持域约束下的非线性资源配置模型”，算法为解析消元/有界一维搜索与SLSQP对照，不能把算法当模型名。

## Baseline optimization specification

min `E+A n^-a+B d^-b`，约束 `[6+eta L]nd≤c`、n∈[.070542,11.965825]、d∈[.134,299.893]；quality OFF、transported mixture OFF，p固定为Q1训练配比均值，L=2048。界限是B1统计支持，不冒称官方硬件上限或实测供应。

令K=c/k。若K<n_min d_min则不可行；若K≥n_max d_max则最优为两上限且可闲置预算。其余情况下预算紧，d=K/n，n的可行区间为[max(n_min,K/d_max),min(n_max,K/d_min)]。无界内点解：

$$n_*=(aA/(bB))^{1/(a+b)}K^{b/(a+b)},\quad d_*=K/n_*.$$

将n_*截取至上述区间即盒约束全局解。在log n坐标，A exp(-a x)+B K^-b exp(b x)严格凸，因此唯一最优。内点资源弹性dlog n*/dlog C=b/(a+b)、dlog d*/dlog C=a/(a+b)。KKT内点有aU=bV，预算正乘子mu=aU/c=bV/c；`dL*/dC=-mu/1e18`。d上限活跃且n可变时mu=aU/c，n上限时mu=bV/c；两上限且预算松弛mu=0。边界点采用单侧导数，不把不可微点当代码错误。

数值对照：log(n),log(d)坐标，线性log预算约束，SLSQP解析梯度，ftol=1e-12,maxiter=1000；4个固定初值为可行对角线的0/.33/.67/1分位。核所有初值成功、与解析Loss差≤1e-8，变量相对差≤1e-4；预算相对违约≤1e-8。KKT用投影梯度和边界符号核对，不能只依赖SLSQP不含bounds的乘子。记录所有初值，不隐藏失败。

## Generalized objective specification

在同一源内曲面上，以明确运输情景定义 `F=L_B(n,d)-h(q-.5)`，h=0/.5/1/1.5×0.36199528619528604（OFF/LOW/REFERENCE/HIGH）。质量校准为B7 SEMI-SYNTHETIC CALIBRATED，运输及q0为SCENARIO-CONDITIONAL；TYPE E=0，真实因果系数未识别。三种题面成本全部比较。主表仅用常数h，不暗用B7规模斜率。rho有效D机制已由Q2说明，不作为此轮主目标额外搜索模型。

固定q时成本为(k n+r)d，d=min(d_max,c/(k n+r))。排除连(n_min,d_min)也无法承担的q。n的下搜索界=max(n_min,min(n_hi,(c/d_max-r)/k))，n_hi=min(n_max,(c/d_min-r)/k)。预算紧段一阶式为 `-aA n^-a+bB[(kn+r)/c]^b kn/(kn+r)=0`，左右差单调，在log n中brentq求根或端点。固定q内解全局唯一。两上限可行直接返回。

外层q先用101个等距可行q点及端点，逐个局部谷区间做bounded scalar refinement(xatol=1e-10)；所有极小候选取最小，1e-10目标平手取较低q。以201点复核网格加密，容差1e-7；不宣称非凸质量目标已获一般解析全局证明。主情景的每个预算另用3初值SLSQP(log n,log d,q)作数值对照，保存失败及最坏差；容差差>1e-6必须诊断。

quality break-even：预算紧处局部激活条件h>mu*d*r'(q0)，预算松弛时局部阈值0。全局阈值 `hcrit=min_{q>q0}[L_ND*(c,q)-L_ND*(c,q0)]/(q-q0)`，包含q→q0极限；用同一网格与局部精化，区分局部与全局阈值（对数成本不预设凸）。q上限边际放松收益为max(0,h-mu*d*r'(qcap))，单位Loss/单位q；不称真实质量价值。

## Scenarios and validation freeze

51预算×参考L：4个h×3条质量成本；其余4个L：REFERENCE质量×3成本，OFF基线覆盖全部5档。qcap=.75压力仅参考h/参考L三成本。供应压力dmax×{.25,.5}仅quality OFF/reference L。均不改预算格点。

配比：B1 n下限70.542M，高于60M/1M证据点，主N-D域不存在获准的非零p运输范围，且1B明确失败；主问题k_mix=0并固定p，不在full simplex寻优。独立A源有限情景见SUPPORT_SPEC：只比较经验凸包内候选，无跨源联合最优宣称。zero-transfer、1M local-transfer与60M attenuated-transfer应分别标注；没有证据时结论可为“不识别/不准接入”。

不确定性：冻结Q2的200个联合bootstrap向量，传播全部5参数至5个L×51预算的baseline解、Loss、mu；仅条件数值敏感性，2.5/50/97.5分位不作外部置信承诺。质量与配比不同场景的min/max为scenario envelope，非CI。

结构变化定义：active-set改变（N/D支持界、q下界/上界、预算松弛），或离散情景最优候选切换。记录格点转变区间，解析可求则报告解析阈值；不把光滑N/D比例变化或L=30k代理交点称实测产业质变。mu以中心差分核对，拐点用单侧。

质量门槛：预算/盒约束/目标回代/单调性、SLSQP多起点、解析一致性、KKT残差、q网格加密、bootstrap输入不变、R3并行、配比simplex和凸包构造、来源标签、图表/registry一致。失败新Run/version隔离，不改冻结数学规格去迎合结果。

检查点：CP2 baseline机器结果+registry立即push；CP3质量/配比/context/结构立即push；CP4不确定性/影子价/验证/图立即push；CP5论文包/QA/状态/Gate4立即push。Q3仅暂定关闭，Gate4待审，Q4不启动。

方法参考：[SciPy SLSQP](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-slsqp.html)、[brentq](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.brentq.html)，与本机1.18.0相符。推导为本项目解析，不复制外部运行结果。
