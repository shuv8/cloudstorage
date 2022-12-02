from sqlalchemy.orm import relationship

from core.role import Role
from app_db import db
from core.user_cloud_space import SpaceType

user_department = db.Table('user_department',
                           db.Column('user_id', db.String, db.ForeignKey('user_model.user_id')),
                           db.Column('department_id', db.Integer, db.ForeignKey('department_model.department_id'))
                           )


class UserModel(db.Model):
    id = db.Column('user_id', db.String, primary_key=True)
    email = db.Column(db.String(100))
    passwordHash = db.Column(db.String(50))
    username = db.Column(db.String(200))
    role = db.Column(db.Enum(Role))
    departments = db.relationship(f"department_model", secondary=user_department, backref='users')
    spaces = relationship("user_space_model", backref="user")


class DepartmentModel(db.Model):
    id = db.Column('department_id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('department_name', db.String)


class UserSpaceModel(db.Model):
    id = db.Column('space_id', db.String, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("user_model.user_id"))
    space_type = db.Column(db.Enum(SpaceType))
    name = db.Column('department_name', db.String)
    parent = relationship("Parent", back_populates="children")
    # add: directory


class DirectoryModel(db.Model):
    id = db.Column('directory_id', db.String, primary_key=True)
    is_root = db.Column('is_root', db.Boolean)
    parent = relationship("directory_model", back_populates="inner_directories")

    inner_directories = relationship('directory_model', remote_side=[id], uselist=True)
    files = relationship("file_model", backref="directory")

    # add access


class FileModel(db.Model):
    id = db.Column('file_id', db.String, primary_key=True)
    type = db.Column(db.String(100))

    parent = relationship("directory_model", back_populates="files")

    # add access
