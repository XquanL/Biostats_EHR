# ehr-utils

The ehr-utils library provides some simple analytical capabilities for EHR data.

## Modules

* `ehr_analysis` provides three simple analytical capabilities for EHR data, including functions that are able to:
1. **Read and parse the data files**
2. **Return the age in years of a given patient**
3. **Indicate a patient's situation based on a test result**

## Installation
Feel free to copy [ehr_analysis.py](https://github.com/biostat821-2023/ehr-utils-XquanL/blob/phase3_new/src/ehr_analysis.py) to your tests/ directory.

## Usage
The `ehr_analysis` contains three functions.
1. **Read and parse the data files**
  
   This function takes both patient and lab file names, or the path to those files (`string`), produces two dictionaries in a tuple format that contain patients' basic information and relevant lab data, respectively.
  
   *Example usage:*
  ```{python}
  from ehr_analysis import parse_data
  
  def test_parse_data():
    data_dict = ehr_analysis.parse_data("tests/test_patients.txt", "tests/test_labs.txt")
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
   ```

    
    
2. **Return the age in years of a given patient**
    
    This function takes the outcome(return value) of the function `parse_data` and a patient ID (`string`), returns the age in years of the given patient.
    
   *Example usage:*
    ```{python}
    from ehr_analysis import patient_age
  
    def test_patient_age() -> None:
    data_dict = ehr_analysis.parse_data("tests/test_patients.txt", "tests/test_labs.txt")
    assert (
        ehr_analysis.patient_age(
            data_dict, "DB22A4D9-7E4D-485C-916A-9CD1386507FB"
        )
        == 52
    )
    ```
    

    
    
3. **Indicate a patient's situation based on a test result**
    
    This function takes the outcome(return value) of the function `parse_data` and a patient ID (`string`), a lab name (`string`), an operator (`string`), and a value of that lab result (`float`), returns a boolean indicating whether the patient has ever had a test with value above (">") or below ("<") the given level. 
    
   *Example usage:*
    ```{python}
    from ehr_analysis import patient_is_sick
  
    data_dict = ehr_analysis.parse_data("tests/test_patients.txt", "tests/test_labs.txt")
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
    ```
 
 ## Development
 We welcome contributions! Before opening a pull request, please confirm that existing regression tests pass:
   ```{python}
   python -m pytest tests/
   ```
    
