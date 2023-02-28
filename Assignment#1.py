"""Python module that provides analytical capabilities on EHR data."""
import datetime


def parse_data(
    patient_filename: str, lab_filename: str
) -> dict[str, dict[str, dict[str, str]]]:
    """Read and parse the data files and return a dictionary of patients.

    N1 is the number of patients
    M1 is the nubmer of columns in patient file
    N2 is the number of labs
    M2 is the number of columns in lab file

    During the preprocessing,
    The entirety of each line is read, which is a O(M1*N1) operation,
    and each column is split once, which is a O(M1) operation.
    Then,
    every line in the patient file is read once, which is a O(N1) operation.
    For every patient, every column is read once,
    which is a O(M1) operation.
    There are N1 patients,
    so a O(N1*M1) operation is performed to make the patients list.
    For big-O analysis, we drop the constant factor,
    yielding O(N1*M1) complexity for the patient file.

    The same analysis is performed for the lab file,
    yielding O(N2*M2) complexity for the lab file.
    The total complexity is O(N1*M1 + N2*M2) = O(N1*M1) + O(N2*M2)
    """
    with open(
        patient_filename, "r", encoding="utf-8-sig"
    ) as patient_file:  # 1 time
        patient_data = patient_file.readlines()  # O(N1*M1)
        columns = patient_data[0].strip().split("\t")  # O(M1)
        patients = {}  # O(1)
        for patient in patient_data[1:]:  # N1 times
            patient_information = patient.strip().split("\t")  # O(M1)
            patient_dict = {}  # O(1)
            for j in range(len(columns)):  # M1 times
                patient_dict[columns[j]] = patient_information[j]  # O(1)
            # set the patient ID as the key
            patients[patient_dict["PatientID"]] = patient_dict  # O(1)
    with open(lab_filename, "r", encoding="utf-8-sig") as lab_file:  # 1 time
        lab_data = lab_file.readlines()  # O(N2*M2)
        columns = lab_data[0].strip().split("\t")  # O(M2)
        labs = {}  # O(1)
        for lab in lab_data[1:]:  # N2 times
            lab_information = lab.strip().split("\t")  # O(M2)
            lab_dict = {}  # O(1)
            for j in range(len(columns)):  # M2 times
                lab_dict[columns[j]] = lab_information[j]  # O(1)
            # set patient ID + lab name as the key
            IDnew = lab_dict["PatientID"] + lab_dict["LabName"]  # O(1)
            labs[IDnew] = lab_dict  # O(1)
    # all_information = [patients, labs]  # O(1)
    # change the return type to dict
    all_information = {"patients": patients, "labs": labs}  # O(1)
    return all_information  # O(1)


def patient_age(
    records: dict[str, dict[str, dict[str, str]]], patient_id: str
) -> int:
    """Take the data and return the age in years of the given patient.

    For every patient, we need to
    determine whether the patient ID is in the patient dictionary,
    which is a O(1) operation,
    and find the patient ID in the patient dictionary,
    which is a O(1) operation,
    and then find the date of birth,
    which is a O(1) operation.
    Then, we need to calculate the age of the patient,
    which is a O(1) operation.

    For big-O analysis,
    it yields O(1) complexity.
    """
    # patients = records[0]  # O(1)
    patients = records["patients"]  # O(1)
    if patient_id in patients:  # O(1)
        date_of_birth = patients[patient_id]["PatientDateOfBirth"]  # O(1)
        birth = datetime.datetime.strptime(
            str(date_of_birth), "%Y-%m-%d %H:%M:%S.%f"
        )  # O(1)
        # calculate the age in years
        age_year = (datetime.datetime.today() - birth).days / 365  # O(1)
        age_year_int = int(age_year)  # O(1)
    return age_year_int  # O(1


def patient_is_sick(
    records: dict[str, dict[str, dict[str, str]]],
    patient_id: str,
    lab_name: str,
    operator: str,
    value: float,
) -> bool:
    """Return a boolean indicating whether the patient is sick.

    For every lab, we need to
    find the patient ID + lab name in the lab dictionary,
    which is a O(1) operation,
    and then find the lab value,
    which is a O(1) operation.
    Then, we need to compare the lab value with the given value,
    which is a O(1) operation.

    For big-O analysis,
    it yields O(N2) complexity.
    """
    # labs = records[1]  # O(1)
    labs = records["labs"]  # O(1)
    id_lab = patient_id + lab_name  # O(1)
    if id_lab in labs:  # O(1)
        lab = labs[id_lab]  # O(1)
        if operator == ">":  # O(1)
            if float(lab["LabValue"]) > value:  # O(1)
                return True  # O(1)
        elif operator == "<":  # O(1)
            if float(lab["LabValue"]) < value:  # O(1)
                return True  # O(1)
    return False  # O(1)


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
            "METABOLIC: GLUCOSE",
            ">",
            4.0,
        )
    )
