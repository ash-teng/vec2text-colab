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

## 可选 strict 5-step 诊断

第 7 节保留 `python_code_alpaca` 上的 5-step corrected diagnostic，但默认 strict：

- `num_steps = 5`
- 不创建 zero unigram buffer
- 不为 32000/32256 维度不一致手动补 0
- 如果 public checkpoint 缺少需要的 unigram 或 shape 不匹配，会保存 failure JSON 并报错

第 7 节只用来证明“不补 0 的 5-step corrected 是否能跑”。如果它失败，或者需要 compatibility padding 才能跑，就不要把它当成主要论文对齐结果。

## 建议 Colab 顺序

1. 正常跑第 1-5.1 节。
2. 用默认参数跑第 6 节。
3. 如果 BLEU 看起来正常，再把 `OFFICIAL_NUM_SAMPLES` 提高到接近 1000。
4. 第 7 节只作为可选 strict/no-zero 诊断。
5. 在不加密 baseline 搞清楚之前，先不要开始加密实验。
