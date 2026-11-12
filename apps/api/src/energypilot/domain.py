"""Bounded energy estimates and local CSV summaries; no equipment control."""
import csv,io,json
from decimal import Decimal,ROUND_HALF_UP
from datetime import datetime
from typing import Literal
from fastapi import APIRouter,Depends,HTTPException,Query
from pydantic import BaseModel,Field,field_validator
from sqlalchemy import select
from sqlalchemy.orm import Session
from .app_helpers import session_dep,require_record
from .auth import actor,writer
from .db import Resource,record_event

router=APIRouter(prefix='/v1/analyses',tags=['energy'])
CENT=Decimal('0.01')
def money(v):return str(v.quantize(CENT,rounding=ROUND_HALF_UP))

class EnergyCreate(BaseModel):
    label:str=Field(min_length=2,max_length=100)
    currency:Literal['BRL','USD','EUR']='BRL'
    baseline_kwh:Decimal=Field(gt=0,le=100000000)
    proposed_kwh:Decimal=Field(ge=0,le=100000000)
    unit_tariff:Decimal=Field(ge=0,le=100000)
    @field_validator('baseline_kwh','proposed_kwh','unit_tariff')
    @classmethod
    def finite(cls,v):
        if not v.is_finite():raise ValueError('Finite decimals only')
        return v

class CsvUsage(BaseModel):
    csv_text:str=Field(min_length=10,max_length=100000)

def estimate(payload):
    v=EnergyCreate.model_validate(payload)
    old=v.baseline_kwh*v.unit_tariff
    new=v.proposed_kwh*v.unit_tariff
    saved=old-new
    change=(v.baseline_kwh-v.proposed_kwh)*100/v.baseline_kwh
    return {'label':v.label,'currency':v.currency,'baseline_kwh':str(v.baseline_kwh),
            'proposed_kwh':str(v.proposed_kwh),'unit_tariff':str(v.unit_tariff),
            'baseline_cost':money(old),'proposed_cost':money(new),
            'monthly_difference':money(saved),'annual_projection':money(saved*12),
            'consumption_change_percent':money(change),
            'notice':'Illustrative scenario only; omits fixed charges, taxes, demand, weather and actual equipment performance.'}

def summarize_csv(source):
    try:
        reader=csv.DictReader(io.StringIO(source))
        if reader.fieldnames!=['month','kwh']:
            raise ValueError('Required CSV headers: month,kwh')
        months=set(); values=[]
        for row in reader:
            if len(values)>=36:raise ValueError('Maximum 36 monthly rows')
            month=row['month']
            try:
                parsed=datetime.strptime(month,'%Y-%m')
                if parsed.strftime('%Y-%m')!=month:raise ValueError
            except (ValueError,TypeError):raise ValueError('Invalid month format') from None
            if month in months:raise ValueError('Duplicate month')
            months.add(month)
            v=Decimal(row['kwh'])
            if not v.is_finite() or v<0 or v>100000000:raise ValueError('Invalid usage')
            values.append((month,v))
    except (KeyError,csv.Error,TypeError,ArithmeticError) as e:
        raise ValueError('Invalid CSV data') from e
    if not values:raise ValueError('Missing readings')
    values.sort()
    total=sum((x for _,x in values),Decimal(0))
    return {'samples':len(values),'total_kwh':money(total),
            'average_kwh':money(total/len(values)),
            'minimum_kwh':money(min(x for _,x in values)),
            'maximum_kwh':money(max(x for _,x in values)),
            'first_month':values[0][0],'last_month':values[-1][0],
            'notice':'Descriptive consumption only; no causal attribution or guaranteed savings.'}

@router.post('',status_code=201)
def create_analysis(payload:EnergyCreate,auth=Depends(writer),session:Session=Depends(session_dep)):
    result=estimate(payload)
    item=Resource(tenant_id=auth['tenant_id'],kind='analysis',status='completed',data_json=json.dumps(result))
    session.add(item);session.flush();record_event(session,auth,'analysis.created',item.id);session.commit()
    return {'id':item.id,**result}

@router.get('')
def analyses(limit:int=Query(default=25,ge=1,le=100),offset:int=Query(default=0,ge=0,le=10000),
             auth=Depends(actor),session:Session=Depends(session_dep)):
    rows=session.scalars(select(Resource).where(Resource.tenant_id==auth['tenant_id'],Resource.kind=='analysis')
          .order_by(Resource.created_at.desc(),Resource.id.desc()).offset(offset).limit(limit)).all()
    return {'analyses':[{'id':x.id,**json.loads(x.data_json)} for x in rows],'limit':limit,'offset':offset}

@router.get('/{analysis_id}')
def detail(analysis_id:str,auth=Depends(actor),session:Session=Depends(session_dep)):
    x=require_record(session,analysis_id,auth['tenant_id'],'analysis')
    return {'id':x.id,**json.loads(x.data_json)}

@router.post('/csv-summary')
def csv_summary(payload:CsvUsage,auth=Depends(actor)):
    try:return summarize_csv(payload.csv_text)
    except (ValueError,ArithmeticError) as exc:raise HTTPException(422,str(exc)) from exc
