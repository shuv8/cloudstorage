from enum import Enum
from typing import Optional

from database.database import DataBaseTemporary
from tests.test_api.mock.database_for_access_tests import DatabaseForAccessTests


class ScopeTypeEnum(Enum):
    Default = 0
    Prod = 1
    Access = 2
    Search = 3
    Separate = 4
    Test = 5

    @staticmethod
    def get_class_by_str(scope: Optional[str] = None):
        if scope == "prod":
            return ScopeTypeEnum.Prod

        if scope == "access":
            return ScopeTypeEnum.Access

        if scope == "search":
            return ScopeTypeEnum.Search

        if scope == "separate":
            return ScopeTypeEnum.Separate

        if scope == "test":
            return ScopeTypeEnum.Test

        if scope == None:
            return ScopeTypeEnum.Default

    @staticmethod
    def return_state_by_scope(scope, default=DataBaseTemporary(), test=None):
        if scope == ScopeTypeEnum.Default:
            return default

        if scope == ScopeTypeEnum.Prod:
            return default

        if scope == ScopeTypeEnum.Test:
            return test

        if scope == ScopeTypeEnum.Separate:
            return DataBaseTemporary()

        if scope == ScopeTypeEnum.Access:
            return DatabaseForAccessTests()

        if scope == ScopeTypeEnum.Search:
            return DatabaseForAccessTests()
