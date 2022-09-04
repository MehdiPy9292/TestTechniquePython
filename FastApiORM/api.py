from fastapi import FastAPI
import db
from sqlalchemy.orm import sessionmaker
import datetime 

#API
app = FastAPI()

#Session
Session = sessionmaker(bind=db.engine)
session = Session()


#add
@app.post("/ajoutPersonne")
async def ajout_personne(personne : db.PersonneSchema):
    nouveauPer = db.Personne(personne.id, personne.nom, personne.prenom, personne.date_naissance)
    age = calculateAge(personne.date_naissance)
    if (age > 150):
        return {"erreur" : "les personnes plus de 150 ne sont pas accepte"}
    else :
        session.add(nouveauPer)

        #save change
        session.commit()

        #closeS
        session.close()
        #return
        return {"id": personne.id, "nom": personne.nom, "prenom" : personne.prenom, "dateNaissance" : personne.date_naissance}

#get
@app.get("/listPersonnes", response_model=list[db.PersonneSchema])
async def list_personnes():
    res = session.query(db.Personne).all()
    return res



#fun
def calculateAge(birthDate):
    birthDate = datetime.datetime.strptime(birthDate, '%d/%m/%Y')
    today = datetime.date.today()
    age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
    print(age)
    return age
