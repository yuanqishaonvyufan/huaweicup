"""Modeling Phase 1 Round 1: read-only full A1-A3 quality-signal audit.

Run from the project root with:
    python 04_code/data_audit/modeling_phase1_q1_audit.py

Outputs are audit/structure diagnostics, never a final Q score or model fit.
"""

from __future__ import annotations

import csv
import hashlib
import json
import lzma
import math
from array import array
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import squareform
from scipy.stats import kurtosis, rankdata, skew


ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "01_data" / "raw" / "real_attachments"
OUT = ROOT / "01_data" / "audits" / "modeling_phase1" / "q1"
FIG = OUT / "figures"
MAPPING = ROOT / "03_models" / "modeling_phase1" / "q1" / "A1_A3_OFFICIAL_MAPPING_v1.csv"
RAW_MANIFEST = ROOT / "01_data" / "raw" / "RAW_SHA256.csv"
SOURCE_PDF = ROOT / "00_problem" / "original" / "F_2026_data_description_user_supplied.pdf"
SOURCE_PDF_SHA = "f5c851bb e4b3d8c9079609c37f2c3b0835244067711d6d761c66adeaa8357835".replace(" ", "")
RUN_ID = "AUDIT-Q1-QUALITY-20260924-v1"

SIGNALS = [
    "fineweb_edu", "fluency_en", "modernbert_cleanliness", "modernbert_readability",
    "modernbert_reasoning", "modernbert_professionalism", "dsir_books", "dsir_wiki",
    "dsir_math", "qurater", "ad_en", "rps_doc_word_count",
    "rps_doc_num_sentences", "rps_doc_unigram_entropy", "rps_doc_frac_unique_words",
    "rps_doc_frac_no_alph_words", "rps_doc_frac_chars_top_2gram",
    "rps_doc_frac_chars_top_3gram", "rps_lines_uppercase_letter_fraction",
    "rps_lines_ending_with_terminal_punctution_mark",
    "rps_lines_numerical_chars_fraction", "rps_doc_mean_word_length",
]
LIST_LENGTHS = {"fineweb_edu": 1, "fluency_en": 2, "modernbert_cleanliness": 6,
                "modernbert_readability": 6, "modernbert_reasoning": 6,
                "modernbert_professionalism": 6, "qurater": 4, "ad_en": 2}
ASSIST_A1 = {"id", "content", "sub_path", "_source_domain", "_source_path"}
ASSIST_EXT = {"id", "sub_path"}

