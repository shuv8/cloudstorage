from enum import Enum


class WorkSpaceStatus(Enum):
    Active = 1
    Archived = 2
    Deleted = 3

    @staticmethod
    def get_enum_from_value(value):
        if str(value) == "1":
            return WorkSpaceStatus.Active
        elif str(value) == "2":
            return WorkSpaceStatus.Archived
        elif str(value) == "3":
            return WorkSpaceStatus.Deleted
        else:
            raise NotImplementedError
