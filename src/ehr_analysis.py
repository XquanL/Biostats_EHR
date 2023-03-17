"""Python module that provides analytical capabilities on EHR data."""
import datetime


def parse_data(
    patient_filename: str, lab_filename: str
) -> tuple[dict[str, dict[str, str]], dict[str, list[dict[str, str]]]]:
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
    so a O(N1*M1) operation is performed to make the patients dictionary.
    For big-O analysis, we drop the constant factor,
    yielding O(N1*M1) complexity for the patient file.

    For the lab file,
    the entirety of each line is read, which is a O(M2*N2) operation,
    and each column is split once, which is a O(M2) operation.
    For every line in the lab file, every column(lab information)
    is split onece, which is a O(M2) operation.
    And we need to make a dictionary of that particular lab outcome,
    which is a O(M2) operation.
    Then, we need to determine whether the patient id that the lab
    information belongs to is in the labs dictionary or not,
    which is a O(1) operation.
    Then, we use the patient id as the key
    and make a list of all lab outcome that patient has as the
    value of the labs dictionary related to that patient,
    which is a O(M2) operation.
    There are N2 lab outcomes,
    so a O(N2*M2) operation is performed to make the labs dictionary.
    For big-O analysis, we drop the constant factor,
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
        # make a dictionary of labs with patient ID as the key
        labs: dict[str, list[dict[str, str]]] = {}  # O(1)
        for lab in lab_data[1:]:  # N2 times
            lab_information = lab.strip().split("\t")  # O(M2)
            lab_map = {
                columns[i]: lab_information[i] for i in range(len(columns))
            }  # O(M2)
            if lab_map["PatientID"] in labs:  # O(1)
                labs[lab_map["PatientID"]].append(lab_map)  # O(1)
            else:
                labs[lab_map["PatientID"]] = [lab_map]  # O(1)
    # all_information = [patients, labs]  # O(1)
    # change the return type to tuple
    return patients, labs  # O(1)


def patient_age(
    records: tuple[dict[str, dict[str, str]], dict[str, list[dict[str, str]]]],
    patient_id: str,
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
    patients = records[0]  # O(1)
    if patient_id in patients:  # O(1)
        date_of_birth = patients[patient_id]["PatientDateOfBirth"]  # O(1)
        birth = datetime.datetime.strptime(
            str(date_of_birth), "%Y-%m-%d %H:%M:%S.%f"
        )  # O(1)
        # calculate the age in years
        age_year = (datetime.datetime.today() - birth).days / 365  # O(1)
        age_year_int = int(age_year)  # O(1)
    return age_year_int  # O(1)


def patient_is_sick(
    records: tuple[dict[str, dict[str, str]], dict[str, list[dict[str, str]]]],
    patient_id: str,
    lab_name: str,
    operator: str,
    value: float,
) -> bool:
    """Return a boolean indicating whether the patient is sick.

    For every patient, we need to
    find the patient ID in the lab dictionary,
    which is a O(1) operation.
    Then, for each lab outcome for that patient,
    we need to determine whether the lab name is the same as the input,
    and then compare the lab value with the given value.
    They are all O(1) operations.
    There are N2/N1 labs outcomes for each patient,
    so a O(N2/N1) operation is performed to figure out
    whether this patient is sick or not.

    For big-O analysis, we drop the constant factor,
    it yields O(N2/N1) complexity.
    """
    # labs = records[1]  # O(1)
    labs = records[1]  # O(1)
    patient_labs = labs[patient_id]  # O(1)
    for lab in patient_labs:  # O(N2/N1)
        # max number of labs for a patient
        if lab["LabName"] == lab_name:  # O(1)
            lab_value = float(lab["LabValue"])  # O(1)
            if operator == ">":  # O(1)
                if lab_value > value:  # O(1)
                    return True  # O(1)
            elif operator == "<":  # O(1)
                if lab_value < value:  # O(1)
                    return True  # O(1)
    return False  # O(1)


def first_time(
    records: tuple[dict[str, dict[str, str]], dict[str, list[dict[str, str]]]],
    patient_id: str,
) -> int:
    """Computes the age of a given patient when their earliest lab was recorded

    For every patient, we need to
    find the lab dictionary that corresponds to the patient ID,
    which is a O(1) operation.
    Then, for each lab outcome for that patient,
    we need to find the earliest lab date,
    which contains operations of O(1) complexity.
    Since there are N2/N1 labs outcomes for each patient,
    a O(N2/N1) operation is performed to figure out
    the earliest lab date for this patient.
    Then, we need to find the birth date of the patient,
    which is a O(1) operation.
    Finally, we need to calculate the age of the patient
    when the earliest lab was recorded,
    which is a O(1) operation.

    For big-O analysis, we drop the constant factor,
    yeilding O(N2/N1) complexity.
    """
    patients = records[0]  # O(1)
    labs = records[1]  # O(1)
    # find the earliest lab date for the patient
    patient_labs = labs[patient_id]  # O(1)
    for i in range(len(patient_labs)):  # O(N2/N1)
        if i == 0:  # O(1)
            earliest_date = patient_labs[i]["LabDateTime"]  # O(1)
            earliest_time = datetime.datetime.strptime(
                str(earliest_date), "%Y-%m-%d %H:%M:%S.%f"
            )  # O(1)
        else:  # O(1)
            lab_date = patient_labs[i]["LabDateTime"]  # O(1)
            lab_time = datetime.datetime.strptime(  # O(1)
                str(lab_date), "%Y-%m-%d %H:%M:%S.%f"
            )
            if lab_time < earliest_time:  # O(1)
                earliest_time = lab_time  # O(1)
    # find the patient's date of birth
    date_of_birth = patients[patient_id]["PatientDateOfBirth"]  # O(1)
    birth = datetime.datetime.strptime(
        str(date_of_birth), "%Y-%m-%d %H:%M:%S.%f"
    )  # O(1)
    # calculate the age in years
    age_year = (earliest_time - birth).days / 365  # O(1)
    age_year_int = int(age_year)  # O(1)
    return age_year_int  # O(1)


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
    print(first_time(records, "1A8791E3-A61C-455A-8DEE-763EB90C9B2C"))
