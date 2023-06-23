from aws_cdk import (
    # Duration,
    Stack,
    aws_iam as iam,
    aws_glue as glue,
    CfnOutput
)
from constructs import Construct

class GlueStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        glue_job = glue.CfnJob(self
                            ,id="Glue-ETL-Process"
                            ,name="ETL-GlueJob"
                            ,command=glue.CfnJob.JobCommandProperty(
                                #For an Apache Spark ETL job, name must be glueetl
                                name="glueetl"
                            ,python_version='3'
                            ,script_location=f's3://{bucket.bucket_name}/gluejob.py'
                            )
                            ,role =glue_role.role_arn
                            ,default_arguments={'--additional-python-modules': 'testn'
                                                ,'--beg_date': 'Default'
                                                ,'--end_date': 'Default'
                                                ,'--job_name': 'ETL-GlueJob'
                                                ,'--class': 'GlueApp'
                                                }
                            ,glue_version="3.0"
                            ,max_retries=10
                            ,max_capacity=10
                            ,timeout=10
                            ,execution_property=glue.CfnJob.ExecutionPropertyProperty(
                                max_concurrent_runs=10
                            )
                            ,worker_type='G.1X'
                            ,number_of_workers=10
                            )

        CfnOutput(self,'Glue-ETL-Process', value=f"name:{glue_job.name} created!")