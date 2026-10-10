$env:PYTHONPATH = $PWD
.\venv\Scripts\python -m uvicorn ghinmac.api.app:app --port 8080 --reload --env-file .env
