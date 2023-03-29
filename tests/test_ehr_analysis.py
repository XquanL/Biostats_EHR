"""Test the object oriented class"""
import pytest

from ehr_analysis import Patient, Lab, parse_data
from fake_files import fake_files

temp_patient = [
    ["id", "gender", "birth_date", "race"],
    ["1", "F", "1947-01-01", "white"],
    ["2", "M", "1975-01-01", "black"],
    ["3", "F", "1990-01-01", "white"],
]

temp_lab = [
    ["patient_id", "lab_name", "lab_value", "lab_units", "lab_date"],
    ["1", "HDL", "50", "mg/dL", "2019-01-01"],
    ["1", "LDL", "100", "mg/dL", "2019-01-01"],
    ["2", "HDL", "50", "mg/dL", "2007-01-01"],
    ["2", "LDL", "100", "mg/dL", "2007-01-01"],
    ["3", "HDL", "50", "mg/dL", "2023-01-01"],
    ["3", "LDL", "100", "mg/dL", "2023-01-01"],
]


def test_parse_data() -> None:
    """Test the parse_data function returns the correct type."""
    with fake_files(temp_patient, temp_lab) as (patient, lab):
        data_dict = parse_data(patient, lab)
    assert isinstance(data_dict, tuple)
    assert isinstance(data_dict[0], list)
    assert isinstance(data_dict[1], list)


def test_Patient_class() -> None:
    """Test the parse_data() Patient has the correct attributes."""
    with fake_files(temp_patient, temp_lab) as (patient, lab):
        patient, labs = parse_data(patient, lab)
    assert patient[0].id == "1"
    assert patient[0].gender == "F"
    assert patient[0].dob == "1947-01-01"
    assert patient[0].race == "white"


def test_Lab_class() -> None:
    """Test the parse_data() Lab has the correct attributes."""
    with fake_files(temp_patient, temp_lab) as (patient, lab):
        patient, labs = parse_data(patient, lab)
    assert labs[0].patient_id == "1"
    assert labs[0].lab_name == "HDL"
    assert labs[0].lab_value == "50"
    assert labs[0].lab_units == "mg/dL"
    assert labs[0].lab_date == "2019-01-01"


def test_patient_age() -> None:
    """test whether the Patient age property returns the correct age"""
    lab1 = Lab(
        patient_id="1",
        lab_name="URINALYSIS: RED BLOOD CELLS",
        lab_value="1.8",
        lab_units="rbc/hpf",
        lab_date="1992-07-01 01:36:17.910",
    )
    patient1 = Patient(
        id="1",
        dob="1950-01-01 00:00:00.000000",
        lab_info=[
            lab1,
        ],
    )
    assert patient1.age == 73


def test_is_sick() -> None:
    """Test whether the is_sick method returns the correct boolean value"""
    lab1 = Lab(
        patient_id="1",
        lab_name="URINALYSIS: RED BLOOD CELLS",
        lab_value="1.8",
        lab_units="rbc/hpf",
        lab_date="1992-07-01 01:36:17.910",
    )
    patient1 = Patient(
        id="1",
        dob="1950-01-01 00:00:00.000000",
        lab_info=[
            lab1,
        ],
    )
    assert patient1.is_sick("URINALYSIS: RED BLOOD CELLS", ">", 1) is True


def test_earliest_admission() -> None:
    """Test whether the earliest_admission property returns the correct age"""
    lab1 = Lab(
        patient_id="1",
        lab_name="URINALYSIS: RED BLOOD CELLS",
        lab_value="1.8",
        lab_units="rbc/hpf",
        lab_date="1992-07-01 01:36:17.910",
    )
    lab2 = Lab(
        patient_id="1",
        lab_name="METABOLIC: GLUCOSE",
        lab_value="103.3",
        lab_units="mg/dL",
        lab_date="1992-06-30 09:35:52.383",
    )
    patient1 = Patient(
        id="1",
        dob="1950-01-01 00:00:00.000000",
        lab_info=[
            lab1,
            lab2,
        ],
    )
    assert patient1.earliest_admission == 42