# Directions describe candidate interpretation, not a finished quality scale.
# The dataset card distinguishes text quality from length, genre and similarity.
META = {
    "fineweb_edu": ("Educational value score", "raw model score", "POSITIVE_CANDIDATE", "list[0]"),
    "fluency_en": ("Binary fluency logits [not fluent, fluent]", "logits", "POSITIVE_CANDIDATE", "logit[1]-logit[0]"),
    "modernbert_cleanliness": ("Formatting/completeness/noise rating logits 0-5", "logits", "POSITIVE_CANDIDATE", "softmax expected level"),
    "modernbert_readability": ("Clarity/coherence rating logits 0-5", "logits", "POSITIVE_CANDIDATE", "softmax expected level"),
    "modernbert_reasoning": ("Reasoning-complexity rating logits 0-5", "logits", "DIRECTION_UNRESOLVED", "softmax expected level"),
    "modernbert_professionalism": ("Required expertise/professionalism logits 0-5", "logits", "DIRECTION_UNRESOLVED", "softmax expected level"),
    "dsir_books": ("Similarity/importance relative to Books", "raw DSIR score, scale unresolved", "DIRECTION_UNRESOLVED", "identity"),
    "dsir_wiki": ("Similarity/importance relative to Wikipedia", "raw DSIR score, scale unresolved", "DIRECTION_UNRESOLVED", "identity"),
    "dsir_math": ("Similarity/importance relative to AutoMathText", "raw DSIR score, scale unresolved", "DIRECTION_UNRESOLVED", "identity"),
    "qurater": ("Four facets: style, expertise, facts, education", "four raw ratings", "DIRECTION_UNRESOLVED", "mean of 4 diagnostic only"),
    "ad_en": ("Binary ad logits [has ad, no ad]", "logits", "POSITIVE_CANDIDATE", "logit[1]-logit[0]"),
    "rps_doc_word_count": ("Normalized word count", "words", "DIRECTION_UNRESOLVED", "identity"),
    "rps_doc_num_sentences": ("Sentence count", "sentences", "DIRECTION_UNRESOLVED", "identity"),
    "rps_doc_unigram_entropy": ("Unigram entropy", "raw entropy, base unresolved", "DIRECTION_UNRESOLVED", "identity"),
    "rps_doc_frac_unique_words": ("Unique-word fraction", "percent-like raw scale", "DIRECTION_UNRESOLVED", "identity"),
    "rps_doc_frac_no_alph_words": ("Nonalphabetic-word fraction", "percent-like raw scale", "DIRECTION_UNRESOLVED", "identity"),
    "rps_doc_frac_chars_top_2gram": ("Character concentration in top 2-gram", "percent-like raw scale", "DIRECTION_UNRESOLVED", "identity"),
    "rps_doc_frac_chars_top_3gram": ("Character concentration in top 3-gram", "percent-like raw scale", "DIRECTION_UNRESOLVED", "identity"),
    "rps_lines_uppercase_letter_fraction": ("Uppercase-letter ratio", "percent-like raw scale", "DIRECTION_UNRESOLVED", "identity"),
    "rps_lines_ending_with_terminal_punctution_mark": ("Lines ending with terminal punctuation", "percent-like raw scale", "DIRECTION_UNRESOLVED", "identity"),
    "rps_lines_numerical_chars_fraction": ("Numeral-character ratio", "percent-like raw scale", "DIRECTION_UNRESOLVED", "identity"),
    "rps_doc_mean_word_length": ("Mean normalized word length", "characters/word", "DIRECTION_UNRESOLVED", "identity"),
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def scalar_value(signal: str, value: object) -> tuple[float, str, list[float]]:
    if value is None:
        return math.nan, "NULL", []
    if signal in LIST_LENGTHS:
        if not isinstance(value, list):
            return math.nan, "WRONG_TYPE", []
        try:
            components = [float(v) for v in value]
        except (TypeError, ValueError):
            return math.nan, "NONNUMERIC_LIST", []
        if len(components) != LIST_LENGTHS[signal] or not all(math.isfinite(v) for v in components):
            return math.nan, f"BAD_LENGTH_OR_NONFINITE:{len(components)}", components
        if signal == "fineweb_edu":
            result = components[0]
        elif signal in ("fluency_en", "ad_en"):
            result = components[1] - components[0]
        elif signal == "qurater":
            result = float(np.mean(components))  # structure diagnostic only
        else:
            logits = np.asarray(components, dtype=float)
            weights = np.exp(logits - logits.max())
            weights /= weights.sum()
            result = float(np.dot(weights, np.arange(len(logits))))
        return result, "OK", components
    try:
        result = float(value)
    except (TypeError, ValueError):
        return math.nan, "NONNUMERIC", []
    return (result, "OK", []) if math.isfinite(result) else (math.nan, "NONFINITE", [])


def validate_mapping() -> tuple[list[dict[str, str]], dict[str, str], str]:
    if sha256(SOURCE_PDF) != SOURCE_PDF_SHA:
        raise ValueError("Official data-description PDF hash changed; stop official mapping")
    with MAPPING.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    if [row["official_id"] for row in rows] != ["A1", "A2", "A3"]:
        raise ValueError("Official A1-A3 IDs/order mismatch")
    with RAW_MANIFEST.open(encoding="utf-8-sig", newline="") as stream:
        expected = {row["relative_path"]: row["sha256"] for row in csv.DictReader(stream)}
    for row in rows:
        relative = row["actual_relative_path"].replace("\\", "/")
        path = RAW / relative
        if not path.is_file() or expected.get(relative) != row["sha256"] or sha256(path) != row["sha256"]:
            raise ValueError(f"DATA_SCHEMA_DISCREPANCY: path/hash for {row['official_id']}")
    return rows, expected, sha256(MAPPING)


def update_components(acc: dict[str, dict], signal: str, values: list[float]) -> None:
    for i, value in enumerate(values):
        item = acc.setdefault(f"{signal}[{i}]", {"n": 0, "sum": 0.0, "sum2": 0.0,
                                                "min": math.inf, "max": -math.inf})
        item["n"] += 1
        item["sum"] += value
        item["sum2"] += value * value
        item["min"] = min(item["min"], value)
        item["max"] = max(item["max"], value)


def scan_file(mapping: dict[str, str], sample_quality: dict[str, str]) -> dict:
    label = mapping["official_id"]
    path = RAW / mapping["actual_relative_path"]
    columns = {signal: array("d") for signal in SIGNALS}
    domains: list[str] = []
    keys = Counter()
    field_counts = Counter()
    errors = {signal: Counter() for signal in SIGNALS}
    component_stats: dict[str, dict] = {}
    ids: set[str] = set()
    row_hashes: set[str] = set()
    content_hashes: set[str] = set()
    repeated_ids = repeated_rows = repeated_content = 0
    overlap_ids = overlap_equal = overlap_different = 0
    bad_json = missing_id = 0
    rows = 0
    with lzma.open(path, "rt", encoding="utf-8") as stream:
        for line in stream:
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                bad_json += 1
                continue
            rows += 1
            keys.update(record.keys())
            field_counts[len(record)] += 1
            raw_hash = hashlib.sha256(line.rstrip("\r\n").encode("utf-8")).hexdigest()
            repeated_rows += int(raw_hash in row_hashes)
            row_hashes.add(raw_hash)
            identifier = record.get("id")
            if identifier is None:
                missing_id += 1
            else:
                identifier = str(identifier)
                repeated_ids += int(identifier in ids)
                ids.add(identifier)
            if "content" in record and record["content"] is not None:
                content_hash = hashlib.sha256(str(record["content"]).encode("utf-8")).hexdigest()
                repeated_content += int(content_hash in content_hashes)
                content_hashes.add(content_hash)
            domain = str(record.get("_source_domain") or ("arxiv" if label == "A2" else "github" if label == "A3" else "MISSING"))
            domains.append(domain)
            quality_hash = hashlib.sha256(json.dumps([record.get(s) for s in SIGNALS],
                                                      ensure_ascii=False, separators=(",", ":"))
                                          .encode("utf-8")).hexdigest()
            if label == "A1" and identifier is not None:
                sample_quality[identifier] = quality_hash
            elif identifier in sample_quality:
                overlap_ids += 1
                if sample_quality[identifier] == quality_hash:
                    overlap_equal += 1
                else:
                    overlap_different += 1
            for signal in SIGNALS:
                if signal not in record:
                    value, status, parts = math.nan, "MISSING_KEY", []
                else:
                    value, status, parts = scalar_value(signal, record[signal])
                columns[signal].append(value)
                errors[signal][status] += 1
                if parts and status == "OK":
                    update_components(component_stats, signal, parts)
    frame = pd.DataFrame({k: np.asarray(v, dtype=float) for k, v in columns.items()})
    frame["_domain"] = domains
    return {"label": label, "mapping": mapping, "frame": frame, "rows": rows,
            "bad_json": bad_json, "missing_id": missing_id, "field_counts": dict(field_counts),
            "keys": dict(keys), "errors": errors, "components": component_stats,
            "unique_ids": len(ids), "duplicate_id_rows": repeated_ids,
            "duplicate_full_rows": repeated_rows, "duplicate_content_rows": repeated_content,
            "overlap_ids": overlap_ids, "overlap_equal": overlap_equal,
            "overlap_different": overlap_different,
            "domains": dict(Counter(domains))}


def numeric_profile(values: pd.Series) -> dict:
    finite = values[np.isfinite(values.to_numpy(dtype=float))].to_numpy(dtype=float)
    if not len(finite):
        return {"finite_n": 0}
    quant = np.percentile(finite, [0, 1, 5, 25, 50, 75, 95, 99, 99.9, 100])
    return {"finite_n": len(finite), "mean": float(np.mean(finite)),
            "median": float(np.median(finite)), "std": float(np.std(finite, ddof=1)) if len(finite)>1 else 0.0,
            "min": float(quant[0]), "p01": float(quant[1]), "p05": float(quant[2]),
            "p25": float(quant[3]), "p50": float(quant[4]), "p75": float(quant[5]),
            "p95": float(quant[6]), "p99": float(quant[7]),
            "p999": float(quant[8]), "max": float(quant[9]),
            "skewness": float(skew(finite)) if len(finite)>2 and np.std(finite)>0 else math.nan,
            "kurtosis": float(kurtosis(finite)) if len(finite)>3 and np.std(finite)>0 else math.nan,
            "unique_count": int(np.unique(finite).size),
            "zero_fraction_of_finite": float(np.mean(finite == 0)),
            "negative_fraction_of_finite": float(np.mean(finite < 0))}


def correlation_and_pca(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict, pd.DataFrame]:
    x = frame[SIGNALS]
    pearson = x.corr(method="pearson")
    spearman = x.corr(method="spearman")
    ranked = np.column_stack([rankdata(x[col].fillna(x[col].median()).to_numpy(float)) for col in SIGNALS])
    ranked = (ranked - ranked.mean(axis=0)) / ranked.std(axis=0, ddof=0)
    eigval, eigvec = np.linalg.eigh(np.corrcoef(ranked, rowvar=False))
    order = np.argsort(eigval)[::-1]
    eigval, eigvec = eigval[order], eigvec[:, order]
    total = max(float(eigval.clip(min=0).sum()), 1e-12)
    pc1 = ranked @ eigvec[:, 0]
    resid = ranked - np.outer(pc1, eigvec[:, 0])
    residual_var = np.var(resid, axis=0)
    distance = 1 - np.abs(spearman.fillna(0).to_numpy(float))
    np.fill_diagonal(distance, 0)
    dendrogram = linkage(squareform(distance, checks=False), method="average")
    cluster = fcluster(dendrogram, t=0.4, criterion="distance")
    cluster_map = pd.DataFrame({"signal": SIGNALS, "exploratory_cluster_abs_rho_0p6": cluster,
                                "pc1_loading_rank_space": eigvec[:, 0],
                                "pc1_residual_variance": residual_var})
    spectrum = {"eigenvalues": eigval.tolist(), "variance_share": (eigval/total).tolist(),
                "positive_eigenvalues": int((eigval>1e-10).sum()),
                "exploratory_cluster_count": int(len(set(cluster)))}
    return pearson, spearman, spectrum, cluster_map


def make_figures(scans: dict, spearman: pd.DataFrame, spectrum: dict) -> list[dict]:
    FIG.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": 9, "figure.dpi": 150})
    fig_rows = []
    missing = np.array([[scans[label]["frame"][s].isna().mean() for s in SIGNALS]
                        for label in ("A1", "A2", "A3")])
    fig, ax = plt.subplots(figsize=(12, 3.3))
    im = ax.imshow(missing, aspect="auto", cmap="Blues", vmin=0, vmax=max(0.01,float(missing.max())))
    ax.set_yticks(range(3), ["A1 n=51,230", "A2 n=17,523", "A3 n=203,752"])
    ax.set_xticks(range(len(SIGNALS)), SIGNALS, rotation=75, ha="right", fontsize=7)
    ax.set_title("FIG-Q1-AUDIT-001 | Missing diagnostic scalar rate | source v1")
    fig.colorbar(im, ax=ax, label="Missing fraction")
    fig.tight_layout()
    name="FIG-Q1-AUDIT-001_missingness.png";fig.savefig(FIG/name);plt.close(fig)
    fig_rows.append({"figure_id":"FIG-Q1-AUDIT-001","file":name,"source":"A1/A2/A3","n":"51,230/17,523/203,752","claim":"missingness by signal"})
    fig, ax = plt.subplots(figsize=(10.5, 9))
    im=ax.imshow(spearman.to_numpy(),vmin=-1,vmax=1,cmap="coolwarm")
    ax.set_xticks(range(len(SIGNALS)), SIGNALS, rotation=90, fontsize=7)
    ax.set_yticks(range(len(SIGNALS)), SIGNALS, fontsize=7)
    ax.set_title("FIG-Q1-AUDIT-002 | A1 raw diagnostic-scalar Spearman | n=51,230")
    fig.colorbar(im,ax=ax,label="Spearman rho")
    fig.tight_layout();name="FIG-Q1-AUDIT-002_correlation.png";fig.savefig(FIG/name);plt.close(fig)
    fig_rows.append({"figure_id":"FIG-Q1-AUDIT-002","file":name,"source":"A1","n":"51,230","claim":"raw signal redundancy/conflict diagnostic"})
    fig,ax=plt.subplots(figsize=(8,4))
    share=np.asarray(spectrum["variance_share"])
    ax.bar(range(1,len(share)+1),share,color="#4c78a8")
    ax.set(xlabel="Rank-correlation component",ylabel="Variance share",title="FIG-Q1-AUDIT-003 | A1 rank-space eigen spectrum | n=51,230")
    fig.tight_layout();name="FIG-Q1-AUDIT-003_eigen_spectrum.png";fig.savefig(FIG/name);plt.close(fig)
    fig_rows.append({"figure_id":"FIG-Q1-AUDIT-003","file":name,"source":"A1","n":"51,230","claim":"effective signal dimensionality diagnostic"})
    return fig_rows


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    mapping, expected, mapping_sha = validate_mapping()
    source_pdf_sha = sha256(SOURCE_PDF)
    sample_quality: dict[str,str] = {}
    scans = {row["official_id"]: scan_file(row, sample_quality) for row in mapping}
    print("A1-A3 stream scans complete", flush=True)
    discrepancy = []
    for scan in scans.values():
        label=scan["label"]
        expect_fields=27 if label=="A1" else 24
        assist=ASSIST_A1 if label=="A1" else ASSIST_EXT
        if scan["rows"] != int(scan["mapping"]["verified_rows"]):
            discrepancy.append(f"{label} row count differs from verified mapping")
        if scan["bad_json"] or scan["missing_id"]:
            discrepancy.append(f"{label} unreadable JSON/missing ID")
        if set(scan["keys"]) != set(SIGNALS)|assist or set(scan["field_counts"]) != {expect_fields}:
            discrepancy.append(f"{label} field schema differs from official mapping")
    if discrepancy:
        alert=OUT/"EVIDENCE_ALERT_A1_A3_SCHEMA_v1.md"
        alert.write_text("# DATA_SCHEMA_DISCREPANCY\n\n"+"\n".join(f"- {x}" for x in discrepancy)+"\nAffected Q1 quality workflow paused.\n",encoding="utf-8")
        raise ValueError("DATA_SCHEMA_DISCREPANCY; see EVIDENCE_ALERT_A1_A3_SCHEMA_v1.md")

    profiles=[]
    for label, scan in scans.items():
        frame=scan["frame"]
        for signal in SIGNALS:
            profile=numeric_profile(frame[signal])
            profiles.append({"source_id":label,"signal_id":signal,"rows":scan["rows"],
                             "missing_n":int(frame[signal].isna().sum()),
                             "missing_rate":float(frame[signal].isna().mean()),
                             "parse_status_counts":json.dumps(dict(scan["errors"][signal]),ensure_ascii=False),
                             "raw_type":"list" if signal in LIST_LENGTHS else "scalar",
                             "diagnostic_reduction":META[signal][3],**profile})
    diag=pd.DataFrame(profiles)
    diag.to_csv(OUT/"QUALITY_SIGNAL_DIAGNOSTICS_v1.csv",index=False,encoding="utf-8-sig")

    a1=scans["A1"]["frame"]
    pearson,spearman,spectrum,cluster_map=correlation_and_pca(a1)
    spearman.to_csv(OUT/"QUALITY_CORRELATION_MATRIX_v1.csv",encoding="utf-8-sig",index_label="signal_id")
    cluster_map.to_csv(OUT/"QUALITY_STRUCTURE_CLUSTERS_v1.csv",index=False,encoding="utf-8-sig")
    corr_by_source={}
    for label,scan in scans.items():
        corr_by_source[label]=scan["frame"][SIGNALS].corr(method="spearman")
    pair_rows=[]
    for i,sa in enumerate(SIGNALS):
        for sb in SIGNALS[i+1:]:
            pair_rows.append({"signal_a":sa,"signal_b":sb,
                              **{f"spearman_{label}":float(corr_by_source[label].loc[sa,sb])
                                 for label in ("A1","A2","A3")},
                              "pearson_A1":float(pearson.loc[sa,sb])})
    pairs=pd.DataFrame(pair_rows)
    pairs.to_csv(OUT/"QUALITY_CORRELATION_PAIRS_v1.csv",index=False,encoding="utf-8-sig")
    positive=pairs.sort_values("spearman_A1",ascending=False).head(12)
    negative=pairs.sort_values("spearman_A1").head(12)
    clear_positive=[s for s in SIGNALS if META[s][2]=="POSITIVE_CANDIDATE"]
    pct={s:a1[s].rank(pct=True).to_numpy(float) for s in clear_positive}
    discordance=[]
    for i,sa in enumerate(clear_positive):
        for sb in clear_positive[i+1:]:
            ra,rb=pct[sa],pct[sb]
            valid=np.isfinite(ra)&np.isfinite(rb)
            rate=float(np.mean(((ra[valid]>=0.8)&(rb[valid]<=0.2))|
                               ((rb[valid]>=0.8)&(ra[valid]<=0.2)))) if valid.any() else math.nan
            discordance.append({"signal_a":sa,"signal_b":sb,"rank_discordance_rate_A1":rate})
    discordant=pd.DataFrame(discordance).sort_values("rank_discordance_rate_A1",ascending=False).head(10)
    conflict=[]
    for kind,selection in (("HIGH_POSITIVE_RAW",positive),("HIGH_NEGATIVE_RAW",negative)):
        for _,row in selection.iterrows():
            conflict.append({"candidate_id":f"QCI-{len(conflict)+1:03d}","kind":kind,
                             "signal_a":row.signal_a,"signal_b":row.signal_b,
                             "rho_A1":row.spearman_A1,"rho_A2":row.spearman_A2,
                             "rho_A3":row.spearman_A3,"rank_discordance_rate_A1":math.nan,
                             "interpretation":"Raw diagnostic association; quality-direction resolution required",
                             "status":"CANDIDATE_NOT_FINAL_CONFLICT"})
    for _,row in discordant.iterrows():
        pair=pairs[((pairs.signal_a==row.signal_a)&(pairs.signal_b==row.signal_b))|
                   ((pairs.signal_a==row.signal_b)&(pairs.signal_b==row.signal_a))].iloc[0]
        conflict.append({"candidate_id":f"QCI-{len(conflict)+1:03d}","kind":"RANK_DISCORDANCE_CANDIDATE",
                         "signal_a":row.signal_a,"signal_b":row.signal_b,
                         "rho_A1":pair.spearman_A1,"rho_A2":pair.spearman_A2,
                         "rho_A3":pair.spearman_A3,
                         "rank_discordance_rate_A1":row.rank_discordance_rate_A1,
                         "interpretation":"A1 top/bottom quintile disagreement between two direction-candidate signals",
                         "status":"CANDIDATE_NOT_FINAL_CONFLICT"})
    for _,row in cluster_map.sort_values("pc1_residual_variance",ascending=False).head(8).iterrows():
        conflict.append({"candidate_id":f"QCI-{len(conflict)+1:03d}","kind":"LATENT_RESIDUAL_CANDIDATE",
                         "signal_a":row.signal,"signal_b":"rank_space_PC1",
                         "rho_A1":math.nan,"rho_A2":math.nan,"rho_A3":math.nan,
                         "rank_discordance_rate_A1":math.nan,
                         "interpretation":"High residual variance after first rank-space component",
                         "status":"CANDIDATE_NOT_FINAL_CONFLICT"})
    pd.DataFrame(conflict).to_csv(OUT/"QUALITY_CONFLICT_INPUT_v1.csv",index=False,encoding="utf-8-sig")

    dictionary=[]
    clusters=dict(zip(cluster_map.signal,cluster_map.exploratory_cluster_abs_rho_0p6))
    for signal in SIGNALS:
        meaning,unit,direction,reduction=META[signal]
        pr={label:diag[(diag.source_id==label)&(diag.signal_id==signal)].iloc[0]
            for label in ("A1","A2","A3")}
        notes=[]
        if any(pr[x]["finite_n"]<pr[x]["rows"] for x in pr):notes.append("missing_or_unparseable")
        if any(pr[x]["skewness"]==pr[x]["skewness"] and abs(pr[x]["skewness"])>5 for x in pr):notes.append("strong_skew_diagnostic")
        if any(pr[x]["unique_count"]<=10 for x in pr):notes.append("discrete_or_near_constant_in_source")
        dictionary.append({"Signal ID":signal,"Official name":signal,"Source file":"A1|A2|A3",
                           "Meaning":meaning,"Direction":direction,"Unit":unit,
                           "Data type":"list" if signal in LIST_LENGTHS else "scalar",
                           "Positive / Negative / Ambiguous":"AMBIGUOUS" if direction=="DIRECTION_UNRESOLVED" else "POSITIVE_CANDIDATE",
                           "Missing rate": "|".join(f"{x}:{pr[x]['missing_rate']:.6g}" for x in pr),
                           "Unique count":"|".join(f"{x}:{int(pr[x]['unique_count'])}" for x in pr),
                           "Skewness":"|".join(f"{x}:{pr[x]['skewness']:.4g}" for x in pr),
                           "Outlier notes":";".join(notes) or "no_flag_from_aggregate_diagnostic",
                           "Transformation candidate":reduction,
                           "Redundancy group":f"EXPLORATORY_{clusters[signal]}",
                           "Evidence type":("E1 provided rule-derived text feature" if signal.startswith("rps_")
                                            else "E1 provided DSIR-derived domain similarity" if signal.startswith("dsir_")
                                            else "E1 provided model-derived annotation"),
                           "Derived-variable risk":("Directly derived from document text; related length/entropy features may share inputs"
                                                    if signal.startswith("rps_") else
                                                    "Target-domain matching score; raw scale/direction unresolved and may track text length"
                                                    if signal.startswith("dsir_") else
                                                    "Classifier/model score; correlated errors and training-data provenance need review"),
                           "Can enter descriptive Q?":"CONDITIONAL_ON_DIRECTION_AND_VALIDATION" if direction!="DIRECTION_UNRESOLVED" else "DIRECTION_UNRESOLVED",
                           "Can enter downstream model?":"NOT_AS_INDEPENDENT_Q_CURRENT_DATA",
                           "Reason":"A1-A3 have no matched A4/A5 run-level Q; source semantics and redundancy require audit"})
    pd.DataFrame(dictionary).to_csv(OUT/"QUALITY_SIGNAL_DICTIONARY_v1.csv",index=False,encoding="utf-8-sig")

    strata=[]
    for label,scan in scans.items():
        frame=scan["frame"]
        for domain,g in frame.groupby("_domain"):
            for signal in SIGNALS:
                strata.append({"source_id":label,"stratum_type":"domain","stratum":domain,
                               "n":len(g),"signal_id":signal,"missing_rate":float(g[signal].isna().mean())})
        fw=frame["fineweb_edu"]
        if fw.notna().sum()>4 and fw.nunique()>3:
            tiers=pd.qcut(fw.rank(method="first"),4,labels=["Q1","Q2","Q3","Q4"])
            for tier,g in frame.groupby(tiers,observed=True):
                for signal in SIGNALS:
                    strata.append({"source_id":label,"stratum_type":"fineweb_edu_raw_quartile_not_final_Q",
                                   "stratum":str(tier),"n":len(g),"signal_id":signal,
                                   "missing_rate":float(g[signal].isna().mean())})
    pd.DataFrame(strata).to_csv(OUT/"QUALITY_MISSINGNESS_STRATA_v1.csv",index=False,encoding="utf-8-sig")
    comp=[]
    for label,scan in scans.items():
        for name,item in scan["components"].items():
            n=item["n"]
            comp.append({"source_id":label,"component":name,"n":n,"mean":item["sum"]/n,
                         "std":max(item["sum2"]/n-(item["sum"]/n)**2,0)**0.5,
                         "min":item["min"],"max":item["max"]})
    pd.DataFrame(comp).to_csv(OUT/"QUALITY_LIST_COMPONENT_DIAGNOSTICS_v1.csv",index=False,encoding="utf-8-sig")

    figs=make_figures(scans,spearman,spectrum)
    fig_lines=["# Quality audit figures", "", "Only diagnosis; no paper result or final Q.", ""]
    for f in figs:
        fig_lines.append(f"- `{f['figure_id']}` — `{f['file']}`; source {f['source']}; n={f['n']}; purpose: {f['claim']}.")
    (FIG/"FIGURES_MANIFEST.md").write_text("\n".join(fig_lines)+"\n",encoding="utf-8")

    report={"run_id":RUN_ID,"status":"CHECKED_AUDIT_RESULT_NOT_FINAL_MODEL",
            "run_utc":datetime.now(timezone.utc).isoformat(),
            "script_sha256":sha256(Path(__file__)),"mapping_sha256":mapping_sha,
            "official_pdf_sha256":source_pdf_sha,
            "inputs":{row["official_id"]:{"path":row["actual_relative_path"],"sha256":row["sha256"]} for row in mapping},
            "sources":{label:{k:v for k,v in scan.items() if k not in ("frame","errors","components","mapping")}
                       for label,scan in scans.items()},
            "shared_quality_metric_count":len(SIGNALS),
            "a1_a2_id_overlap":scans["A2"]["overlap_ids"],
            "a1_a3_id_overlap":scans["A3"]["overlap_ids"],
            "spectrum":spectrum,
            "top_positive_pairs":positive[["signal_a","signal_b","spearman_A1"]].to_dict("records"),
            "top_negative_pairs":negative[["signal_a","signal_b","spearman_A1"]].to_dict("records"),
            "figures":figs,"random_seed":"NOT_USED_DETERMINISTIC"}
    (OUT/"QUALITY_AUDIT_METRICS_v1.json").write_text(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False),encoding="utf-8")
    print("A1-A3 audit outputs saved",OUT,flush=True)


if __name__ == "__main__":
    main()
