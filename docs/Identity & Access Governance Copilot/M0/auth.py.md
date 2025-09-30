
Required imports:

os - to get the env variable "TOKEN_TTL_HOURS" to create a authenticator.
datetime as dt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer

Purpose: To create a jwt encoded token used for Authorization when running any inbound api requests

defs:

1. create_token(payload: dict) -> str:

	1. ttl - creates a ttl time to show how long the Authorization token can last.
	2. data  - payload received via parameter
	3.  data["exp"] - appends ttl to data dict in dt.datetime.utcnow() + dt.timedelta(hours=ttl)
	4. returns jwt secret - jwt.encode(data, SECRET, algorithm=ALG)


2.  verify_token(credentials=Depends(security)):
	1. the credentials runs through HTTPBearer where HTTPBearer looks for Authorization token and finds the key with Bearer <key> 
	2. get the token  by getting from the parameter credentials.credentials.
	3. decodes the data and the value is received
	4. Expected errors:
		1. Token Expired
		2. Invalid Token
