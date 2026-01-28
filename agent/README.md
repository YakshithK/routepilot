# Route Pilot Agent (Flask)

Minimal Flask service with a single endpoint:

- `GET /health` → `{ "status": "ok" }`

## Setup (Windows PowerShell)

Create and activate the virtualenv:

```powershell
cd agent
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install deps:

```powershell
pip install -r requirements.txt
```

Run:

```powershell
python app.py
```

Test:

```powershell
curl http://127.0.0.1:5000/health
```


