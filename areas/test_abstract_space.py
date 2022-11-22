import pytest

from abstract_space import AbstractSpace, DirectoryManager


class TestAbstractSpace:
    @pytest.fixture(scope='function')
    def abstract_space(self):
        return AbstractSpace()

    def test_provide_main_directory(self, abstract_space):
        assert isinstance(abstract_space.provide_main_directory(), DirectoryManager)
