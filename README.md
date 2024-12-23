# project_template

## Outline of this README

- [Introduction](#introduction)
- [Workflow](#workflow)
- [Project Setup](#project-setup)
- [Folder Structure](#folder-structure)
- [How To](#how-to)
- [Typical Runtime](#typical-runtime)
- [Contact & Support](#contact--support)

## Introduction

Project/repo template I found useful

## Workflow

The pipeline consists of the following components:

- __Preprocessing__ - ingesting data and create intermediate features
- __Postprocessing__ - combining the results from the above models to generate veg analytics and features tables, including

```mermaid
%%{init: {"flowchart": {"htmlLabels": false}} }%%

flowchart LR

    subgraph "`**Template**`"

        direction LR
        subgraph Preprocessing
            A[input] ---> B[features]
        end

        subgraph Postprocessing
            B ---> C[outputs]
        end
    end



```

## Project Setup

0) Make sure you have `git` installed on your machine. I recommend using [Homebrew](https://brew.sh/) to install it on a Mac. I also recommend using Viusal Studio Code as your IDE.

    ```bash
    # installing git via homebrew
    brew install git

    # installing Visual Studio Code
    brew install --cask visual-studio-code
    ```

1) Clone this repo to your local machine, e.g.,

    ```bash
    git clone https://github.com/McK-Private/project_template.git
    ```

2) Create virual environment, after installing [Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) to your machine.

    From the terminal, run:

    ```bash
    conda env create -f environment.yml
    ```

3) Activate the environment. From the terminal, run:

    ```bash
    conda activate project_template
    ```

3) (If you use PDAL) Installation `pdal` for Python first!
PDAL Python support is hosted in a separate repository than PDAL itself at GitHub. If you have a working PDAL installation and a working Python installation, you can install the extension using the following procedure on Unix. The procedure on Windows is similar.

    ```bash
    conda install --channel conda-forge pdal python-pdal --name project_template
    ```

4) Make sure the environment is activated. `(project_template)` should be visible to the left of your terminal command line. Then install all the packages in requirements.txt by invoking:

    ```bash
    pip install -r requirements.txt
    ```

5) Install pre-commit so the repo is automatically formatted to [black](https://ljvmiranda921.github.io/notebook/2018/06/21/precommits-using-black-and-flake8/).

    From the terminal, run

    ```bash
    pre-commit install

    # optional (this will run automatically with each commit)
    pre-commit run --all-files
    ```

## Folder Structure

This project files are structured as follows:

```bash

.
├── data                    # for all data files
│   ├── 01_raw
│   │
│   ├── 02_intermediate
│   │
│   ├── 03_primary
│   │
│   ├── 04_feature
│   │
│   ├── 05_model_input
│   │
│   ├── 06_models
│   │
│   ├── 07_model_output
│   │
│   └── 08_reporting
│
├── docs                    # for all documentation
│
├── experiments             # for experimental code / notebooks
│
└── src                     # for all source code
    └──utils
        ├── config.py
        └── helpers.py



```

## How-to

### Run the pipeline locally

1. ...

## Typical Runtime

The typical runtime is as follows:

| Step | Runtime |
|------|---------|
| Preprocessing | ??? hours |
| Postprocessing | ??? hours |

## Contact & Support

For general questions, access to the data or questions related to the pipeline please contact...:

- Person 1: [email](mailto: <xxx@yy.com>)
