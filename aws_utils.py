import os
from boto3.s3.transfer import S3Transfer
import boto3
import constants


def upload_file_to_aws(filepath):
    """
    This function uploads the given file to aws s3 and makes its access
    rights - public read.
    :param filepath: Local path of the file to be uploaded. (String)
    :return: AWS link of the file uploaded. (String)
    """
    try:
        client = boto3.client('s3', aws_access_key_id=constants.aws_access_key_id,
                              aws_secret_access_key=constants.aws_secret_access_key)
        transfer = S3Transfer(client)
        filename = os.path.basename(filepath)
        transfer.upload_file(filepath, constants.bucket_name, constants.aws_folder_name + "/" + filename)
        response = client.put_object_acl(ACL='public-read', Bucket=constants.bucket_name,
                                         Key="{}/{}".format(constants.aws_folder_name, filename))
        aws_file_link = "{}/{}/{}".format(constants.aws_file_link, constants.aws_folder_name, filename)
        return aws_file_link
    except Exception as err:
        msg = "Error occured while uploading file on aws. Error : {}".format(err)
        return msg
