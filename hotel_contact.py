from sqlwrapper import *
import random

def insert_number(request):
    d=request.json
    gensql('insert','hotel_contacts',d)
    return json.dumps({"Return": "Record Inserted Successfully","ReturnCode": "RIS","Status": "Success","StatusCode": "200"},indent = 4)

def select_number(request):
    d=request.json
    d1 = json.loads(gensql('select','hotel_contacts','*',d))
    return(json.dumps({"Message":"Record Selected Successfully","Message_Code":"RSS","Service_Status":"Success","output":d1},indent=4))

def delete_number(request):
    d1=request.json['number']
    d2=request.json['business_id']
    dbput("delete from hotel_contacts where number='"+d1+"'and business_id='"+d2+"'")
    return(json.dumps({"Message":"Record Deleted Successfully","Message Code":"RDS","Service Status":"Success"},indent=4))
