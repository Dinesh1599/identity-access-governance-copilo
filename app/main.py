from fastapi import FastAPI, Depends
from . import auth
from .schemas import AccessRequest
from .access_control import evaluate_access


app = FastAPI(title="Identity & Access Governance Copilot")


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/check-access")
def check_access(req: AccessRequest, _: dict = Depends(auth.verify_token)):
    return evaluate_access(req)