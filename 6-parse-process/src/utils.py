# src/utils.py

def format_patient_name(first_name, last_name):
    """
    Formats the patient's name.
    """
    return f"{last_name}, {first_name}"

def log_message(message):
    """
    Logs a message to the console.
    """
    print(f"[INFO] {message}")
