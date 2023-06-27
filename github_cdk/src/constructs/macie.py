import aws_cdk.aws_macie as macie
from constructs import Construct



class DynamodbStack(Stack):

  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)


    cfn_session = macie.CfnSession(self, "MyCfnSession",
        finding_publishing_frequency="findingPublishingFrequency",
        status="status"
    )

    cfn_allow_list = macie.CfnAllowList(self, "MyCfnAllowList",
        criteria=macie.CfnAllowList.CriteriaProperty(
            regex="regex",
            s3_words_list=macie.CfnAllowList.S3WordsListProperty(
                bucket_name="bucketName",
                object_key="objectKey"
            )
        ),
        name="name",

        # the properties below are optional
        description="description",
        tags=[CfnTag(
            key="key",
            value="value"
        )]
    )