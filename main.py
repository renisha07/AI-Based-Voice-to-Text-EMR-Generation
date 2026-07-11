from audio.speech_to_text import listen
from nlp.extractor import extract_information

from emr.generate_emr import generate_emr

from database.save_patient import save_patient

from pdf.generate_pdf import generate_pdf


# ==========================================
# MAIN WORKFLOW
# ==========================================

def process_consultation():

    try:
        print("===================================")
        print("AI Voice-to-Text EMR Started")
        print("===================================")

        # -----------------------------
        # Record Voice
        # -----------------------------

        text = listen()

        if text == "":
            print("No speech detected.")
            return

        print("\nRecognized Text:\n")
        print(text)

        # -----------------------------
        # Extract Information
        # -----------------------------

        patient = extract_information(text)

        print("\nExtracted Information:\n")
        print(patient)

        # -----------------------------
        # Generate EMR
        # -----------------------------

        emr = generate_emr(patient)

        # -----------------------------
        # Save Database
        # -----------------------------

        save_patient(patient)

        # -----------------------------
        # Generate PDF
        # -----------------------------

        generate_pdf(patient)

        print("\n===================================")
        print("PROJECT COMPLETED SUCCESSFULLY")
        print("===================================")

    except Exception as e:

        print("\nError:", e)


# ==========================================
# START PROGRAM
# ==========================================

if __name__ == "__main__":
    process_consultation()