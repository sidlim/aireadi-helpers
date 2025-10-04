import os
import numpy as np
import pandas as pd

def load_patients(dataset_directory):
    df = pd.read_csv(os.path.join(dataset_directory, 'participants.tsv'), sep='\t')
    # Every other file uses the column name 'person_id' rather than 'participant_id', so let's fix this:
    df['person_id'] = df['participant_id']
    return(df)

def load_conditions(dataset_directory, patients_df, mapping = {'Glaucoma': 437541}):
    df = patients_df.copy()
    cond_unfiltered = pd.read_csv(os.path.join(dataset_directory, 'clinical_data/condition_occurrence.csv'))
    # Initialize with not having condition:
    for condition in mapping.keys():
        df[condition] = False
    # If the pt has the condition, set to True
    for condition, code in mapping.items():
        subset = cond_unfiltered[cond_unfiltered['condition_concept_id'] == code]
        df.loc[df['person_id'].isin(subset['person_id']), condition] = True
    return(df)

def load_measurements(dataset_directory, patients_df, mapping = {'Systolic Blood Pressure': 3004249}):
    # TODO: Handle types of measurements (SBP and DBP are examples) that are repeated for some patients
    # Probably groupby person_id -> mean -> merge
    df = patients_df.copy()
    meas_unfiltered = pd.read_csv(os.path.join(dataset_directory, 'clinical_data/measurement.csv'))
    # Match the measurement person_id to the df person_id and add data cols:
    for measurement, code in mapping.items():
        subset = meas_unfiltered[meas_unfiltered['measurement_concept_id'] == code]
        subset.loc[subset['value_source_value'] == 'Invalid', 'value_as_number'] = np.nan
        df = df.merge(subset[['person_id', 'value_as_number']], on = 'person_id', how = 'left')
        df[measurement] = df['value_as_number']
        df = df.drop(columns = ['value_as_number'])
    return(df)

def get_imaging_paths(dataset_directory, patients_df, modality=None, manufacturer=None, model_name=None, anatomic_region=None, imaging=None):
    manifest = pd.read_csv(os.path.join(dataset_directory, f'retinal_{modality}/manifest.tsv'), sep = '\t')
    if (manufacturer is not None):
        manifest = manifest[manifest.manufacturer == manufacturer]
    if (model_name is not None):
        manifest = manifest[manifest.manufacturers_model_name == model_name]
    if (anatomic_region is not None):
        manifest = manifest[manifest.anatomic_region == anatomic_region]
    if (imaging is not None):
        manifest = manifest[manifest.imaging == imaging]
    manifest['person_id'] = manifest.participant_id
    return(manifest)

def get_fundus_paths(dataset_directory, patients_df, manufacturer=None, model_name=None, anatomic_region=None, imaging=None):
    return(get_imaging_paths(dataset_directory, patients_df, modality='photography', manufacturer=manufacturer, model_name=model_name, anatomic_region=anatomic_region, imaging=imaging))

def get_oct_paths(dataset_directory, patients_df, manufacturer=None, model_name=None, anatomic_region=None, imaging=None):
    return(get_imaging_paths(dataset_directory, patients_df, modality='oct', manufacturer=manufacturer, model_name=model_name, anatomic_region=anatomic_region, imaging=imaging))

def get_octa_paths(dataset_directory, patients_df, manufacturer=None, model_name=None, anatomic_region=None, imaging=None):
    return(get_imaging_paths(dataset_directory, patients_df, modality='octa', manufacturer=manufacturer, model_name=model_name, anatomic_region=anatomic_region, imaging=imaging))

def get_flio_paths(dataset_directory, patients_df, manufacturer=None, model_name=None, anatomic_region=None, imaging=None):
    return(get_imaging_paths(dataset_directory, patients_df, modality='flio', manufacturer=manufacturer, model_name=model_name, anatomic_region=anatomic_region, imaging=imaging))

'''

_omop_key = pd.read_csv('./omop_table.tsv', sep = '\t')
_omop_key['SRC_CD_ DESCRIPTION'] = _omop_key['SRC_CD_ DESCRIPTION'].fillna('')

def code_matches(codes):
    return(_omop_key[_omop_key['TARGET_ CONCEPT_ID'].isin(codes)])

def get_value_encoding(code):
    entries = _omop_key[_omop_key['TARGET_ CONCEPT_ID'] == code]
    mappings = entries['Choices, Calculations, OR Slider Labels From REDCap CODEBOOK']
    dict_str = mappings[mappings.notnull()].values[0]
    pair_strs = dict_str.split(' | ')
    pairs = map(lambda str: str.split(', '), pair_strs)
    return({float(pair[0]): pair[1] for pair in pairs})

def desc_includes(desc_substring):
    matches = _omop_key['SRC_CD_ DESCRIPTION'].str.contains(desc_substring)
    return(_omop_key[matches])

def load_observations(df, mapping = {'Marital Status': 3004249}):
    df = df.copy()
    obs_unfiltered = pd.read_csv(os.path.join(_data_dir, 'clinical_data/observation.csv'))
    # Match the measurement person_id to the df person_id and add data cols:
    for observation, code in mapping.items():
        subset = obs_unfiltered[obs_unfiltered['observation_concept_id'] == code]
        encoding = get_value_encoding(code)
        ordered_categories = [v for k,v in sorted(encoding.items(), key=lambda pair: pair[0])]
        temp_merge = df[['person_id']].merge(subset[['person_id','value_as_number']], on = 'person_id', how = 'left')
        if temp_merge['value_as_number'].isnull().any():
            ordered_categories.insert(0, 'Not Applicable')
            temp_merge = temp_merge.fillna('Not Applicable')
        df[observation] = pd.Categorical(temp_merge['value_as_number'].replace(encoding), 
                                         categories = ordered_categories, ordered = True)
    return(df)

'''