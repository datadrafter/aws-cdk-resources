from aws_cdk import aws_docdb as docdb

cfn_dBCluster = docdb.CfnDBCluster(self, "MyCfnDBCluster",
    availability_zones=["availabilityZones"],
    backup_retention_period=123,
    copy_tags_to_snapshot=False,
    db_cluster_identifier="dbClusterIdentifier",
    db_cluster_parameter_group_name="dbClusterParameterGroupName",
    db_subnet_group_name="dbSubnetGroupName",
    deletion_protection=False,
    enable_cloudwatch_logs_exports=["enableCloudwatchLogsExports"],
    engine_version="engineVersion",
    kms_key_id="kmsKeyId",
    master_username="masterUsername",
    master_user_password="masterUserPassword",
    port=123,
    preferred_backup_window="preferredBackupWindow",
    preferred_maintenance_window="preferredMaintenanceWindow",
    restore_to_time="restoreToTime",
    restore_type="restoreType",
    snapshot_identifier="snapshotIdentifier",
    source_db_cluster_identifier="sourceDbClusterIdentifier",
    storage_encrypted=False,
    tags=[CfnTag(
        key="key",
        value="value"
    )],
    use_latest_restorable_time=False,
    vpc_security_group_ids=["vpcSecurityGroupIds"]
)