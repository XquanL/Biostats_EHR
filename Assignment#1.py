"""Python module that provides analytical capabilities on EHR data."""
import datetime


def parse_data(
    patient_filename: str, lab_filename: str
) -> list[list[dict[str, str]]]:
    """Read and parse the data files and return a dictionary of patients."""
    with open(patient_filename, "r") as patient_file:
        patient_data = patient_file.readlines()
        columns = patient_data[0].strip().split("\t")
        columns[0] = columns[0][1:]  # remove \ufeff from the first column
        patients = []
        for patient in patient_data[1:]:
            patient_information = patient.strip().split("\t")
            patient_dict = {}
            for j in range(len(columns)):
                patient_dict[columns[j]] = patient_information[j]
            patients.append(patient_dict)
    with open(lab_filename, "r") as lab_file:
        lab_data = lab_file.readlines()
        columns = lab_data[0].strip().split("\t")
        columns[0] = columns[0][1:]  # remove \ufeff from the first column
        labs = []
        for lab in lab_data[1:]:
            lab_information = lab.strip().split("\t")
            lab_dict = {}
            for j in range(len(columns)):
                lab_dict[columns[j]] = lab_information[j]
            labs.append(lab_dict)
    all_information = [patients, labs]
    return all_information


def patient_age(records: list[list[dict[str, str]]], patient_id: str) -> int:
    """Take the data and return the age in years of the given patient."""
    patients = records[0]
    for patient in patients:
        # print(patient)
        if patient["PatientID"] == patient_id:
            date_of_birth = patient["PatientDateOfBirth"]
            birth = datetime.datetime.strptime(
                str(date_of_birth), "%Y-%m-%d %H:%M:%S.%f"
            )
            # calculate the age in years
            age_year = (datetime.datetime.today() - birth).days / 365
            age_year_int = int(age_year)
    return age_year_int


def patient_is_sick(
    records: list[list[dict[str, str]]],
    patient_id: str,
    lab_name: str,
    operator: str,
    value: float,
) -> bool:
    """Return a boolean indicating whether the patient is sick."""
    labs = records[1]
    for lab in labs:
        if lab["PatientID"] == patient_id:
            if lab["LabName"] == lab_name:
                if operator == ">":
                    if float(lab["LabValue"]) > value:
                        return True
                elif operator == "<":
                    if float(lab["LabValue"]) < value:
                        return True
    return False


if __name__ == "__main__":
    path = "/Users/liuxiaoquan/Documents/Spring2023/Biostats 821/"
    patients_filename = path + "PatientCorePopulatedTable.txt"
    labs_filename = path + "LabsCorePopulatedTable.txt"
    records = parse_data(patients_filename, labs_filename)
    print(patient_age(records, "1A8791E3-A61C-455A-8DEE-763EB90C9B2C"))
    print(
        patient_is_sick(
            records,
            "1A8791E3-A61C-455A-8DEE-763EB90C9B2C",
            "METABOLIC: ALBUMIN",
            ">",
            4.0,
        )
    )
