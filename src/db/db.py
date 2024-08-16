from sqlalchemy import create_engine, MetaData
from src.config import DevelopmentConfig
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pymysql

res_config = DevelopmentConfig()


conn = pymysql.connect(
    host=res_config.MYSQL_HOST,
    user=res_config.MYSQL_USER,
    password=res_config.MYSQL_PASS,
    db=res_config.MYSQL_DB,
    connect_timeout=10,    # Tiempo de espera para la conexión
    read_timeout=10,       # Tiempo de espera para las operaciones de lectura
    write_timeout=10,      # Tiempo de espera para las operaciones de escritura
)



