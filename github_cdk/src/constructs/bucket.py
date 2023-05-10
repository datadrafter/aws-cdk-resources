from aws_cdk import aws_s3
from aws_cdk import aws_kms
from aws_cdk import RemovalPolicy
from aws_cdk import Duration
from constructs import Construct

from kms import *

_DEFAULT_LIFECYCLE_RULE = aws_s3.LifecycleRule(
    id="default-lifecycle-rule",
    noncurrent_version_expiration=Duration.days(60),
    # transition=[
    #     aws_s3.Transition(
    #     storage_class=aws_s3.StorageClass("INTELLIGENT_TIERING"),
    #     transition_after=Duration.days(0),
    #     )
    # ],
)

class S3Constructs:
    """ 
    This is a construct class to create
    S3 Bucket
    """ 

    @staticmethod
    def create_s3_bucket(
        scope: Construct, bucket_name: str, kms_key: aws_kms.Key
    ) -> aws_s3.Bucket:
        bucket = aws_s3.Bucket(
            scope,
            id=bucket_name,
            block_public_access=aws_s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY,
            encryption_key=kms_key,
            versioned=True,
            bucket_key_enabled=True,
            lifecycle_rules=[_DEFAULT_LIFECYCLE_RULE],
        )
        return bucket

    
class BucketEnablement(Construct):
    "This is a construct that creates kms and s3 bucket"

    def __init__(
        self,
        scope: Construct,
        account: str,
        region: str,
        id="bucket_enablement_construct",
        ) -> None:
        super().__init__(scope,id)

        bucket_prefix ='my-s3-bucket'
        kms_prefix = 'my-s3-bucket-kms'

        def add_tags(resource:Construct, custom_tags={}):
            base_tags = {
            "tag_key": "value_1",
            "tag_key_2" : "value_2",
            "tag_key_3" : "value_3",
            }
            for k,v in base_tags.items():
                Tags.of(resource).add(key,value)

        kms_key_id= f"{kms_prefix}-{account}-{region}"
        kms_key= KMSConstructs.create_s3_bucket_kms(self,kms_key_id)
        self._kms_key = kms_key
        add_tags(tags)

        
        bucket_name = f"{my-s3-bucket}-{account}-{region}"
        bucket = S3Constructs.create_s3_bucket(self, bucket_name, kms_key)
        self._s3_bucket = bucket

        def kms_key(self) -> aws_kms.Key:
            return self._kms_key

        def s3_bucket(self) -> aws_s3.Bucket:
            return self._s3_bucket

