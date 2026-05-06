# vec2text Colab LMI Legacy Notebook

<p>
  <a href="README.md"><kbd>English</kbd></a>
  <a href="README.zh-CN.md"><kbd>中文</kbd></a>
</p>

这个仓库包含用于运行 `vec2text` 实验的 Colab notebook。当前分支的主要 notebook 是：

- `colab_lmi_legacy.ipynb`：用于较重 LMI 路径的 Google Colab 工作流，包含较保守的依赖配置和兼容性补丁。

## 第 1 节：检查 GPU

检查当前 PyTorch、CUDA 和 GPU 环境。先跑这一节，确认 Colab 已经切到 GPU runtime，最好是 A100 或其他高显存 GPU。

## 第 2 节：克隆仓库并安装依赖

把 upstream `vec2text` 仓库 clone 到 Colab，并安装 Python 依赖。这一节会固定较旧的 Hugging Face 相关包，卸载冲突的 `peft`，以 editable mode 安装 `vec2text`，然后自动重启 Colab runtime。

自动重启后，不要重新跑安装 cell。请从 “Continue Here After Restart” 继续。

## 第 3 节：运行环境设置

设置 cache 路径和 tokenizer 行为相关的环境变量，让 Colab 运行更稳定、更可复现。

## 第 3.1 节：可选 Hugging Face Token

从 Colab Secrets 里读取 `HF_TOKEN`。同时会把它复制到 `LLAMA_TOKEN`，因为 LMI 路径会加载 `meta-llama/Llama-2-7b-hf`，需要 Llama 访问权限。

## 第 3.2 节：可选 Google Drive 保存

挂载 Google Drive，并创建保存目录：

```text
/content/drive/MyDrive/vec2text_results
```

如果这一节成功运行，后面的结果文件会复制到 Google Drive。

## 第 4 节：Colab 兼容性补丁

对 clone 下来的 upstream `vec2text` 代码打 runtime patch，让它能在当前 Colab、Transformers、Accelerate 和旧 checkpoint 组合下运行。这些 patch 处理缺失 import、模型加载、dtype、generation config、trainer 参数等兼容问题。

## 第 4.2 节：Runtime Monkey Patch

对当前 Python session 里的 Transformers/Accelerate 行为做临时 patch，避免模型加载时遇到 meta-device 相关错误。

## 第 5 节：导入 Library

从 Colab clone 的本地仓库导入 `vec2text`，并确认 Python 用的是正确的本地路径。

## 第 5.1 节：Tied-Weights 兼容补丁

补上新版 Transformers 期望存在的 tied-weight metadata 属性。

## 第 5 节：`gtr-base` Smoke Test

加载 `gtr-base` corrector，并用两句简单文本跑一个小的 inversion 测试。这一节用来确认基础 `vec2text` API 是通的，再继续跑更重的 LMI 路径。

结果会保存到本地：

```text
results/gtr_outputs.json
```

如果已经挂载 Google Drive，也会保存到 Drive。

## 第 6 节：LMI Smoke Test

加载 LMI inverter 和 LMI corrector 模型。这一节主要确认重模型能下载、能通过 Hugging Face 权限验证，并且能加载到当前 GPU。

它主要是 readiness check。后面的 eval section 可能会复用这些模型，也可能根据当前 runtime 状态重新加载。

## 第 7 节：LMI Base Sample Eval

运行原始的 LMI base inverter trainer/eval 路径。这个结果适合用来和 corrected 输出做对比。

输出文件名会比较短，而且不会覆盖旧结果，例如：

```text
lmi_base_n10_s42_224825.json
lmi_base_n10_s42_224825_samples.json
```

文件名含义：

- `base`：base inverter 路径
- `n10`：样本数 10
- `s42`：随机种子 42
- `224825`：UTC 时间

## 第 8 节：LMI Corrected Sample Eval

运行 LMI corrector 路径，思路更接近 `gtr-base` smoke test。它会抽样 prompt，用 `lmi_corrector` 做多步 corrected inversion，打印 reference/prediction，并保存 summary metrics 和逐样本结果。

输出文件名例如：

```text
lmi_corr_n10_s42_224825.json
lmi_corr_n10_s42_224825_samples.json
```

如果你想看“原始 prompt vs 还原 prompt”，主要看这一节。

## 第 9 节：可选 Larger Eval

用于后续更大规模 eval。建议先确认 10-sample 的 base 和 corrected 路径都跑通，再增加样本数。
