from player import french_word_functions as fwf 
import numpy as np
import pandas as pd
import docx2txt
import re
import json
from os import listdir
from collections import Counter
import copy

def process_all_plays(input_directory, output_path, metadata_path):
    """
    The function allows to process all files in a specified directory.
    Params:
        input_directory - the path to the folder containing the txt files
        output_path - directory in which the json summaries will be saved.
        metadata_path - path to the metadata file, a tab-delimited txt file with informtion about all plays.
        regex_pattern - a regex pattern which identifies dramatic character names.
    Returns:
        no returns, the files will be saved in output_path directory.
    """
    all_files = [f for f in listdir(input_directory) if f.count('.docx') > 0]
    metadata_df = pd.read_csv(metadata_path, sep='\t')
    # identify what does the beginning of the play indices looks like, e.g., 'F_', 'C_', etc.
    play_indices_start = ''.join([symbol for symbol in metadata_df['index'][0] if not symbol.isdigit()])
    for file in all_files:
        print(file)
        play_data_dict = process_play(input_directory + file, metadata_df, input_directory, play_indices_start)
        json_name = output_path + str(file.replace('.docx', '.json'))
        with open(json_name, 'w') as fp:
            json.dump(play_data_dict, fp, ensure_ascii=False, indent=2)


def process_play(file_name, metadata_df,  input_path, play_indices_start):
    """
    The function parses a txt file and creates a summary with features and metadata for the play.
    Params:
        file_name - a string, name of the file with the play text.
        metadata_df - a dataframe containing the info about the play.
        play_indices_start - a string, the beginning of the play indices looks like, e.g., 'F_', 'C_', etc.
    Returns:
        play_data - a dictionary with detailed play summary by scenes, metadata, and features
    """
    play_index = file_name.replace(input_path, '').replace('.docx', '').replace(play_indices_start, '')
    play_meta = metadata_df[metadata_df['index'] == play_indices_start + play_index][['title', 'last_name',
                                                                                      'first_name', 'date']].values
    comedy = docx2txt.process(file_name)
    play_data = fwf.add_play_info(play_meta)
    play_data = process_play_summary(play_data, comedy)
    play_data['metadata'] = fwf.metadata_processing(comedy, play_data)

    return play_data


def parse_characters(play_text):
    """
    The function creates a dictionary where the keys are dramatic characters and values
    are their collective_numbers if applicable.
    Params:
        play_text - a string with the play summary.
    Returns:
        characters_summary - the dictionary with dramatic character info.
    """
    play_text = play_text.replace('\n\n', '\n')
    characters_summary = {}
    characters = play_text[play_text.find('DRAMATIC CHARACTERS') + len('DRAMATIC CHARACTERS'):
                           play_text.find('ACT 1')]
    noise = ['', ' ', '\xa0', '-', '–', '/']
    dramatic_characters = [character.strip() for character in characters.split('\n') if character not in noise]
    for character in dramatic_characters:
        collective_number = re.findall(r'\d', character)
        if len(collective_number) == 0:
            characters_summary[character] = {'collective_number': None}
        else:
            number = collective_number[0]
            character = character.replace(number, '').strip()
            characters_summary[character] = {'collective_number': int(number)}

    return characters_summary


def character_parsing(names, characters):
    """
    The function processes a scene and counts the number of speaking and non-speaking characters.
    Params:
        names - lines of strings with dramatic character names accompanied by "NON_SPEAKING" in case they are not speaking.
        characters - a dictionary with the info about evey dramaic character of the play.
    Returns:
        scene_characters - the dictionary with the number of speaking and non-speaking characters in the scene.
    """
    scene_characters = {}
    for name in names:
        symbols = ['-', '–', '*', '/']
        for symbol in symbols:
            name = name.replace(symbol, '')
        if name.lower().count('non_speaking') > 0:
            name = name.lower().replace('non_speaking', '').upper()
            speaking_status = 'non_speaking'
        else:
            speaking_status = 'speaking'
        name = name.strip()
        if name.isdigit() is False and name != '':
            scene_characters[name] = speaking_status
    speech_dict = fwf.speach_analysis(scene_characters, characters)
    scene_characters['num_speakers'] = speech_dict['number_speaking_characters']
    scene_characters['perc_non_speakers'] = speech_dict['percentage_non_speaking']

    return scene_characters


def process_play_summary(play_data, play_text):
    play_data['characters'] = parse_characters(play_text)
    play_summary = {}
    noise = ['', ' ', '\xa0', '-', '–', '/']
    acts = [act for act in play_text[play_text.find('ACT 1'):].split('ACT') if act not in noise]
    for act_num, act in enumerate(acts, 1):
        scenes = [scene.strip() for scene in act.split('SCENE')][1:]
        play_summary['act_' + str(act_num)] = fwf.parse_scenes(scenes,  play_data['characters'])
    play_data['play_summary'] = play_summary

    return play_data
