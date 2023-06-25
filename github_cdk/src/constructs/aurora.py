from aws_cdk import (
    Stack,
    CfnOutput,
    Environment,
    Tags,
    Duration,
    CustomResource,
    custom_resources as cr,
    aws_ec2 as ec2,
    aws_rds as rds,
    aws_secretsmanager as secretsmanager,
    aws_kms as kms,
    aws_iam as iam,
    aws_lambda as lambda_,
)
from constructs import Construct


class AuroraServerlessV2Stack(Stack):
    def __init__(
        self,
        scope: Construct,
        _id: str,
        # vpc: ec2.IVpc,
        stage_name: str,
        db_user: str="admin",
        db_name: str="mydb",
        **kwargs,
    ) -> None:
        super().__init__(scope, _id, **kwargs)
        
        vpc = ec2.Vpc(self, "VPC")
        
        db_user = "admin"
        secret = rds.DatabaseSecret(self, "AuroraSecret", username=db_user)
        aurora_cluster_credentials = rds.Credentials.from_secret(secret, db_user)

        instance_count = 1

        cluster = rds.DatabaseCluster(self, "AuroraCluster",
            cluster_identifier='y3-shimizu-cdk-aurora',
            engine=rds.DatabaseClusterEngine.aurora_mysql(version=rds.AuroraMysqlEngineVersion.VER_3_01_0),
            instances=instance_count,
            instance_props=rds.InstanceProps(
                vpc=vpc,
            ),
            credentials=aurora_cluster_credentials,
        )
