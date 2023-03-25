"""Object-oriented EHR Analysis."""

import datetime


class Patient:
    """Patient class."""

    def __init__(
        self,
        id: str,
        gender: str,
        dob: str,
        race: str,
        lab_info: list[dict[str, str]],
    ) -> None:
        """Initiate patient class."""
        self.id = id
        self.gender = gender
        self.dob = dob
        self.race = race
        self.lab_info = lab_info

    def __str__(self) -> str:
        """Print patient info."""
        return "patient " + self.id + " info"

    def is_sick(self, lab_name: str, operator: str, value: float) -> bool:
        """Return a boolean indicating whether the patient is sick."""
        for i in range(len(self.lab_info)):
            if self.lab_info[i]["LabName"] == lab_name:
                labvalue = float(self.lab_info[i]["LabValue"])
                if operator == ">":
                    if labvalue > value:
                        return True
                elif operator == "<":
                    if labvalue < value:
                        return True
        return False

    @property
    def age(self) -> int:
        """Calculate the age in years of the given patient."""
        birth = datetime.datetime.strptime(
            str(self.dob), "%Y-%m-%d %H:%M:%S.%f"
        )
        age_year = (datetime.datetime.today() - birth).days / 365
        age_year_int = int(age_year)
        return age_year_int

    @property
    def earliest_admission(self) -> int:
        """Find the earliest admission date for the patient."""
        for i in range(len(self.lab_info)):
            if i == 0:
                earliest_date = self.lab_info[i]["LabDateTime"]
                earliest_time = datetime.datetime.strptime(
                    str(earliest_date), "%Y-%m-%d %H:%M:%S.%f"
                )
            else:
                lab_date = self.lab_info[i]["LabDateTime"]
                lab_time = datetime.datetime.strptime(
                    str(lab_date), "%Y-%m-%d %H:%M:%S.%f"
                )
                if lab_time < earliest_time:
                    earliest_time = lab_time
        birth = datetime.datetime.strptime(
            str(self.dob), "%Y-%m-%d %H:%M:%S.%f"
        )
        age_year = (earliest_time - birth).days / 365
        age_year_int = int(age_year)
        return age_year_int


class Lab:
    """Lab class."""

    def __init__(
        self,
        patient_id: str,
        lab_name: str,
        lab_value: str,
        lab_units: str,
        lab_date: str,
    ):
        """Initiate lab class."""
        self.patient_id = patient_id
        self.lab_name = lab_name
        self.lab_value = lab_value
        self.lab_units = lab_units
        self.lab_date = lab_date

    def __str__(self) -> str:
        """Print lab info."""
        return "lab " + self.lab_name + " info for patient " + self.patient_id


def parse_data(
    patient_filename: str, lab_filename: str
) -> tuple[list[Patient], list[Lab]]:
    """Parse the patient and lab data files and return a tuple of lists."""
    patient_list = []
    lab_list = []
    with open(patient_filename, "r", encoding="utf-8-sig") as patient_file:
        patient_data = patient_file.readlines()
        for lines in patient_data[1:]:
            patient_info = lines.strip().split("\t")
            patient = Patient(
                patient_info[0],
                patient_info[1],
                patient_info[2],
                patient_info[3],
                [],
            )
            patient_list.append(patient)
    with open(lab_filename, "r", encoding="utf-8-sig") as lab_file:
        lab_data = lab_file.readlines()
        for lines in lab_data[1:]:
            lab_info = lines.strip().split("\t")
            lab = Lab(
                lab_info[0],
                lab_info[1],
                lab_info[2],
                lab_info[3],
                lab_info[4],
            )
            lab_list.append(lab)
    for i in range(len(patient_list)):
        for j in range(len(lab_list)):
            if patient_list[i].id == lab_list[j].patient_id:
                patient_list[i].lab_info.append(
                    {
                        "PatientID": lab_list[j].patient_id,
                        "LabName": lab_list[j].lab_name,
                        "LabValue": lab_list[j].lab_value,
                        "LabUnits": lab_list[j].lab_units,
                        "LabDateTime": lab_list[j].lab_date,
                    }
                )
    return patient_list, lab_list


if __name__ == "__main__":
    patient1 = Patient(
        id="1",
        gender="male",
        dob="1950-01-01 00:00:00.000000",
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
    print(patient1)
    print(patient1.is_sick("URINALYSIS: RED BLOOD CELLS", ">", 1))
    print(patient1.age)
    print(patient1.earliest_admission)
