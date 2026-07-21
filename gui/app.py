import ttkbootstrap as ttk
import threading
import time
from ttkbootstrap.constants import *
from tkinter import END, Text
from tkinter import messagebox

from audio.speech_to_text import listen
from nlp.extractor import extract_information
from database.save_patient import save_patient
from pdf.generate_pdf import generate_pdf
from database.search_patient import search_patient
# ==========================================
# Global Variable
# ==========================================

patient_data = {}

# ==========================================
# Functions
# ==========================================

def record_consultation():

    global patient_data

    status_label.config(text="🎤 Recording...")
    record_status.config(text="🎤 Listening...")

    progress.start()

    app.update()

    text = listen()

    progress.stop()

    if not text:
        status_label.config(text="❌ No Speech Detected")
        return

    patient_data = extract_information(text)

    fill_form(patient_data)

    status_label.config(text="✅ Consultation Completed")

    record_status.config(text="✅ Ready")
def search_existing_patient():

    patient_name = entry_search.get().strip()

    if patient_name == "":
        messagebox.showwarning(
            "Warning",
            "Please enter a patient name."
        )
        return

    patient = search_patient(patient_name)

    if patient is None:
        messagebox.showerror(
            "Not Found",
            "Patient not found."
        )
        return

    prescription = patient[5]

    medicine = ""
    dosage = ""
    frequency = ""
    duration = ""

    if prescription:
        for line in prescription.splitlines():

            if line.startswith("Medicine"):
                medicine = line.split(":",1)[1].strip()

            elif line.startswith("Dosage"):
                dosage = line.split(":",1)[1].strip()

            elif line.startswith("Frequency"):
                frequency = line.split(":",1)[1].strip()

            elif line.startswith("Duration"):
                duration = line.split(":",1)[1].strip()

    data = {

        "patient_name": patient[0],
        "age": patient[1],
        "gender": patient[2],
        "symptoms": patient[3],
        "diagnosis": patient[4],
        "medicine": medicine,
        "dosage": dosage,
        "frequency": frequency,
        "duration": duration,
        "advice": patient[6],
        "follow_up": patient[7],
        "blood_pressure": patient[8],
        "sugar_level": patient[9]

    }

    fill_form(data)

    messagebox.showinfo(
        "Success",
        "Patient loaded successfully."
    )

def fill_form(data):

    entry_name.delete(0, END)
    entry_name.insert(0, data["patient_name"])

    entry_age.delete(0, END)
    entry_age.insert(0, data["age"])

    entry_gender.set(data["gender"])

    entry_bp.delete(0, END)
    entry_bp.insert(0, data["blood_pressure"])

    entry_sugar.delete(0, END)
    entry_sugar.insert(0, data["sugar_level"])

    entry_medicine.delete(0, END)
    entry_medicine.insert(0, data["medicine"])

    entry_dosage.delete(0, END)
    entry_dosage.insert(0, data["dosage"])

    entry_frequency.delete(0, END)
    entry_frequency.insert(0, data["frequency"])

    entry_duration.delete(0, END)
    entry_duration.insert(0, data["duration"])

    entry_followup.delete(0, END)
    entry_followup.insert(0, data["follow_up"])

    txt_symptoms.delete("1.0", END)
    txt_symptoms.insert("1.0", data["symptoms"])

    txt_diagnosis.delete("1.0", END)
    txt_diagnosis.insert("1.0", data["diagnosis"])

    txt_advice.delete("1.0", END)
    txt_advice.insert("1.0", data["advice"])


def save_database():

    global patient_data

    if not patient_data:
        messagebox.showwarning(
            "Warning",
            "Please record a consultation first."
        )
        return

    save_patient(patient_data)

    messagebox.showinfo(
        "Success",
        "Patient saved successfully."
    )


def generate_pdf_report():

    global patient_data

    if not patient_data:
        messagebox.showwarning(
            "Warning",
            "Please record a consultation first."
        )
        return

    generate_pdf(patient_data)

    messagebox.showinfo(
        "Success",
        "PDF Generated Successfully."
    )


