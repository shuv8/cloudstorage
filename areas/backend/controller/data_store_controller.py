from core.base_storage_item import BaseStorageItem
from service.data_store_service import DataStoreService


class DataStoreController:

    def __init__(self):
        self.data_store_service = DataStoreService()

    def search_in_cloud(self, user_mail: str, file_name: str) -> list[tuple[BaseStorageItem, str]]:
        return self.data_store_service.search_in_cloud(user_mail, file_name)


