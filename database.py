from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#I commented his code for security reasons
#engine=create_engine("postgresql://postgres:{PASSWORD}@localhost/item_db"),
#echo=True)

Base=declarative_base()

SessionLocal=sessionmaker(bind=engine)