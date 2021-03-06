import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://ouajkbkn:sux35jMh4OOWUHikcOwwqUxCl8WYuJzu@drona.db.elephantsql.com:5432/ouajkbkn")
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open ("books.csv")
    reader = csv.reader(f)
    
    
    for isbn, titulo, autor, año in reader:
        db.execute("INSERT INTO libros (ISBN, Titulo, Autor, Año) VALUES (:ISBN, :Titulo, :Autor, :Año)",{"ISBN": isbn, "Titulo": titulo, "Autor": autor, "Año": año})
        print(f"ISBN: {isbn} - Titulo: {titulo} - Autor:{autor} - Año: {año}")
        db.commit()

if __name__ == "__main__":
    main()
    
    