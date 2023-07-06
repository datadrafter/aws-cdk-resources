from aws_cdk import aws_secretsmanager as secretsmanager

cfn_secret = secretsmanager.CfnSecret(self, "MyCfnSecret",
    description="description",
    generate_secret_string=secretsmanager.CfnSecret.GenerateSecretStringProperty(
        exclude_characters="excludeCharacters",
        exclude_lowercase=False,
        exclude_numbers=False,
        exclude_punctuation=False,
        exclude_uppercase=False,
        generate_string_key="generateStringKey",
        include_space=False,
        password_length=123,
        require_each_included_type=False,
        secret_string_template="secretStringTemplate"
    ),
    kms_key_id="kmsKeyId",
    name="name",
    replica_regions=[secretsmanager.CfnSecret.ReplicaRegionProperty(
        region="region",

        # the properties below are optional
        kms_key_id="kmsKeyId"
    )],
    secret_string="secretString",
    tags=[CfnTag(
        key="key",
        value="value"
    )]
)