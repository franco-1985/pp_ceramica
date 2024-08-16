from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.config import DevelopmentConfig


res_config = DevelopmentConfig()

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{res_config.MYSQL_USER}:{res_config.MYSQL_PASS}@{res_config.MYSQL_HOST}/{res_config.MYSQL_DB}"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

meta = MetaData()
Base = declarative_base()


#conn = engine.connect()


