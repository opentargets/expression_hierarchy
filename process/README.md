# Expression hierarchy process
This README describes the intended process for generating the hierarchy displayed in the UI.

## Inputs
The hierarchy as displayed on the UI has the following inputs:
* `merged_rna_protein_tissues.txt` The tissue names provided to OT from the RNA and protein
* `organs.tsv` Hierarchy from Expression Atlas
* `anatomical_systems.tsv` Hierarchy from Expression Atlas
* `curations.tsv` Manual curations (see below)

### Notes on inputs
* Tissue name is used as an index, but multiple tissue names are linked to the same `UBERON` codes in the organs.txt and anatomical_systems.txt files.

## Outputs
* `map.json` This file is intended to allow quick access to organs and anatomical systems associated with a specific tissue name.
* `hierarchy.json` This file contains the same information as `map.json` but from the perspective of the organs and anatomical systems (ie. these are the keys).

## Manual curation
Note that the following tissues have slightly different names in the RNA and protein expression data, but are considered the same. The process of generating the hierarchy uses the `curations.tsv` file to map these.
```
endometrium == endometrium 1 == endometrium 2
gallbladder == gall bladder
prostate == prostate gland
salivary gland == saliva-secreting gland
skeletal muscle == skeletal muscle tissue
skin == skin 1 == skin 2
smooth muscle == smooth muscle tissue
soft tissue 1 == soft tissue 2 == soft tissue
stomach == stomach 1 == stomach 2
```