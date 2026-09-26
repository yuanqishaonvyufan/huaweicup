# F 题最终稿附录 E 代码材料

本目录对应 `11_delivery/v7/F_final_candidate_v7_最终投稿版.docx`。

GitHub 分支：[`final-v7-codebook-20260926`](https://github.com/yuanqishaonvyufan/huaweicup/tree/final-v7-codebook-20260926/04_code/final_v7_codebook)。

- `E1.md`—`E4.md`：论文附录 E 的核心代码段和用途说明。
- `appendix_e/*.py`：附录中展示的主要模型函数，省去完整程序的路径、运行记录和交付检查代码。
- `Q1.md`—`Q4.md`：逐问完整支撑源程序快照、SHA-256、输入结果入口及 Codex 提示词。
- `Q1_manifest.json`—`Q4_manifest.json`：完整支撑程序文件、行数和哈希清单。
- `prompts/ALL.md`：可直接粘贴到 Codex 的总提示词。
- `11_delivery/v7/附录E_主要源程序及支撑材料.docx`：合并后的 Word 附录。

附录核心函数来自当前研究代码和冻结规格。重新计算时，请遵守项目 `PROJECT_RULES.md` 和 `09_handoff/PROJECT_STATE.md`；正式运行具有固定编号，必须在隔离副本内复算，不能覆盖已登记输入或结果。

## 生成

在项目根目录运行：

```powershell
python 04_code/final_v7_codebook/build_appendix_e.py --docx "11_delivery/v7/附录E_主要源程序及支撑材料.docx"
```

构建 Word 只读取已登记的源码和清单，不运行建模实验。
