from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as _sqlalchemy
from sqlmodel import SQLModel, create_engine
from pydantic import BaseModel

# connect
engine = create_engine('sqlite:///sqlalchemy.sqlite', echo=True)
# 
base = declarative_base()

class Personne(base):
    __tablename__ = "personne"
    id = _sqlalchemy.Column("id", _sqlalchemy.Integer, primary_key=True)
    nom = _sqlalchemy.Column("nom", _sqlalchemy.String)
    prenom = _sqlalchemy.Column("prenom", _sqlalchemy.String)
    date_naissance = _sqlalchemy.Column("date_naissance", _sqlalchemy.String)

    def __init__(self, id, nom, prenom, date_naissance):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance

class PersonneSchema(BaseModel):
    id:int
    nom:str
    prenom:str
    date_naissance:str

    class Config:
        orm_mode = True


base.metadata.create_all(engine)