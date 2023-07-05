from aws_cdk import aws_s3outposts as s3outposts

# policy: Any

cfn_access_point = s3outposts.CfnAccessPoint(self, "MyCfnAccessPoint",
    bucket="bucket",
    name="name",
    vpc_configuration=s3outposts.CfnAccessPoint.VpcConfigurationProperty(
        vpc_id="vpcId"
    ),

    # the properties below are optional
    policy=policy
)