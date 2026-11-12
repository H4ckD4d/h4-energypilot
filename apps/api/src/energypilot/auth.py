"""High-entropy API key SHA-256 digest demo auth. Not an enterprise identity provider."""
import hashlib,hmac,json,os,re
from fastapi import Depends,HTTPException,Security
from fastapi.security import APIKeyHeader

KEY=APIKeyHeader(name='X-API-Key',auto_error=False)
ROLES={'admin','editor','viewer'}

def actor(key: str | None=Security(KEY)):
    if not key or len(key)<24:
        raise HTTPException(401,'API key required')
    try:
        entries=json.loads(os.environ['H4_TENANTS'])
    except (ValueError,KeyError,TypeError) as exc:
        raise HTTPException(503,'Tenant authentication not configured') from exc
    if not isinstance(entries,list) or len(entries)>1000:
        raise HTTPException(503,'Invalid tenant configuration')
    observed=hashlib.sha256(key.encode()).hexdigest()
    matches=[]
    for row in entries:
        if not isinstance(row,dict) or row.get('disabled') is True:
            continue
        digest=row.get('key_sha256')
        if not (isinstance(digest,str) and re.fullmatch('[0-9a-f]{64}',digest)):
            continue
        if not hmac.compare_digest(digest,observed):
            continue
        if (row.get('role') not in ROLES or not isinstance(row.get('tenant_id'),str)
            or not row['tenant_id'] or not isinstance(row.get('actor_id'),str) or not row['actor_id']):
            continue
        matches.append({k:row[k] for k in ('tenant_id','actor_id','role')})
    if len(matches)>1:
        raise HTTPException(503,'Ambiguous credentials')
    if not matches:
        raise HTTPException(401,'Invalid API key')
    return matches[0]

def writer(auth=Depends(actor)):
    if auth['role'] not in ('admin','editor'):
        raise HTTPException(403,'Write access required')
    return auth
