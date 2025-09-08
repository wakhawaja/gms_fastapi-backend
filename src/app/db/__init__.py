# app/db/__init__.py

from .mongo import db, init_db, close_db, ping_db
from .collections import users_collection, parts_collection, services_collection