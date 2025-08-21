from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, ForeignKey, String, Column, Date
from sqlalchemy.orm import relationship
from dataclasses import dataclass

db = SQLAlchemy()

@dataclass
class InmateModel(db.Model):
    __tablename__ = 'inmate'

    inmateid = Column(Integer, primary_key=True)
    fullname = Column(String, nullable=False)
    inmatenum = Column(Integer, nullable=False)
    arrivaldate = Column(Date, nullable=False)
    sentencetime = Column(Date, nullable=False)
    penalty = Column(Integer, nullable=False)
    cellid = Column(ForeignKey('cell.cellid'), nullable=False)
    crimeid = Column(ForeignKey('crime.crimeid'), nullable=False)

    crime = relationship('CrimeModel')
    cell = relationship('CellModel')

    def __init__(self, fullname, inmatenum, arrivaldate, sentencetime, penalty, cellid, crimeid):
        self.fullname = fullname
        self.inmatenum = inmatenum
        self.arrivaldate = arrivaldate
        self.sentencetime = sentencetime
        self.penalty = penalty
        self.cellid = cellid
        self.crimeid = crimeid


@dataclass
class CellModel(db.Model):
    __tablename__ = 'cell'

    cellid = Column(Integer, primary_key=True)
    cellnum = Column(Integer, nullable=False)
    numberofbeds = Column(Integer, nullable=False)

    def count_inmates(cellid) -> int:
        return db.session.query(InmateModel).filter_by(cellid=cellid).count()

@dataclass
class CrimeModel(db.Model):
    __tablename__ = 'crime'

    crimeid = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)

@dataclass
class UserModel(db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)