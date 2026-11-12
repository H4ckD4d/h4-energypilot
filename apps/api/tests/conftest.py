import hashlib,json
import pytest
from fastapi.testclient import TestClient
from energypilot.app import app

OWNER='owner_demo_0123456789_abcdef12345'
VIEWER='viewer_demo_0123456789_abcdef12345'
OTHER='other_demo_0123456789_abcdef12345'
REVOKED='revoked_demo_0123456789_abcdef12345'

def headers(token=OWNER):return {'X-API-Key':token}

@pytest.fixture
def client(tmp_path,monkeypatch):
    monkeypatch.setenv('H4_DATABASE_URL',f'sqlite:///{tmp_path / "demo.db"}')
    monkeypatch.setenv('H4_CREATE_TABLES','1')
    entries=[
      {'tenant_id':'company-a','actor_id':'owner','role':'admin','key_sha256':hashlib.sha256(OWNER.encode()).hexdigest()},
      {'tenant_id':'company-a','actor_id':'viewer','role':'viewer','key_sha256':hashlib.sha256(VIEWER.encode()).hexdigest()},
      {'tenant_id':'company-b','actor_id':'other','role':'admin','key_sha256':hashlib.sha256(OTHER.encode()).hexdigest()},
      {'tenant_id':'company-a','actor_id':'revoked','role':'admin','key_sha256':hashlib.sha256(REVOKED.encode()).hexdigest(),'disabled':True},
    ]
    monkeypatch.setenv('H4_TENANTS',json.dumps(entries))
    with TestClient(app) as c:yield c
