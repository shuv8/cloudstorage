from sqlalchemy.orm import relationship
from core.role import Role
from app_db import get_current_db
from core.user_cloud_space import SpaceType
from sqlalchemy.orm import DeclarativeMeta

#
# user_department = db.Table('user_department',
#                            db.Column('user_id', db.String, db.ForeignKey('user.user_id')),
#                            db.Column('department_id', db.Integer, db.ForeignKey('department.department_id'))
#                            )


db = get_current_db()


class UserDepartment(db.Model):
    __tablename__ = "user_department"

    user_id = db.Column(db.String, db.ForeignKey("user.user_id"), primary_key=True)
    department_id = db.Column(db.String, db.ForeignKey("department.department_id"), primary_key=True)


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
    spaces = db.relationship(
        "UserSpaceModel",
        backref="users"
    )


class DepartmentModel(db.Model):
    __tablename__ = 'department'

    id = db.Column('department_id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('department_name', db.String)


class UserSpaceModel(db.Model):
    __tablename__ = 'user_space'

    id = db.Column('space_id', db.String, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    parent_id = db.Column('parent_id', db.String, db.ForeignKey('user_space.space_id'), nullable=True)
    space_type = db.Column(db.Enum(SpaceType))

    parent = db.relationship("UserSpaceModel", back_populates="children")
    children = db.relationship("UserSpaceModel")
    # add: directory


class DirectoryModel(db.Model):
    __tablename__ = 'directory'

    id = db.Column('directory_id', db.String, primary_key=True)
    is_root = db.Column('is_root', db.Boolean)
    parent_id = db.Column('parent_id', db.String, db.ForeignKey('directory.directory_id'), nullable=True)

    parent = db.relationship("DirectoryModel", back_populates="inner_directories")
    inner_directories = relationship('DirectoryModel', remote_side=[id], uselist=True)
    files = db.relationship("FileModel", backref="directory")

    # add access


class FileModel(db.Model):
    __tablename__ = 'file'

    id = db.Column('file_id', db.String, primary_key=True)
    type = db.Column(db.String(100))
    directory_id = db.Column('directory_id', db.String, db.ForeignKey('directory.directory_id'))

    parent = db.relationship("DirectoryModel", back_populates="files")

    # add access
