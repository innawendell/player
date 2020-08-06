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

or install using pip from the github directory in the regular mode:

`pip install git+https://github.com/innawendell/player.git`

or in the "editable" mode:
`pip install git+https://github.com/innawendell/player.git#egg=player`

## txt_processor.py
This script processes text files in the txt with a custom markup.
Three arguments are required to run this script:
1. `input_path` The path where the txt files are stored.
2. `ouput_path` The path where the json files should be saved.
3. `metadata_path` The path to the metadata tab-delimited tsv file.
Example of a metadata file: https://github.com/innawendell/European_Comedy/blob/master/Russian_Comedies/Russian_Comedies.tsv
	

### Run this script:
```
txt_processor.py -i "Russian_Comedies/Txt_files/" \
-o "Russian_Comedies/Play_Jsons/" \
-m "Russian_Comedies/Russian_Comedies.tsv"
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
