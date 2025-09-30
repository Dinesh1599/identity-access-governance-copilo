from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class UserIn(BaseModel):
    id: str
    roles: List[str] = []
    department: Optional[str] = None


class AccessRequest(BaseModel):
    user: UserIn
    role: Optional[str] = None
    resource: Optional[str] = None

class AccessUser(BaseModel):
    id: Optional[str] = None
    display_name: Optional[str] = None
    department: Optional[str] = None
    roles: List[str] = []


class AccessRequest(BaseModel):
    user: AccessUser 
    resource: str
    action: str
    role: Optional[str] = None # requested role


class AnomalyIn(BaseModel):
    anomaly: Dict[str, Any]


class DecisionRequest(BaseModel):
    user: AccessUser
    current_perms: List[str] = []
    requested_perms: List[str] = []


class PolicyQuery(BaseModel):
    question: str   