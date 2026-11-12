"""H4 API: tenant-scoped pilot. Never expose unchanged to public customer traffic."""
import os,json
from contextlib import asynccontextmanager
from fastapi import FastAPI,Depends,HTTPException,Request,Query
from sqlalchemy import select,text
from sqlalchemy.orm import Session
from .db import Base,Resource,AuditEvent,make_engine
from .auth import actor
from .app_helpers import session_dep,require_record
from .domain import router

@asynccontextmanager
async def lifespan(app:FastAPI):
    engine=make_engine()
    app.state.engine=engine
    if os.getenv('H4_CREATE_TABLES')=='1':
        Base.metadata.create_all(engine)
    try:yield
    finally:engine.dispose()

app=FastAPI(title='H4 EnergyPilot API',version='0.1.0',lifespan=lifespan,
            description='Technical starter; not production-ready.')

@app.middleware('http')
async def security_headers(request:Request,call_next):
    response=await call_next(request)
    response.headers['X-Content-Type-Options']='nosniff'
    response.headers['X-Frame-Options']='DENY'
    response.headers['Referrer-Policy']='no-referrer'
    response.headers['Permissions-Policy']='camera=(), microphone=(), geolocation=()'
    response.headers['Cache-Control']='no-store'
    response.headers['X-Robots-Tag']='noindex'
    return response

@app.get('/healthz',include_in_schema=False)
def healthz():return {'status':'alive'}

@app.get('/readyz',include_in_schema=False)
def readyz(session:Session=Depends(session_dep)):
    session.execute(text('SELECT 1'))
    return {'status':'ready'}

@app.get('/v1/me')
def whoami(auth=Depends(actor)):
    return auth

@app.get('/v1/audit')
def audit_log(limit:int=Query(default=25,ge=1,le=100),offset:int=Query(default=0,ge=0,le=10000),
              auth=Depends(actor),session:Session=Depends(session_dep)):
    entries=session.scalars(select(AuditEvent).where(AuditEvent.tenant_id==auth['tenant_id'])
                    .order_by(AuditEvent.created_at.desc(),AuditEvent.id.desc())
                    .offset(offset).limit(limit)).all()
    return {'events':[{'action':e.action,'subject_id':e.subject_id,'actor_id':e.actor_id,
                       'created_at':e.created_at.isoformat()} for e in entries],
            'limit':limit,'offset':offset}

app.include_router(router)
