from typing import Sequence
from aws_cdk import core as cdk
import aws_cdk.aws_lakeformation as lf


class LakeformationTablePermisionStack(cdk.Construct):

    def __init__(self, scope: cdk.Construct, id: str,
                 data_lake_principal_identifier: str,
                 database_name: str,
                 permissions: Sequence[str],
                 *,
                 prefix=None):
        super().__init__(scope, id)

        lf.CfnPermissions(
            self,
            id='permission',
            data_lake_principal=lf.CfnPermissions.DataLakePrincipalProperty(
                data_lake_principal_identifier=data_lake_principal_identifier),
            resource=lf.CfnPermissions.ResourceProperty(
                table_resource=lf.CfnPermissions.TableResourceProperty(
                    database_name=database_name,
                    table_wildcard={}
                )
            ),
            permissions=permissions,
            permissions_with_grant_option=permissions
        )