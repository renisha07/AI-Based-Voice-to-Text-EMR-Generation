from database.db_connection import connect_database


def search_patient(patient_name):

    connection = connect_database()

    if connection is None:
        return None

    cursor = connection.cursor()

    query = """
    SELECT
        patient_name,
        age,
        gender,
        symptoms,
        diagnosis,
        prescription,
        advice,
        follow_up,
        blood_pressure,
        sugar_level

    FROM patients

    WHERE LOWER(patient_name)=LOWER(%s)

    ORDER BY patient_id DESC

    LIMIT 1
    """

    cursor.execute(query, (patient_name,))

    patient = cursor.fetchone()

    cursor.close()
    connection.close()

    return patient