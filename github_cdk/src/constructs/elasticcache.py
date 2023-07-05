from aws_cdk import aws_elasticache as elasticache

cfn_cache_cluster = elasticache.CfnCacheCluster(self, "MyCfnCacheCluster",
    cache_node_type="cacheNodeType",
    engine="engine",
    num_cache_nodes=123,

    # the properties below are optional
    auto_minor_version_upgrade=False,
    az_mode="azMode",
    cache_parameter_group_name="cacheParameterGroupName",
    cache_security_group_names=["cacheSecurityGroupNames"],
    cache_subnet_group_name="cacheSubnetGroupName",
    cluster_name="clusterName",
    engine_version="engineVersion",
    ip_discovery="ipDiscovery",
    log_delivery_configurations=[elasticache.CfnCacheCluster.LogDeliveryConfigurationRequestProperty(
        destination_details=elasticache.CfnCacheCluster.DestinationDetailsProperty(
            cloud_watch_logs_details=elasticache.CfnCacheCluster.CloudWatchLogsDestinationDetailsProperty(
                log_group="logGroup"
            ),
            kinesis_firehose_details=elasticache.CfnCacheCluster.KinesisFirehoseDestinationDetailsProperty(
                delivery_stream="deliveryStream"
            )
        ),
        destination_type="destinationType",
        log_format="logFormat",
        log_type="logType"
    )],
    network_type="networkType",
    notification_topic_arn="notificationTopicArn",
    port=123,
    preferred_availability_zone="preferredAvailabilityZone",
    preferred_availability_zones=["preferredAvailabilityZones"],
    preferred_maintenance_window="preferredMaintenanceWindow",
    snapshot_arns=["snapshotArns"],
    snapshot_name="snapshotName",
    snapshot_retention_limit=123,
    snapshot_window="snapshotWindow",
    tags=[CfnTag(
        key="key",
        value="value"
    )],
    transit_encryption_enabled=False,
    vpc_security_group_ids=["vpcSecurityGroupIds"]
)