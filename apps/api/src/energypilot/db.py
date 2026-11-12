"""Database storage; SQLite for local demos, PostgreSQL URL accepted for future pilots."""
import os
from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import String, DateTime, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

def newid():
    return str(uuid4())

def utcnow():
    return datetime.now(timezone.utc)

class Resource(Base):
    __tablename__='resources'
    id: Mapped[str]=mapped_column(String(36),primary_key=True,default=newid)
    tenant_id: Mapped[str]=mapped_column(String(128),nullable=False,index=True)
    kind: Mapped[str]=mapped_column(String(40),nullable=False,index=True)
    status: Mapped[str]=mapped_column(String(32),nullable=False)
    data_json: Mapped[str]=mapped_column(Text,nullable=False)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=utcnow)

class AuditEvent(Base):
    __tablename__='audit_events'
    id: Mapped[str]=mapped_column(String(36),primary_key=True,default=newid)
    tenant_id: Mapped[str]=mapped_column(String(128),nullable=False,index=True)
    actor_id: Mapped[str]=mapped_column(String(128),nullable=False)
    action: Mapped[str]=mapped_column(String(80),nullable=False)
    subject_id: Mapped[str]=mapped_column(String(36),nullable=False)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=utcnow)

def make_engine():
    url=os.environ.get('H4_DATABASE_URL','sqlite:///./h4-local.db')
    kwargs={'connect_args':{'check_same_thread':False}} if url.startswith('sqlite') else {}
    return create_engine(url,pool_pre_ping=True,**kwargs)

def record_event(session,actor,action,subject_id):
    session.add(AuditEvent(tenant_id=actor['tenant_id'],actor_id=actor['actor_id'],
                           action=action,subject_id=subject_id))
