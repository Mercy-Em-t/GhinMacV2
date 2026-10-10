import zipfile
import os

def create_cartridge(name, yaml_content, tools_content, html_content):
    os.makedirs(name, exist_ok=True)
    with open(f"{name}/company.yaml", "w") as f:
        f.write(yaml_content)
    with open(f"{name}/tools.py", "w") as f:
        f.write(tools_content)
    with open(f"{name}/index.html", "w") as f:
        f.write(html_content)
        
    with zipfile.ZipFile(f"{name}.zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(name):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(name, '..')))

# 1. Healthcare Clinic
clinic_yaml = """name: "GhInMac Healthcare"
departments:
  triage:
    allowed_tools: ["query_db", "schedule_appointment", "check_symptoms"]
    max_budget_per_task: 150
  doctors:
    allowed_tools: ["query_db", "prescribe_medication", "view_records"]
    max_budget_per_task: 500
  billing:
    allowed_tools: ["query_db", "process_insurance"]
    max_budget_per_task: 100
llm_provider: "gemini"
"""

clinic_tools = """def query_db(args):
    return "Simulated DB: Patient records retrieved."

def schedule_appointment(args):
    return f"Appointment scheduled for {args.get('patient')} at {args.get('time')}."

def prescribe_medication(args):
    return f"Prescription {args.get('medication')} sent to pharmacy for {args.get('patient')}."

def process_insurance(args):
    return "Insurance claim submitted successfully."
"""

clinic_html = """<html><body><h1>GhInMac Healthcare</h1>
<button onclick="fetch('/tasks', {method: 'POST', body: JSON.stringify({department: 'triage', payload: {symptoms: 'fever'}})})">Admit Patient</button>
<button onclick="fetch('/tasks', {method: 'POST', body: JSON.stringify({department: 'doctors', payload: {patient_id: '123', action: 'consult'}})})">Doctor Consult</button>
</body></html>"""

create_cartridge("cartridge_clinic", clinic_yaml, clinic_tools, clinic_html)

# 2. Law Firm
law_yaml = """name: "GhInMac Legal Partners"
departments:
  intake:
    allowed_tools: ["query_db", "conflict_check", "schedule_consultation"]
  litigation:
    allowed_tools: ["query_db", "draft_subpoena", "review_evidence"]
  accounting:
    allowed_tools: ["query_db", "bill_hours"]
llm_provider: "gemini"
"""

law_tools = """def query_db(args):
    return "Simulated DB: Case files retrieved."

def conflict_check(args):
    return "No conflicts of interest found for this client."

def draft_subpoena(args):
    return f"Subpoena drafted for {args.get('target')}."

def bill_hours(args):
    return f"Billed {args.get('hours')} hours to client {args.get('client_id')}."
"""

law_html = """<html><body><h1>GhInMac Legal Partners</h1>
<button onclick="fetch('/tasks', {method: 'POST', body: JSON.stringify({department: 'intake', payload: {client: 'John Doe', case_type: 'civil'}})})">New Client Intake</button>
<button onclick="fetch('/tasks', {method: 'POST', body: JSON.stringify({department: 'litigation', payload: {case_id: '99', action: 'draft'}})})">Draft Subpoena</button>
</body></html>"""

create_cartridge("cartridge_lawfirm", law_yaml, law_tools, law_html)
