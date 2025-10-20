# src/pre_authorization.py
import random
import logging
from datetime import datetime

# Mock database of patients, procedures, and pre-authorization requests
PATIENTS = {
    "12345": {"first_name": "John", "last_name": "Doe"},
    "67890": {"first_name": "Jane", "last_name": "Smith"},
}

PROCEDURES = {
    "MRI": {"name": "Magnetic Resonance Imaging", "cost": 1500},
    "CT Scan": {"name": "Computed Tomography Scan", "cost": 1200},
}

PRE_AUTHORIZATION_REQUESTS = {}

def submit_pre_authorization_request(patient_id, procedure_code):
    """
    Submits a mock pre-authorization request for a given patient and procedure.
    """
    if patient_id not in PATIENTS:
        logging.error(f"Patient with ID {patient_id} not found.")
        return None
    if procedure_code not in PROCEDURES:
        logging.error(f"Procedure with code {procedure_code} not found.")
        return None

    request_id = f"REQ-{random.randint(1000, 9999)}"
    status = random.choice(["approved", "denied", "pending"])

    PRE_AUTHORIZATION_REQUESTS[request_id] = {
        "patient_id": patient_id,
        "procedure_code": procedure_code,
        "status": status,
        "submitted_at": datetime.now().isoformat()
    }

    logging.info(f"Submitted pre-authorization request {request_id} for patient {patient_id} and procedure {procedure_code}. Status: {status}")
    return request_id

def check_pre_authorization_status(request_id):
    """
    Checks the status of a mock pre-authorization request.
    """
    if request_id not in PRE_AUTHORIZATION_REQUESTS:
        logging.error(f"Request with ID {request_id} not found.")
        return None

    request = PRE_AUTHORIZATION_REQUESTS[request_id]

    # Simulate a pending request getting approved or denied later
    if request["status"] == "pending":
        if random.random() > 0.5:
            request["status"] = "approved"
            logging.info(f"Request {request_id} has been approved.")
        else:
            request["status"] = "denied"
            logging.info(f"Request {request_id} has been denied.")

    return request["status"]

def get_request_details(request_id):
    """
    Retrieves the details of a pre-authorization request.
    """
    return PRE_AUTHORIZATION_REQUESTS.get(request_id)
