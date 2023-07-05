from dms.dms_event_subscription import DMSEventSubscription
from dms.dms_schedule import Schedule
from glue.processing import Discover
from glue.processing import Process


class DmsCdkStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        instance_construct = DMSInstance(self, "InstanceContruct")

        target_bucket = s3.Bucket(self, "targetbucket")
        processed_bucket = s3.Bucket(self, "processedbucket")

        sns_topic = sns.Topic(self, 'dms-topic', display_name='Eventos de DMS')

        dms_endpoints = DMSEndpoints(self, "endpoints", target_bucket=target_bucket)

        dms_task = DMSTask(
            self, "task", dms_instance=instance_construct.instance, 
            source_endpoint=dms_endpoints.source, target_endpoint=dms_endpoints.target )
        
        subs = DMSEventSubscription (self, 'evn-subs', sns_topic=sns_topic)

        discover = Discover(self, 'discover', sns_topic=sns_topic, dms_instance=instance_construct.instance, dms_task=dms_task.task, bucket=target_bucket)
        process  = Process(
            self, 'process', crawler=discover.crawler, source_bucket=target_bucket,
            processed_bucket= processed_bucket
        )

        Schedule(self, 'schedule', task=dms_task)