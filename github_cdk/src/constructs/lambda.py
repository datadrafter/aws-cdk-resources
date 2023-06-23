from aws_cdk import Duration, Size, aws_iam, aws_lambda
from aws_cdk import aws_lambda_destinations as destinations 
from aws_cdk import aws_s3, aws_s3_notifications
from constructs import Construct

from github_cdk.iam import create_lambda_role

def create_lambda(
    scope: Construct,
    lambda_role: aws_iam.Role
) -> aws_lambda.Function:
    lambda_name = "my-lambda-function",
    mylambdafunction = aws_lambda.Function(
        scope=scope,
        function_name= lambda_name,
        id=lambda_name,
        description="description",
        code=aws_lambda.Code.from_asset(path="./lambdas/yourlambdafunction"),
        handler="yourlambdafunction.lambda_handler",
        runtime=aws_lambda.Runtime.PYTHON_3_9,
        role=lambda_role,
        timeout=Duration.minutes(15),
        memory_size=10240,
        ephermeral_storage_size=Size.mebibytes(10240)
    )

class LambdaStack():

    def__init__(self, scope:Construct, account: str, region: str, env_name: str, error_email_address: str, id='lambda-enablement-constructs') -> None:
    super().__init__(scope, id)

    lambdarole = create_lambda_role(
        self, account
    )

    bucket_name = {
        "bucket1": "bucketname1",
        "bucket2": "bucketname2"
    }

    mylambdafunction = create_lambda(
        scope=self,
        lambda_role=lambdarole,
        env_name=env_name,
        bucket_name=bucket_name,
    )

    self._mylambdafunction = mylambdafunction

    @property
    def lambdarole(self) -> aws_lambda.Function:
        return self._lambdarole 

    @property
    def mylambdafunction(self) -> aws_lambda.Function:
        return self._mylambdafunction 

    