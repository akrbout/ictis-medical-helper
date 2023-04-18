import os

from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, ARRAY, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ["DB_CONNECTION_STRING"]
Base = declarative_base()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Role(Base):
    __tablename__ = 'Role'
    RoleID = Column(UUID(as_uuid=True), primary_key=True)
    Name = Column(String, unique=True, nullable=False)
    Description = Column(Text, nullable=False)
    Rights = Column(ARRAY(Integer), nullable=False)


class Client(Base):
    __tablename__ = 'Client'
    ClientID = Column(UUID(as_uuid=True), primary_key=True)
    Role = Column(UUID(as_uuid=True), ForeignKey('Role.RoleID'))
    DateOfLastAuth = Column(DateTime, nullable=False)
    IsDeleted = Column(Boolean, nullable=False)


class Registration(Base):
    __tablename__ = 'Registration'
    RegId = Column(UUID, primary_key=True)
    Doc = Column(UUID(as_uuid=True))
    Patient = Column(UUID(as_uuid=True))
    RegDate = Column(DateTime, nullable=False)


class Patient(Base):
    __tablename__ = 'Patient'
    PID = Column(UUID(as_uuid=True), ForeignKey('Client.ClientID'), primary_key=True)
    FullName = Column(String, nullable=False)
    DateOfBirth = Column(DateTime, nullable=False)
    PhoneNumber = Column(String, nullable=False)
    RegistrationAddress = Column(String, nullable=False)
    DMSNumber = Column(String)
    MedicalCard = Column(UUID(as_uuid=True))


class Disease(Base):
    __tablename__ = 'Disease'
    DiseaseID = Column(UUID(as_uuid=True), primary_key=True)
    PredictDiagnosis = Column(String, nullable=False)
    RealDiagnosis = Column(String)
    Symptoms = Column(String, nullable=False)
    Treatment = Column(String)
    Medicines = Column(String)


class MedicalCard(Base):
    __tablename__ = 'MedicalCard'
    CardID = Column(UUID(as_uuid=True), primary_key=True)
    Client = Column(UUID(as_uuid=True), ForeignKey('Client.ClientID'))
    Diseases = Column(ARRAY(UUID(as_uuid=True)))


class Specification(Base):
    __tablename__ = 'Specification'
    SpecID = Column(UUID(as_uuid=True), primary_key=True)
    SpecName = Column(String, nullable=False)
    SpecDescription = Column(String, nullable=False)


class Doctor(Base):
    __tablename__ = 'Doctor'
    DID = Column(UUID(as_uuid=True), ForeignKey('Client.ClientID'), primary_key=True)
    FullName = Column(String, nullable=False)
    DateOfBirth = Column(DateTime, nullable=False)
    PhoneNumber = Column(String, nullable=False)
    RegistrationAddress = Column(String, nullable=False)
    Specification = Column(UUID(as_uuid=True), ForeignKey('Specification.SpecID'))


class Administrator(Base):
    __tablename__ = 'Administrator'
    AID = Column(UUID(as_uuid=True), ForeignKey('Client.ClientID'), primary_key=True)
    FullName = Column(String, nullable=False)
    PhoneNumber = Column(String, nullable=False)
    EmailAddress = Column(String)


def create_db():
    Base.metadata.create_all(bind=engine)
