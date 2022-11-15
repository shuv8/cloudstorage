import uuid


class UserCloudSpace:
    __space_id: uuid = None

    def provide_data(self):
        return self
