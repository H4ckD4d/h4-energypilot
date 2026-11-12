from .conftest import OWNER,VIEWER,OTHER,REVOKED,headers

def test_health_and_auth(client):
    assert client.get('/healthz').status_code==200
    assert client.get('/readyz').status_code==200
    assert client.get('/v1/me').status_code==401
    assert client.get('/v1/me',headers=headers(OWNER)).json()['role']=='admin'
    assert client.get('/v1/me',headers=headers(VIEWER)).json()['role']=='viewer'
    assert client.get('/v1/me',headers=headers(REVOKED)).status_code==401
    assert client.get('/v1/me',headers=headers('bad')).status_code==401

def test_security_and_audit(client):
    response=client.get('/v1/audit',headers=headers())
    assert response.status_code==200
    assert response.headers['X-Robots-Tag']=='noindex'
    assert response.headers['Cache-Control']=='no-store'
    assert client.get('/v1/audit?limit=101',headers=headers()).status_code==422
    assert client.get('/v1/audit?offset=-1',headers=headers()).status_code==422

def test_fail_closed_when_unconfigured(client,monkeypatch):
    monkeypatch.delenv('H4_TENANTS')
    assert client.get('/v1/me',headers=headers()).status_code==503
