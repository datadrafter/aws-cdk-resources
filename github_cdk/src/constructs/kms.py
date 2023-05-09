from aws_cdk import aws_kms
from aws_cdk import aws_iam
from aws_cdk import RemovalPolicy
from constructs import Construct

class KMSConstructs:
    """ 
    This is consturct class to create
    kms keys
    """

    @staticmethod
    def create_s3_bucket_kms(
        scope: Construct, kms_key_id: str
    ) -> aws_kms.Key:
        kms_key = aws_kms.Key(
            scope,
            id=kms_key_id,
            alias=f"alias/{kms_key_id}",
            description="This is my kms key for bucket encryption",
            enabled=True,
            enabled_key_rotation=True,
            removal_policy=RemovalPolicy.DESTROY,
        )
        return kms_key
