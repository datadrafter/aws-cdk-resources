from aws_cdk import App
from aws_cdk import aws_iam
from aws_cdk import Environment
from aws_cdk import Tags

from constructs import Construct

from typing import Any
from typing import Optional

class DevEnvironment(Environment):
    """
    Contains all the information of my Dev account
    """

    def __init__(
        self,
        scope: App,
        name: Optional[str] = None,
        account: Optional[str] = None,
        region: Optional[str] = None,
        dr_region: Optional[str] = None,
    ) -> None:
    # if not name:
    #     name = scope.node.try_get_context("env") or "dev"

        super().__init__(account=account, region=region)
        self._account = account
        self._scope = scope
        self._dr_region = dr_region
        self._env_name = name

    @property
    def name(self) -> str:
        return self._env_name

    def account(self) -> str:
        return self._account

    def dr_region(self) -> str:
        return self._dr_region

    def get_config(self) -> str:
        return _get_env_config(self._scope, key)

def init_app() -> App:
    "Create CDK App standard tags"

    app = App()

    for key, value in _get_tag(app).items():
        Tags.of(app).add(key, value)

    return app

def _get_tags(app: App) -> dict[str, str]:
    return {
        "tag1" : "value1",
        "tag2" : "value2",
        "tag3" : "value3",
        "tag4" : "value4",
    }

def _get_env_config(scope: Construct, key: str) -> Any:
    env_name = scope.node.try_get_context("env") or "dev"
    env_config = scope.node.try_get_context(env_name) or {}
    return env_config.get(key)


    