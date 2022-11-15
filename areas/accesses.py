import uuid


class BaseAccess:
    __ids: list = None
    __item_id: uuid.UUID = None

    def get_ids(self) -> list:
        return self.__ids

    def set_ids(self, new_ids: list):
        if all(map(lambda new_id: isinstance(new_id, uuid.UUID), new_ids)):
            self.__ids = new_ids
        else:
            raise TypeError

    def add_id_to_ids(self, new_id: uuid.UUID):
        if isinstance(new_id, uuid.UUID):
            self.__ids.append(new_id)
        else:
            raise TypeError

    def get_id_from_ids(self, index: int) -> uuid.UUID:
        if index >= len(self.__ids):
            raise IndexError
        else:
            return self.__ids[index]

    def remove_id_from_ids(self, delete_id: uuid.UUID):
        if isinstance(delete_id, uuid.UUID):
            self.__ids.remove(delete_id)
        else:
            raise TypeError

    def get_item_id(self) -> uuid.UUID:
        return self.__item_id

    def set_item_id(self, new_item_id: uuid.UUID):
        if isinstance(new_item_id, uuid.UUID):
            self.__item_id = new_item_id
        else:
            raise TypeError
