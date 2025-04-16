from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#URL_DB="mysql+mysqlconnector://root:0000@localhost:3306/tienda_mascota_nur"

#URL_DB="mysql+mysqlconnector://db_admin:david@192.168.80.21:3306/tienda_mascota_nur"
#URL_DB="mysql+mysqlconnector://root:david@172.17.0.2:3306/tienda_mascota_nur"
URL_DB="mysql+mysqlconnector://root:DqOsjYcNqvshUtDVREFPmaUUEZDKIxqs@mysql.railway.internal:3306/tienda_mascota"
crear=create_engine(URL_DB)
SessionLocal=sessionmaker(autocommit=False,autoflush=False, bind=crear)
base=declarative_base()

def get_db():
    cnn=SessionLocal()
    try:
        yield cnn
    finally:
        cnn.close()