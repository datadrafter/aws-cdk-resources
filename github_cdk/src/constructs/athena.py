from aws_cdk import core as aws_cdk
from aws_cdk import aws_athena as athena 

class AthenaStack(cdk.Stack):
    
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

    def athena_properties():
        cfn_data_catalog_props = athena.CfnDataCatalogProps(
            name = 'test_prop',
            type = 'type',
            description = 'description',
            parameters = {
                'parameter_key': 'parameter_value'
            },
            tags = [CfnTag(
                key = 'key1',
                value = 'value1'
            )]
        )