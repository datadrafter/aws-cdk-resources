from glob import glob
from os.path import abspath, exists

from aws_cdk import aws_elasticbeanstalk as eb
from aws_cdk import aws_iam as iam
from aws_cdk import aws_s3_assets as assets
from aws_cdk import core as cdk

import json

from aws_cdk import aws_elasticbeanstalk as eb

# This list can be auto-generated using the AWS CLI if you already built a
# prototype EB environment by hand.
#
# aws elasticbeanstalk describe-configuration-settings \
#        --application-name APPNAME --environment-name ENVNAME > settings.js
#
# You do need to do some massaging of the output:
# 1) Convert the JSON to Python using json.loads(open('settings.js').read())
# 2) replace Namespace -> namespace
# 3) replace OptionName -> option_name
# 4) replace ResourceName -> resource_name
# 5) replace Value -> value
# 6) Remove the top-level, "ConfigurationSettings"
# 7) Keep only the settings that you need to customize. Let Elastic Beanstalk fill in the rest.
#
config = {
    "SolutionStackName": "64bit Amazon Linux 2 v3.2.4 running Corretto 11",
    "PlatformArn": "arn:aws:elasticbeanstalk:us-east-2::platform/Corretto 11 running on 64bit Amazon Linux 2/3.2.4",
    "OptionSettings": [
        {
            "resource_name": "AWSEBAutoScalingGroup",
            "namespace": "aws:autoscaling:asg",
            "option_name": "Availability Zones",
            "value": "Any",
        },
        {
            "namespace": "aws:autoscaling:launchconfiguration",
            "option_name": "InstanceType",
            "value": "t3.small",
        },
        {
            "resource_name": "AWSEBAutoScalingGroup",
            "namespace": "aws:autoscaling:asg",
            "option_name": "Cooldown",
            "value": "120",
        },
        {
            "resource_name": "AWSEBAutoScalingGroup",
            "namespace": "aws:autoscaling:asg",
            "option_name": "EnableCapacityRebalancing",
            "value": "true",
        },
        {
            "resource_name": "AWSEBAutoScalingGroup",
            "namespace": "aws:autoscaling:asg",
            "option_name": "MaxSize",
            "value": "8",
        },
        {
            "resource_name": "AWSEBAutoScalingGroup",
            "namespace": "aws:autoscaling:asg",
            "option_name": "MinSize",
            "value": "4",
        },
        {
            "namespace": "aws:autoscaling:launchconfiguration",
            "option_name": "SSHSourceRestriction",
            "value": "tcp,22,22,10.1.2.3/32",
        },
        {
            "namespace": "aws:ec2:instances",
            "option_name": "EnableSpot",
            "value": "true",
        },
        {
            "namespace": "aws:elasticbeanstalk:application",
            "option_name": "Application Healthcheck URL",
            "value": "/health",
        },
        {
            "namespace": "aws:elasticbeanstalk:application:environment",
            "option_name": "SERVER_PORT",
            "value": "5000",
        },
        {
            "namespace": "aws:elasticbeanstalk:cloudwatch:logs",
            "option_name": "StreamLogs",
            "value": "true",
        },
        {
            "namespace": "aws:elasticbeanstalk:cloudwatch:logs:health",
            "option_name": "HealthStreamingEnabled",
            "value": "true",
        },
        {
            "namespace": "aws:elasticbeanstalk:cloudwatch:logs",
            "option_name": "RetentionInDays",
            "value": "7",
        },
        {
            "namespace": "aws:elasticbeanstalk:cloudwatch:logs:health",
            "option_name": "RetentionInDays",
            "value": "7",
        },
        {
            "namespace": "aws:elasticbeanstalk:command",
            "option_name": "DeploymentPolicy",
            "value": "TrafficSplitting",
        },
        {
            "resource_name": "AWSEBV2LoadBalancerTargetGroup",
            "namespace": "aws:elasticbeanstalk:environment:process:default",
            "option_name": "HealthCheckPath",
            "value": "/health",
        },
        {
            "namespace": "aws:elasticbeanstalk:healthreporting:system",
            "option_name": "SystemType",
            "value": "enhanced",
        },
        {
            "namespace": "aws:elasticbeanstalk:trafficsplitting",
            "option_name": "EvaluationTime",
            "value": "10",
        },
        {
            "namespace": "aws:elasticbeanstalk:trafficsplitting",
            "option_name": "NewVersionPercent",
            "value": "10",
        },
        {
            "namespace": "aws:elasticbeanstalk:xray",
            "option_name": "XRayEnabled",
            "value": "false",
        },
        {
            "resource_name": "AWSEBV2LoadBalancerListener443",
            "namespace": "aws:elbv2:listener:443",
            "option_name": "DefaultProcess",
            "value": "default",
        },
        {
            "resource_name": "AWSEBV2LoadBalancerListener443",
            "namespace": "aws:elbv2:listener:443",
            "option_name": "ListenerEnabled",
            "value": "true",
        },
        {
            "resource_name": "AWSEBV2LoadBalancerListener443",
            "namespace": "aws:elbv2:listener:443",
            "option_name": "Protocol",
            "value": "HTTPS",
        },
        {
            "resource_name": "AWSEBV2LoadBalancerListener443",
            "namespace": "aws:elbv2:listener:443",
            "option_name": "Rules",
        },
        {
            "resource_name": "AWSEBV2LoadBalancerListener443",
            "namespace": "aws:elbv2:listener:443",
            "option_name": "SSLPolicy",
            "value": "ELBSecurityPolicy-TLS-1-2-2017-01",
        },
        {
            "resource_name": ":default",
            "namespace": "aws:elbv2:listener:default",
            "option_name": "ListenerEnabled",
            "value": "false",
        },
    ],
}


