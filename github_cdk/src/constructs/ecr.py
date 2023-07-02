from aws_cdk import core
from aws_cdk import aws_ecr as ecr


class CdkEcrStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        repo = ecr.Repository(self, 'MyRepository', repository_name='cdk-repo')
        repo.add_lifecycle_rule(
            description='Lifecycle rule for cdk-repo',
            max_image_count=50,
            rule_priority=1
        )