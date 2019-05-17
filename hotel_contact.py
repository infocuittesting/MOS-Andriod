from sqlwrapper import *
import random

def Insert_Contact_Number(request):
    d=request.json
    gensql('insert','hotel_contacts',d)
    return json.dumps({"Return": "Record Inserted Successfully","ReturnCode": "RIS","Status": "Success","StatusCode": "200"},indent = 4)

def Select_Contact_Number(request):
    d=request.json
    d1 = json.loads(gensql('select','hotel_contacts','*',d))
    return(json.dumps({"Message":"Record Selected Successfully","Message_Code":"RSS","Service_Status":"Success","output":d1},indent=4))

def Delete_Contact_Number(request):
    d1=request.json['number']
    d2=request.json['business_id']
    dbput("delete from hotel_contacts where number='"+d1+"'and business_id='"+d2+"'")
    return(json.dumps({"Message":"Record Deleted Successfully","Message Code":"RDS","Service Status":"Success"},indent=4))
