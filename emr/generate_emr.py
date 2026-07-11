from datetime import datetime

def generate_emr(patient):

    emr = f"""

===========================================
        ELECTRONIC MEDICAL RECORD
===========================================

Patient Name : {patient['patient_name']}
Age          : {patient['age']}
Gender       : {patient['gender']}

Symptoms
---------
{patient['symptoms'] if patient['symptoms'] else "Not Available"}

Diagnosis
---------
{patient['diagnosis'] if patient['diagnosis'] else "Not Available"}

Prescription
------------
Medicine   : {patient['medicine'] if patient['medicine'] else "Not Available"}
Dosage     : {patient['dosage'] if patient['dosage'] else "Not Available"}
Frequency  : {patient['frequency'] if patient['frequency'] else "Not Available"}
Duration   : {patient['duration'] if patient['duration'] else "Not Available"}

Advice
------
{patient['advice'] if patient['advice'] else "Not Available"}

Follow-up
---------
{patient['follow_up'] if patient['follow_up'] else "Not Available"}

Blood Pressure
--------------
{patient['blood_pressure'] if patient['blood_pressure'] else "Not Available"}

Sugar Level
-----------
{patient['sugar_level'] if patient['sugar_level'] else "Not Available"}

Visit Date
----------
{datetime.today().strftime("%d-%m-%Y")}

===========================================

"""

    print("\n📄 Generated EMR:\n")
    print(emr)

    return emr