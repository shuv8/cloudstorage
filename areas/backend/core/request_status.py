from enum import Enum


class RequestStatus(Enum):
    Open = 1
    InReview = 2
    Approved = 3
    Declined = 4
    Closed = 5

    @staticmethod
    def get_enum_from_value(value):
        if str(value) == "1":
            return RequestStatus.Open
        elif str(value) == "2":
            return RequestStatus.InReview
        elif str(value) == "3":
            return RequestStatus.Approved
        elif str(value) == "4":
            return RequestStatus.Declined
        elif str(value) == "5":
            return RequestStatus.Closed
        else:
            raise NotImplementedError
