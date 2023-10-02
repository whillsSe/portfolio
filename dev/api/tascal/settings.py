import os
from os.path import join,dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__),'env')
load_dotenv(dotenv_path)

PRIVATE_KEY = os.environ.get("JWT_PRIVATE_KEY")
DB_URI = os.environ.get("SQLALCHEMY_DB_URI")
DB_ECHO = os.environ.get("SQLALCHEMY_ECHO")