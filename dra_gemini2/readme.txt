Initial Setup
==============
mkdir -p deployment-readiness-agent
cd deployment-readiness-agent

touch ado_tools.py
touch agent.py
touch readme.md
touch requirements.txt
touch synthetic_data.json
touch todo.txt


python virtual env and install dependices
==========================================
cd deployment-readiness-agent
python -m venv .venv 
source .venv/bin/activate
# pip install google-adk pydantic
pip install -r requirements.txt



How to run
==============
adk run .
adk web agent.py



Directory Structure
==============
deployment-readiness-agent/
├── ado_tools.py
├── agent.py
├── readme.md
├── requirements.txt
├── synthetic_data.json
└── todo.txt