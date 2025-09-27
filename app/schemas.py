from pydantic import BaseModel
from typing import List, Optional


class UserIn(BaseModel):
    id: str
    roles: List[str] = []
    department: Optional[str] = None


class AccessRequest(BaseModel):
    user: UserIn
    role: Optional[str] = None
    resource: Optional[str] = None