# app/main.py
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import json, os

from .auth import verify_token
from .db import Base, engine, get_db
from .model import User, Anomaly
from .schemas import AccessRequest, AnomalyIn, DecisionRequest, PolicyQuery
from .access_control import evaluate_access
from .connectors.graph import fetch_azure_ad_users
from .chains import summarize_anomaly, least_privilege_decision, policy_qa




app = FastAPI(title="Identity & Access Governance Copilot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"status": "ok", "service": "IAG Copilot"}


@app.post("/check-access")

def check_access(req: AccessRequest, _: dict = Depends(verify_token)):
    return evaluate_access(req)


@app.post("/connectors/run")
def run_connector(source: str = "graph", db: Session = Depends(get_db), _: dict = Depends(verify_token)):
    if source != "graph":
        raise HTTPException(status_code=400, detail="Unsupported source")

    users = fetch_azure_ad_users()
    synced = 0
    for u in users:
        ext_id = u.get("id")
        if not ext_id:
            continue

        user = db.query(User).filter(User.external_id == ext_id).one_or_none()
        if not user:
            user = User(external_id=ext_id)
            db.add(user)

        user.upn = u.get("userPrincipalName", "") or " "
        user.display_name = u.get("displayName", "") or " "
        user.department = u.get("department", "") or " "
        synced += 1

    db.commit()
    return {"synced": synced}


@app.get("/users")
def list_users(limit: int = 50, db: Session = Depends(get_db), _: dict = Depends(verify_token)):
    rows = db.query(User).limit(limit).all()
    return [
        {
            "id": r.id,
            "external_id": r.external_id,
            "upn": r.upn,
            "display_name": r.display_name,
            "department": r.department,
            "roles": [t.name for t in r.roles],
        }
        for r in rows
    ]


@app.post("/summarize")
def summarize(body: AnomalyIn, db: Session = Depends(get_db), _: dict = Depends(verify_token)):
    text = summarize_anomaly(body.anomaly)
    rec = Anomaly(raw_json=json.dumps(body.anomaly), status="summarized")
    db.add(rec)
    db.commit()
    return {"summary": text}


@app.post("/decision")
def decision(body: DecisionRequest, _: dict = Depends(verify_token)):
    text = least_privilege_decision(
        user=body.user.model_dump(),
        current=body.current_perms,
        requested=body.requested_perms,
    )
    return {"recommendation": text}


@app.post("/policy-chat")
def policy_chat(body: PolicyQuery, _: dict = Depends(verify_token)):
    answer = policy_qa(body.question)
    return {"answer": answer}
