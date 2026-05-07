# vec2text Colab LMI Run-Only Notebook

<p>
  <a href="README.md"><kbd>English</kbd></a>
  <a href="README.zh-CN.md"><kbd>中文</kbd></a>
</p>

这个分支保留较短的 Colab 流程，用来直接生成 LMI corrected sample outputs。legacy/debug notebook 里的 smoke test、对比 eval 和 optional larger eval 都已经删掉。

主要 notebook：

- `colab_lmi_legacy.ipynb`

## 第 1 节：检查 GPU

检查 PyTorch、CUDA 和当前 GPU。先跑这一节，确认 Colab 已经在 GPU runtime 上，再继续跑较重的 LMI 路径。

## 第 2 节：克隆仓库并安装依赖

克隆 upstream `vec2text`，安装依赖，固定 legacy-compatible 的 Hugging Face 版本，卸载冲突的 `peft`，以 editable mode 安装 `vec2text`，然后自动重启 Colab runtime。

自动重启后，不要重新跑安装 cell。请从 “Continue Here After Restart” 继续。

## 第 3 节：运行环境设置

设置 notebook 需要的 cache 和 tokenizer 环境变量。

## 第 3.1 节：可选 Hugging Face Token

从 Colab Secrets 读取 `HF_TOKEN`，并复制到 `LLAMA_TOKEN`。LMI 路径会加载 `meta-llama/Llama-2-7b-hf`，所以需要这个权限。

## 第 3.2 节：可选 Google Drive 保存

挂载 Google Drive，并创建：

```text
/content/drive/MyDrive/vec2text_results
```

如果挂载成功，eval 跑完后结果文件会复制到这里。

## 第 4 节：Colab 兼容性补丁

应用当前 Colab 和 Transformers/Accelerate 环境需要的 runtime patch。这些 patch 处理旧 checkpoint 行为、模型加载、dtype、trainer 默认参数和 generation config 兼容性。

## 第 4.2 节：Runtime Monkey Patch

对当前 session 应用 Transformers/Accelerate 模型加载补丁，避免 meta-device 相关兼容问题。

## 第 5 节：导入 Library

从 clone 下来的本地仓库导入 `vec2text`，并确认导入路径正确。

## 第 5.1 节：Tied-Weights 兼容补丁

补上新版 Transformers 期望存在的 tied-weight metadata。

## 第 6 节：LMI Corrected Sample Eval

抽样 prompts，按需加载 LMI inverter 和 corrector，用 `lmi_corrector` 跑 corrected inversion，打印 reference/prediction，并保存 summary metrics 和逐样本输出。

输出文件名较短，且不会覆盖旧结果，例如：

```text
lmi_corr_n10_s42_224825.json
lmi_corr_n10_s42_224825_samples.json
```

文件名含义：

- `corr`：corrected LMI 路径
- `n10`：样本数 10
- `s42`：随机种子 42
- `224825`：UTC 时间

如果想换一组固定随机样本，修改 `sample_seed`。
