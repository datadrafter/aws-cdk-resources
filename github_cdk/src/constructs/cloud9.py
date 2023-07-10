from aws_cdk import aws_cloud9 as cloud9

cfn_environment_eC2 = cloud9.CfnEnvironmentEC2(self, "MyCfnEnvironmentEC2",
    instance_type="instanceType",

    # the properties below are optional
    automatic_stop_time_minutes=123,
    connection_type="connectionType",
    description="description",
    image_id="imageId",
    name="name",
    owner_arn="ownerArn",
    repositories=[cloud9.CfnEnvironmentEC2.RepositoryProperty(
        path_component="pathComponent",
        repository_url="repositoryUrl"
    )],
    subnet_id="subnetId",
    tags=[CfnTag(
        key="key",
        value="value"
    )]
)