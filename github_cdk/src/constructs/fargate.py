from aws_cdk import core
from aws_cdk import aws_ecr
from aws_cdk import aws_ec2
from aws_cdk import aws_ecs
from aws_cdk import aws_logs
from aws_cdk import aws_events
from aws_cdk import aws_events_targets


class AwsCdkFargateBatchStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # ECR
        ecr_repository = aws_ecr.Repository(
            self,
            id='ecr_repository',
            repository_name='sample_repository'
        )
        
        # VPC
        vpc = aws_ec2.Vpc(self,
            id='vpc',
            cidr='10.0.0.0/16',
            max_azs=2,
            nat_gateways=1,
            vpn_gateway=False
        )

        # Create ecs cluester.
        ecs_cluster = aws_ecs.Cluster(
            self,
            id='ecs_cluster',
            cluster_name='sample_fargate_batch_cluster',
            vpc=vpc
        )

        # Create fargate task definition.
        fargate_task_definition = aws_ecs.FargateTaskDefinition(
            self,
            id='fargate-task-definition',
            cpu=256,
            memory_limit_mib=512,
            family='fargate-task-definition'
        )

        # Add container to task definition.
        fargate_task_definition.add_container(
            id='container',
            image=aws_ecs.ContainerImage.from_ecr_repository(ecr_repository),
            logging=aws_ecs.LogDriver.aws_logs(
                stream_prefix='ecs',
                log_group=aws_logs.LogGroup(
                    self,
                    id='log-group',
                    log_group_name='/ecs/fargate/fargate-batch'
                )
            )
        )

        # Create cloud watch event rule.
        rule = aws_events.Rule(
            self,
            id='rule',
            rule_name='execute-task-rule',
            description='Event rule to execute ecs task.',
            schedule=aws_events.Schedule.cron(
                day=None,
                hour=None,
                minute='*/5', # execute by every 5 minutes.
                month=None,
                week_day=None,
                year=None
            )
        )

        rule.add_target(
            target=aws_events_targets.EcsTask(
                cluster=ecs_cluster,
                task_definition=fargate_task_definition,
                task_count=1
            )
        )