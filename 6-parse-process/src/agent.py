# src/agent.py
import logging
import time
from src.utils import setup_logging, load_config
from src.pre_authorization import (
    submit_pre_authorization_request,
    check_pre_authorization_status,
    get_request_details,
    PATIENTS,
    PROCEDURES
)

def main():
    """
    Main function for the AI agent to simulate a pre-authorization request.
    """
    setup_logging()
    logging.info("AI Agent for Medical Insurance Pre-Authorization started.")

    config = load_config()
    if not config:
        logging.error("Agent shutting down due to missing configuration.")
        return

    # Get a random patient and procedure for the simulation
    patient_id = list(PATIENTS.keys())[0]
    procedure_code = list(PROCEDURES.keys())[0]

    # Submit a pre-authorization request
    request_id = submit_pre_authorization_request(patient_id, procedure_code)
    if not request_id:
        return

    # Check the status of the request
    status = check_pre_authorization_status(request_id)
    logging.info(f"Initial status of request {request_id}: {status}")

    # If the request is pending, check again after a short delay
    if status == "pending":
        logging.info("Request is pending. Checking again in 5 seconds...")
        time.sleep(5)
        status = check_pre_authorization_status(request_id)
        logging.info(f"Updated status of request {request_id}: {status}")

    # Print the final details of the request
    details = get_request_details(request_id)
    logging.info(f"Final details of request {request_id}: {details}")

    logging.info("AI Agent simulation finished.")

if __name__ == "__main__":
    main()
