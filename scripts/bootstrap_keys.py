"""Generate lab-only, random tenant API credentials; never commit the output."""
import secrets,hashlib,json
rows=[]
for tenant,actor,role in [('demo-company','owner','admin'),('demo-company','analyst','viewer')]:
    key=secrets.token_urlsafe(40)
    rows.append({'tenant_id':tenant,'actor_id':actor,'role':role,'key_sha256':hashlib.sha256(key.encode()).hexdigest()})
    print(f'{actor} local API key (store privately): {key}')
print('H4_TENANTS='+json.dumps(rows,separators=(',',':')))
