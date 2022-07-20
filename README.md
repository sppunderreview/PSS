# A New Spectral Similarity for Scalable Program Clone Search
Anonymized artifact for NDSS 2023 submission

# Download
In order to clone this repository, one needs git-lfs.
1. Install git-lfs https://www.atlassian.com/git/tutorials/git-lfs#installing-git-lfs
2. Type "git lfs clone git@github.com:sppunderreview/spp.git"

# Usage
One can produce LaTeX tables inside the "Results/" folder, using precomputed results disseminated into each framework folder.

## Basic computation
Paths have to be corrected:
1. Inside benchmark core scripts such as "GCoreutilsOptions/makeBenchCO.py".
2. Inside scripts for frameworks, such as "MutantX/" folder.

Inside a framework folder:
* 'RunMakeMD3.py' computes the results of a framework in scenario III.
* 'RunMakeMD.py' uses scenario III results to compute scenarios I and II results.
* 'RunMakeMD4.py' computes additional results needed in scenario IV.

### Some frameworks have a complex workflow
For instance, a function embedding requires a learning phase, embedding generation, and distance computation.

Only then should MDs be computed.

## Dataset
Dataset disassembling requires IDA Pro under a Linux system.
Asm2veck folder contains the Java source code for function embeddings Asm2Vec as well as IDA's disassembling process.