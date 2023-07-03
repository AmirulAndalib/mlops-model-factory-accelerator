from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
import argparse
from azure.ai.ml.entities import Data
from azure.ai.ml.constants import AssetTypes
import os
import json

parser = argparse.ArgumentParser("provision_endpoints")
parser.add_argument("--subscription_id", type=str, help="Azure subscription id")
parser.add_argument("--resource_group_name", type=str, help="Azure Machine learning resource group")
parser.add_argument("--workspace_name", type=str, help="Azure Machine learning Workspace name")
parser.add_argument("--data_purpose", type=str, help="data to be registered identified by purpose")
parser.add_argument("--data_config_path", type=str, help="data config path")
parser.add_argument("--environment_name",type=str,help="data config path")
 
args = parser.parse_args()

data_purpose = args.data_purpose
data_config_path = args.data_config_path
environment_name = args.environment_name

ml_client = MLClient(
    DefaultAzureCredential(), args.subscription_id, args.resource_group_name, args.workspace_name
)

config_file = open(data_config_path)
data_config = json.load(config_file)

for elem in data_config['datasets']:
    if 'DATA_PURPOSE' in elem and 'ENV_NAME' in elem:
        if data_purpose == elem["DATA_PURPOSE"] and environment_name == elem['ENV_NAME']:
            data_path = elem["DATA_PATH"]
            dataset_desc = elem["DATASET_DESC"]
            dataset_name = elem["DATASET_NAME"]


            aml_dataset = Data(
                path=data_path,
                type=AssetTypes.URI_FOLDER,
                description=dataset_desc,
                name=dataset_name,
            )

            ml_client.data.create_or_update(aml_dataset)

            aml_dataset_unlabeled = ml_client.data.get(name=dataset_name, label="latest")

            print(aml_dataset_unlabeled.latest_version)
            print(aml_dataset_unlabeled.id)