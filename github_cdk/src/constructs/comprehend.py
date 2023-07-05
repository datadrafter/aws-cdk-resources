from aws_cdk import aws_comprehend as comprehend

cfn_flywheel = comprehend.CfnFlywheel(self, "MyCfnFlywheel",
    data_access_role_arn="dataAccessRoleArn",
    data_lake_s3_uri="dataLakeS3Uri",
    flywheel_name="flywheelName",

    # the properties below are optional
    active_model_arn="activeModelArn",
    data_security_config=comprehend.CfnFlywheel.DataSecurityConfigProperty(
        data_lake_kms_key_id="dataLakeKmsKeyId",
        model_kms_key_id="modelKmsKeyId",
        volume_kms_key_id="volumeKmsKeyId",
        vpc_config=comprehend.CfnFlywheel.VpcConfigProperty(
            security_group_ids=["securityGroupIds"],
            subnets=["subnets"]
        )
    ),
    model_type="modelType",
    tags=[CfnTag(
        key="key",
        value="value"
    )],
    task_config=comprehend.CfnFlywheel.TaskConfigProperty(
        language_code="languageCode",

        # the properties below are optional
        document_classification_config=comprehend.CfnFlywheel.DocumentClassificationConfigProperty(
            mode="mode",

            # the properties below are optional
            labels=["labels"]
        ),
        entity_recognition_config=comprehend.CfnFlywheel.EntityRecognitionConfigProperty(
            entity_types=[comprehend.CfnFlywheel.EntityTypesListItemProperty(
                type="type"
            )]
        )
    )
)