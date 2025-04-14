from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# importing the elements defined in the model
from model.base import Base
from model.produto import Produto

db_path = "database/"
# Checks if the directory does not exist
if not os.path.exists(db_path):
   # then creates the directory
   os.makedirs(db_path)

# database access URL (this is a local SQLite access URL)
db_url = 'sqlite:///%s/db.sqlite3' % db_path

# creates the connection engine with the database
engine = create_engine(db_url, echo=False)

# Instantiates a session maker with the database
Session = sessionmaker(bind=engine)

# creates the database if it does not exist
if not database_exists(engine.url):
    create_database(engine.url) 

# creates the database tables if they do not exist
Base.metadata.create_all(engine)
