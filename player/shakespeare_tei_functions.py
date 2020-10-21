import pandas as pd
from os import listdir
from bs4 import BeautifulSoup as bs
import json
from player import russian_tei_functions as rtf
from player import text_processing_functions as tpf
from player import french_tei_functions as ftf


def process_all_plays(input_directory, output_path, custom_flag=False, metadata_path=None):
    """
    The function allows to process all files in a specified directory.
    Params:
        input_directory - the path to the folder containing the txt files
        output_path - directory in which the json summaries will be saved.
        metadata_path - path to the metadata file, a tab-delimited txt file with informtion about all plays.
    Returns:
        no returns, the files will be saved in output_path directory.
    """
    all_files = [f for f in listdir(input_directory) if f.count('.xml') > 0]
    if custom_flag:
        metadata_df = pd.read_csv(metadata_path, sep='\t')
    else:
        metadata_df = pd.DataFrame()
    for file in all_files:
        play_data_dict = process_play(input_directory + file, metadata_df, custom_flag)
        json_name = output_path + str(file.replace('.xml', '.json'))
        with open(json_name, 'w') as fp:
            json.dump(play_data_dict, fp, ensure_ascii=False, indent=2)


def process_play(file_name, metadata_df, custom_flag):
    """
    The function parses a txt file and creates a summary with features and metadata for the play.
    Params:
        file_name - a string, name of the file with the play text.
        metadata_df - a dataframe containing the info about the play.
    Returns:
        play_data - a dictionary with detailed play summary by scenes, metadata, and features
    """
    print(file_name)
    with open(file_name, 'r') as file:
        soup = bs(file, 'lxml')
    if custom_flag:
        if file_name.count('/') > 0:
            play_index = file_name.split('/')[-1].replace('.xml', '')
        else:
            play_index = file_name.replace('.xml', '')
        play_meta = metadata_df[metadata_df['index'] == play_index][['title', 'last_name',
                                                                     'first_name', 'date']].values
    else:
        play_meta = []
    play_data = add_play_info(soup, play_meta, custom_flag)
    play_data['characters'] = create_character_cast(soup)
    play_data['play_summary'] = process_summary(soup, play_data['characters'])
    play_data['metadata'] = additional_metadata(soup, play_data)

    return play_data



def create_character_cast(play_soup):
    """
    The function creates a dictionary where the keys are dramatic characters and values are their alternative names 
    and collective_numbers if applicable.
    Params:
        play_soup - play xml turned into beautiful soup object.
    Returns:
        character_dict - the dictionary with dramatic character info.
    """
    character_dict = {}
    dramatic_characters = play_soup.find_all('person') + play_soup.find_all('persongrp')
    for character_tag in dramatic_characters:
        character_dict[character_tag['xml:id'].split('_')[0]] =  {"alternative_names": 
                                                                  character_tag['xml:id']}

                                                                                 
    return character_dict


def process_summary(soup, character_cast_dictionary):  
    act_info = {}
    acts = soup.find_all('div', {'type': 'act'})
    for act_num, act in enumerate(acts, 1):
        scenes = act.find_all('div', {'type': ['scene', 'extra_scene']})
        act_info['act'+'_'+str(act_num)] = ftf.parse_scenes(scenes, 
                                                        character_cast_dictionary)
    return act_info


def additional_metadata(play_soup, play_data):
    """
    Process all play features.
    """
    metadata_dict = {}
    for process in [process_speakers_features, 
                    percentage_of_scenes_discont_change]:
        metadata_dict = process(play_soup, play_data, metadata_dict)

    return metadata_dict


def find_speakers(scene):
    """
    The function creates a list of the speakers in a scene in the order of their utterances. 
    The number of times a speaker appears in the list corresponds to the number of utterances the speaker makes.
    Params:
        scene - a beautiful soup object of the scene xml.
    Returns:
        speakers_lst - a list of speakers in the scene.
    """
    speakers_lst = []
    speakers = [utterance['who'] for utterance in scene.find_all('sp')]
    for speaker in speakers:
        speaker_count = str(speaker).count(' ')
        # if multiple speakers
        if speaker_count > 0:
            multiple_speakers = str(speaker).split(' ')
            [speakers_lst.append(sp.strip()) for sp in multiple_speakers]
        else:
            speakers_lst.append(speaker)
   
    return speakers_lst


def extract_utterances(character_cast_dict, scene):
    """
    The function identifies all utterances in a scene and creates a list of dramatic characters who
    make those utterances.
    Params:
        character_cast_dict - a dictionary where keys are dramatic characters and values are their alterantive names
                              and collective numbers.
        scene - a beautiful soup object of the scene xml.
    Returns:
        utterance_lst - a list of speakers who make utterances in the given scene.
    """
    # look up by alternative name
    reverse_dict = dict(zip([val['alternative_names'] for val in character_cast_dict.values()],
                            character_cast_dict.keys()))

    utterance_lst = [reverse_dict[name.replace('#', '')] for name in find_speakers(scene)]
    
    return utterance_lst
