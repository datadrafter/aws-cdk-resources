from aws_cdk import aws_workspaces as workspaces

cfn_workspace = workspaces.CfnWorkspace(self, "MyCfnWorkspace",
    bundle_id="bundleId",
    directory_id="directoryId",
    user_name="userName",

    # the properties below are optional
    root_volume_encryption_enabled=False,
    tags=[CfnTag(
        key="key",
        value="value"
    )],
    user_volume_encryption_enabled=False,
    volume_encryption_key="volumeEncryptionKey",
    workspace_properties=workspaces.CfnWorkspace.WorkspacePropertiesProperty(
        compute_type_name="computeTypeName",
        root_volume_size_gib=123,
        running_mode="runningMode",
        running_mode_auto_stop_timeout_in_minutes=123,
        user_volume_size_gib=123
    )
)