# Evaluating Gender Bias in Machine Translation

This repository is an extension of the work presented in [Evaluating Gender Bias in Machine Translation](https://arxiv.org/abs/1906.00591) by Gabriel Stanovsky, Noah A. Smith, and Luke Zettlemoyer (ACL 2019), and [Gender Coreference and Bias Evaluation at WMT 2020](https://arxiv.org/pdf/2010.06018.pdf) by Tom Kocmi, Tomasz Limisiewicz, and Gabriel Stanovsky (WMT2020).

Our project builds upon the foundational research by addressing additional biases and incorporating support for Portuguese, reflecting our commitment to enhancing fairness in machine translation across diverse languages.

## Requirements

- [fast_align](https://github.com/clab/fast_align): install and point an environment variable called `FAST_ALIGN_BASE` to its root folder (the one containing the `build` folder).

## Installation

1. Create a Conda environment:

   ```bash
   conda create -n mypython3 python=3.8
   source activate mypython3
   conda install anaconda
   ```

2. Clone the `mt_gender` and `fast_align` repositories:

   ```bash
   git clone https://github.com/gabrielStanovsky/mt_gender.git
   git clone https://github.com/clab/fast_align.git
   conda install cmake
   ```

3. Compile `fast_align`:

   ```bash
   cd fast_align
   mkdir -p build
   cd build
   cmake ..
   make
   ```

4. Check if it was installed properly:

   ```bash
   cd ../../ && fast_align/build/fast_align
   ```

5. Set the environment variable `FAST_ALIGN_BASE` to the root folder of `fast_align`:
   ```bash
   export FAST_ALIGN_BASE=/path/to/fast_align
   ```

## Project Changes

In this updated version of the project, the following significant enhancements have been made:

- **Error Correction**: Numerous errors identified in the original project have been corrected to enhance the stability and accuracy of the evaluations.
- **Language Support**: Added comprehensive support for the Portuguese language, facilitating the assessment of gender bias in Portuguese translations, thereby broadening the applicability of the project.
- **Project unbIAs**: These changes were made as part of the initiative under the [unbIAs project](https://github.com/ramos-ai/unbIAs), which aims to reduce biases in artificial intelligence systems. This alignment with unbIAs underscores our commitment to promoting fairness in AI technologies.

## How to Run

After completing the installation steps:

1. Ensure all dependencies are installed by running:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure the necessary environment variables as described in the Installation section.

3. For the general gender accuracy number, run:

   ```bash
    cd /content/mt_gender/src &&  ../scripts/evaluate_all_languages.sh ../data/aggregates/en.txt ../../winomtout &> ../../winomtout/baseline
   ```

4. For the general gender accuracy number, run:

   ```bash
    cd /content/mt_gender/src &&  ../scripts/evaluate_all_languages.sh ../data/aggregates/en_pro.txt ../../winomtout &> ../../winomtout/pro
   ```

5. For the general gender accuracy number, run:
   ```bash
    cd /content/mt_gender/src &&  ../scripts/evaluate_all_languages.sh ../data/aggregates/en_anti.txt ../../winomtout &> ../../winomtout/anti
   ```

For detailed step-by-step instructions, refer to the provided notebook (WinoMT_Scores_add_portuguese.ipynb), which includes specific configurations and examples.

## License

This project uses the following license: [MIT](https://github.com/ramos-ai/winopt?tab=MIT-1-ov-file).