def clear_form():

    global patient_data

    patient_data = {}

    entries = [
        entry_name,
        entry_age,
        entry_bp,
        entry_sugar,
        entry_medicine,
        entry_dosage,
        entry_frequency,
        entry_duration,
        entry_followup
    ]

    for item in entries:
        item.delete(0, END)

    entry_gender.set("")

    txt_symptoms.delete("1.0", END)
    txt_diagnosis.delete("1.0", END)
    txt_advice.delete("1.0", END)

    status_label.config(text="🟢 Status : Ready")

    record_status.config(text="🟢 Ready to Record")


# ==========================================
# Main Window
# ==========================================

app = ttk.Window(themename="flatly")

app.title("AI-Based Voice-to-Text EMR Generation")

app.state("zoomed")

app.minsize(1366,768)

# ==========================================
# Header
# ==========================================

header = ttk.Frame(app, bootstyle="primary")
header.pack(fill=X)

title = ttk.Label(
    header,
    text="🏥 AI-Based Voice-to-Text EMR Generation",
    font=("Segoe UI", 20, "bold"),
    bootstyle="inverse-primary"
)
title.pack(pady=10)

# ==========================================
# Status Bar
# ==========================================

status_frame = ttk.Frame(app)
status_frame.pack(fill=X, padx=20, pady=10)

status_label = ttk.Label(
    status_frame,
    text="🟢 Status : Ready",
    font=("Segoe UI", 12, "bold"),
    bootstyle="success"
)

status_label.pack(anchor=W)
# ==========================================
# Search Existing Patient
# ==========================================

search_frame = ttk.Frame(app)

search_frame.pack(fill=X, padx=20, pady=5)

entry_search = ttk.Entry(search_frame, width=50)
entry_search.pack(side=LEFT, padx=10, pady=10)

ttk.Button(
    search_frame,
    text="Search",
    bootstyle="primary",
    command=search_existing_patient
).pack(side=LEFT, padx=10)
# ==========================================
# Voice Recording
# ==========================================

voice_card = ttk.Labelframe(
    app,
    text="🎤 Voice Recording",
    bootstyle="info"
)

voice_card.pack(fill=X, padx=20, pady=3)

record_status = ttk.Label(
    voice_card,
    text="🟢 Ready to Record",
    font=("Segoe UI", 11, "bold"),
    bootstyle="success"
)

record_status.grid(row=0, column=0, padx=20, pady=15)

btn_record = ttk.Button(
    voice_card,
    text="🎤 Start Recording",
    bootstyle="success",
    width=20,
    command=record_consultation
)

btn_record.grid(row=0, column=1, padx=10)

btn_stop = ttk.Button(
    voice_card,
    text="⏹ Stop",
    bootstyle="danger",
    width=15
)

btn_stop.grid(row=0, column=2, padx=10)

progress = ttk.Progressbar(
    voice_card,
    length=250,
    mode="indeterminate",
    bootstyle="success-striped"
)

progress.grid(row=0, column=3, padx=20)

timer_label = ttk.Label(
    voice_card,
    text="00:00",
    font=("Consolas", 14, "bold")
)

timer_label.grid(row=0, column=4, padx=10)
# ==========================================
# Main Frames
# ==========================================

content = ttk.Frame(app)
content.pack(fill=X, padx=15, pady=5)

left = ttk.Frame(content)
left.pack(side=LEFT, fill=X, expand=True, padx=(0,10))

right = ttk.Frame(content)
right.pack(side=RIGHT, fill=X, expand=True, padx=(10,0))

# ==========================================
# Patient Information
# ==========================================

patient_card = ttk.Labelframe(
    left,
    text="👤 Patient Information",
    bootstyle="primary"
)

patient_card.pack(fill=X, pady=5)

ttk.Label(patient_card, text="Patient Name").grid(row=0,column=0,padx=10,pady=5,sticky=W)
entry_name = ttk.Entry(patient_card,width=35)
entry_name.grid(row=0,column=1,padx=10,pady=5)

ttk.Label(patient_card,text="Age").grid(row=1,column=0,padx=10,pady=5,sticky=W)
entry_age = ttk.Entry(patient_card,width=20)
entry_age.grid(row=1,column=1,padx=10,pady=5)

ttk.Label(patient_card,text="Gender").grid(row=2,column=0,padx=10,pady=5,sticky=W)
entry_gender = ttk.Combobox(
    patient_card,
    values=["Male","Female","Other"],
    state="readonly",
    width=18
)
entry_gender.grid(row=2,column=1,padx=10,pady=5)

