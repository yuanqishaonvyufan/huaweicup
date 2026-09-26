"""Editorial v6 of the frozen v5 manuscript; no model is recomputed."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt
from lxml import etree
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "11_delivery/v5/F_final_candidate_v5_参考论文深度吸收完整版.docx"
OUT = ROOT / "11_delivery/v6"
STEM = "F_final_candidate_v6_获奖范文格式语言优化版"
FIG_DIR = ROOT / "06_results/figures/paper_v6"


HEADING_REWRITES = {
    63: "二、问题分析与总体思路",
    79: "五、模型建立与求解",
    84: "5.1 问题一模型的建立与求解",
    85: "5.1.1 问题分析与技术路线",
    90: "5.1.2 数据与模型准备",
    141: "5.1.4 求解与结果分析",
    157: "5.2 问题二模型的建立与求解",
    158: "5.2.1 问题分析与技术路线",
    161: "5.2.2 数据与模型准备",
    189: "5.2.4 求解与结果分析",
    215: "5.3 问题三模型的建立与求解",
    216: "5.3.1 问题分析与技术路线",
    219: "5.3.2 数据与模型准备",
    259: "5.3.4 求解与结果分析",
    284: "5.4 问题四模型的建立与求解",
    285: "5.4.1 问题分析与技术路线",
    293: "5.4.2 数据与模型准备",
    335: "5.4.4 求解与结果分析",
    372: "七、模型评价",
    381: "八、模型改进与推广",
}

REWRITES = {
    7: "算力约束下大语言模型的质量评价、资源配置与能力前沿预测",
    9: "围绕数据质量、领域配比、模型规模与能力演进的递进关系，本文建立规则明确的质量评价、来源分层的标度律、支持域约束下的资源优化和能力前沿条件预测框架。四问分别使用可比资料建模，并检验结果能否跨来源传递。",
    10: "针对问题一，使用A1固定参考分位把22项信号转为规则效用，等权形成Q_full，并以五维画像解释评分差异。A1中commoncrawl与arxiv的Q_full均值为0.7600、0.7356；42项候选中有7项统计分歧、3项领域反转。17域配比模型在1M留出集上使平均Loss的RMSE由0.2846降至0.2278，13个响应域全部改善；1B迁移失败，10B与70B估算外推的中心化误差比分别为2.3452、2.2672。",
    11: "针对问题二，B1八条训练轨迹拟合得到加性N—D幂律，衰减指数α=0.33997658、β=0.27987813。整规模留出、前向预测和双维分块的宏RMSE分别为0.000146888、0.000111642、0.000114134。在此基础上推导边际弹性与等Loss替代关系；B7半合成质量表的45个单元斜率均为负，共同斜率为−0.361995。",
    12: "针对问题三，将题设训练、注意力与质量处理成本统一为FLOPs，在统计支持域内解析求解并用数值优化核对。参考上下文2048、质量与配比收益关闭时，预算10¹⁹、10²²、10²⁴ FLOPs对应的最优(N,D)依次为(0.221309,7.049698)、(5.202388,299.893)、(11.965825,299.893)，Loss依次为2.998935、2.143211、2.093379；N、D均以十亿计。两个支持上界依次活跃，高预算平台由支持域产生。",
    13: "针对问题四，用C8六项原始任务得分构造28天90%分位前沿。候选Loss—Benchmark桥接在留一规模验证中未优于均值基准，因而直接在能力分数空间预测。主规格的参数关联描述份额为17.02%，其余82.98%包含未观测训练量等多种来源。在训练D固定及外生正增长参照下，2027年三档条件中心为79.76、77.93、76.11，2028年为87.13、83.48、79.84。",
    14: "本文的主要特点是把质量评分与解释画像并报、依据来源和支持域控制模型传递，并分开呈现参数区间、模型范围与外生情景。质量分不是普适训练收益；能力预测距末次观测约30和42个月，所给区间是条件模型结果，仍需长期同口径数据检验。",
    58: "大语言模型训练效果受参数量、数据量、数据内容和领域结构共同影响。扩大模型或增加训练数据通常需要更多算力；提高数据质量与延长上下文也会改变成本。在给定预算下，资源配置因而是一个相互制约的联合决策问题。",
    59: "经验标度律为规模和数据量的权衡提供了起点[1]。本题还给出文档级质量标注、训练运行级损失和模型级能力评测。本文先辨明各类资料的观测单位，再依次研究质量评价、规模响应、预算配置与能力前沿，使后续推断有可检验的数据基础。",
    61: "参数量、训练数据量、数据质量和领域配比共同影响训练损失与任务表现；固定算力和上下文开销又限制了可行投入。题目要求先评价数据价值和资源响应，再据此讨论预算分配及未来能力演进。",
    62: "问题一建立质量评价并检验领域配比响应；问题二刻画规模、数据、质量和配比对损失的关系；问题三在题设成本约束下优化资源配置；问题四研究规模关联、能力前沿和增长放缓情景。四问具有递进关系，其衔接取决于共同量尺与数据支持范围。",
    64: "四类附件分属文档、训练运行和模型评测三个层次。先在各自量尺中建立可核对的关系，再检验能否把上一问的结果用于下一问。直接拼接不同来源的Loss，会把来源差异混入质量或技术收益。",
    65: "技术路线由四条证据链组成：质量信号的规则评价与配比留出检验，B1内部N—D曲面及半合成质量情景，题设成本下的支持域优化，以及同口径评测前沿的独立预测。跨来源系数只在资料提供共同量尺时估计，否则以显式情景呈现。",
    66: "全文将附件内经验估计、半合成校准和外生条件推演分别报告。桥接或规模迁移检验不通过时，结论留在原资料范围内；这也是四问之间的模型选择结果。",
    70: "为明确计算对象和可检验范围，本文采用以下五项假设。相应的适用边界集中在各问结果之后讨论。",
    71: "假设一：B1表内的N、D和Loss可用于估计同来源响应曲面。外部原始运行与验证量尺尚待进一步核对，参数按附件内部关系解释。",
    72: "假设二：当前标注体系中的五个定向质量信号可用于相应属性描述，固定A1参考可用于同体系比较。其余信号通过公布的用途规则计分。",
    73: "假设三：观测配方附近的领域响应可由线性单纯形对比近似；是否跨规模适用由留出检验决定。",
    74: "假设四：给定上下文和质量成本形式后，题设FLOPs代理定义条件优化问题。统计支持域限定模型可解释的配置范围，预算允许闲置。",
    75: "假设五：在固定任务组合和筛选规则下，历史高分位可描述合格模型群体；未来投影另依赖趋势、残差扩散和外生增长路径。",
    80: "四问均按问题分析、数据准备、模型建立、求解与检验的次序展开。表2列出附件用途和相应量尺，为后续图表与数值比较提供索引。",
    81: "质量资料按文本ID去重，配方资料按训练运行索引匹配，B1按完整轨迹划分验证，能力资料核对模型身份、评测日期与原始任务分数。",
    83: "对生成机制或共同量尺不明的字段保留原始标记，后续结果分别注明经验估计、半合成校准或条件情景。",
    86: "问题一同时处理文档质量与训练配比。前者把22项异构信号转化为可复算的评分，并保留五维解释画像；后者在17域配比和13个验证领域损失之间估计局部响应。两类资料分开建模，再通过检验决定后续使用范围。",
    87: "质量模型采用A1固定参考分位及预先确定的用途目标；配比模型在单纯形正交坐标上拟合，并以1M留出、逐域误差和跨规模压力检验评价。问题一技术路线见图1。",
    91: "先按竞赛附件[5]和字段数据卡[6]核对质量信号含义。A1—A3保留272505条物理记录的全部22项字段；跨表去重后为261086个文本ID。列表字段保留原分量，并按冻结规则生成教育价值、流畅度、无广告程度、清洁度和可读性五个解释坐标。",
    92: "质量表示分为两层：Q_full覆盖22项信号，回答按既定规则如何评分；五维画像及DQ0用于解释评分差异。两层权重与方向均在观察训练Loss之前确定，字段合同列于附录A。",
    93: "逐项效用使用A1训练参考的中秩分位。五个有依据的正向信号采用高分位高效用；其余17项以A1训练集中DQ0最高20%文本的逐项中位分位为目标，按接近程度计分。QuRating四分量先各自转换后合为一项；词数、句数先取log(1+x)；缺失项赋中性值0.5并另报实测覆盖数。",
    94: "设第j项参考中的有效数为n_j，小于和等于x的记录数分别为n_<(x)、n_=(x)。中秩分位为[n_<(x)+n_=(x)/2]/n_j，并列记录得到相同分位。A2、A3沿用这一固定坐标。",
    97: "预先固定的六组相关诊断显示，DSIR三项在A1—A3的两两Spearman系数均超过0.99，具有明显冗余；词数与一元熵、句数的相关提示长度混杂。相关符号本身不足以判定语义冲突，图2保留有符号数值供后续分类。",
    101: "W0对规则效用等权，W1仅按A1内部相关性作去冗余对照，DQ0保留五维正向属性的摘要。三种表示服务于不同解释目的，领域次序的差别需在结果中并列呈现。",
    107: "当两项效用的绝对Spearman相关超过0.5，W1相应降低重复信号的权重；Q_full仍以W0等权为主。两种权重均未用训练Loss反向调节。",
    108: "逐样本评分按固定参考计算，领域均值按实际文本数汇总。跨领域汇总须说明采用文本数加权还是领域等权，两种权重代表不同总体。",
    110: "表4 质量评分的领域结果与五维对照",
    111: "A1七域中W0与W1的点估计次序一致；五维DQ0则把arxiv排在commoncrawl之前，与Q_full相反。A2、A3去重扩展与对应领域均值接近，说明同一标注体系的描述具有一定复现性。两种排序的差别来自评分用途与指标集合，故综合分须与五维解释层并报。",
    112: "五个核心信号构成正向解释坐标；其余17项按公布的用途目标进入Q_full。词数、句数、文本形态和DSIR相似性仍保留原始解释角色，相关或相似不被重复计作独立质量证据。",
    119: "图3展示五维领域画像。A1 arxiv的五项平均相对分位约为0.840、0.752、0.690、0.865、0.807，去重扩展为0.834、0.748、0.682、0.864、0.806；github的两层画像也接近。这是同标注体系的描述复现，尚需训练干预验证其效用。",
    120: "五项核心信号的第一主成分解释约48.11%的方差；“无广告”独立成组仅在九个分层中的三个复现。结果支持保留五维主画像，并以DQ0作为透明的辅助摘要。",
    121: "本文区分语义目标取舍和已定向信号的统计排序分歧。用同领域文本的中秩分位计算极端分歧率，以τ=0.80为主阈值，并用0.75、0.90检验敏感性；同时考察不并列文本对的逆序比例。",
    126: "42项候选中确认语义冲突为0，统计分歧为7，冗余候选5，尺度伪象12，领域反转3，尚未解决15。以可读性与无广告程度为例，τ=0.80时A1、A2去重扩展、A3去重扩展的极端分歧率分别为8.811%、13.332%、8.676%。分类结果表明综合评分需要明示用途，五维层仍须呈现相反评价。",
    138: "领域评分需检验表示方式对排序的影响。图4并列W0、W1和五维DQ0的A1七域次序：前两者相近，而五维摘要反转arxiv与commoncrawl的相对位置。A2、A3去重扩展用于同体系复核。",
    142: "训练阶段五折综合分数分别为M0 1.001578、M1 0.750417、M2 0.749715；M2的惩罚参数在训练阶段确定。参数与验收规则在读取A6—A11留出Loss前冻结，M3升级条件未触发。A7用于预定候选验收。",
    143: "表5与图5给出主要留出结果。1M下M1平均响应RMSE为0.2278，低于M0的0.2846；13个领域均改善，逐域RMSE平均由0.7129降至0.4540。M1−M0均方误差差的成对bootstrap区间为[−0.03949,−0.01893]；M2相对M1的差异区间跨零，因此保留较简洁的M1。",
    147: "跨规模时分别中心化观测与预测，仅比较配比响应的相对形状。60M的误差比为0.8876，呈部分迁移；1B达到3.108，明显劣于常数基准。A6与A8使用同一组配比，几何支持证据不重复计数。",
    150: "10B、70B估算表的13域平均中心化误差比分别为1.7295、2.1613；配比与训练点虽有重合，响应形状仍失配。两组估算Loss只用于压力检验，与1B迁移失败共同限定M1的使用范围。",
    151: "问题一得到可复算的22项综合评分、五维画像和1M附近的配比响应。质量评价是规则定义，配比收益是局部留出关联；后续质量情景与资源优化分别处理这两条证据链。",
    153: "图6汇总1M、60M、1B及10B/70B估算表的中心化误差比。1M局部成立、60M部分迁移，1B与估算外推失配；后续模型不继承通用跨规模配比系数。",
    159: "问题二先用B1的八条完整轨迹估计N—D响应，再检验弹性、替代和分组预测。B7提供半合成质量斜率，A表提供局部配比响应；两项均作为独立的条件扩展。问题二技术路线见图7。",
    162: "B1包括八个参数规模、每个规模147个检查点，共1176行；N与D分别以十亿参数、十亿token计。模型估计和验证均保留完整轨迹结构。",
    163: "以规模轨迹为留出单位，避免同一训练路径的检查点同时进入训练和测试。B2、B4、B5只比较各自来源内部的中心化响应形状。",
    164: "五参数形式分别表示Loss底值、参数与数据衰减幅度及各自指数，并与零响应、对数线性基准比较。12组预定初值收敛至相同极小值；Jacobian秩为5，条件数约33.83，说明本附件内的数值拟合稳定。",
    167: "在B1同一量尺中，按完整轨迹等权的均方误差估计加性幂律[1]；各轨迹行数相同，因此与逐行均方误差等价。正幅度和正指数保证模型内资源增加时预测Loss下降且边际改善递减。",
    173: "参数与误差适用于B1附件量尺。Pythia公开研究说明受控训练轨迹的用途[3]，但本附件的原始运行、验证语料和tokenizer尚未完全追溯，外部校准有待新证据。",
    180: "有限替代要求式（10）右端分母为正，且新配置仍位于支持范围。图8给出总Loss弹性；边际导数和等Loss替代分别由式（9）、式（10）及数值示例说明。在N=1、D=100时预测Loss为2.385578，N与D的总Loss弹性为−0.050447、−0.040100，等Loss对数替代率为−1.258018。N减少至0.8时D约需135.5586；减少至0.5时D约需315.8275，已超过支持上限299.893。",
    183: "图9并列B1八条轨迹的观测、拟合和残差。三类分组留出误差共同支持附件内部加性曲面的规则性；密集检查点属于同一训练过程，外部预测仍需共同量尺检验。",
    194: "三类留出均满足预定的B1内部用途容差。极端规模留出含单侧外推，其余规模主要是插值。200次整轨迹重抽样均有效，但原始轨迹只有八条，参数分位反映固定模型与当前资料的条件波动。",
    195: "B2、B4、B5来源内中心化误差相对零响应基准的中位比分别为0.855084、0.436601、0.555135。B3为派生插值；B9/B10的四条D=0记录不预测，另128条估算Loss只用于外推范围说明。",
    196: "B6为B7的精确子集，不重复计数。B7的450个唯一N—D—Q点构成45个单元，单元内Q—Loss斜率全为负，共同斜率−0.361995。加入规模调节后，留一规模的中心化宏RMSE由0.052964降至0.043679，检验的是半合成表内形状。",
    203: "表9的替代示例取N=1、D=100、ΔQ=0.1，分别固定另一资源计算。Q使用B7情景刻度；不同有效数据机制即使匹配局部斜率，也会给出不同的有限替代，因此该示例按条件情景解释。",
    206: "M1的配比代理对单纯形切向变化给出局部关联。1B迁移失败且严格凸包支持仅2/256，非零跨来源系数k_s缺少可估量尺。问题二据此形成B1幂律主干，以及分别标注来源的质量、配比条件扩展。",
    208: "图11展示200次整轨迹重抽样的五参数条件分位及α—β联合波动。所有重抽样有效且参数未触及边界；窄参数带只反映B1规则曲面和固定加性形式。",
    211: "图12上半部分显示B7单元质量斜率随N、D的变化，下半部分在假定运输系数下计算有限替代。Q由0.5升至0.6、λ=1时，N或D的减少比例各自固定另一资源，不相加为总节约。",
    214: "问题二的主结果是B1量尺中的N—D曲面及边际替代。B7斜率刻画半合成质量响应，A表配比关联限定于局部；后续预算基线仅使用已验证的B1曲面。",
    217: "问题三在给定FLOPs预算下配置参数量、训练数据量和条件情景中的质量投入。先统一成本单位与统计支持域，再用解析解确定基线配置，以数值解核对，并比较成本形式、上下文和配比情景。问题三技术路线见图13。",
    218: "预算是上限，达到N、D统计支持界后可以闲置。由此可区分内点配置、数据上界活跃及双上界平台；这些是模型约束状态，不是现实训练收益的终点。",
    220: "训练、注意力和质量处理成本均采用题设形式。N、D以十亿计，前两项换算乘10¹⁸，按token支付的质量成本乘10⁹；上下文L_ctx作为外生档位，η=0.0002，参考Q0=0.5为情景值。",
    225: "主规格关闭质量收益与配比运输，最小化B1内部Loss。支持域为N∈[0.070542,11.965825]、D∈[0.134,299.893]；Q固定0.5，p取训练均值。矩形表示统计范围，内部并非每点都有独立实验。",
    231: "固定上下文且质量成本增量为零时，目标随N、D增大而下降。若两支持上界都可承担，直接取两上界；否则预算紧约束给出ND=K=c/k。代入幂律并令x=logN后，目标的非恒定部分严格凸，内点由唯一一阶条件确定：",
    239: "51档预算、每档四个SLSQP初值共204次对照均成功，解析解与数值解的最大目标差为4.86×10⁻¹³，最大投影KKT残差为2.78×10⁻¹⁷。这核验了条件优化问题的求解精度。",
    240: "按活跃约束定义结构转移。图14显示，预算约9.325359×10²¹时D先达到299.893；约2.300064×10²²时N和D同时达到支持上界。此后模型内Loss为2.093379，10²⁴预算只使用约2.3001%。平台来自支持域约束。",
    253: "固定Q后的一维N问题只有唯一内点或边界解；质量外层可出现不同局部谷。数值求解因此检查端点、网格和多组初值，选取与加密网格一致的条件解。",
    254: "图16和表12按两个支持界阈值呈现51档预算路径。固定上下文2048且质量收益关闭时，已使用算力内部的训练与注意力比例不随预算发生转移；高预算总份额变化来自预算闲置。",
    260: "基线资源配置首先由B1曲面和题设成本确定。配比收益在主规格中取零：A来源的局部响应虽可用于有限候选比较，但跨规模运输证据不足。",
    269: "主规格的配置对应B1支持域和题设FLOPs成本。以下质量、上下文与配比比较均在各自明示的条件下报告。",
    270: "在10¹⁹预算和对数质量成本下，局部启动门槛约0.472240，全局门槛约0.235678；参考条件收益0.361995处于两者之间。图18显示小幅增加Q与有限跃迁的不同判断，这是半合成收益接入题设成本后的条件机制。",
    274: "图19给出五档外生上下文的成本敏感性。10¹⁹预算下，上下文从2048增至131072，基线Loss由2.998935升至3.367161；模型目标中没有另计长上下文的能力收益。成本项相等的L_ctx=30000由6/η解析得到。",
    278: "图20区分预算约束的影子价与质量上界的边际价值。基线10¹⁹ FLOPs处归一预算乘子约0.020096，有限差分与解析值相差约4.73×10⁻¹³；两支持上界活跃后乘子为零。",
    283: "问题三给出可复核的基线预算路径和条件质量、配比及上下文情景。参数传播带反映B1源内稳定性，机制包络反映收益搬运、成本形式与支持域选择；两类不确定性分别解释。",
    286: "问题四先从同口径原始任务分数构造历史前沿，再检验Loss—能力桥接、参数关联和动态外推。桥接未通过留一规模比较，因此能力预测直接使用评测分数。问题四技术路线见图21。",
    287: "图22将853条合格模型的六项原始得分均值与28天90%分位并列；前沿由2024年6月的36.453升至2025年3月的52.333。该分位刻画近期较高表现的筛选群体，允许随样本构成回落。",
    290: "六任务能力变化并不均衡。图23左栏按相同原始量尺列出端点增量，MATH Lvl 5约增加34.02分，MUSR约增加2.53分；右栏是同一描述回归规格下的参数关联分量。两栏分别反映任务变化与统计关联。",
    294: "C8提供逐任务评测，C1提供模型身份与参数，C9用于可用性和异常筛选。按完整ID、参数差异不超过2%、六任务完整、已报告许可证、模型可用及无异常标记筛选，得到853条主样本：基础预训练92条、对话或微调539条、合并221条、其他1条。",
    295: "日期采用评测文件时间。C1中81个重复ID对应的162行整组排除；C8的1958个文件中4个截断文件记入审计但不解析，每个模型目录取最新可解析记录。C3早期分数与主分析量尺不同；C4训练D记录稀少且口径混合。",
    298: "按六项原始任务得分等权形成0—100分能力值，再取每个28天窗口的90%分位，窗口至少包含15个模型。2024-06-16至2025-03-14的前沿增量为15.87965分。该定义区别于C1归一化Average，也区别于全生态累计最高纪录。",
    302: "七个相对可比的Pythia规模上，线性和单调候选的留一规模RMSE分别为0.552834、0.436635，均高于均值基准0.424448。满足主样本C1参数一致性的只有两条，图24展示候选拟合与留出误差。检验结果不支持将B1 Loss数值转换为C8能力分数。",
    305: "因此Q2、Q3的Loss保留原附件量尺，Q4在C8任务分数空间独立预测。负向桥接检验决定了四问如何衔接。",
    311: "主样本853条记录中仅九条训练D非空；同时满足同阶段N、D与C4 compute可用定义的只有六条。完整N—D贡献由此无法估计。本文先以类型和家族效应控制的回归描述参数关联。",
    315: "主规格θ_N=4.595943，参数关联分量增加2.703245分，调整残差增加13.176404分，分别占前沿增量的17.0233%和82.9767%。图25展示这两个描述分量；后者包括未观测训练D、算法、架构、后训练、家族构成和评测波动。",
    318: "表14显示参数关联比例对筛选和起点敏感：只保留已知家族、严格许可证或较晚起点时可变为负值。固定端点、仅重抽系数得到的条件区间为[13.90%,23.00%]，与这些定义变化分别报告。",
    320: "各家族时间趋势并不一致。六条可用基础模型上的raw6=截距+b_N lnN+b_D lnD仅作描述性敏感性；留一实体后系数大幅波动，结果不运输到853条前沿样本。",
    323: "预定比较持续性、截断线性、有界logit线性和最近13周局部logit四种动态模型。以至少16个历史周端点训练并滚动预测，现有资料只允许4周20折和13周11折回测；表16报告各模型MAE。",
    328: "logit反变换使预测留在0—100分量尺内，不构成真实能力饱和的经验结论。固定历史中点的分段趋势未得到信息准则支持，故保留单趋势。",
    329: "滚动窗口重叠，折次不独立；资料保留的是模型最新评测记录，尚非完整历史榜单快照。因此回测属于现有资料下的拟样本外检验。",
    331: "主规格参数关联份额为17.02%，但家族和筛选群体改变后可出现不同方向。图26并列同家族趋势与2027年条件中心的群体敏感性，供解释全局时间系数。",
    336: "预测原点为2026-09-25，末次观测为2025-03-14，相隔560天。2027-09-25和2028-09-25分别距末次观测约30和42个月；表17与图27同时给出目标日期、条件中心、条件模型区间和独立的模型范围。",
    340: "条件模型区间由四周循环残差块重抽样构造[4]：1000次重抽后重新估计冻结模型，并按残差标准差乘sqrt(1+h/4)的假定扩散规则加入未来扰动。95%分位只对应这一模型与扩散设定。",
    341: "表17最后一列为四个预定动态模型的中心预测范围，用于显示模型选择敏感性；它与前一列的条件模型区间含义不同。",
    342: "外生放缓情景另取透明的正增长参照。历史前沿排序邻点的插值lnN在2024-06-16至2025-03-14两端相差0.588181，跨38.714周，端点斜率为每周0.015193。若从预测原点起假设训练D固定且C≈6ND，此路径作为参考对数compute增长；全时段参数分量趋势−0.029739分/周并未被改写为正向经验增长。",
    344: "ρ=1为原动态模型条件中心，ρ=0.5和0为外生增长保留比例。用θ_N=4.595943分/lnN在能力分数空间平移参考路径，表18给出2027、2028两期限的条件中心。",
    346: "表18不给未来情景分配概率；表17的条件95%区间只对应ρ=1。固定训练D和正增长端点路径均属外生设定，情景差值按假设路径解释。",
    349: "现有动态验证覆盖4周和13周，logit模型MAE分别为1.7566、1.5293；26周和52周没有可用折次。图28并列四种预定模型的滚动误差与条件覆盖，显示长期区间尚缺同期限检验。",
    353: "原规模代理采用全时段非正的参数分量趋势，三条放缓路径因此重合。图29改用另行声明的正增长端点参照，并固定训练D；灰蓝区间仍只属于ρ=1原模型。",
    356: "两期限的参考中心为79.76、87.13；中度放缓为77.93、83.48；强放缓为76.11、79.84。差异是冻结参数关联系数作用于外生路径的条件结果；实际能力还会随训练D、算法和评测规则变化。",
    359: "本节按真正留出的单位汇总检验。Q1留出训练运行，Q2留出规模轨迹与前向块，Q3比较解析和数值解，Q4对现有历史端点作短期滚动回测。误差保留原附件量尺，表19列出各问的检验对象和结论范围。",
    360: "Q1的1M留出RMSE由0.2846降至0.2278，13域均改善；1B中心化误差比为3.108，限定跨规模使用。Q2三类分组宏RMSE依次约为0.000146888、0.000111642、0.000114134，支持B1附件内部曲面的规则性。",
    361: "Q4桥接的线性、单调候选RMSE为0.552834、0.436635，均高于均值基准0.424448；能力预测改用原始任务分数。前沿模型仅有4周和13周回测，未来12和24个月条件区间尚无同期限覆盖检验。",
    362: "Q3的最大解析—数值目标差为4.86×10⁻¹³，属于求解精度检查；没有独立真实最优配置作外部标签。各问的检验单位、比较基准和未覆盖对象见表19。",
    364: "总体上，Q1支持局部配比关联，Q2支持来源内曲面，Q3支持题设条件下的数值最优性，Q4的桥接检验阻断Loss到能力分数的直接换算。",
    366: "质量评价比较W0、W1与五维DQ0：前两者在A1七域点估计次序一致，五维摘要则反转arxiv与commoncrawl的相对次序。分歧阈值0.75、0.80、0.90用于检查统计分类的稳健性。",
    367: "预算配置对机制设定更敏感。同一半合成质量收益下，指数、幂函数和对数成本的条件最优Q约为0.675、0.507、1.000；上下文由2048增至131072时，10¹⁹预算的基线Loss由2.998935升至3.367161。",
    368: "能力分解的17.02%参数关联份额随群体筛选和时间起点变化，可出现负值。预测分别呈现条件模型区间、四模型中心范围及ρ=1、0.5、0的外生情景中心，三者对应不同不确定性来源。",
    369: "表20汇总已实际运行的权重、支持域、成本和预测结构敏感性。参数抽样带的宽窄应与机制情景和群体选择分开解读。",
    371: "综合而言，B1参数传播在既定曲面内较稳定；质量收益搬运、支持域选择、家族筛选和长期模型结构对解释影响更大。",
    374: "模型首先以公开规则处理22项异构质量信号，同时保留五维画像，使综合评分可复算且可解释。统计分歧与语义目标取舍分别识别，避免凭相关符号判断指标冲突。",
    375: "验证设计尊重资料依赖结构：配比模型留出训练运行并报告13域结果，标度律留出完整轨迹与前向块，资源优化将解析解、数值核验及活跃约束并列。",
    376: "跨问传递始终连同量尺与支持域报告。B7质量斜率作为半合成校准，配比规模迁移由留出检验裁定；能力预测把条件区间、模型范围和外生增长情景分别呈现。",
    379: "主要限制来自资料和量尺。Q_full的部分方向取决于评价用途；A、B表缺少同运行质量—配比—损失键，真实质量弹性与跨来源配比系数尚未识别。B1外部训练来源和共同Loss锚需进一步核对，Q3最优配置只针对题设成本代理及统计支持域。",
    380: "C8训练D记录不足，参数关联与调整残差不能分解为完整规模和纯技术效应；Q4增长情景依赖外生路径及固定D。能力观测止于2025年3月，距预测原点560天，长期区间缺同期限验证。这些限制决定了条件配置与前沿预测的应用范围。",
    383: "后续可增加同文本人工目标标注与配对训练干预，检验Q_full用途目标是否对应真实训练收益。对长度、数字比例和DSIR相似性等指标，可按语言、领域和任务设置参考画像，再用新增样本检验排序稳定性。",
    384: "标度律研究需要补齐验证集、tokenizer和训练阶段信息，建立跨附件共同Loss锚；质量与配比系数应在多规模真实训练中配对估计。资源优化还需实际数据供应、处理成本和长上下文收益。",
    385: "能力预测应补充2025年3月之后的同口径逐任务评测、训练token和历史榜单快照。积累足够长的序列后，分别进行时间外推、家族外检验，并在12与24个月同期限校准区间。",
    388: "可迁移的是分析顺序：先确定指标方向与用途，再核对资源响应的量尺和支持域，随后给出预算成本与活跃约束，最后分别处理预测参数、模型与情景不确定性。新任务仍需重估具体评分权重、幂律系数和成本。",
    389: "本题形成规则明确的22项质量分、1M范围内的局部配比响应、B1内部的规模—数据替代曲面，以及题设成本下的条件资源配置。能力前沿预测由C8同口径任务分数独立完成，并随观测更新继续检验。",
    416: "Q1经验支持分类为：A6/A8各256组配比的IN/NEAR/OUT数量为2/252/2，A10的64组为15/46/3；域外样本不足以单独估计稳定误差。Q2在B2/B4/B5的来源内中心化形状比分别约0.855/0.437/0.555。Q4原非正参数趋势使旧放缓路径重合，正文另用已声明的外生正增长参照。",
}

DELETE = {
    67, 68, 88, 89, 96, 109, 152, 156, 160, 166, 207,
    226, 227, 229, 273, 275, 282, 299, 309, 310, 330, 334,
    347, 348, 352, 363, 377, 386, 390, 391, 279,
}

FIGURE_TITLES = {
    1: "六组质量信号的相关性",
    2: "五维质量的领域画像",
    3: "质量评分规则下的领域排序",
    4: "1M留出样本的逐领域预测误差",
    5: "配比响应的跨规模误差",
    6: "参数与数据对总Loss的弹性",
    7: "B1训练轨迹的拟合与残差",
    8: "标度律的分组验证误差",
    9: "幂律参数的整轨迹重抽样",
    10: "B7质量响应与条件替代",
    11: "基线资源配置与Loss路径",
    12: "质量成本情景的最优路径",
    13: "预算构成与支持界转移",
    14: "参数传播与机制情景范围",
    15: "质量投入的局部与全局门槛",
    16: "上下文成本敏感性",
    17: "预算与质量的影子价",
    18: "C8六任务能力前沿",
    19: "六任务前沿变化及参数关联",
    20: "Loss—Benchmark桥接检验",
    21: "前沿变化的参数关联分解",
    22: "家族趋势与群体敏感性",
    23: "能力前沿的条件预测",
    24: "前沿模型的滚动验证",
    25: "外生增长放缓情景",
}

ROUTES = [
    ("Q1", 90, 1, "问题一技术路线", [
        ("数据整理", "A1—A3 质量信号\nA4—A5 领域配比"),
        ("模型构造", "固定分位与Q_full\n正交配比响应M1"),
        ("独立检验", "去重扩展与1M留出\n跨规模压力检验"),
        ("输出", "质量画像与局部响应\n证据与支持范围"),
    ]),
    ("Q2", 161, 7, "问题二技术路线", [
        ("数据分层", "B1 八条训练轨迹\nB7及A表条件资料"),
        ("模型建立", "N—D加性幂律\n质量与配比情景项"),
        ("模型检验", "整轨迹及前向留出\n联合参数重抽样"),
        ("结果解释", "边际弹性与等Loss替代\n来源内及条件结论"),
    ]),
    ("Q3", 219, 13, "问题三技术路线", [
        ("输入", "B1冻结曲面\n题设FLOPs成本"),
        ("约束求解", "统一单位与支持域\n解析内点及活跃界"),
        ("数值核验", "51档预算与204次对照\n质量成本情景"),
        ("配置分析", "基线预算路径\n上下文与参数敏感性"),
    ]),
    ("Q4", 287, 21, "问题四技术路线", [
        ("样本构造", "C1/C8/C9身份筛选\n六项原始任务得分"),
        ("历史分析", "28天九成分位前沿\nLoss桥接留出检验"),
        ("动态建模", "参数关联与剩余分量\n四模型短期滚动"),
        ("条件预测", "12与24个月目标\n外生增长保留情景"),
    ]),
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def set_east_asian_font(style, font: str, size: float, bold: bool | None = None) -> None:
    style.font.name = "Times New Roman"
    style.font.size = Pt(size)
    if bold is not None:
        style.font.bold = bold
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.insert(0, rfonts)
    rfonts.set(qn("w:eastAsia"), font)


def rewrite_text(doc, originals: list) -> None:
    for i, replacement in {**HEADING_REWRITES, **REWRITES}.items():
        originals[i].text = replacement
    # Give Latin variables, attachment IDs and numerals breathing room in Chinese
    # prose; leave equation and table XML untouched.
    for i in REWRITES:
        p = originals[i]
        if p.style and p.style.name == "PaperBody":
            value = re.sub(r"(?<=[\u4e00-\u9fff])(?=[A-Za-z0-9])", " ", p.text)
            value = re.sub(r"(?<=[A-Za-z0-9])(?=[\u4e00-\u9fff])", " ", value)
            p.text = value
    heading_map = {old: originals[i].text for i, old in
                   ((i, p.text) for i, p in enumerate(Document(SOURCE).paragraphs))
                   if old != originals[i].text and i in HEADING_REWRITES}
    for p in originals:
        if p.style and p.style.name == "PaperTOC":
            name, sep, page = p.text.partition("\t")
            if name in heading_map:
                p.text = heading_map[name] + sep + page


def map_figure_number(old: int) -> int:
    if old <= 5:
        return old + 1
    if old <= 10:
        return old + 2
    if old <= 17:
        return old + 3
    return old + 4


def renumber_figures(originals: list) -> None:
    pattern = re.compile(r"(?<![\d])图(\d+)(?![-—\d])")
    for p in originals:
        if p.style is None:
            continue
        if p.style.name == "PaperCaption":
            m = re.match(r"^图(\d+)\s", p.text)
            if m:
                old = int(m.group(1))
                p.text = f"图{map_figure_number(old)} {FIGURE_TITLES[old]}"
            continue
        if p.style.name not in ("PaperBody", "PaperH2", "PaperH3"):
            continue
        updated = pattern.sub(lambda m: f"图{map_figure_number(int(m.group(1)))}", p.text)
        if updated != p.text:
            p.text = updated


def remove_paragraph(paragraph) -> None:
    element = paragraph._element
    element.getparent().remove(element)


def move_before(paragraph, target) -> None:
    target._element.addprevious(paragraph._element)


def draw_route(out: Path, boxes: list[tuple[str, str]]) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (2600, 500), "white")
    dr = ImageDraw.Draw(img)
    bold_path = Path(r"C:\Windows\Fonts\simhei.ttf")
    regular_path = Path(r"C:\Windows\Fonts\simsun.ttc")
    if not bold_path.exists():
        bold_path = regular_path
    bold = ImageFont.truetype(str(bold_path), 60)
    body = ImageFont.truetype(str(regular_path), 49)
    xs = [36, 676, 1316, 1956]
    for i, (heading, detail) in enumerate(boxes):
        x0, x1 = xs[i], xs[i] + 556
        dr.rectangle((x0, 82, x1, 408), outline="black", width=4)
        dr.line((x0 + 25, 192, x1 - 25, 192), fill="black", width=2)
        hb = dr.textbbox((0, 0), heading, font=bold)
        dr.text(((x0 + x1 - (hb[2] - hb[0])) / 2, 111), heading, font=bold, fill="black")
        for k, line in enumerate(detail.split("\n")):
            bb = dr.textbbox((0, 0), line, font=body)
            dr.text(((x0 + x1 - (bb[2] - bb[0])) / 2, 230 + 72 * k), line,
                    font=body, fill="black")
        if i < 3:
            ax, ay = x1 + 10, 245
            dr.line((ax, ay, xs[i + 1] - 18, ay), fill="black", width=5)
            dr.polygon([(xs[i + 1] - 18, ay - 13), (xs[i + 1] - 18, ay + 13),
                        (xs[i + 1] - 2, ay)], fill="black")
    img.save(out, dpi=(400, 400))


def insert_route(anchor, filename: Path, number: int, title: str) -> None:
    fig = anchor.insert_paragraph_before()
    fig.style = "Normal"
    fig.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fig.paragraph_format.space_before = Pt(7)
    fig.paragraph_format.space_after = Pt(2)
    fig.paragraph_format.keep_with_next = True
    fig.add_run().add_picture(str(filename), width=Inches(6.2))
    cap = anchor.insert_paragraph_before(f"图{number} {title}", style="PaperCaption")
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_after = Pt(8)


def set_repeat_header(row) -> None:
    trpr = row._tr.get_or_add_trPr()
    if trpr.find(qn("w:tblHeader")) is None:
        trpr.append(OxmlElement("w:tblHeader"))


def set_cant_split(row) -> None:
    trpr = row._tr.get_or_add_trPr()
    if trpr.find(qn("w:cantSplit")) is None:
        trpr.append(OxmlElement("w:cantSplit"))


def add_border(parent, side: str, size: int) -> None:
    border = OxmlElement(f"w:{side}")
    border.set(qn("w:val"), "single")
    border.set(qn("w:sz"), str(size))
    border.set(qn("w:color"), "000000")
    parent.append(border)


def three_line_table(table) -> None:
    tblpr = table._tbl.tblPr
    for child in list(tblpr):
        if child.tag == qn("w:tblBorders"):
            tblpr.remove(child)
    borders = OxmlElement("w:tblBorders")
    add_border(borders, "top", 12)
    add_border(borders, "bottom", 12)
    tblpr.append(borders)
    set_repeat_header(table.rows[0])
    for ri, row in enumerate(table.rows):
        set_cant_split(row)
        for cell in row.cells:
            tcpr = cell._tc.get_or_add_tcPr()
            for child in list(tcpr):
                if child.tag in (qn("w:shd"), qn("w:tcBorders")):
                    tcpr.remove(child)
            if ri == 0:
                cb = OxmlElement("w:tcBorders")
                add_border(cb, "bottom", 6)
                tcpr.append(cb)
            for p in cell.paragraphs:
                p.paragraph_format.space_before = Pt(1)
                p.paragraph_format.space_after = Pt(1)
                p.paragraph_format.line_spacing = 1.0
                for run in p.runs:
                    run.font.name = "Times New Roman"
                    run.font.size = Pt(10.5)
                    if ri == 0:
                        run.bold = True
                    rpr = run._r.get_or_add_rPr()
                    rfonts = rpr.find(qn("w:rFonts"))
                    if rfonts is None:
                        rfonts = OxmlElement("w:rFonts")
                        rpr.insert(0, rfonts)
                    rfonts.set(qn("w:eastAsia"), "宋体")


def remove_package_thumbnail(path: Path) -> None:
    target = path.with_suffix(".cleaning.docx")
    with ZipFile(path) as src, ZipFile(target, "w", ZIP_DEFLATED) as dst:
        for item in src.infolist():
            if item.filename.startswith("docProps/thumbnail."):
                continue
            data = src.read(item.filename)
            if item.filename == "_rels/.rels":
                root = etree.fromstring(data)
                for rel in list(root):
                    if "metadata/thumbnail" in rel.get("Type", ""):
                        root.remove(rel)
                data = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
            elif item.filename == "[Content_Types].xml":
                root = etree.fromstring(data)
                for part in list(root):
                    if "thumbnail" in part.get("PartName", "").lower():
                        root.remove(part)
                data = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
            dst.writestr(item, data)
    target.replace(path)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    doc = Document(SOURCE)
    original = list(doc.paragraphs)
    old_title = original[7].text
    renumber_figures(original)
    rewrite_text(doc, original)
    # Put the marginal comparison directly after the elasticity figure. Lead the
    # parameter propagation figure with its main result rather than a caveat.
    for idx in (119, 120):
        move_before(original[idx], original[117])
    for idx in (186, 187, 188):
        move_before(original[idx], original[183])
    move_before(original[268], original[266])
    for i in sorted(DELETE, reverse=True):
        remove_paragraph(original[i])

    styles = doc.styles
    h3 = styles["PaperH3"] if "PaperH3" in styles else styles.add_style("PaperH3", WD_STYLE_TYPE.PARAGRAPH)
    h3.base_style = styles["PaperBody"]
    for name, east, size, bold in [
        ("Normal", "宋体", 12, False), ("Title", "黑体", 16, True),
        ("PaperH1", "黑体", 14, True), ("PaperH2", "黑体", 12, True),
        ("PaperH3", "宋体", 12, True), ("PaperBody", "宋体", 12, False),
        ("PaperCaption", "宋体", 12, False), ("PaperTOC", "宋体", 12, False),
        ("PaperRef", "宋体", 12, False), ("PaperEquation", "宋体", 12, False),
    ]:
        set_east_asian_font(styles[name], east, size, bold)
    styles["PaperH1"].paragraph_format.space_before = Pt(11)
    styles["PaperH1"].paragraph_format.space_after = Pt(7)
    styles["PaperH2"].paragraph_format.space_before = Pt(8)
    styles["PaperH2"].paragraph_format.space_after = Pt(4)
    styles["PaperH3"].paragraph_format.space_before = Pt(7)
    styles["PaperH3"].paragraph_format.space_after = Pt(3)
    styles["PaperBody"].paragraph_format.space_after = Pt(1)
    styles["PaperTOC"].paragraph_format.space_after = Pt(0)
    styles["PaperRef"].paragraph_format.left_indent = Inches(0.28)
    styles["PaperRef"].paragraph_format.first_line_indent = Inches(-0.28)

    for p in doc.paragraphs:
        if p.style is None:
            continue
        if re.match(r"^\d+\.\d+\.\d+\s", p.text) and p.style.name == "PaperH2":
            p.style = h3
        if p.style.name == "PaperH1":
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.keep_with_next = True
        elif p.style.name in ("PaperH2", "PaperH3"):
            p.paragraph_format.keep_with_next = True
        elif p.style.name == "PaperCaption":
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.keep_together = True
            if p.text.startswith("表"):
                p.paragraph_format.keep_with_next = True
        elif p.style.name == "PaperBody":
            p.paragraph_format.widow_control = True

    for qid, anchor_index, number, title, boxes in ROUTES:
        path = FIG_DIR / f"SCHEM-{qid}-V6-001.png"
        draw_route(path, boxes)
        insert_route(original[anchor_index], path, number, title)

    # Academic tables only. The official cover information table keeps its template.
    for table in doc.tables[1:]:
        three_line_table(table)

    doc.core_properties.title = original[7].text
    for field in ("author", "last_modified_by", "comments", "keywords", "identifier"):
        setattr(doc.core_properties, field, "")
    out = OUT / (STEM + ".docx")
    doc.save(out)
    remove_package_thumbnail(out)
    manifest = {
        "source": str(SOURCE.relative_to(ROOT)), "source_sha256": sha(SOURCE),
        "docx": str(out.relative_to(ROOT)), "docx_sha256": sha(out),
        "title_before": old_title, "title_after": original[7].text,
        "removed_redundant_paragraphs": sorted(DELETE),
        "rewritten_paragraphs": len(REWRITES),
        "diagram_ids": [f"SCHEM-{qid}-V6-001" for qid, *_ in ROUTES],
        "academic_tables_three_line": len(doc.tables) - 1,
        "original_figure_count": len(FIGURE_TITLES), "total_figure_captions": 29,
    }
    (ROOT / "08_paper/v6").mkdir(parents=True, exist_ok=True)
    (ROOT / "08_paper/v6/BUILD_MANIFEST_v6.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
