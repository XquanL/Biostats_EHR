# ehr-utils

The ehr-utils library provides some simple analytical capabilities for EHR data.

## Modules

* `ehr_analysis` provides four simple analytical capabilities for EHR data and two class(`Patient` and `Lab`), including functions that are able to:
1. **Read and parse the data files**
2. **Return the age in years of a given patient**
3. **Indicate a patient's situation based on a test result**
4. **Compute the age of a given patient when their earliest lab was recorded**

## Installation
Feel free to copy [ehr_analysis.py](https://github.com/biostat821-2023/ehr-utils-XquanL/blob/phase3_new/src/ehr_analysis.py) to your tests/ directory.

## Usage
The `ehr_analysis` contains three functions.
1. **Read and parse the data files**
  
   This function takes both patient and lab file names, or the path to those files (`string`), produces two lists in a tuple format that contain patients' basic information(`Patient` class) and relevant lab data(`Lab` class), respectively.
  
   *Example usage:*
  ```{python}
  from ehr_analysis import parse_data
  
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
   ```

    
    
2. **Return the age in years of a given patient**
    
    This is a property of the class `Patient`, which returns the age in years of the given patient.
    
   *Example usage:*
    ```{python}
    from ehr_analysis import patient_age
  
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
    ```
    

    
    
3. **Indicate a patient's situation based on a test result**
    
    This is a property of the class `Patient`, which takes a lab name (`string`), an operator (`string`), and a value of that lab result (`float`), returns a boolean indicating whether the patient has ever had a test with value above (">") or below ("<") the given level. 
    
   *Example usage:*
    ```{python}
    from ehr_analysis import patient_is_sick
  
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
    assert patient1.is_sick("URINALYSIS: RED BLOOD CELLS", ">", 1) == True
    ```



4. **Compute the age of a given patient when their earliest lab was recorded**

    This is a method of the class `Patient`, which returns the age in years (`int`) of a given patient when their earliest lab was recorded.
    
   *Example usage:*
    ```{python}
    from ehr_analysis import patient_is_sick
  
    def test_earliest_admission() -> None:
    """Test whether the earliest_admission property returns the correct admission"""
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
    ```


 ## Development
 We welcome contributions! Before opening a pull request, please confirm that existing regression tests pass:
   ```{python}
   python -m pytest tests/
   ```
    
