from repository.TestStorageRepository import TestStorageRepository


class TestService:
    test_repo = TestStorageRepository()

    def get_test_id(self):
        return self.test_repo.get_test_id()
