from .conftest import headers,OWNER,VIEWER,OTHER
DATA={'label':'Store Lab','currency':'BRL','baseline_kwh':'1000','proposed_kwh':'750','unit_tariff':'0.8'}

def test_energy_projection_and_isolation(client):
    out=client.post('/v1/analyses',json=DATA,headers=headers())
    assert out.status_code==201,out.text
    item=out.json();assert item['baseline_cost']=='800.00'
    assert item['monthly_difference']=='200.00' and item['annual_projection']=='2400.00'
    assert client.get(f'/v1/analyses/{item["id"]}',headers=headers(OTHER)).status_code==404

def test_negative_savings_and_bad_values(client):
    over=client.post('/v1/analyses',json={**DATA,'proposed_kwh':'1200'},headers=headers()).json()
    assert over['monthly_difference']=='-160.00'
    assert client.post('/v1/analyses',json={**DATA,'baseline_kwh':'0'},headers=headers()).status_code==422
    assert client.post('/v1/analyses',json={**DATA,'unit_tariff':'NaN'},headers=headers()).status_code==422

def test_csv_validation(client):
    csv='month,kwh\n2026-01,120\n2026-02,80\n'
    res=client.post('/v1/analyses/csv-summary',json={'csv_text':csv},headers=headers(VIEWER))
    assert res.status_code==200,res.text
    assert res.json()['average_kwh']=='100.00'
    bad='month,kwh\n2026-01,20\n2026-01,30\n'
    assert client.post('/v1/analyses/csv-summary',json={'csv_text':bad},headers=headers()).status_code==422

def test_roles_and_list(client):
    assert client.post('/v1/analyses',json=DATA,headers=headers(VIEWER)).status_code==403
    client.post('/v1/analyses',json=DATA,headers=headers())
    assert len(client.get('/v1/analyses',headers=headers()).json()['analyses'])==1
    assert client.get('/v1/analyses',headers=headers(OTHER)).json()['analyses']==[]
