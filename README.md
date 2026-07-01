# vec2text Colab LMI Table 2 Baseline Notebook

This branch focuses on a Table 2-style baseline for the Language Model Inversion reproduction.

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

## Optional Strict 5-Step Diagnostic

Section 7 keeps a 5-step corrected diagnostic on `python_code_alpaca`, but it is strict by default:

- `num_steps = 5`
- no created zero unigram buffer
- no zero-padding compatibility for 32000/32256 shape mismatch
- if the public checkpoint is missing the needed unigram or shape, the cell saves a failure JSON and raises

Use Section 7 only to document whether strict 5-step corrected inversion is possible without compatibility padding. Do not use a failed or compatibility-padded Section 7 run as the main paper-comparable result.

## Suggested Colab Order

1. Run Sections 1-5.1 as usual.
2. Run Section 6 with the defaults above.
3. Inspect the sample CSV in Google Drive to sanity-check predictions against references.
4. If BLEU is reasonable, increase `OFFICIAL_NUM_SAMPLES` toward 1000.
5. Run Section 7 only as an optional strict/no-zero diagnostic.
6. Do not start encryption experiments until the no-encryption baseline is understood.
