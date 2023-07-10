from aws_cdk import aws_grafana as grafana

cfn_workspace = grafana.CfnWorkspace(self, "MyCfnWorkspace",
    account_access_type="accountAccessType",
    authentication_providers=["authenticationProviders"],
    permission_type="permissionType",

    # the properties below are optional
    client_token="clientToken",
    data_sources=["dataSources"],
    description="description",
    grafana_version="grafanaVersion",
    name="name",
    network_access_control=grafana.CfnWorkspace.NetworkAccessControlProperty(
        prefix_list_ids=["prefixListIds"],
        vpce_ids=["vpceIds"]
    ),
    notification_destinations=["notificationDestinations"],
    organizational_units=["organizationalUnits"],
    organization_role_name="organizationRoleName",
    role_arn="roleArn",
    saml_configuration=grafana.CfnWorkspace.SamlConfigurationProperty(
        idp_metadata=grafana.CfnWorkspace.IdpMetadataProperty(
            url="url",
            xml="xml"
        ),

        # the properties below are optional
        allowed_organizations=["allowedOrganizations"],
        assertion_attributes=grafana.CfnWorkspace.AssertionAttributesProperty(
            email="email",
            groups="groups",
            login="login",
            name="name",
            org="org",
            role="role"
        ),
        login_validity_duration=123,
        role_values=grafana.CfnWorkspace.RoleValuesProperty(
            admin=["admin"],
            editor=["editor"]
        )
    ),
    stack_set_name="stackSetName",
    vpc_configuration=grafana.CfnWorkspace.VpcConfigurationProperty(
        security_group_ids=["securityGroupIds"],
        subnet_ids=["subnetIds"]
    )
)