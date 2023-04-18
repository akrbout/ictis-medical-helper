from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID


class RoleModel(BaseModel):
    RoleID: UUID
    Name: str
    Description: str
    Rights: List[int]


class ClientModel(BaseModel):
    ClientID: UUID
    Role: UUID
    DateOfLastAuth: str
    IsDeleted: bool


class RegistrationModel(BaseModel):
    RegId: UUID
    Doc: Optional[UUID]
    Patient: Optional[UUID]
    RegDate: str


class PatientModel(BaseModel):
    PID: UUID
    FullName: str
    DateOfBirth: str
    PhoneNumber: str
    RegistrationAddress: str
    DMSNumber: Optional[str]
    MedicalCard: Optional[UUID]


class DiseaseModel(BaseModel):
    DiseaseID: UUID
    PredictDiagnosis: str
    RealDiagnosis: Optional[str]
    Symptoms: str
    Treatment: Optional[str]
    Medicines: Optional[str]


class MedicalCardModel(BaseModel):
    CardID: UUID
    Client: UUID
    Diseases: Optional[List[UUID]]


class SpecificationModel(BaseModel):
    SpecID: UUID
    SpecName: str
    SpecDescription: Optional[str]


class DoctorModel(BaseModel):
    DID: UUID
    FullName: str
    DateOfBirth: str
    PhoneNumber: str
    RegistrationAddress: str
    Specification: UUID


class AdministratorModel(BaseModel):
    AID: UUID
    FullName: str
    PhoneNumber: str
    EmailAddress: Optional[str]
