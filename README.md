# Player
### Feature Extraction from txt, xml (TEI), and Word files for dramatic plays.
<img src="https://user-images.githubusercontent.com/35588235/89479487-cff7e100-d747-11ea-9918-09b71905e58f.png" alt="masks" height="200"/>

### Project Description
The package creates features creates features from play texts.

### Current Project Owners:
|Project Owners     
|---------
Inna Wendell

---
---
---

# Usage
How do I use this code as a library? 
Clone the repo and run:
`python setup.py install`

or install using pip from the github directory:

`pip install git+https://github.com/innawendell/player.git`


## txt_processor.py
This script processes Russian (old or new orthography) txt files with a custom markup.
* For more details on the tags: https://github.com/innawendell/European_Comedy/blob/master/TAGS_EXPLANATION.md.
* Examples of text files: https://github.com/innawendell/European_Comedy/tree/master/Russian_Comedies/Txt_files

Three arguments are required to run this script:
1. `input_path` The path where the txt files are stored.
2. `ouput_path` The path where the json files should be saved.
3. `metadata_path` The path to the metadata tab-delimited file.

Example of a metadata file: https://github.com/innawendell/European_Comedy/blob/master/Russian_Comedies/Russian_Comedies.tsv
	

### Run this script:
```
txt_processor.py -i "Russian_Comedies/Txt_files/" \
-o "Russian_Comedies/Play_Jsons/" \
-m "Russian_Comedies/Russian_Comedies.tsv"
```

## russian_tei_processor.py
* This script processes xml (TEI) files in Russian obtained from https://dracor.org/. 
* The markup was adjusted to meet our research goals. 
* For more details, see https://github.com/innawendell/European_Comedy/blob/master/TAGS_EXPLANATION.md.

Examples of the Russian TEI files: https://github.com/innawendell/European_Comedy/tree/master/Russian_Comedies/TEI_files.

Two agruments are required to run this script:
1. `input_path` The path where the TEI files are stored.
2. `ouput_path` The path where the json files should be saved.

Additionally, a user can specify two optional arguments:
1. `custom_flag` Boolean, where `True` indicates that a user will be suppplying a custom metadata file. 
	Default value is `False`, in which case the script uses metadata from the TEI file.
2. `metadata_path` The path to the metadata tab-delimited tsv file.

Example of a metadata file: https://github.com/innawendell/European_Comedy/blob/master/Russian_Comedies/Russian_Comedies.tsv.

Note: if the corpus includes plays written in free iambs, you will need to provide a metadata file, since this information
is not recorded in the TEI.

### Run this script with default arguments:
```
russian_tei_processor.py -i "Russian_Comedies/TEI_files/" \
-o "Russian_Comedies/Play_Jsons/" 
```
### Run this script with optional arguments:
```
russian_tei_processor.py -i "Russian_Comedies/TEI_files/" \
-o "Russian_Comedies/Play_Jsons/" \
-c True \
-m "Russian_Comedies/Russian_Comedies.tsv"
```

## french_tei_processor.py
* This script processes xml (TEI) files in French obtained from http://www.theatre-classique.fr/. 
* The markup was adjusted to meet our research goals. 
* For more details, see https://github.com/innawendell/European_Comedy/blob/master/TAGS_EXPLANATION.md.

Examples of the French TEI files: https://github.com/innawendell/European_Comedy/tree/master/French_Comedies/TEI_files.

Two agruments are required to run this script:
1. `input_path` The path where the TEI files are stored.
2. `ouput_path` The path where the json files should be saved.

Additionally, a user can specify two optional arguments:
1. `custom_flag` boolean, `True` indicates that you will be using your custom metadata file. 
	The default value is `False`, in which case the script uses metadata from the TEI file.
2. `metadata_path` The path to the metadata tab-delimited file.

Example of a metadatafile: https://github.com/innawendell/European_Comedy/blob/master/French_Comedies/French_Comedies.tsv.

### Run this script with default arguments:
```
french_tei_processor.py -i "French_Comedies/TEI_files/" \
-o "French_Comedies/Play_Jsons/" \
```
### Run this script with optional arguments:
```
french_tei_processor.py -i "French_Comedies/TEI_files/" \
-o "French_Comedies/Play_Jsons/" \
-c True \
-m "French_Comedies/French_Comedies.tsv"
```

## french_word_processor.py
This script processes summaries of the French plays manually entered in Word Documents.

Examples of the Word Documents: https://github.com/innawendell/European_Comedy/tree/master/French_Comedies/Word_Docs.

Three agruments are required to run this script:
1. `input_path` The path where the Word Documents are stored.
2. `ouput_path` The path where the json files should be saved.
3. `metadata_path` The path to the metadata tab-delimited file.

Example of a metadata file: https://github.com/innawendell/European_Comedy/blob/master/French_Comedies/French_Comedies.tsv.

### Run this script:
```
french_word_processor.py -i "French_Comedies/Word_Docs/" \
-o "French_Comedies/Play_Jsons/" \
-m "French_Comedies/French_Comedies.tsv"
```

## shakespeare_processor.py
* This script processes xml (TEI) files in English obtained from https://dracor.org/shake.
* The markup was adjusted to meet our research goals. 
* For more details, see https://github.com/innawendell/European_Comedy/blob/master/TAGS_EXPLANATION.md.

Examples of Shakespeare's TEI files:
https://github.com/innawendell/European_Comedy/blob/master/Contrastive_Material/TEI_files.


Two agruments are required to run this script:
1. `input_path` The path where the TEI files are stored.
2. `ouput_path` The path where the json files should be saved.

Additionally, a user can specify two optional arguments:
1. `custom_flag` boolean, `True` indicates that you will be using your custom metadata file. 
	The default value is `False`, in which case the script uses metadata from the TEI file.

Metadata file has to follow this format: https://github.com/innawendell/European_Comedy/blob/master/Contrastive_Material/Contrastive_material.tsv.

### Run this script with default arguments:
```
shakespeare_processor.py -i "Contrastive_Material/TEI_files/"" \
-o "Contrastive_Material/Play_Jsons/"" 
```

### Run this script with optional arguments:
```
shakespeare_processor.py -i "Contrastive_Material/TEI_files/"" \
-o "/Contrastive_Material/Play_Jsons/" \
-c True \
-m "Contrastive_Material/Contrastive_material.tsv"
```	


## generic_word_processor.py
This script processes summaries of the plays in any language manually entered in Word Documents.

Examples of the Word Documents: https://github.com/innawendell/European_Comedy/tree/master/Contrastive_Material/Word_Docs.

Three agruments are required to run this script:
1. `input_path` The path where the Word Documents are stored.
2. `ouput_path` The path where the json files should be saved.
3. `metadata_path` The path to the metadata tab-delimited file.

Metadata file has to follow this format: https://github.com/innawendell/European_Comedy/blob/master/Contrastive_Material/Contrastive_material.tsv.

### Run this script:
```
generic_word_processor.py -i '../European_Comedy/Contrastive_Material/Word_Docs/' \
-o '../European_Comedy/Contrastive_Material/Play_Jsons/' \
-m '../European_Comedy/Contrastive_Material/Contrastive_material.tsv'
```

## Scripts
All scripts in directory `scripts` are automatically installed into the path.

# Development

### conda
How do I enhance libraries, add new code and run tests on existing code in this repo?
```
conda create --name player python=3.7 --yes
conda activate player
python setup.py develop
conda install --name player --file requirements.txt --yes
```
