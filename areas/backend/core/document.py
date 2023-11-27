from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


class Document:
    def __init__(
            self,
            name: Optional[str],
            task_id: Optional[UUID],
            file: UUID,
            time: datetime,

            _id: Optional[UUID] = None,
    ):
        self.__id: UUID = _id or uuid4()
        self.__name: str = name
        self.__task_id: Optional[UUID] = task_id
        self.__file: UUID = file
        self.__time: datetime = time

    def get_id(self) -> UUID:
        return self.__id

    def get_time(self) -> datetime:
        return self.__time

    def set_time(self, new_time: datetime):
        if isinstance(new_time, datetime):
            self.__time = new_time
        else:
            raise TypeError

    time = property(get_time, set_time)

    def get_task_id(self) -> UUID:
        return self.__task_id

    def set_task_id(self, new_task_id: Optional[UUID]):
        if isinstance(new_task_id, Optional[UUID]):
            self.__task_id = new_task_id
        else:
            raise TypeError

    task_id = property(get_task_id, set_task_id)

    def get_file(self) -> UUID:
        return self.__file

    def load_file(self, new_file: UUID):
        if isinstance(new_file, UUID):
            self.__file = new_file
        else:
            raise TypeError

    file = property(get_file, load_file)

    def get_name(self) -> str:
        return self.__name

    def set_name(self, new_name: str):
        if isinstance(new_name, str):
            self.__name = new_name
        else:
            raise TypeError

    name = property(get_name, set_name)
