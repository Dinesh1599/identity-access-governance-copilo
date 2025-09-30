import os
import datetime as dt
import jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer


SECRET = os.getenv("JWT_SECRET", "change_me")
ALG = "HS256"
security = HTTPBearer()


def create_token(payload: dict) -> str:
    ttl = int(os.getenv("TOKEN_TTL_HOURS", "1"))
    data = payload.copy()
    data["exp"] = dt.datetime.utcnow() + dt.timedelta(hours=ttl)
    print(data)
    return jwt.encode(data, SECRET, algorithm=ALG)


def verify_token(credentials=Depends(security)):
    token = credentials.credentials
    try:
        return jwt.decode(token, SECRET, algorithms=[ALG])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token") 


"""

THERE IS SO MUCH TO LEARN HERE. ESPECIALLY HOW fastapi's HTTPBearer and Depends() works. check it out again with CHATGpt

"""