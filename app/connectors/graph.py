import os, requests
from typing import Dict, Any, List


TENANT = os.getenv("MS_TENANT_ID")
CLIENT_ID = os.getenv("MS_CLIENT_ID")
CLIENT_SECRET = os.getenv("MS_CLIENT_SECRET")


SCOPE = "https://graph.microsoft.com/.default"
TOKEN_URL = f"https://login.microsoftonline.com/{TENANT}/oauth2/v2.0/token"




def _token() -> str:
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
        "scope": SCOPE,
    }
    r = requests.post(TOKEN_URL, data=data, timeout=30)
    r.raise_for_status()
    return r.json()["access_token"]




def fetch_azure_ad_users() -> List[Dict[str, Any]]:
    access_token = _token()
    url = (
        "https://graph.microsoft.com/v1.0/users?"
        "$select=id,userPrincipalName,displayName,department"
    )
    r = requests.get(url, headers={"Authorization": f"Bearer {access_token}"}, timeout=30)
    r.raise_for_status()
    print(r.json())
    return r.json().get("value", [])