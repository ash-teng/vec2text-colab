# vec2text Colab LMI Legacy Notebook

<p>
  <a href="README.md"><kbd>English</kbd></a>
  <a href="README.zh-CN.md"><kbd>中文</kbd></a>
</p>

This repository contains Colab notebooks for running `vec2text` experiments. The main notebook in this branch is:

- `colab_lmi_legacy.ipynb`: a Google Colab workflow for the heavier LMI path with a conservative dependency setup and compatibility patches.

## Section 1. Check GPU

Checks the current PyTorch, CUDA, and GPU environment. Use this first to confirm Colab is running with a GPU runtime, preferably A100 or another high-memory GPU.

## Section 2. Clone the Repository and Install Dependencies

Clones the upstream `vec2text` repository into Colab and installs the required Python packages. This section pins older Hugging Face packages for compatibility, removes conflicting `peft`, installs `vec2text` in editable mode, and then restarts the Colab runtime automatically.

After the automatic restart, do not rerun the install cell. Continue from the "Continue Here After Restart" section.

## Section 3. Runtime Setup

Sets runtime environment variables for cache paths and tokenizer behavior. These settings keep the Colab run more predictable.

## Section 3.1. Optional Hugging Face Token

Loads `HF_TOKEN` from Colab Secrets if available. The token is also copied into `LLAMA_TOKEN`, which is needed by the LMI path because it loads `meta-llama/Llama-2-7b-hf`.

## Section 3.2. Optional Google Drive Save

Mounts Google Drive and creates a save directory at:

```text
/content/drive/MyDrive/vec2text_results
```

If this section is run successfully, later result files are copied to Google Drive.

## Section 4. Colab Compatibility Patches

Applies runtime patches to the cloned upstream `vec2text` code so it works with the current Colab, Transformers, Accelerate, and checkpoint behavior. These patches handle missing imports, loading behavior, dtype issues, generation config defaults, and trainer compatibility.

## Section 4.2. Runtime Monkey Patch

Applies a session-only Transformers/Accelerate patch for model-loading behavior that can otherwise fail with meta-device errors.

## Section 5. Import the Library

Imports `vec2text` from the cloned repository and verifies that Python is using the intended local Colab copy.

## Section 5.1. Tied-Weights Compatibility Patch

Adds missing tied-weight metadata attributes expected by newer Transformers versions.

## Section 5. `gtr-base` Smoke Test

Loads the supported `gtr-base` corrector and runs a small text inversion smoke test on two example sentences. This verifies that the basic `vec2text` API works before running the heavier LMI path.

The result is saved locally as:

```text
results/gtr_outputs.json
```

If Google Drive is mounted, it is also saved to Drive.

## Section 6. LMI Smoke Test

Loads the LMI inverter and LMI corrector models. This section checks that the heavy LMI models can be downloaded, authenticated, and loaded on the current GPU.

This is mainly a readiness check. Later evaluation sections may load or reuse these models depending on the runtime state.

## Section 7. LMI Base Sample Eval

Runs the original trainer/eval path for the LMI base inverter. This path is useful for comparing the base inverter output against the corrected output.

Outputs use short, non-overwriting filenames such as:

```text
lmi_base_n10_s42_224825.json
lmi_base_n10_s42_224825_samples.json
```

The filename includes:

- `base`: base inverter path
- `n10`: number of samples
- `s42`: sample seed
- `224825`: UTC time

## Section 8. LMI Corrected Sample Eval

Runs the LMI corrector path, similar in spirit to the `gtr-base` smoke test. It samples prompts, runs multi-step corrected inversion with `lmi_corrector`, prints reference/prediction pairs, and saves both summary metrics and sample-level outputs.

Outputs use short, non-overwriting filenames such as:

```text
lmi_corr_n10_s42_224825.json
lmi_corr_n10_s42_224825_samples.json
```

This is the section to use when you want to inspect results similar to the smoke test: original prompt versus recovered prompt.

## Section 9. Optional Larger Eval

Placeholder section for running larger evaluations after the 10-sample runs are working. Increase sample counts only after the smaller base and corrected runs succeed.
