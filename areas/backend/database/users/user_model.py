from enum import Enum

from core.role import Role
from app_db import db

class UserORM(db.Model):
    id = db.Column('user_id', db.String, primary_key=True)
    email = db.Column(db.String(100))
    passwordHash = db.Column(db.String(50))
    username = db.Column(db.String(200))
    role = db.Column(db.Enum(Role))

    # space_manager = db.relationship('SpaceManager', remote_side=id, join=('SpaceManager.parent_id==SpaceManager.id'), backref='sub-regions')
    # _department_manager
