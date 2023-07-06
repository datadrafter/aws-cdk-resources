from aws_cdk import (
    core as cdk,
    aws_lambda as cdk_lambda,
    aws_appsync as cdk_appsync,
    aws_dynamodb as cdk_dynamodb
)
from aws_cdk.aws_appsync import (
    AuthorizationConfig, AuthorizationMode, AuthorizationType,
    MappingTemplate
)


class CdkAppSyncStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct,
                 construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        graph_api = cdk_appsync.GraphqlApi(
            self, 'HelloAppSyncFromCDK',
            name='HelloAppSyncFromCDK',
            authorization_config=AuthorizationConfig(
                default_authorization=AuthorizationMode(
                    authorization_type=AuthorizationType.API_KEY
                )
            ),
            schema=cdk_appsync.Schema.from_asset('schema.graphql'),
            xray_enabled=False
        )

        # DynamoDB DataSource を追加
        hash_table = cdk_dynamodb.Table(
            self, "HashTable",
            partition_key=cdk_dynamodb.Attribute(
                name="key",
                type=cdk_dynamodb.AttributeType.STRING
            ),
            billing_mode=cdk_dynamodb.BillingMode.PAY_PER_REQUEST,
            time_to_live_attribute='ttl'
        )
        range_table = cdk_dynamodb.Table(
            self, "RangeTable",
            partition_key=cdk_dynamodb.Attribute(
                name="key",
                type=cdk_dynamodb.AttributeType.STRING
            ),
            sort_key=cdk_dynamodb.Attribute(
                name="range",
                type=cdk_dynamodb.AttributeType.STRING
            ),
            billing_mode=cdk_dynamodb.BillingMode.PAY_PER_REQUEST,
            time_to_live_attribute='ttl'
        )
        range_table.add_local_secondary_index(
            sort_key=cdk_dynamodb.Attribute(
                name="_s_sort",
                type=cdk_dynamodb.AttributeType.STRING
            ),
            index_name='key-ssort_index'
        )
        range_table.add_local_secondary_index(
            sort_key=cdk_dynamodb.Attribute(
                name="_n_sort",
                type=cdk_dynamodb.AttributeType.NUMBER
            ),
            index_name='key-nsort_index'
        )
        hash_source = graph_api.add_dynamo_db_data_source(
            'hashDataSource', hash_table)
        range_source = graph_api.add_dynamo_db_data_source(
            'rangeDataSource', range_table)

        # getUsers に全件取得の Resolver を付与 (プログラムベース)
        hash_source.create_resolver(
            type_name='Query',
            field_name='getUsers',
            request_mapping_template=MappingTemplate.dynamo_db_scan_table(),
            response_mapping_template=MappingTemplate.dynamo_db_result_list()
        )

        # addUser に vtl テンプレートの Resolver を付与 (VTLベース)
        hash_source.create_resolver(
            type_name='Mutation',
            field_name='createUser',
            request_mapping_template=MappingTemplate.from_file(
                'resolvers/createUser.vtl'
            ),
            response_mapping_template=MappingTemplate.from_file(
                'resolvers/defaultResponse.vtl'
            )
        )
        hash_source.create_resolver(
            type_name='Mutation',
            field_name='updateUser',
            request_mapping_template=MappingTemplate.from_file(
                'resolvers/updateUser.vtl'
            ),
            response_mapping_template=MappingTemplate.from_file(
                'resolvers/defaultResponse.vtl'
            )
        )

        # hello に固定文字列を返す Lambda 関数の Resolver を付与
        fixed_str = cdk_lambda.Function(
            self, 'FixedStringLambda',
            runtime=cdk_lambda.Runtime.PYTHON_3_8,
            code=cdk_lambda.Code.asset('lambda'),
            handler='fixed_string.handler',
            environment={},
        )
        graph_api.add_lambda_data_source(
            'FixedStringFn', fixed_str
        ).create_resolver(
            type_name='Query', field_name='hello'
        )