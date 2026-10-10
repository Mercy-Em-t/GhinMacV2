def query_db(args):
    return "Simulated DB: Patient records retrieved."

def schedule_appointment(args):
    return f"Appointment scheduled for {args.get('patient')} at {args.get('time')}."

def prescribe_medication(args):
    return f"Prescription {args.get('medication')} sent to pharmacy for {args.get('patient')}."

def process_insurance(args):
    return "Insurance claim submitted successfully."
