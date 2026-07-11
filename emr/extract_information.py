import re

def extract_information(text):

    data = {
        "patient_name": "",
        "age": "",
        "gender": "",
        "symptoms": "",
        "medicine": "",
        "diagnosis": "",
        "advice": "",
        "follow_up": "",
        "blood_pressure": "",
        "sugar_level": "",
        "dosage": "",
        "frequency": "",
        "duration": ""
    }

    text_lower = text.lower()

    # ---------------------------------
    # Patient Name
    # ---------------------------------

    name_match = re.search(r'patient\s+name\s+([A-Za-z]+)', text, re.IGNORECASE)

    if not name_match:
        name_match = re.search(r'patient\s+([A-Za-z]+)', text, re.IGNORECASE)

    if not name_match:
        name_match = re.search(r'name\s+([A-Za-z]+)', text, re.IGNORECASE)

    if name_match:
        data["patient_name"] = name_match.group(1)

    # ---------------------------------
    # Age
    # ---------------------------------

    age = re.search(r'\b(\d{1,3})\b', text)

    if age:
        data["age"] = age.group(1)

    # ---------------------------------
    # Gender
    # ---------------------------------

    if any(word in text_lower for word in ["male", "mail"]):
        data["gender"] = "Male"

    elif any(word in text_lower for word in ["female", "femail"]):
        data["gender"] = "Female"

    # ---------------------------------
    # Symptoms
    # ---------------------------------

    symptom_list = [
        "fever",
        "cough",
        "cold",
        "headache",
        "vomiting",
        "diabetes",
        "pain",
        "body pain",
        "sore throat",
        "fatigue"
    ]

    symptoms = []

    for symptom in symptom_list:
        if symptom in text_lower:
            symptoms.append(symptom)

    data["symptoms"] = ", ".join(symptoms)

    # ---------------------------------
    # Medicines
    # ---------------------------------

    medicine_list = [
        "paracetamol",
        "crocin",
        "dolo",
        "azithromycin",
        "amoxicillin",
        "cetirizine"
    ]

    medicines = []

    for medicine in medicine_list:
        if medicine in text_lower:
            medicines.append(medicine.title())

    data["medicine"] = ", ".join(medicines)

    # ---------------------------------
    # Diagnosis
    # ---------------------------------

    diagnosis_list = [
        "viral fever",
        "bacterial infection",
        "diabetes",
        "hypertension",
        "migraine",
        "common cold",
        "food poisoning",
        "dengue",
        "typhoid"
    ]

    for diagnosis in diagnosis_list:
        if diagnosis in text_lower:
            data["diagnosis"] = diagnosis
            break

    # ---------------------------------
    # Advice
    # ---------------------------------

    if re.search(r'drink.*water', text_lower):
        data["advice"] = "Drink Plenty of Water"

    elif re.search(r'take.*rest', text_lower):
        data["advice"] = "Take Complete Bed Rest"

    elif re.search(r'avoid.*oily', text_lower):
        data["advice"] = "Avoid Oily Food"

    elif re.search(r'eat.*healthy', text_lower):
        data["advice"] = "Eat Healthy Diet"

    elif re.search(r'fluids', text_lower):
        data["advice"] = "Take Enough Fluids"

    # ---------------------------------
    # Follow Up
    # ---------------------------------

    follow = re.search(r'follow\s*up.*?(\d+)\s*days?', text_lower)

    if follow:
        data["follow_up"] = follow.group(1) + " Days"

    # ---------------------------------
    # Blood Pressure
    # ---------------------------------

    bp = re.search(r'(\d{2,3}/\d{2,3})', text)

    if bp:
        data["blood_pressure"] = bp.group(1)

    # ---------------------------------
    # Sugar Level
    # ---------------------------------

    sugar = re.search(
        r'(blood\s*)?sugar(\s*level)?(\s*is)?\s*(\d+)',
        text_lower
    )

    if sugar:
        data["sugar_level"] = sugar.group(4) + " mg/dL"

    # ---------------------------------
    # Dosage
    # ---------------------------------

    dosage = re.search(r'(\d+\s*mg)', text_lower)

    if dosage:
        data["dosage"] = dosage.group(1).upper()

    # ---------------------------------
    # Frequency
    # ---------------------------------

    if (
        "once daily" in text_lower
        or "daily once" in text_lower
        or "once a day" in text_lower
        or "one time daily" in text_lower
    ):
        data["frequency"] = "Once Daily"

    elif (
        "twice daily" in text_lower
        or "daily twice" in text_lower
        or "twice a day" in text_lower
        or "two times daily" in text_lower
        or "2 times daily" in text_lower
        or "two times a day" in text_lower
    ):
        data["frequency"] = "Twice Daily"

    elif (
        "three times daily" in text_lower
        or "thrice daily" in text_lower
        or "3 times daily" in text_lower
        or "three times a day" in text_lower
    ):
        data["frequency"] = "Three Times Daily"

    elif (
        "morning and night" in text_lower
        or "morning & night" in text_lower
        or "morning evening" in text_lower
    ):
        data["frequency"] = "Morning & Night"

    # ---------------------------------
    # Duration
    # ---------------------------------

    duration = re.search(r'for\s+(\d+)\s*days?', text_lower)

    if duration:
        data["duration"] = duration.group(1) + " Days"

    return data