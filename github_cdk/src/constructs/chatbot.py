from aws_cdk import aws_chatbot as chatbot

cfn_microsoft_teams_channel_configuration = chatbot.CfnMicrosoftTeamsChannelConfiguration(self, "MyCfnMicrosoftTeamsChannelConfiguration",
    configuration_name="configurationName",
    iam_role_arn="iamRoleArn",
    team_id="teamId",
    teams_channel_id="teamsChannelId",
    teams_tenant_id="teamsTenantId",

    # the properties below are optional
    guardrail_policies=["guardrailPolicies"],
    logging_level="loggingLevel",
    sns_topic_arns=["snsTopicArns"],
    user_role_required=False
)