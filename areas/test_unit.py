import pytest
import uuid
from random import choice
from string import ascii_letters
from faker import Faker
from faker.providers import file

from accesses import BaseAccess
from base_storage_item import BaseStorageItem
from files import File, FileManager


class TestBaseAccess:

    @pytest.fixture(scope='function')
    def access(self):
        return BaseAccess()

    @pytest.fixture(scope='function')
    def uuids(self):
        return [uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]

    def test_ids(self, access, uuids):
        access.set_ids(uuids)
        assert access.get_ids() == uuids
        access.set_ids(list())
        assert access.get_ids() == []
        new_uuid = uuid.uuid4()
        access.set_ids([new_uuid])
        assert access.get_ids() == [new_uuid]
        access.set_ids(uuids)
        new_uuid = uuid.uuid4()
        access.add_id_to_ids(new_uuid)
        assert access.get_ids()[-1] == new_uuid
        assert access.get_id_from_ids(2) == uuids[2]
        access.remove_id_from_ids(new_uuid)
        assert len(access.get_ids()) == 3
        assert new_uuid not in access.get_ids()

    def test_item_id(self, access, uuids):
        access.set_item_id(uuids[0])
        assert access.get_item_id() == uuids[0]
        access.set_item_id(uuids[1])
        assert access.get_item_id() == uuids[1]

    def test_negative(self, access):
        try:
            access.set_ids([1, 2, uuid.uuid4()])
        except TypeError:
            pass
        access.set_ids([uuid.uuid4()])
        try:
            access.get_id_from_ids(1)
        except IndexError:
            pass
        try:
            access.add_id_to_ids(1)
        except TypeError:
            pass
        try:
            access.remove_id_from_ids(1)
        except TypeError:
            pass
        try:
            access.set_item_id(1)
        except TypeError:
            pass


class TestBaseStorageItem:

    @pytest.fixture(scope='function')
    def base_storage_item(self):
        return BaseStorageItem()

    @pytest.fixture(scope='function')
    def uuids(self):
        return [uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]

    @pytest.fixture(scope='function')
    def random_name(self):
        return ''.join(choice(ascii_letters) for _ in range(12))

    def test_id(self, base_storage_item):
        new_uuid = uuid.uuid4()
        base_storage_item.set_id(new_uuid)
        assert base_storage_item.get_id() == new_uuid
        new_uuid = uuid.uuid4()
        base_storage_item.set_id(new_uuid)
        assert base_storage_item.get_id() == new_uuid

    def test_name(self, base_storage_item, random_name):
        base_storage_item.set_name(random_name)
        assert base_storage_item.get_name() == random_name
        base_storage_item.set_name('newname')
        assert base_storage_item.get_name() == 'newname'

    def test_accesses(self, base_storage_item):
        base_accesses = [BaseAccess(), BaseAccess(), BaseAccess()]
        base_storage_item.set_accesses(base_accesses)
        assert base_storage_item.get_accesses() == base_accesses
        new_base_accesses = [BaseAccess(), BaseAccess(), BaseAccess()]
        base_storage_item.set_accesses(new_base_accesses)
        assert base_storage_item.get_accesses() == new_base_accesses
        old_accesses = []
        old_accesses.extend(new_base_accesses)
        new_access = BaseAccess()
        base_storage_item.add_access(new_access)
        assert base_storage_item.get_accesses() == old_accesses + [new_access]
        base_storage_item.remove_access(new_access)
        assert new_access not in base_storage_item.get_accesses()

    def test_negative(self, base_storage_item):
        try:
            base_storage_item.set_id(1)
        except TypeError:
            pass
        try:
            base_storage_item.set_name(1)
        except TypeError:
            pass
        try:
            base_storage_item.set_accesses(1)
        except TypeError:
            pass
        try:
            base_storage_item.set_accesses([1, 2, uuid.uuid4()])
        except TypeError:
            pass
        try:
            base_storage_item.add_access(1)
        except TypeError:
            pass
        try:
            base_storage_item.remove_access(1)
        except TypeError:
            pass


class TestFile:

    @pytest.fixture(scope='function')
    def file_obj(self):
        return File()

    @pytest.fixture(scope='session')
    def fake(self):
        faker = Faker()
        faker.add_provider(file)
        return faker

    def test_type(self, file_obj, fake):
        new_type = fake.file_extension()
        file_obj.set_type(new_type)
        assert file_obj.get_type() == new_type
        new_type = fake.file_extension()
        file_obj.set_type(new_type)
        assert file_obj.get_type() == new_type

    def test_negative(self, file_obj):
        try:
            file_obj.set_type(1)
        except TypeError:
            pass


class TestFileManager:

    @pytest.fixture(scope='function')
    def file_manager(self):
        return FileManager()

    def test_file_manager(self, file_manager):
        files_list = [File(), File(), File()]
        file_manager.set_items(files_list)
        assert file_manager.get_items() == files_list
        new_files_list = [File(), File(), File()]
        file_manager.set_items(new_files_list)
        assert file_manager.get_items() == new_files_list
        old_files = []
        old_files.extend(new_files_list)
        new_file = File()
        file_manager.add_item(new_file)
        assert file_manager.get_items() == old_files + [new_file]
        file_manager.remove_item(new_file)
        assert new_file not in file_manager.get_items()

    def test_negative(self, file_manager):
        try:
            file_manager.set_items([1, 2, File()])
        except TypeError:
            pass
        try:
            file_manager.add_item(1)
        except TypeError:
            pass
        try:
            file_manager.remove_item(1)
        except TypeError:
            pass
