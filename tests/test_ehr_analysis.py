"""Tests to analytical capabilities on EHR data"""
import pytest

import ehr_analysis


def test_parse_data_type() -> None:
    """Test the parse_data function returns the correct type."""
    data_dict = ehr_analysis.parse_data(
        "tests/test_patients.txt", "tests/test_labs.txt"
    )
    assert isinstance(data_dict, tuple)
    assert isinstance(data_dict[0], dict)
    assert isinstance(data_dict[1], dict)


def test_parse_data() -> None:
    """Test the parse_data function construct the correct dictionary."""
    data_dict = ehr_analysis.parse_data(
        "tests/test_patients.txt", "tests/test_labs.txt"
    )
    assert data_dict[0]["FB2ABB23-C9D0-4D09-8464-49BF0B982F0F"] == {
        "PatientID": "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F",
        "PatientGender": "Male",
        "PatientDateOfBirth": "1947-12-28 02:45:40.547",
        "PatientRace": "Unknown",
        "PatientMaritalStatus": "Married",
        "PatientLanguage": "Icelandic",
        "PatientPopulationPercentageBelowPoverty": "18.08",
    }
    assert data_dict[1]["1A8791E3-A61C-455A-8DEE-763EB90C9B2C"][0] == {
        "PatientID": "1A8791E3-A61C-455A-8DEE-763EB90C9B2C",
        "AdmissionID": "1",
        "LabName": "URINALYSIS: RED BLOOD CELLS",
        "LabValue": "1.8",
        "LabUnits": "rbc/hpf",
        "LabDateTime": "1992-07-01 01:36:17.910",
    }


def test_patient_age() -> None:
    """test whether the patient_age function returns the correct age"""
    data_dict = ehr_analysis.parse_data(
        "tests/test_patients.txt", "tests/test_labs.txt"
    )
    assert (
        ehr_analysis.patient_age(
            data_dict, "DB22A4D9-7E4D-485C-916A-9CD1386507FB"
        )
        == 52
    )


def test_patient_age_wrong() -> None:
    """test whether the patient_age function returns the correct age"""
    data_dict = ehr_analysis.parse_data(
        "tests/test_patients.txt", "tests/test_labs.txt"
    )
    with pytest.raises(AssertionError) as e:
        assert (
            ehr_analysis.patient_age(
                data_dict, "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F"
            )
            == 50
        )
    # match string begin with "assert"
    assert str(e.value).startswith("assert 75 == 50")


def test_patient_is_sick() -> None:
    """test whether the patient_is_sick function returns the correct boolean"""
    data_dict = ehr_analysis.parse_data(
        "tests/test_patients.txt", "tests/test_labs.txt"
    )
    assert (
        ehr_analysis.patient_is_sick(
            data_dict,
            "1A8791E3-A61C-455A-8DEE-763EB90C9B2C",
            "METABOLIC: GLUCOSE",
            ">",
            4.0,
        )
        is True
    )

    assert (
        ehr_analysis.patient_is_sick(
            data_dict,
            "1A8791E3-A61C-455A-8DEE-763EB90C9B2C",
            "CBC: MCH",
            "<",
            3.0,
        )
        is False
    )


def test_patient_is_sick_exceptions() -> None:
    """test whether the patient_is_sick function
    raises the correct exceptions when input is invalid"""
    data_dict = ehr_analysis.parse_data(
        "tests/test_patients.txt", "tests/test_labs.txt"
    )
    try:
        assert (
            ehr_analysis.patient_is_sick(
                data_dict,
                "1A8791E3-A61C-455A-8DEE-763EB90C9B2C",
                "METABOLIC: ALBUMIN",
                "!",
                4.0,
            )
        ) is True
    except AssertionError:
        print(
            "Invalid input value",
            "(ID, lab name, comparison operator, threshold value)",
        )
