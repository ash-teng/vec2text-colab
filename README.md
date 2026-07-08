# vec2text Colab LMI Table 2 Defense Notebook

This branch builds on the Table 2-style baseline and adds prompt-transformation defense experiments for the Language Model Inversion reproduction.

Main notebook:

- `colab_lmi_legacy.ipynb`

## What This Branch Does

Section 6 now defaults to the paper's Table 2 `Alpaca Code Generation` setting:

```python
OFFICIAL_DATASET_KEY = "python_code_alpaca"
OFFICIAL_NUM_SAMPLES = 100
OFFICIAL_BATCH_SIZE = 1
OFFICIAL_KEEP_FROZEN_EMBEDDINGS = True
```

The closest paper target is Table 2, raw `Llama-2 7B (LM)`, `Ours` on Alpaca Code Generation:

| Metric | Paper Target |
|---|---:|
| BLEU | 46.22 |
| Exact Match | 10.5 |
| Token F1 | 74.9 |

Section 6 is the main no-encryption baseline. It uses the upstream `trainer.evaluate(...)` path and does not load the corrected LMI model, so it avoids the manual zero-padding compatibility workaround.

Section 6 also saves sample-level outputs for visual inspection:

- `table2_official_eval_...json`: aggregate metrics and paper deltas
- `table2_official_samples_...json`: prediction/reference rows with per-sample scores
- `table2_official_samples_...csv`: spreadsheet-friendly table for Google Drive or Sheets

The paper reports BLEU, CS, Exact Match, and Token F1. This notebook directly compares BLEU, Exact Match, and Token F1. It also reports the upstream `emb_cos_sim`, but that value is not the same as the paper's CS metric because the paper used OpenAI `text-embeddings-ada-002` semantic embeddings for CS.

## Defense Transform Experiments

Section 8 tests prompt transformations against the same Table 2 inversion setup. It keeps the original prompt as the reference text, but recomputes logits-style `frozen_embeddings` from each transformed prompt before running the inverter. This means the defense metrics answer:

> If the victim model sees the transformed prompt, how much of the original prompt can the LMI attack recover?

Default settings:

```python
DEFENSE_DATASET_KEY = "python_code_alpaca"
DEFENSE_NUM_SAMPLES = 10
DEFENSE_EVAL_BATCH_SIZE = 1
DEFENSE_EMBED_BATCH_SIZE = 4
DEFENSE_METHODS = ["none", "sha256_full", "hmac_words", "redact_literals"]
```

Available methods:

| Method | What It Tests |
|---|---|
| `none` | Recomputed no-defense control. |
| `sha256_full` | Teacher-style one-way hash of the whole prompt. Good privacy destruction control, but not usable prompt encryption by itself. |
| `hmac_words` | Secret-key one-way word tags using HMAC-SHA256. Tests keyed hashing at word level. |
| `base64_full` | Reversible encoding control. Add it manually to `DEFENSE_METHODS` if needed. |
| `redact_literals` | Replaces quoted strings and numbers with placeholders. More practical than full hashing, but weaker. |

Section 8 saves:

- `table2_defense_eval_...json`: aggregate method metrics and deltas from the Section 6 baseline if Section 6 was run first
- `table2_defense_samples_...json`: sample-level rows for all methods
- `table2_defense_samples_...csv`: spreadsheet-friendly table with `method`, original `reference`, `transformed_prompt`, and `prediction`

When Google Drive is mounted, this branch uses this experiment root:

```python
/content/drive/MyDrive/vec2text_results/table2_defense_transformations
```

Each Section 8 defense run creates a dated subfolder inside that root, for example:

```python
/content/drive/MyDrive/vec2text_results/table2_defense_transformations/defense_20260630_153012_n10_python_code_alpaca
```

This keeps repeated defense runs separate for comparison.

You can change the folder before running Section 3.2:

```python
DRIVE_EXPERIMENT_DIR = "my_custom_experiment_name"
```

You can also force a custom Section 8 run folder before running Section 8:

```python
DEFENSE_DRIVE_RUN_FOLDER = "defense_redact_only_20260630"
```

One-way hash functions are intentionally included because they match the proposed defense idea, but they are not a complete encryption solution: after hashing the prompt, the LLM cannot recover the original task semantics without an external mechanism. Use them as a privacy upper bound / negative utility control, then compare against less destructive methods.

## Real Estate JSON Inversion Baseline

Section 9 runs a no-defense inversion baseline on a custom JSON list of real-estate questions.

This branch includes:

- `datasets/500_easy_houseqs_questions.json`
- `datasets/500_insurance_appeal_questions.json`

Section 9 defaults to this dataset. In Colab, it first checks:

```python
/content/500_easy_houseqs_questions.json
```

If that file is not present, it downloads the branch copy from GitHub. You can replace it with your own JSON list or a JSON list of objects with a `question` field:

```python
REAL_ESTATE_QUESTIONS_JSON_PATH = "/content/my_questions.json"
REAL_ESTATE_QUESTIONS_JSON_URL = "https://raw.githubusercontent.com/ash-teng/vec2text-colab/refs/heads/codex/real-estate-json-inversion/datasets/500_insurance_appeal_questions.json"
REAL_ESTATE_RUN_LABEL = "insurance_appeal"
REAL_ESTATE_NUM_SAMPLES = 10      # smoke test
REAL_ESTATE_NUM_SAMPLES = 500     # full run
REAL_ESTATE_SAMPLE_MODE = "first" # or "random"
REAL_ESTATE_SAMPLE_SEED = 42
```

Section 9 saves:

- `real_estate_inversion_eval_...json`: aggregate metrics
- `real_estate_inversion_samples_...json`: sample-level predictions
- `real_estate_inversion_samples_...csv`: spreadsheet-friendly table with original question, tokenized reference, prediction, BLEU, token overlap, and sensitive-marker recall

Use this section before defense runs. It answers:

> Can the public LMI inverter recover real-estate user questions before any defense is applied?

## Optional Strict 5-Step Diagnostic

Section 7 keeps a 5-step corrected diagnostic on `python_code_alpaca`, but it is strict by default:

- `num_steps = 5`
- no created zero unigram buffer
- no zero-padding compatibility for 32000/32256 shape mismatch
- if the public checkpoint is missing the needed unigram or shape, the cell saves a failure JSON and raises

Use Section 7 only to document whether strict 5-step corrected inversion is possible without compatibility padding. Do not use a failed or compatibility-padded Section 7 run as the main paper-comparable result.

## Suggested Colab Order

1. Run Sections 1-5.1 as usual.
2. For paper-aligned Table 2 reproduction, run Section 6 with the defaults above.
3. For the real-estate custom dataset, run Section 9 instead of Section 6.
4. Start Section 9 with `REAL_ESTATE_NUM_SAMPLES = 10`; then increase it to `500`.
5. Inspect the sample CSV in Google Drive to sanity-check predictions against references.
6. Run Section 8 only after the no-defense baseline is clear.
7. Run Section 7 only as an optional strict/no-zero diagnostic.
