"""Object-oriented EHR Analysis."""

import sqlite3
import pickle
import datetime
from dataclasses import dataclass

connection = sqlite3.connect("ehr_data.db")


@dataclass
class Lab:
    """Lab class for lab information."""

    patient_id: str
    cursor = connection.cursor()

    @property
    def lab_name(self) -> str:
        """Return the lab name."""
        self.cursor.execute(
            "SELECT lab_name FROM Labs WHERE patient_id = ?",
            (self.patient_id,),
        )
        return self.cursor.fetchone()[0]

    @property
    def lab_value(self) -> str:
        """Return the lab value."""
        self.cursor.execute(
            "SELECT lab_value FROM Labs WHERE patient_id = ?",
            (self.patient_id,),
        )
        return self.cursor.fetchone()[0]

    @property
    def lab_units(self) -> str:
        """Return the lab units."""
        self.cursor.execute(
            "SELECT lab_units FROM Labs WHERE patient_id = ?",
            (self.patient_id,),
        )
        return self.cursor.fetchone()[0]

    @property
    def lab_date(self) -> str:
        """Return the lab date."""
        self.cursor.execute(
            "SELECT lab_date FROM Labs WHERE patient_id = ?",
            (self.patient_id,),
        )
        return self.cursor.fetchone()[0]

    def __str__(self) -> str:
        """Print lab info."""
        return "lab " + self.lab_name + " info for patient " + self.patient_id


@dataclass
class Patient:
    """Patient class for patient information."""

    id: str
    cursor = connection.cursor()

    @property
    def gender(self) -> str:
        """Return the patient gender."""
        self.cursor.execute(
            "SELECT gender FROM Patients WHERE id = ?",
            (self.id,),
        )
        return self.cursor.fetchone()[0]

    @property
    def dob(self) -> str:
        """Return the patient date of birth."""
        self.cursor.execute(
            "SELECT dob FROM Patients WHERE id = ?",
            (self.id,),
        )
        return self.cursor.fetchone()[0]

    @property
    def race(self) -> str:
        """Return the patient race."""
        self.cursor.execute(
            """SELECT race FROM Patients WHERE id = ?""",
            (self.id,),
        )
        return self.cursor.fetchone()[0]

    @property
    def lab_info(self) -> list[Lab]:
        """Return the lab info for the patient."""
        self.cursor.execute(
            "SELECT lab_info FROM Patients WHERE id = ?",
            (self.id,),
        )
        lab_info = self.cursor.fetchone()[0]
        lab_info = pickle.loads(lab_info)
        return lab_info

    def __str__(self) -> str:
        """Print patient info."""
        return "patient " + self.id + " info"

    def is_sick(self, lab_name: str, operator: str, value: float) -> bool:
        """Return a boolean indicating whether the patient is sick."""
        for i in range(len(self.lab_info)):
            if self.lab_info[i].lab_name == lab_name:
                labvalue = float(self.lab_info[i].lab_value)
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
                earliest_date = self.lab_info[i].lab_date
                earliest_time = datetime.datetime.strptime(
                    str(earliest_date), "%Y-%m-%d %H:%M:%S.%f"
                )
            else:
                lab_date = self.lab_info[i].lab_date
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


def parse_data(
    patient_filename: str, lab_filename: str
) -> tuple[list[Patient], list[Lab]]:
    """Parse the patient and lab data files and return a tuple of lists."""
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS Labs")
    cursor.execute("DROP TABLE IF EXISTS Patients")

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Labs(patient_id VARCHAR, lab_name VARCHAR,"
        "lab_value VARCHAR, lab_units VARCHAR, lab_date VARCHAR)"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Patients(id VARCHAR PRIMARY KEY,"
        "gender VARCHAR, dob VARCHAR, race VARCHAR, lab_info BLOB)"
    )
    patient_list = []
    lab_list = []

    with open(lab_filename, "r", encoding="utf-8-sig") as lab_file:
        lab_data = lab_file.readlines()
        for lines in lab_data[1:]:
            lab_info = lines.strip().split("\t")
            lab_list.append(Lab(lab_info[0]))
            cursor.execute(
                "INSERT INTO Labs VALUES (?, ?, ?, ?, ?)",
                (
                    lab_info[0],
                    lab_info[1],
                    lab_info[2],
                    lab_info[3],
                    lab_info[4],
                ),
            )

    with open(patient_filename, "r", encoding="utf-8-sig") as patient_file:
        patient_data = patient_file.readlines()
        for lines in patient_data[1:]:
            patient_info = lines.strip().split("\t")
            lab_info = []
            for i in range(len(lab_list)):
                if lab_list[i].patient_id == patient_info[0]:
                    lab_info.append(lab_list[i])
                patient_info = patient_info + [lab_info]
            patient_list.append(Patient(patient_info[0]))
            cursor.execute(
                "INSERT INTO Patients VALUES (?, ?, ?, ?, ?)",
                (
                    patient_info[0],
                    patient_info[1],
                    patient_info[2],
                    patient_info[3],
                    pickle.dumps(patient_info[4]),
                ),
            )

    connection.commit()
    return patient_list, lab_list
