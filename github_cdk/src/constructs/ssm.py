from aws_cdk import aws_ssm
from aws_cdk import aws_s3

def _create_ssm_parameter(
    self, my_bucket: aws_s3.Bucket, config_file_path: str,
) -> None:
    path_name = "/folder1/subfolder1/subfolder2"
    config_file_path = "/folder1/subfolder1/subfolder2"
    my_bucket = "my_s3_bucket"
    aws_ssm.StringParameter(
        self,
        id=path_name,
        parameter_name=path_name,
        string_value=config_file_path,
        description="This parameter will contail the bucket storing the config file"
    )

    path_param_name: "/folder1/subfolder1/subfolder2"
    aws_ssm.StringParameter(
        self,
        id=path_param_name,
        parameter_name=path_param_name,
        string_value=config_file_path,
        ddescription="This parameter will contail the bucket storing the config file",
    )

    _create_ssm_parameter(my_bucket,config_file_path)