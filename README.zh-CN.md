# vec2text Colab LMI Table 2 Baseline Notebook

这个分支专门用于 Language Model Inversion 复现里的 Table 2 baseline。

主要 notebook：

- `colab_lmi_legacy.ipynb`

## 这个分支做什么

第 6 节默认改成论文 Table 2 的 `Alpaca Code Generation` 设置：

```python
OFFICIAL_DATASET_KEY = "python_code_alpaca"
OFFICIAL_NUM_SAMPLES = 100
OFFICIAL_BATCH_SIZE = 1
OFFICIAL_KEEP_FROZEN_EMBEDDINGS = True
```

最接近的原文目标是 Table 2，raw `Llama-2 7B (LM)`，`Ours`，Alpaca Code Generation：

| 指标 | 原文目标 |
|---|---:|
| BLEU | 46.22 |
| Exact Match | 10.5 |
| Token F1 | 74.9 |

第 6 节是主要的“不加密 baseline”。它走 upstream 的 `trainer.evaluate(...)`，不加载 corrected LMI model，所以不会进入手动补 0 的 compatibility workaround。

第 6 节也会保存逐样本输出，方便直观看 pred/true：

- `table2_official_eval_...json`：总指标和原文差距
- `table2_official_samples_...json`：逐样本 prediction/reference 和单样本分数
- `table2_official_samples_...csv`：适合在 Google Drive 或 Sheets 里打开的表格

原文表格报告 BLEU、CS、Exact Match、Token F1。这个 notebook 会直接比较 BLEU、Exact Match、Token F1。它也会输出 upstream 的 `emb_cos_sim`，但这个值不是原文的 CS，因为原文 CS 使用 OpenAI `text-embeddings-ada-002` 语义 embedding 计算。

## 房地产 JSON inversion baseline

第 9 节用于跑自定义房地产问题 JSON 的“不加密 baseline inversion”。

这个分支内置：

- `datasets/500_easy_houseqs_questions.json`

Colab 里第 9 节会先找：

```python
/content/500_easy_houseqs_questions.json
```

如果没有这个文件，就会从当前 GitHub 分支自动下载内置 dataset。你也可以换成自己的 JSON list，或者带 `question` 字段的 JSON object list：

```python
REAL_ESTATE_QUESTIONS_JSON_PATH = "/content/my_questions.json"
REAL_ESTATE_NUM_SAMPLES = 10      # 先 smoke test
REAL_ESTATE_NUM_SAMPLES = 500     # 再完整跑
REAL_ESTATE_SAMPLE_MODE = "first" # 或 "random"
REAL_ESTATE_SAMPLE_SEED = 42
```

第 9 节会保存：

- `real_estate_inversion_eval_...json`：总体指标
- `real_estate_inversion_samples_...json`：逐样本 prediction
- `real_estate_inversion_samples_...csv`：适合放 Google Drive / Sheets 里看的表格，包含 original question、tokenized reference、prediction、BLEU、token overlap、sensitive-marker recall

建议先跑第 9 节确认“不加防御时能不能反推出房地产问题”，再跑 defense。

## 可选 strict 5-step 诊断

第 7 节保留 `python_code_alpaca` 上的 5-step corrected diagnostic，但默认 strict：

- `num_steps = 5`
- 不创建 zero unigram buffer
- 不为 32000/32256 维度不一致手动补 0
- 如果 public checkpoint 缺少需要的 unigram 或 shape 不匹配，会保存 failure JSON 并报错

第 7 节只用来证明“不补 0 的 5-step corrected 是否能跑”。如果它失败，或者需要 compatibility padding 才能跑，就不要把它当成主要论文对齐结果。

## 建议 Colab 顺序

1. 正常跑第 1-5.1 节。
2. 如果要复现论文 Table 2，跑第 6 节。
3. 如果要跑你的房地产问题 JSON，跑第 9 节，不需要先跑第 6 节。
4. 第 9 节先用 `REAL_ESTATE_NUM_SAMPLES = 10` 试跑，再改成 `500`。
5. 在 Google Drive 里打开 sample CSV，肉眼检查 prediction/reference。
6. baseline 搞清楚以后，再跑 defense。
7. 第 7 节只作为可选 strict/no-zero 诊断。
