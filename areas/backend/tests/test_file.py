import pytest

from cloud_storage_service.files import File


@pytest.fixture()
def file():
    return File(
        name="test",
        _type=".txt",
    )


class TestFile:

    def test_type_property(self, file):
        file.type = ".pdf"
        assert file.type == ".pdf"

        with pytest.raises(TypeError):
            file.type = 42
