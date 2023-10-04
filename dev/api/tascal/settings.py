import os
from os.path import join,dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__),'env')
load_dotenv(dotenv_path)

with open(os.environ.get('JWT_PUBLIC_KEY_PATH'), 'r') as f:
    PUBLIC_KEY = f.read()

JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM",'RS256')
JWT_COOKIE_SECURE = os.environ.get("JWT_COOKIE_SECURE")
DB_ECHO = os.environ.get("SQLALCHEMY_ECHO")
SERVER_NAME = os.environ.get("SERVER_NAME")

DB_ACCOUNT = os.environ.get('DB_ACCOUNT')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_NAME = os.environ.get('DB_NAME')
DB_SERVICE_NAME = os.environ.get('DB_SERVICE_NAME')

# DBのURIを組み立てる
DB_URI = f"mysql+pymysql://{DB_ACCOUNT}:{DB_PASSWORD}@{DB_SERVICE_NAME}:3306/{DB_NAME}"