from aws_cdk import aws_codegurureviewer as codegurureviewer
from aws_cdk import aws_codeguruprofiler as codeguruprofiler


# CodeGuru Profiler 
cfn_profiling_group = codeguruprofiler.CfnProfilingGroup(self, "MyCfnProfilingGroup",
    profiling_group_name="profilingGroupName",

    # the properties below are optional
    agent_permissions=agent_permissions,
    anomaly_detection_notification_configuration=[codeguruprofiler.CfnProfilingGroup.ChannelProperty(
        channel_uri="channelUri",

        # the properties below are optional
        channel_id="channelId"
    )],
    compute_platform="computePlatform",
    tags=[CfnTag(
        key="key",
        value="value"
    )]
)


# CodeGuru Reviewer
cfn_repository_association = codegurureviewer.CfnRepositoryAssociation(self, "MyCfnRepositoryAssociation",
    name="name",
    type="type",

    # the properties below are optional
    bucket_name="bucketName",
    connection_arn="connectionArn",
    owner="owner",
    tags=[CfnTag(
        key="key",
        value="value"
    )]
)