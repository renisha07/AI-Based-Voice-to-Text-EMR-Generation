import re


def extract_information(text):
    """
    Extract patient information from speech text.
    """

    patient = {
        "patient_name": "",
        "age": "",
        "gender": "",
        "symptoms": "",
        "diagnosis": "",
        "medicine": "",
        "dosage": "",
        "frequency": "",
        "duration": "",
        "advice": "",
        "follow_up": "",
        "blood_pressure": "",
        "sugar_level": ""
    }

    text_lower = text.lower()

    # ---------------------------------
    # Patient Name
    # ---------------------------------

    name_patterns = [
        r"patient\s+([A-Za-z]+)",
        r"name\s+is\s+([A-Za-z]+)",
        r"patient name\s+([A-Za-z]+)"
    ]

    for pattern in name_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            patient["patient_name"] = match.group(1).title()
            break

    # ---------------------------------
    # Age
    # ---------------------------------

    age_patterns = [
        r"age\s*(\d+)",
        r"(\d+)\s*years"
    ]

    for pattern in age_patterns:
        match = re.search(pattern, text_lower)
        if match:
            patient["age"] = match.group(1)
            break

    # ---------------------------------
    # Gender
    # ---------------------------------

    if "female" in text_lower:
        patient["gender"] = "Female"

    elif "male" in text_lower or "mail" in text_lower:
        patient["gender"] = "Male"

    # ---------------------------------
    # Blood Pressure
    # ---------------------------------

    bp = re.search(r"(\d{2,3}/\d{2,3})", text)

    if bp:
        patient["blood_pressure"] = bp.group(1)

    # ---------------------------------
    # Sugar Level
    # ---------------------------------

    sugar = re.search(r"sugar\s*(\d+)", text_lower)

    if sugar:
        patient["sugar_level"] = sugar.group(1)

    # ---------------------------------
    # Symptoms
    # ---------------------------------

    symptoms_list = [

        "fever",
        "cough",
        "cold",
        "headache",
        "vomiting",
        "body pain",
        "stomach pain",
        "chest pain",
        "weakness",
        "dizziness",
        "diabetes"

    ]

    found = []

    for symptom in symptoms_list:

        if symptom in text_lower:
            found.append(symptom)

    patient["symptoms"] = ", ".join(found)

    # ---------------------------------
    # Diagnosis
    # ---------------------------------

    if "viral fever" in text_lower:
        patient["diagnosis"] = "Viral Fever"

    elif "diabetes" in text_lower:
        patient["diagnosis"] = "Diabetes"

    elif "cold" in text_lower:
        patient["diagnosis"] = "Common Cold"

    elif patient["symptoms"]:
        patient["diagnosis"] = "General Checkup"

    # ---------------------------------
    # Medicine
    # ---------------------------------

    medicines = [

        "paracetamol",
        "crocin",
        "dolo",
        "cetirizine",
        "azithromycin",
        "metformin",
        "amoxicillin"

    ]

    for med in medicines:

        if med in text_lower:
            patient["medicine"] = med.title()
            break

    # ---------------------------------
    # Dosage
    # ---------------------------------

    dose = re.search(r"(\d+\s*mg)", text_lower)

    if dose:
        patient["dosage"] = dose.group(1)

    # ---------------------------------
    # Frequency
    # ---------------------------------

    if "twice daily" in text_lower or "twice a day" in text_lower:
        patient["frequency"] = "Twice Daily"

    elif "once daily" in text_lower or "once a day" in text_lower:
        patient["frequency"] = "Once Daily"

    elif "three times daily" in text_lower or "three times a day" in text_lower:
        patient["frequency"] = "Three Times Daily"

    # ---------------------------------
    # Duration
    # ---------------------------------

    duration_patterns = [

        r"for\s*(\d+)\s*days",
        r"(\d+)\s*days"

    ]

    for pattern in duration_patterns:

        duration = re.search(pattern, text_lower)

        if duration:
            patient["duration"] = duration.group(1) + " Days"
            break

    # ---------------------------------
    # Advice
    # ---------------------------------

    if (
        "drink water" in text_lower
        or "drink plenty of water" in text_lower
        or "drink a plenty of water" in text_lower
    ):

        patient["advice"] = "Drink Plenty of Water"

    elif (
        "take rest" in text_lower
        or "take proper rest" in text_lower
        or "bed rest" in text_lower
    ):

        patient["advice"] = "Take Proper Rest"

    # ---------------------------------
    # Follow-up
    # ---------------------------------

    follow_patterns = [

        r"follow up after\s*(\d+)\s*days",
        r"follow.?up.?(\d+)\s*days",
        r"after\s*(\d+)\s*days"

    ]

    for pattern in follow_patterns:

        follow = re.search(pattern, text_lower)

        if follow:
            patient["follow_up"] = follow.group(1) + " Days"
            break

    return patient