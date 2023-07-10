from aws_cdk import aws_datapipeline as datapipeline

cfn_pipeline = datapipeline.CfnPipeline(self, "MyCfnPipeline",
    name="name",

    # the properties below are optional
    activate=False,
    description="description",
    parameter_objects=[datapipeline.CfnPipeline.ParameterObjectProperty(
        attributes=[datapipeline.CfnPipeline.ParameterAttributeProperty(
            key="key",
            string_value="stringValue"
        )],
        id="id"
    )],
    parameter_values=[datapipeline.CfnPipeline.ParameterValueProperty(
        id="id",
        string_value="stringValue"
    )],
    pipeline_objects=[datapipeline.CfnPipeline.PipelineObjectProperty(
        fields=[datapipeline.CfnPipeline.FieldProperty(
            key="key",

            # the properties below are optional
            ref_value="refValue",
            string_value="stringValue"
        )],
        id="id",
        name="name"
    )],
    pipeline_tags=[datapipeline.CfnPipeline.PipelineTagProperty(
        key="key",
        value="value"
    )]
)
