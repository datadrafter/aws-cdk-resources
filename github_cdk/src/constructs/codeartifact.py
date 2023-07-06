from constructs import Construct
import aws_cdk as cdk
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_codeartifact as codeartifact
)


class CodeartifactStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, app_config: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        repo_postfix = ""
        if app_config["current_environment"]["Name"] != "prod":
            repo_postfix = "-" + app_config["current_environment"]["Name"]

        domain_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": [
                            "codeartifact:DescribePackageVersion",
                            "codeartifact:DescribeRepository",
                            "codeartifact:GetPackageVersionReadme",
                            "codeartifact:GetRepositoryEndpoint",
                            "codeartifact:ListPackageVersionAssets",
                            "codeartifact:ListPackageVersionDependencies",
                            "codeartifact:ListPackageVersions",
                            "codeartifact:ListPackages",
                            "codeartifact:PublishPackageVersion",
                            "codeartifact:PutPackageMetadata",
                            "codeartifact:ReadFromRepository"
                        ],
                        "Resource": "*",
                        "Condition": {
                            "StringEquals": {
                                "aws:PrincipalOrgID": app_config["PrincipalOrgID"]
                            }
                        }
                    }
                ]
            }

        domain = codeartifact.CfnDomain(self, 
            "my-core" + repo_postfix,
            domain_name="my-core" + repo_postfix,
            permissions_policy_document=domain_policy
        )

        npm_repo = codeartifact.CfnRepository(self,
            "my-npm" + repo_postfix,
            domain_name=domain.domain_name,
            domain_owner=self.account,
            repository_name="my-npm" + repo_postfix,
            external_connections=["public:npmjs"]            
        )
        npm_repo.add_depends_on(domain)

        nuget_repo = codeartifact.CfnRepository(self,
            "my-nuget" + repo_postfix,
            domain_name=domain.domain_name,
            domain_owner=self.account,
            repository_name="my-nuget" + repo_postfix,
            external_connections=["public:nuget-org"]
        )
        nuget_repo.add_depends_on(domain)

        pip_repo = codeartifact.CfnRepository(self,
            "my-pip" + repo_postfix,
            domain_name=domain.domain_name,
            domain_owner=self.account,
            repository_name="my-pip" + repo_postfix,
            external_connections=["public:pypi"]
        )
        pip_repo.add_depends_on(domain)

        github_user_or_org_name = app_config["GitHubUserOrOrganization"]
        github_npm_repo_naming_pattern = app_config["GitHubNpmRepoNamingPatter"]
        github_nuget_repo_naming_pattern = app_config["GitHubNugetRepoNamingPatter"]
        github_pip_repo_naming_pattern = app_config["GitHubPipRepoNamingPatter"]
        github_repo_refs = app_config["current_environment"]["RepoRefs"]

        auth_subjects = []
        for ref in github_repo_refs:
            auth_subjects.append(f"repo:{github_user_or_org_name}/{github_npm_repo_naming_pattern}:ref:refs/{ref}")
            auth_subjects.append(f"repo:{github_user_or_org_name}/{github_nuget_repo_naming_pattern}:ref:refs/{ref}")
            auth_subjects.append(f"repo:{github_user_or_org_name}/{github_pip_repo_naming_pattern}:ref:refs/{ref}")

        github_publish_role = iam.Role(self, 
            "github-publish",
            assumed_by=iam.FederatedPrincipal(                
                federated=app_config["current_environment"]["GitHubOIDCProviderArn"],
                assume_role_action="sts:AssumeRoleWithWebIdentity",
                conditions={
                "ForAllValues:StringLike":
                    {
                        "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
                        "token.actions.githubusercontent.com:sub": auth_subjects
                    }
                }
            )
        )
        
        iam.Policy(self,
            "github-publish-to-repo-policy",
            statements=[
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=[
                        "codeartifact:GetAuthorizationToken",
                        "sts:GetServiceBearerToken"
                    ],
                    resources=[
                        "*"
                    ]
                ),
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=[
                        "codeartifact:GetRepositoryEndpoint",
                        "codeartifact:PublishPackageVersion",
                        "codeartifact:PutPackageMetadata"
                    ],
                    resources=[
                        npm_repo.attr_arn,
                        nuget_repo.attr_arn,
                        pip_repo.attr_arn
                    ]
                )
            ],
            roles=[github_publish_role]
        )

        cdk.CfnOutput(self, "github_publish_role", value=github_publish_role.role_arn)

              