from service.TestService import TestService


class DataStoreController:
    test_service = TestService()

    def get_test_id(self):
        return self.test_service.get_test_id()

