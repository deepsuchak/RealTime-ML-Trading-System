from typing import List
import pandas as pd

import hopsworks
from src.config import hopsworks_config as config
def push_value_to_feature_store(
        value: dict,
        feature_group_name: str,
        feature_group_version: int,
        feaure_group_primary_keys: str,
        feature_group_event_time: str):
    '''
    Pushes the value to the feature store (given the feature_group_name)

    Args:
        value: Value to push to the feature store
        feature_group_name: Feature group name
        feature_group_version: Feature group version
        feaure_group_primary_key: Feature group primary key
        feature_group_event_time: Feature group event time

    Returns:
        None
    ''' 
    project = hopsworks.login(project=config.hopsworks_project_name,
                              api_key_value=config.hopsworks_api_key)

    feature_store = project.get_feature_store()

    feature_group = feature_store.get_or_create_feature_group(
        name=feature_group_name,
        version=feature_group_version,
        primary_key=feaure_group_primary_keys,
        event_time =feature_group_event_time,
        online_enabled=True,
        # expectation_suite=expectation_suite_transactions
    )

    # transform value to a pandas dataframe
    
    value_df = pd.DataFrame([value])

    # push the value to the feature group
    feature_group.insert(value_df)


