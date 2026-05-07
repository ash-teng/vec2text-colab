# vec2text Colab LMI Run-Only Notebook

<p>
  <a href="README.md"><kbd>English</kbd></a>
  <a href="README.zh-CN.md"><kbd>中文</kbd></a>
</p>

This branch keeps a shorter Colab workflow for producing LMI corrected sample outputs. It removes the smoke-test, comparison, and optional larger-eval sections from the legacy/debug notebook.

Main notebook:

- `colab_lmi_legacy.ipynb`

## Section 1. Check GPU

Checks PyTorch, CUDA, and the current GPU. Use this to confirm Colab is running on a GPU runtime before starting the heavier LMI path.

## Section 2. Clone the Repository and Install Dependencies

Clones upstream `vec2text`, installs dependencies, pins the legacy-compatible Hugging Face stack, removes conflicting `peft`, installs `vec2text` in editable mode, and automatically restarts the Colab runtime.

After the automatic restart, do not rerun the install cell. Continue from "Continue Here After Restart".

## Section 3. Runtime Setup

Sets cache and tokenizer environment variables used by the notebook.

## Section 3.1. Optional Hugging Face Token

Loads `HF_TOKEN` from Colab Secrets and mirrors it to `LLAMA_TOKEN`. This is needed for the LMI path because it loads `meta-llama/Llama-2-7b-hf`.

## Section 3.2. Optional Google Drive Save

Mounts Google Drive and creates:

```text
/content/drive/MyDrive/vec2text_results
```

If mounted, result files are copied there after the eval cell finishes.

## Section 4. Colab Compatibility Patches

Applies the runtime patches needed for the current Colab and Transformers/Accelerate environment. These patches handle old checkpoint behavior, model loading, dtype handling, trainer defaults, and generation config compatibility.

## Section 4.2. Runtime Monkey Patch

Applies a session-only Transformers/Accelerate model-loading patch for meta-device compatibility.

## Section 5. Import the Library

Imports `vec2text` from the cloned local repository and verifies the import path.

## Section 5.1. Tied-Weights Compatibility Patch

Adds tied-weight metadata expected by newer Transformers versions.

## Section 6. LMI Corrected Sample Eval

Samples prompts, loads the LMI inverter and corrector if needed, runs corrected inversion with `lmi_corrector`, prints reference/prediction pairs, and saves both summary metrics and sample-level outputs.

Outputs use short, non-overwriting filenames such as:

```text
lmi_corr_n10_s42_224825.json
lmi_corr_n10_s42_224825_samples.json
```

Filename fields:

- `corr`: corrected LMI path
- `n10`: number of samples
- `s42`: sample seed
- `224825`: UTC time

Change `sample_seed` if you want a different fixed random sample.
