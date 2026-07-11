from datetime import datetime

def save_report(emr):

    filename = datetime.now().strftime("EMR_%d_%m_%Y_%H_%M_%S.txt")

    filepath = f"reports/{filename}"

    with open(filepath, "w") as file:
        file.write(emr)

    print(f"\n📁 EMR saved successfully:\n{filepath}")