def create_eb_config(c=config):
    options = []
    for setting in c["OptionSettings"]:
        options += [eb.CfnEnvironment.OptionSettingProperty(**setting)]

    return options


class CdkElasticBeanstalkStack(cdk.Stack):
    def __init__(
        self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Get the path to the JAR file from context
        jarpath = self.node.try_get_context("jarpath")
        if not jarpath or not exists(abspath(jarpath)):
            raise RuntimeError(
                "Set value for jarpath with 'cdk synth --context jarpath=PATH'"
            )

        # Construct an S3 asset from the highest-versioned JAR available in the
        # ../target dir.
        jarfile = assets.Asset(self, "app.jar", path=jarpath)

        # Get the ARN for the TLS certificate from context
        tls_cert_arn = self.node.try_get_context("tls_cert_arn")
        if not tls_cert_arn:
            raise RuntimeError(
                "Set value for tls_cert_arn with 'cdk synth --context tls_cert_arn=ARN'"
            )

        # Get the app name from context and construct the env name from that.
        appname = self.node.try_get_context("appname")
        if not appname:
            raise RuntimeError(
                "Set value for appname with 'cdk synth --context appname=NAME'"
            )
        envname = f"{appname}-env"

        app = eb.CfnApplication(self, "Application", application_name=appname)

        self.eb_service_role = iam.CfnServiceLinkedRole(
            self,
            "ServiceLinkedRole",
            aws_service_name="elasticbeanstalk.amazonaws.com",
        )
        instance_profile = eb.CfnEnvironment.OptionSettingProperty(
            namespace="aws:autoscaling:launchconfiguration",
            option_name="IamInstanceProfile",
            value=self.eb_service_role.get_att("arn").to_string(),
        )
        certificate = eb.CfnEnvironment.OptionSettingProperty(
            namespace="aws:elbv2:listener:443",
            option_name="SSLCertificateArns",
            value=tls_cert_arn,
        )

        settings = config.create_eb_config()
        settings += [instance_profile, certificate]

        # Create an app version from the S3 asset defined above
        # The S3 "putObject" will occur first before CF generates the template
        appversion = eb.CfnApplicationVersion(
            self,
            "AppVersion",
            application_name=appname,
            source_bundle=eb.CfnApplicationVersion.SourceBundleProperty(
                s3_bucket=jarfile.s3_bucket_name, s3_key=jarfile.s3_object_key
            ),
        )

        ebenv = eb.CfnEnvironment(
            self,
            "Environment",
            application_name=appname,
            environment_name=envname,
            solution_stack_name=config.config["SolutionStackName"],
            platform_arn=config.config["PlatformArn"],
            option_settings=settings,
            # This line is critical - reference the label created in this same stack
            version_label=appversion.ref,
        )

        # Also very important - make sure that `app` exists before creating an app version
        appversion.add_depends_on(app)