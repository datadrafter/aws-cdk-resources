from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_autoscaling as autoscaling,
    aws_ecs_patterns as ecs_patterns,
)
from constructs import Construct

class EcsJenkinsSlaveStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        queue = sqs.Queue(
            self, "EcsJenkinsSlaveQueue",
            visibility_timeout=Duration.seconds(300),
        )

        vpc = ec2.Vpc(self, "MyVpc", max_azs=3)
        cluster = ecs.Cluster(self, "EcsSlaveCluster", vpc=vpc, enable_fargate_capacity_providers=True)
        ecs_patterns.ApplicationLoadBalancedFargateService
        self.cluster = Cluster(
            self, 'EcsSlaveCluster',
            vpc=ec2.Vpc
        )

        self.cluster.add_auto_scaling_group(asg)
        self.cluster.add_capacity("DefaultAutoScalingGroup",
                            instance_type=ec2.InstanceType("t2.micro"))

        Stack.CfnOutput(
            self, "Cluster",
            value=self.cluster.cluster_name
        )
