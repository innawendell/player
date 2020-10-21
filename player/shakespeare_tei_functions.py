import pandas as pd
from os import listdir
from bs4 import BeautifulSoup as bs
import json
import copy
from player import russian_tei_functions as rtf
from player import text_processing_functions as tpf
from player import french_tei_functions as ftf
from player import russian_tei_functions as rtf
from player import text_processing_functions as tpf


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


def add_play_info(soup, metadata, custom_flag=False):
    """
    Update play metadata from the metadata_df. We can provide our own metadata or use the TEI metadataa
    """
    play_data = {}
    if custom_flag:
        play_data['title'] = metadata[0][0]
        first_name = metadata[0][2]
        if type(first_name) != float:
            play_data['author'] = str(metadata[0][1] + ', ' + first_name).strip()
        else:
            play_data['author'] = metadata[0][1].strip()
        play_data['creation_date'] = metadata[0][3]
    else:
        play_data['title'] = soup.find('title').get_text()
        play_data['author'] = soup.find('author').get_text()
        play_data['creation_date'] = int(soup.find('date', {'type': 'written'})['when'])
        
    return play_data


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
        act_info['act'+'_'+str(act_num)] = parse_scenes(scenes, 
                                                        character_cast_dictionary)
    return act_info

def number_present_characters(play_dictionary):
    """
    The function calculates the number of characters present in the play. If a character is listed in cast, but doesn't
    appear on stage, he/she doesn't count.
    Params:
        play_dictionary - a dictioanry with data for the play, which includes the characters present in each scene.
    Returns:
        total_number_present_characters - int.
    """
    all_present_characters = set()
    for key in play_dictionary['play_summary'].keys():
        for scene in play_dictionary['play_summary'][key]:
            for item in play_dictionary['play_summary'][key][scene].keys():
                if item != 'num_utterances' and item != 'num_speakers' and item != 'perc_non_speakers':
                    all_present_characters.add(item)
    total_number_present_characters = 0
    appearing_on_stage = set(play_dictionary['characters']).intersection(all_present_characters)
    for character in appearing_on_stage: 
        total_number_present_characters += 1
  
    return total_number_present_characters


def process_speakers_features(soup, play_data, metadata_dict):
    """
    Iarkho's features described in Iarkho's work on the evolution of 5-act tragedy in verse.
    """
    metadata_dict['num_present_characters'] = number_present_characters(play_data)
    metadata_dict['num_scenes_text'] = tpf.estimate_number_scenes(play_data['play_summary'])[0]
    metadata_dict['num_scenes_iarkho'] = tpf.estimate_number_scenes(play_data['play_summary'])[1]
    play_summary_copy = copy.deepcopy(play_data['play_summary'])
    distribution, speech_types, non_speakers = tpf.speech_distribution_iarkho(play_summary_copy)
    metadata_dict['speech_distribution'] = distribution
    metadata_dict['percentage_monologues'] = speech_types['perc_monologue']
    metadata_dict['percentage_duologues'] = speech_types['perc_duologue']
    metadata_dict['percentage_non_duologues'] = speech_types['perc_non_duologue']
    metadata_dict['percentage_above_two_speakers'] = speech_types['perc_over_two_speakers']
    metadata_dict['av_percentage_non_speakers'] = non_speakers
    metadata_dict['sigma_iarkho'] = round(tpf.sigma_iarkho(
                                    [item[0] for item in metadata_dict['speech_distribution']],
                                    [item[1] for item in metadata_dict['speech_distribution']]), 3)
    
    return metadata_dict


def additional_metadata(play_soup, play_data):
    """
    Process all play features.
    """
    metadata_dict = {}
    for process in [process_speakers_features, 
                    rtf.percentage_of_scenes_discont_change]:
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


def identify_scene_cast(scene, scene_status):
    """
    The function parses the scene xml and identifes the string that contains the dramatic characters' who are present 
    in the scene.
    Params:
        scene - a beautiful soup object of the scene xml.
        scene_status - if a scene_status is "extra" the character cast would be given in the markup,
                        e.g., cast="#King_LLL #Berowne_LLL,."
    Returns:
        scene_cast - a string that contains the dramaric characters present in the scene.

    """
    if scene_status.count('extra') != 0 :
        scene_cast = str(scene['cast'])
    else:
        scene_cast = str(scene.find_all('stage')[0]['who'])
        
    #remove noise from names
    scene_cast = [name.split('_')[0] for name in scene_cast.replace('#', '').split(' ')]
    
    return scene_cast


def count_utterances(scene, character_cast_dict, scene_status):
    """
    The function counts the number of utterances each dramatic character makes in a given scene.
    Params:
        scene - a beautiful soup object of the scene xml.
        character_cast_dict - a dictionary where keys are dramatic characters and values are their alterantive names
                              and collective numbers.
        characters_current_scene - a list of dramatic characters that are listed for the scene.
        excluded_characters - a list of characters who are listed as exluded.
        scene_status - scene_status - whether a scene is regular or extra.
    Returns:
        scene_ino - a dictionary where keys are charcters and values are the number of utterances.
    """
    scene_info = {}
    scene_cast = identify_scene_cast(scene, scene_status)
    # account for dramatic characters from a previous scene re-appearing in the new scene.
    utterance_lst = extract_utterances(character_cast_dict, scene)
    # run a quality check
    ftf.check_cast_vs_speakers(scene_cast, utterance_lst, scene)
    # count how many utterances each speaker makes
    scene_info = ftf.count_handler(scene_cast, utterance_lst)
        
    return scene_info



def parse_scenes(scenes, character_cast_dictionary):
    """
    The function goes through a list of scenes and updates complete_scene_info dictionary with informtion
    about each scene speaking characters, their utterance counts, and percentage of non-speaking characters.
    Params:
        scenes - a list scenes.
        name_pattern - regex expression for identifying character names.
        character_cast_dictionary, reverse_character_cast - dictionaries for lookup of alternative names 
                                                            for each dramatic character.
    Returns:
        complete_scene_info - a dictionary where keys are scenes and values are dramatic characters and their 
                             utternace counts as well as the number of speakers and percentage of non-speakers.
    """
    other_meta_fields = ['num_speakers', 'perc_non_speakers', 'num_utterances']
    complete_scene_info = {} 
    scene_names = []
    sc_num = 0
    extra_scene_number = 1
    for scene in scenes:
        scene_status, sc_num, extra_scene_number = rtf.handle_scene_name_and_count(scene, sc_num, extra_scene_number)
        if sc_num != 1 :
            previous_cast = [name for name in complete_scene_info[scene_names[-1]].keys()
                            if name not in other_meta_fields]
        else:
            previous_cast = []
        scene_summary = count_utterances(scene, character_cast_dictionary, scene_status)
        scene_summary['num_utterances'] = sum(list(scene_summary.values()))
        scene_summary['num_speakers'], scene_summary['perc_non_speakers'] = ftf.count_characters(scene_summary)
        if float(sc_num) > 1:
            current_scene = [key for key in scene_summary.keys() if key not in other_meta_fields]
            scene_status = tpf.check_if_no_change(current_scene, previous_cast, scene_status)           
        complete_scene_info[str(sc_num) + '_' + str(scene_status)] =  scene_summary
        #check to make sure all character names are in scene cast as they appear in the play cast
        scene_names.append(str(sc_num) + '_' + str(scene_status))

    return complete_scene_info


