import os
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(patient):

    # Create reports folder if it doesn't exist
    os.makedirs("reports", exist_ok=True)

    filename = datetime.now().strftime("reports/EMR_%d_%m_%Y_%H_%M_%S.pdf")

    doc = SimpleDocTemplate(filename, pagesize=A4)

    styles = getSampleStyleSheet()

    story = []

    # ----------------------------------------
    # Hospital Name
    # ----------------------------------------

    story.append(Paragraph("<b><font size=18> BEL HEALTH CARE </font></b>", styles["Title"]))

    story.append(Paragraph("<b>Electronic Medical Record</b>", styles["Heading2"]))

    story.append(Spacer(1, 20))

    # ----------------------------------------
    # Patient Details
    # ----------------------------------------

    story.append(Paragraph(f"<b>Patient Name :</b> {patient['patient_name']}", styles["Normal"]))
    story.append(Paragraph(f"<b>Age :</b> {patient['age']}", styles["Normal"]))
    story.append(Paragraph(f"<b>Gender :</b> {patient['gender']}", styles["Normal"]))

    story.append(
        Paragraph(
            f"<b>Visit Date :</b> {datetime.now().strftime('%d-%m-%Y')}",
            styles["Normal"],
        )
    )

    story.append(Spacer(1, 15))

    # ----------------------------------------
    # Symptoms
    # ----------------------------------------

    story.append(Paragraph("<b>Symptoms</b>", styles["Heading2"]))
    story.append(
        Paragraph(
            patient["symptoms"] if patient["symptoms"] else "Not Available",
            styles["Normal"],
        )
    )

    story.append(Spacer(1, 10))

    # ----------------------------------------
    # Diagnosis
    # ----------------------------------------

    story.append(Paragraph("<b>Diagnosis</b>", styles["Heading2"]))
    story.append(
        Paragraph(
            patient["diagnosis"] if patient["diagnosis"] else "Not Available",
            styles["Normal"],
        )
    )

    story.append(Spacer(1, 10))

    # ----------------------------------------
    # Prescription
    # ----------------------------------------

    story.append(Paragraph("<b>Prescription</b>", styles["Heading2"]))

    story.append(
        Paragraph(
            f"Medicine : {patient['medicine'] if patient['medicine'] else 'Not Available'}",
            styles["Normal"],
        )
    )

    story.append(
        Paragraph(
            f"Dosage : {patient['dosage'] if patient['dosage'] else 'Not Available'}",
            styles["Normal"],
        )
    )

    story.append(
        Paragraph(
            f"Frequency : {patient['frequency'] if patient['frequency'] else 'Not Available'}",
            styles["Normal"],
        )
    )

    story.append(
        Paragraph(
            f"Duration : {patient['duration'] if patient['duration'] else 'Not Available'}",
            styles["Normal"],
        )
    )

    story.append(Spacer(1, 10))

    # ----------------------------------------
    # Advice
    # ----------------------------------------

    story.append(Paragraph("<b>Advice</b>", styles["Heading2"]))

    story.append(
        Paragraph(
            patient["advice"] if patient["advice"] else "Not Available",
            styles["Normal"],
        )
    )

    story.append(Spacer(1, 10))

    # ----------------------------------------
    # Follow Up
    # ----------------------------------------

    story.append(Paragraph("<b>Follow-up</b>", styles["Heading2"]))

    story.append(
        Paragraph(
            patient["follow_up"] if patient["follow_up"] else "Not Available",
            styles["Normal"],
        )
    )

    story.append(Spacer(1, 10))

    # ----------------------------------------
    # Vitals
    # ----------------------------------------

    story.append(Paragraph("<b>Vitals</b>", styles["Heading2"]))

    story.append(
        Paragraph(
            f"Blood Pressure : {patient['blood_pressure'] if patient['blood_pressure'] else 'Not Available'}",
            styles["Normal"],
        )
    )

    story.append(
        Paragraph(
            f"Sugar Level : {patient['sugar_level'] if patient['sugar_level'] else 'Not Available'}",
            styles["Normal"],
        )
    )

    # ----------------------------------------
    # Build PDF
    # ----------------------------------------

    doc.build(story)

    print(f"\n📄 PDF Generated Successfully!\n{filename}")