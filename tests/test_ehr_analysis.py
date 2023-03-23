"""Test the object oriented class"""
import pytest

from ehr_analysis import Patient, Lab, parse_data


def test_parse_data_type() -> None:
    """Test the parse_data function returns the correct type."""
    data_dict = parse_data("tests/test_patients.txt", "tests/test_labs.txt")
    assert isinstance(data_dict, tuple)
    assert isinstance(data_dict[0], list)
    assert isinstance(data_dict[1], list)


def test_Patient_class() -> None:
    """Test the Patient class"""
    patient, labs = parse_data(
        "tests/test_patients.txt", "tests/test_labs.txt"
    )
    assert patient[0].id == "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F"
    assert patient[0].gender == "Male"
    assert patient[0].DOB == "1947-12-28 02:45:40.547"
    assert patient[0].race == "Unknown"
    assert patient[0].lab_info == []


def test_Lab_class() -> None:
    """Test the Lab class"""
    patient, labs = parse_data(
        "tests/test_patients.txt", "tests/test_labs.txt"
    )
    assert labs[0].patient_id == "1A8791E3-A61C-455A-8DEE-763EB90C9B2C"
    assert labs[0].lab_name == "URINALYSIS: RED BLOOD CELLS"
    assert labs[0].lab_value == "1.8"
    assert labs[0].lab_units == "rbc/hpf"
    assert labs[0].lab_date == "1992-07-01 01:36:17.910"


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
