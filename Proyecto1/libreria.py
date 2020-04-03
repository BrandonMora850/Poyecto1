import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://kololixs:SQ5cXGAXFkRRJ1rqH3tV64fddcpcPKsW@drona.db.elephantsql.com:5432/kololixs")
db = scoped_session(sessionmaker(bind=engine))

def main():
        
        libreria = db.execute("SELECT * FROM public . libros LIMIT 10").fetchall()
        print(libreria)

if __name__ == "__main__":
    main()