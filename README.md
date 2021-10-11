This folder is the supplemental material for the DAGM submission
"Diff2Dist: Learning Spectrally Distinct Edge Functions, with Applications to Cell Morphology Analysis".

tissue_mod contains the files we modified from the software package Tissue. These should replace the corrsponding
files from the official repository for Tissue, available here:
https://gitlab.com/slcu/teamHJ/tissue

DAGM_expts_and_figures.ipynb is a python notebook which runs the code used to produce all distance-learning figures in the main text.
Note we have not included the cell image dataset with this supplementary material, so some other similar dataset should be used. 

The code for processing cell mesh files (like those produced by Tissue) is in the folder image_proc. Since graph distance metrics
(not image analysis) is the main focus of this work we do not make any guarantees that this code will be of use. 