ttk.Label(patient_card,text="Blood Pressure").grid(row=3,column=0,padx=10,pady=5,sticky=W)
entry_bp = ttk.Entry(patient_card,width=20)
entry_bp.grid(row=3,column=1,padx=10,pady=5)

ttk.Label(patient_card,text="Sugar Level").grid(row=4,column=0,padx=10,pady=5,sticky=W)
entry_sugar = ttk.Entry(patient_card,width=20)
entry_sugar.grid(row=4,column=1,padx=10,pady=5)

# ==========================================
# Prescription
# ==========================================

prescription_card = ttk.Labelframe(
    right,
    text="💊 Prescription",
    bootstyle="warning"
)

prescription_card.pack(fill=X, pady=5)

ttk.Label(prescription_card,text="Medicine").grid(row=0,column=0,padx=10,pady=5,sticky=W)
entry_medicine = ttk.Entry(prescription_card,width=35)
entry_medicine.grid(row=0,column=1,padx=10,pady=5)

ttk.Label(prescription_card,text="Dosage").grid(row=1,column=0,padx=10,pady=5,sticky=W)
entry_dosage = ttk.Entry(prescription_card,width=20)
entry_dosage.grid(row=1,column=1,padx=10,pady=5)

ttk.Label(prescription_card,text="Frequency").grid(row=2,column=0,padx=10,pady=5,sticky=W)
entry_frequency = ttk.Entry(prescription_card,width=20)
entry_frequency.grid(row=2,column=1,padx=10,pady=5)

ttk.Label(prescription_card,text="Duration").grid(row=3,column=0,padx=10,pady=5,sticky=W)
entry_duration = ttk.Entry(prescription_card,width=20)
entry_duration.grid(row=3,column=1,padx=10,pady=5)

ttk.Label(prescription_card,text="Follow-up").grid(row=4,column=0,padx=10,pady=5,sticky=W)
entry_followup = ttk.Entry(prescription_card,width=20)
entry_followup.grid(row=4,column=1,padx=10,pady=5)
# ==========================================
# Clinical Details
# ==========================================

clinical_card = ttk.Labelframe(
    app,
    text="🩺 Clinical Details",
    bootstyle="success"
)

clinical_card.pack(fill=X, padx=20, pady=5)

# Symptoms

ttk.Label(
    clinical_card,
    text="Symptoms"
).grid(row=0, column=0, padx=10, pady=5, sticky="nw")

txt_symptoms = Text(
    clinical_card,
    width=80,
    height=1
)

txt_symptoms.grid(row=0, column=1, padx=10, pady=5)

# Diagnosis

ttk.Label(
    clinical_card,
    text="Diagnosis"
).grid(row=1, column=0, padx=10, pady=5, sticky="nw")

txt_diagnosis = Text(
    clinical_card,
    width=80,
    height=1
)

txt_diagnosis.grid(row=1, column=1, padx=10, pady=5)

# Advice

ttk.Label(
    clinical_card,
    text="Advice"
).grid(row=2, column=0, padx=10, pady=5, sticky="nw")

txt_advice = Text(
    clinical_card,
    width=80,
    height=1
)

txt_advice.grid(row=2, column=1, padx=10, pady=5)

# ==========================================
# Action Buttons
# ==========================================

button_frame = ttk.Frame(app)
button_frame.pack(fill=X, padx=20, pady=3)

ttk.Button(
    button_frame,
    text="💾 Save Database",
    bootstyle="primary",
    width=18,
    command=save_database
).pack(side=LEFT, padx=10)

ttk.Button(
    button_frame,
    text="📄 Generate PDF",
    bootstyle="warning",
    width=18,
   command=generate_pdf_report
).pack(side=LEFT, padx=10)
ttk.Button(
    button_frame,
    text="🗑 Clear",
    bootstyle="secondary",
    width=15,
    command=clear_form
).pack(side=LEFT, padx=10)
ttk.Button(
    button_frame,
    text="❌ Exit",
    bootstyle="danger",
    width=15,
    command=app.destroy
).pack(side=RIGHT, padx=10)
# ==========================================
# Run GUI
# ==========================================

app.mainloop()