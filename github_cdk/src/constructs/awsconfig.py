from aws_cdk import aws_config as config

# input_parameters: Any

cfn_config_rule = config.CfnConfigRule(self, "MyCfnConfigRule",
    source=config.CfnConfigRule.SourceProperty(
        owner="owner",

        # the properties below are optional
        custom_policy_details=config.CfnConfigRule.CustomPolicyDetailsProperty(
            enable_debug_log_delivery=False,
            policy_runtime="policyRuntime",
            policy_text="policyText"
        ),
        source_details=[config.CfnConfigRule.SourceDetailProperty(
            event_source="eventSource",
            message_type="messageType",

            # the properties below are optional
            maximum_execution_frequency="maximumExecutionFrequency"
        )],
        source_identifier="sourceIdentifier"
    ),

    # the properties below are optional
    config_rule_name="configRuleName",
    description="description",
    input_parameters=input_parameters,
    maximum_execution_frequency="maximumExecutionFrequency",
    scope=config.CfnConfigRule.ScopeProperty(
        compliance_resource_id="complianceResourceId",
        compliance_resource_types=["complianceResourceTypes"],
        tag_key="tagKey",
        tag_value="tagValue"
    )
)