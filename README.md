##  Human-like Affective Cognition in Foundation Models

### 🧐 What is this?
This is a supporting repository for our paper titled "Human-like Affective Cognition in Foundation Models".
This repository contains code for generating the affective evals, collecting human participant data, and evaluating models on the stimuli. It also contains the data used in the paper. We also provide analysis code for the data collected.

### 📂 Repo structure
```
├── code                 
│   ├── analysis
|   ├── facs_expression
│   ├── prolific-exp-1
│   ├── prolific-exp-2
│   ├── prompt_instructions
│   └── src 
├── data   
│   ├── conditions_1 
|   ├── conditions_2
│   ├── images
│   ├── x_results
│   └── results
├── .gitignore
├── LICENSE            
└── requirements.txt
```

### 🚀 Getting started  
##### Using miniforge
1. install miniforge from `https://github.com/conda-forge/miniforge` (eg `Miniforge3-MacOSX-arm64`)
2. `bash Miniforge3-MacOSX-arm64.sh`
3. close terminal
4. `conda create --name name-of-my-env python==3.10`
5. `pip install -r requirements.txt` 

#### 🎭 Generating Affective Evals
Prompt for generating Affective Evals is in `code/prompt_instructions/` and the python script is at `code/src/affect.py`. To generate, run the following commands:
1. `cd code/src`
2. `python affect.py` This file populates the causal template to generate the affective scenarios. We use an internal API to interact with LLMs. You can replace the API with standard APIs. We recommend using the latest LLMs for better results.
3. `python generate_conditions.py` for generating conditions by stitching the affective scenarios.
4. See `code/facs_expression` for instructions on generating FACS expressions.

#### 🤠 Human Experiments
We provide code to run Human experiments of 2 kinds:
1. Prolific Experiment for Testing Human Participants with text based stimuli: `code/prolific-exp-1`
2. Prolific Experiment for Testing Human Participants with image based stimuli: `code/prolific-exp-2`

#### 🤖 Evaluating Models
We provide code to evaluate models on the affective stimuli in `code/src/evaluate_llm.py`. To evaluate models on the multimodal stimuli, see `code/src/evaluate_x_llm.py`.
For both these files, you will need to install the appropriate packages to interact with the LLMs.

#### 📦 Data
The data used in the paper is in `data/`. The data is organized into conditions, images, and results. The results are organized into 2 folders: one for text-based stimuli `data/conditions_1` and the other for image-based stimuli `data/conditions_2`. The images used in the image-based stimuli are in `data/images`. `data/x_results` contains the results for multimodal stimuli and `data/results` contains the results for text-based stimuli.

#### 📊 Analysis
See `code/analysis` for code to analyze the data collected from human experiments.
