import os
from typing import List
from aws_cdk import aws_cognito as cognito
from aws_cdk import core as cdk
from aws_cdk import aws_iam as iam


class CognitoStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.project = self.node.try_get_context("project")
        self.stage = self.node.try_get_context("stage")

        user_pool = self.create_user_pool()
        self.create_identity_provider_google(user_pool=user_pool)

        clients: List[cognito.IUserPoolClient] = []
        clients.append(
            self.create_user_pool_client(
                client_name="web_client",
                user_pool=user_pool,
                callback_urls=os.environ["web_client_callback_urls"].split(","),
                logout_urls=os.environ["web_client_logout_urls"].split(","),
            )
        )
        clients.append(
            self.create_user_pool_client(
                client_name="mobile_client",
                user_pool=user_pool,
                callback_urls=os.environ["mobile_client_callback_urls"].split(","),
                logout_urls=os.environ["mobile_client_logout_urls"].split(","),
            )
        )

        self.create_identity_pool(user_pool=user_pool, clients=clients)

    def authenticatedPolicy(self) -> iam.PolicyDocument:
        return iam.PolicyDocument(
            statements=[
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=["cognito-sync:*", "cognito-identity:*"],
                    resources=["*"],
                )
            ]
        )

    def unauthenticatedPolicy(self) -> iam.PolicyDocument:
        return iam.PolicyDocument(
            statements=[
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=["cognito-sync:*"],
                    resources=["*"],
                )
            ]
        )

    def create_identity_pool(
        self, user_pool: cognito.IUserPool, clients: List[cognito.IUserPoolClient]
    ) -> cognito.CfnIdentityPool:

        identity_pool = cognito.CfnIdentityPool(
            self,
            id="identity_pool",
            identity_pool_name=f"{self.project}-{self.stage}",
            allow_unauthenticated_identities=True,
            cognito_identity_providers=[
                cognito.CfnIdentityPool.CognitoIdentityProviderProperty(
                    client_id=x.user_pool_client_id,
                    provider_name=f"cognito-idp.{self.region}.amazonaws.com/{user_pool.user_pool_id}",
                )
                for x in clients
            ],
        )

        authenticated_role = iam.Role(
            self,
            id="auth_role",
            role_name=f"{self.project}-{self.stage}-cognito-auth-role",
            assumed_by=iam.FederatedPrincipal(  # type: ignore
                federated="cognito-identity.amazonaws.com",
                conditions={
                    "StringEquals": {
                        "cognito-identity.amazonaws.com:aud": identity_pool.ref
                    },
                    "ForAnyValue:StringLike": {
                        "cognito-identity.amazonaws.com:amr": "authenticated"
                    },
                },
                assume_role_action="sts:AssumeRoleWithWebIdentity",
            ),
            inline_policies={"policy": self.authenticatedPolicy()},
        )

        unauthenticated_role = iam.Role(
            self,
            id="unauth_role",
            role_name=f"{self.project}-{self.stage}-cognito-unauth-role",
            assumed_by=iam.FederatedPrincipal(  # type: ignore
                federated="cognito-identity.amazonaws.com",
                conditions={
                    "StringEquals": {
                        "cognito-identity.amazonaws.com:aud": identity_pool.ref
                    },
                    "ForAnyValue:StringLike": {
                        "cognito-identity.amazonaws.com:amr": "unauthenticated"
                    },
                },
                assume_role_action="sts:AssumeRoleWithWebIdentity",
            ),
            inline_policies={"policy": self.unauthenticatedPolicy()},
        )

        cognito.CfnIdentityPoolRoleAttachment(
            self,
            id="role_attachment",
            identity_pool_id=identity_pool.ref,
            roles={
                "authenticated": authenticated_role.role_arn,
                "unauthenticated": unauthenticated_role.role_arn,
            },
        )
        return identity_pool

    def create_identity_provider_google(self, user_pool: cognito.IUserPool) -> None:
        client_id = os.environ["google_client_id"]
        client_secret = os.environ["google_client_secret"]
        cognito.UserPoolIdentityProviderGoogle(
            self,
            "google",
            client_id=client_id,
            client_secret=client_secret,
            user_pool=user_pool,
            scopes=["openid", "email", "profile"],
            attribute_mapping=cognito.AttributeMapping(
                email=cognito.ProviderAttribute.GOOGLE_EMAIL,
            ),
        )

    def create_user_pool_client(
        self,
        client_name: str,
        user_pool: cognito.IUserPool,
        logout_urls: List[str],
        callback_urls: List[str],
    ) -> cognito.IUserPoolClient:
        client = cognito.UserPoolClient(
            self,
            id=client_name,
            user_pool_client_name=client_name,
            user_pool=user_pool,  # type: ignore
            generate_secret=False,
            refresh_token_validity=cdk.Duration.days(30),
            access_token_validity=cdk.Duration.minutes(60),
            id_token_validity=cdk.Duration.minutes(60),
            auth_flows=cognito.AuthFlow(
                admin_user_password=False,
                custom=True,
                user_password=False,
                user_srp=True,
            ),
        )
        cfn_client: cognito.CfnUserPoolClient = client.node.default_child  # type: ignore
        cfn_client.callback_ur_ls = callback_urls
        cfn_client.logout_ur_ls = logout_urls
        cfn_client.allowed_o_auth_flows_user_pool_client = True
        cfn_client.allowed_o_auth_flows = ["code"]
        cfn_client.allowed_o_auth_scopes = [
            "phone",
            "email",
            "openid",
            "aws.cognito.signin.user.admin",
            "profile",
        ]

        return client  # type: ignore

    def create_user_pool(self) -> cognito.IUserPool:
        user_pool = cognito.UserPool(
            self,
            id="user_pool",
            user_pool_name=f"{self.project}-{self.stage}",
            self_sign_up_enabled=True,
            sign_in_case_sensitive=False,
            auto_verify=cognito.AutoVerifiedAttrs(email=True),
            standard_attributes=cognito.StandardAttributes(
                email=cognito.StandardAttribute(required=True)
            ),
            password_policy=cognito.PasswordPolicy(
                min_length=6,
                require_lowercase=False,
                require_uppercase=False,
                require_symbols=False,
                require_digits=False,
            ),
            removal_policy=cdk.RemovalPolicy.DESTROY,
            account_recovery=cognito.AccountRecovery.EMAIL_ONLY,
        )
        user_pool.add_domain(
            id="domain",
            cognito_domain=cognito.CognitoDomainOptions(
                domain_prefix=f"{self.project}-{self.stage}"
            ),
        )
        return user_pool  # type: ignore