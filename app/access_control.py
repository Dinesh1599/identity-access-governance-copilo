from .schemas import AccessRequest

def evaluate_access(req: AccessRequest):
    # RBAC
    if req.role and req.role in req.user.roles:
        return {"access": True, "reason": "RBAC: role present"}
    # ABAC example
    if req.resource == "finance" and req.user.department == "Finance":
        return {"access": True, "reason": "ABAC: department == Finance"}
    # SoD example (toy)
    conflicts = {("Requestor", "Approver"), ("Maker", "Checker")}
    roles = set(req.user.roles)
    for a, b in conflicts:
        if a in roles and b in roles:
            return {"access": False, "reason": f"SoD: {a}/{b} conflict"}
    return {"access": False, "reason": "Denied by default"}     