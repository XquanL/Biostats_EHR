"""Test the object oriented class"""
import pytest

from ehr_analysis import Patient, Lab, parse_data
import fake_files

# make a fake patient file
patient_table = [
    ["id","name","birth_date"],
    ["1","Alice","1947-01-01"],
    ["2","Bob","1975-01-01"],
    ["3","Charlie","1990-01-01"],
]

# make a fake lab file
lab_table = [
    ["patient_id","lab_name","lab_value","lab_units","lab_date"],
    ["1","HDL","50","mg/dL","2019-01-01"],
    ["1","LDL","100","mg/dL","2019-01-01"],
    ["2","HDL","50","mg/dL","2007-01-01"],
    ["2","LDL","100","mg/dL","2007-01-01"],
    ["3","HDL","50","mg/dL","2023-01-01"],
    ["3","LDL","100","mg/dL","2023-01-01"],
]

path_patient = fake_files.write_file(patient_table, "tests")
path_lab = fake_files.write_file(lab_table, "tests")


def test_parse_data_type() -> None:
    """Test the parse_data function returns the correct type."""
    data_dict = parse_data(path_patient, path_lab)
    assert isinstance(data_dict, tuple)
    assert isinstance(data_dict[0], list)
    assert isinstance(data_dict[1], list)


def test_Patient_class() -> None:
    """Test the Patient class"""
    patient, labs = parse_data(path_patient, path_lab)
    assert patient[0].id == "1"
    assert patient[0].name == "Alice"
    assert patient[0].dob == "1947-01-01"


def test_Lab_class() -> None:
    """Test the Lab class"""
    patient, labs = parse_data(path_patient, path_lab)
    assert labs[0].patient_id == "1"
    assert labs[0].lab_name == "HDL"
    assert labs[0].lab_value == "50"
    assert labs[0].lab_units == "mg/dL"
    assert labs[0].lab_date == "2019-01-01"


def test_patient_age() -> None:
    """test whether the Patient age property returns the correct age"""
    patient1 = Patient(
        id="1",
        gender="male",
        DOB="1950-01-01 00:00:00.000000",
        race="white",
        lab_info=[
            {
                "PatientID": "1",
                "AdmissionID": "1",
                "LabName": "URINALYSIS: RED BLOOD CELLS",
                "LabValue": "1.8",
                "LabUnits": "rbc/hpf",
                "LabDateTime": "1992-07-01 01:36:17.910",
            },
            {
                "PatientID": "1",
                "AdmissionID": "1",
                "LabName": "METABOLIC: GLUCOSE",
                "LabValue": "103.3",
                "LabUnits": "mg/dL",
                "LabDateTime": "1992-06-30 09:35:52.383",
            },
        ],
    )
    assert patient1.age == 73


def test_is_sick() -> None:
    """Test whether the is_sick method returns the correct boolean value"""
    patient1 = Patient(
        id="1",
        gender="male",
        DOB="1950-01-01 00:00:00.000000",
        race="white",
        lab_info=[
            {
                "PatientID": "1",
                "AdmissionID": "1",
                "LabName": "URINALYSIS: RED BLOOD CELLS",
                "LabValue": "1.8",
                "LabUnits": "rbc/hpf",
                "LabDateTime": "1992-07-01 01:36:17.910",
            },
            {
                "PatientID": "1",
                "AdmissionID": "1",
                "LabName": "METABOLIC: GLUCOSE",
                "LabValue": "103.3",
                "LabUnits": "mg/dL",
                "LabDateTime": "1992-06-30 09:35:52.383",
            },
        ],
    )
    assert patient1.is_sick("URINALYSIS: RED BLOOD CELLS", ">", 1) is True


def test_earliest_admission() -> None:
    """Test whether the earliest_admission property returns the correct age"""
    patient1 = Patient(
        id="1",
        gender="male",
        DOB="1950-01-01 00:00:00.000000",
        race="white",
        lab_info=[
            {
                "PatientID": "1",
                "AdmissionID": "1",
                "LabName": "URINALYSIS: RED BLOOD CELLS",
                "LabValue": "1.8",
                "LabUnits": "rbc/hpf",
                "LabDateTime": "1992-07-01 01:36:17.910",
            },
            {
                "PatientID": "1",
                "AdmissionID": "1",
                "LabName": "METABOLIC: GLUCOSE",
                "LabValue": "103.3",
                "LabUnits": "mg/dL",
                "LabDateTime": "1992-06-30 09:35:52.383",
            },
        ],
    )
    assert patient1.earliest_admission == 42
