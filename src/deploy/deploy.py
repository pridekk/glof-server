import os
import shutil
import json
import boto3
from datetime import datetime


def zip_lambdas(version: str = "20210728100001"):
    for item in config["lambda_folders"]:

        path = "../lambdas/" + item

        folder_names = []

        with open(path + "/seed.txt", "w") as seed_file:
            seed_file.write("for lambda provisioned concurrency deploy version:")
            seed_file.write(version)

        for folderName, subfolders, filenames in os.walk(path):
            folder_names.append(folderName)

        for folder in folder_names:
            if "__pycache__" in folder:
                shutil.rmtree(folder)

        shutil.make_archive(f"lambdas/{version}/{item.split('/')[-1]}", "zip", path)


def upload_lambdas(stage, version):
    s3 = boto3.client("s3", aws_access_key_id=config["stages"][stage]["access_key"],
                      aws_secret_access_key=config["stages"][stage]["secret_key"],
                      region_name=config["stages"][stage]["region"])

    for file in os.listdir(f"lambdas/{version}"):
        print(file)
        print(f"lambdas/{version}/{file}")
        response = s3.upload_file(Filename=f"lambdas/{version}/{file}",
                                  Bucket=config["stages"][stage]["bucket"],
                                  Key=f'lambdas/{config["stages"][stage]["folder"]}/{version}/{file}')
        print(response)


def update_formation(stackname: str, stage: str, version: str, region: str):

    cloud_formation = boto3.client("cloudformation", region)

    cloud_formation.update_stack(StackName=stackname,
                                 TemplateURL=f"https://glof-test.s3.us-east-1.amazonaws.com/formations/glof_{stage}.yaml",
                                 Parameters=[{"ParameterKey": "LambdaVersion", "ParameterValue": version},
                                             {"ParameterKey": "DeployStage", "ParameterValue": stage}],
                                 Capabilities=['CAPABILITY_AUTO_EXPAND', 'CAPABILITY_NAMED_IAM', 'CAPABILITY_IAM'])


def create_formation(stackname: str, stage: str, version: str, region: str):

    cloud_formation = boto3.client("cloudformation", region)

    cloud_formation.create_stack(StackName=stackname,
                                 TemplateURL=f"https://glof-test.s3.us-east-1.amazonaws.com/formations/glof_{stage}.yaml",
                                 Parameters=[{"ParameterKey": "LambdaVersion", "ParameterValue": version},
                                             {"ParameterKey": "DeployStage", "ParameterValue": stage}],
                                 Capabilities=['CAPABILITY_AUTO_EXPAND', 'CAPABILITY_NAMED_IAM', 'CAPABILITY_IAM'])


config = json.load(open("config.json"))

if __name__ == "__main__":
    version = datetime.now().strftime("%Y%m%d%H%M%S")
    # version = "20210907100330"
    # zip_lambdas(version)
    version = "20211108233723"
    # upload_lambdas("dev", version)
    # upload_lambdas("prod", version)
    update_formation("GLOF-DEV", "dev", version, 'us-east-1')
    # create_formation("SPEC-BATCH-PROD", "prod", version)
