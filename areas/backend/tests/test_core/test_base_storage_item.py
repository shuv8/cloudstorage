import uuid

import pytest

from core.accesses import UrlAccess, UserAccess, DepartmentAccess
from core.files import File


@pytest.fixture()
def file():
    return File(
        name="test",
        _type=".txt",
    )


@pytest.fixture()
def access():
    return UrlAccess("tg.ru")


@pytest.fixture()
def access2():
    return UserAccess("name")


@pytest.fixture()
def access3():
    return DepartmentAccess("name")


class TestBaseStorageItem:

    def test_name_property(self, file):
        file.name = "test2"
        assert file.name == "test2"

        with pytest.raises(TypeError):
            file.name = 42

    def test_id_property(self, file):
        _id = uuid.uuid4()

        file.id = _id
        assert file.id == _id

        with pytest.raises(TypeError):
            file.id = "test"

    def test_suspicious_property(self, file):
        file.is_suspicious = True
        assert file.is_suspicious == True

        with pytest.raises(TypeError):
            file.is_suspicious = "test"

    def test_accesses_property(self, file, access, access2, access3):
        file.accesses = [access]
        assert file.accesses == [access]

        with pytest.raises(TypeError):
            file.accesses = "test"

        file.add_access(access2)
        assert file.accesses == [access, access2]

        file.add_access(access3)

        with pytest.raises(TypeError):
            file.add_access(34)

        file.remove_access(access)
        assert file.accesses == [access2, access3]

        with pytest.raises(TypeError):
            file.remove_access(34)
