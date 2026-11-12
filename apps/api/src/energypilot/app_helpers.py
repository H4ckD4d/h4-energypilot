from fastapi import HTTPException,Request
from sqlalchemy import select
from sqlalchemy.orm import Session
from .db import Resource

def session_dep(request:Request):
    with Session(request.app.state.engine) as session:
        yield session

def require_record(session:Session,id:str,tenant_id:str,kind:str):
    record=session.scalar(select(Resource).where(Resource.id==id,Resource.tenant_id==tenant_id,Resource.kind==kind))
    if record is None:
        raise HTTPException(404,'Not found')
    return record
