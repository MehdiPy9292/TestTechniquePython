from msilib.schema import Error
from urllib.request import Request
import datetime 
from fastapi import FastAPI
app = FastAPI()

class Personne:
    def _init_(self, nom, prenom, date_naissance):
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance


import mysql.connector as MC
try:
    mydb = MC.connect(
        host="localhost",
        user="root",
        passwd=""
    )
    cursor = mydb.cursor()
    # create Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS personnes (
            nom varchar(100) DEFAULT NULL,
            prenom varchar(100) DEFAULT NULL,
            date_naissance varchar(100) DEFAULT NULL
            );
        """)
    # ajouter une personne
    @app.post("/nouveauPersonne")
    async def ajouter_personne(personne : Personne):
        age = calculateAge(personne.date_naissance)
        if (age > 150):
            return {"Erreur: on accepte les personnes ayant moins de 150ans"}
        else :
            # Execute
            insertInto = "INSERT INTO personnes (nom, prenom, date_naissance) VALUES (%s, %s)"
            val = (personne.nom, personne.prenom, personne.date_naissance)
            cursor.execute(insertInto, val)
    # recuperer les personnes
    @app.get("/listPersonnes")
    async def listPersonnes():
        cursor.execute("Select * from personnes order by nom")
        rows = cursor.fetchall()
        for row in rows:
            age = calculateAge(row[2])
            return {"nom" : row[0], "prenom" :  row[1], "date_naissance" : row[2], "age" : age}
    
except MC.Error as err: 
    print(err)



def calculateAge(birthDate):
    birthDate = datetime.datetime.strptime(birthDate, '%Y-%m-%d')
    today = datetime.date.today()
    age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
    print(age)
    return age
