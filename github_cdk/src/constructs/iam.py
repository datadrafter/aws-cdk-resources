from aws_cdk import aws_iam
from aws_cdk import Environment
from aws_cdk import Stack
from constructs import Constructs

_MY_SAML_LOGIN_ROLE_NAME = "my-reporting-role"
_MY_POLICY_NAME = "my-reporting-role-read-only"


class LoginRolesStack(Stack):
    """This stack contains SAML login roles that align to Actuarial business
    partners. This consist of a custom role that is used to grant read-only
    access to resources.

    This is seperated into its own stack because, in practice, this stack is 
    only deployed to non-prod environments since Actuarial partners should only
    have access to dev and staging environments.
    """

    def __init__(
        self,
        scope: Construct,
        stack_id: str,
        env: Environment,
        **kwargs,
    ) -> None:
        """
        :param scope: Parent of this stack.
        :parak stack_id: The construct ID of this stack.
        :param env: The AWS environment where this stack will be deployed.
         """
        super().__init__(scope,stack_id,env=env,**kwargs)

        assert env
        self._account = env.account
        self._region = env.region

        saml_principal = aws_iam.FederatedPrincipal (
            f"arn:aws:iam::{env.account}:saml-provider/infra-azure-ad",
            {
                "StringEquals": {
                    "SAML:aud": "https//signin.aws.amazon.com/saml",
                }
            },
            "sts:AssumeRolewithSAML",
        )

        my_policy = aws_iam_ManagedPolicy (
            self,
            _MY_POLICY_NAME,
            managed_policy_name =_MY_POLICY_NAME,
            description="Provides read-only access for Actuarial users",
            statements = [
                self._get_policy_statement(),
                self._get_s3_policy_statement(),
            ],
        )

        aws_iam.Role(
            self,
            _MY_SAML_LOGIN_ROLE_NAME,
            role_name=_MY_SAML_LOGIN_ROLE_NAME,
            description="SAML login role for reporting users that provides read-only access",
            assumed_by=saml_principal,
            managed_policies=[actuarial_policy],
        )
    def _get_policy_statement(self) -> aws_iam_PolicyStatement:
        policy_statement = aws_iam.PolicyStatement()

        policy_statement.effect = aws.iam.Effect.ALLOW
        policy_statement.add_actions("athena:GetDataCatalog")
        policy_statement.add_actions("athena:GetNameQuery")
        policy_statement.add_actions("athena:GetQueryResults")
        policy_statement.add_actions("athena:GetQueryExecution")
        policy_statement.add_actions("athena:GetWorkGroup")
        policy_statement.add_actions("athena:ListDataCatalogs")
        policy_statement.add_actions("athena:ListWorkGroups")
        policy_statement.add_actions("athena:ListQueryExecution")
        policy_statement.add_actions("athena:ListNamedQueries")
        policy_statement.add_actions("athena:ListDatabases")
        policy_statement.add_actions("athena:ListTableMetadata")
        policy_statement.add_actions("athena:BatchGetNamedQuery")
        policy_statement.add_actions("athena:BatchGetQueryExeution")
        policy_statement.add_actions("athena:CreateNamedQuery")
        policy_statement.add_actions("athena:StartQueryExecution")
        policy_statement.add_actions("glue:GetTables")
        policy_statement.add_actions("glue:GetPartitions")
        policy_statement.add_actions("glue:GetPartition")
        policy_statement.add_actions("s3:ListBucket")
        policy_statement.add_actions("s3:ListBucketMultipartUploads")
        policy_statement.add_actions("s3:ListMultiplepartUploadParts")
        policy_statement.add_actions("s3:PutObject")
        policy_statement.add_actions("s3:GetObject")
        policy_statement.add_actions("s3:GetBucketLocation")
        policy_statement.add_actions("kms:Decrypt")
        policy_statement.add_actions("kms:DescribeKey")
        policy_statement.add_actions("kms:GenerateDataKey")

        policy_statement.add_resources(
            f"arn.aws.iam::*{self._account}-{self._region}"
        )

        policy_statement.add_resources(
            f"arn.aws.iam::*{self._account}-{self._region}/*"
        )
        policy_statement.add_resources(f"arn:aws:athena:*{self._account}:*")
        policy_statement.add_resources(f"arn:aws:kms:*{self._account}:*")
        policy_statement.add_resources(f"arn:aws:glue:*{self._account}:*")

        return policy_statement

    def _get_s3_policy_statement(self) -> aws_iam.PolicyStatement:
        policy_statement = aws_iam.PolicyStatements()
        policy_statement.effect = aws_iam.PolicyStatement()
        policy_statement.effect = aws_iam.Effect.ALLOW
        policy_statement.add_actions("s3:ListAllMyBuckets")
        policy_statement.add_actions(f"arn:aws:s3:::*")

        return policy_statement






