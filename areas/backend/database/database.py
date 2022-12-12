from sqlalchemy.orm import relationship, backref

from core.accesses import Access, AccessType
from core.role import Role
from app_db import get_current_db
from core.user_cloud_space import SpaceType
from flask import current_app

db = get_current_db(current_app)


class UserDepartment(db.Model):
    __tablename__ = "user_department"

    user_id = db.Column(db.String, db.ForeignKey("user.user_id"), primary_key=True)
    department_id = db.Column(db.String, db.ForeignKey("department.department_id"), primary_key=True)


class FileDirectory(db.Model):
    __tablename__ = "file_directory"

    file_id = db.Column(db.String, db.ForeignKey("file.file_id"), primary_key=True)
    directory_id = db.Column(db.String, db.ForeignKey("directory.directory_id"), primary_key=True)


class DepartmentModel(db.Model):
    __tablename__ = 'department'

    id = db.Column('department_id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('department_name', db.String, unique=True)


class AccessModel(db.Model):
    __tablename__ = 'access'

    id = db.Column('access_id', db.Integer, primary_key=True, autoincrement=True)
    access_level = db.Column(db.Enum(Access))
    access_type = db.Column(db.Enum(AccessType))
    value = db.Column(db.String)

    parent_file_id = db.Column('parent_file_id', db.String, db.ForeignKey("file.file_id"), nullable=True)
    parent_id = db.Column('parent_id', db.String, db.ForeignKey("directory.directory_id"), nullable=True)


class FileModel(db.Model):
    __tablename__ = 'file'

    id = db.Column('file_id', db.String, primary_key=True)
    name = db.Column('name', db.String)
    type = db.Column(db.String(100))

    accesses: list[AccessModel] = db.relationship(
        'AccessModel',
        uselist=True,
        backref="file",
        cascade="all,delete"
    )


class DirectoryModel(db.Model):
    __tablename__ = 'directory'

    id = db.Column('directory_id', db.String, primary_key=True)
    name = db.Column('name', db.String)
    is_root = db.Column('is_root', db.Boolean)
    parent_id = db.Column('parent_id', db.String, db.ForeignKey('directory.directory_id'), nullable=True)

    spaces = db.relationship(
        'UserSpaceModel',
        uselist=True,
        backref="directory"
    )

    inner_directories = db.relationship(
        'DirectoryModel',
        uselist=True
    )

    files: list[FileModel] = db.relationship(
        "FileModel",
        secondary=FileDirectory.__table__,
        backref="directory"
    )

    accesses: list[AccessModel] = db.relationship(
        'AccessModel',
        uselist=True,
        backref="directory",
        cascade="all,delete"
    )


class UserSpaceModel(db.Model):
    __tablename__ = 'user_space'

    id = db.Column('space_id', db.String, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    space_type = db.Column(db.Enum(SpaceType))

    root_directory_id = db.Column(db.String, db.ForeignKey('directory.directory_id'))
    root_directory: DirectoryModel = db.relationship("DirectoryModel", backref=backref("user_space", uselist=True))


class UrlSpaceModel(db.Model):
    __tablename__ = 'url_space'

    id = db.Column('id', db.String, primary_key=True)

    root_directory_id = db.Column(db.String, db.ForeignKey('directory.directory_id'))
    root_directory: DirectoryModel = db.relationship("DirectoryModel", backref=backref("url_space", uselist=True))


class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column('user_id', db.String, primary_key=True)
    email = db.Column(db.String(100))
    passwordHash = db.Column(db.String(50))
    username = db.Column(db.String(200))
    role = db.Column(db.Enum(Role))
    departments = db.relationship(
        "DepartmentModel",
        secondary=UserDepartment.__table__,
        backref="users"
    )
    spaces: list[UserSpaceModel] = db.relationship(
        "UserSpaceModel",
        backref="users"
    )
