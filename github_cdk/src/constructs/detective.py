from aws_cdk import aws_detective as detective

cfn_graph_props = detective.CfnGraphProps(
    auto_enable_members=False,
    tags=[CfnTag(
        key="key",
        value="value"
    )]
)