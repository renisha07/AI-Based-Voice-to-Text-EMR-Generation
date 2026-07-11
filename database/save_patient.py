from datetime import datetime
from database.db_connection import connect_database


def save_patient(patient):

    connection = connect_database()

    if connection is None:
        return

    cursor = connection.cursor()

    prescription = f"""
Medicine : {patient['medicine']}
Dosage : {patient['dosage']}
Frequency : {patient['frequency']}
Duration : {patient['duration']}
"""

    query = """
    INSERT INTO patients
    (
        patient_name,
        age,
        gender,
        symptoms,
        diagnosis,
        prescription,
        visit_date,
        advice,
        follow_up,
        blood_pressure,
        sugar_level
    )

    VALUES
    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    values = (

    patient["patient_name"] if patient["patient_name"] else "Unknown",

    int(patient["age"]) if str(patient["age"]).isdigit() else None,

    patient["gender"] if patient["gender"] else "Unknown",

    patient["symptoms"],

    patient["diagnosis"],

    prescription,

    datetime.today().date(),

    patient["advice"],

    patient["follow_up"],

    patient["blood_pressure"],

    patient["sugar_level"]

)


    print("\n========== SAVING TO DATABASE ==========")
    print("Medicine   :", patient["medicine"])
    print("Dosage     :", patient["dosage"])
    print("Frequency  :", patient["frequency"])
    print("Duration   :", patient["duration"])
    print("Prescription String:")
    print(prescription)
    print("========================================\n")

    cursor.execute(query, values)

    connection.commit()

    cursor.close()

    connection.close()

    print("✅ Patient saved successfully.")