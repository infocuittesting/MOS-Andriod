from sqlwrapper import *
import random
#-------------------room_type------------#
def Insert_Roomtype(request):
    d=request.json
    d.update({'roomtype_id': (str(d['roomtype_name'][:3]) +str(random.randint(100,300))).lower(),'roomtype_name':d['roomtype_name'].title()})
    print(d['roomtype_id'])
    gensql('insert','room_type',d)
    return json.dumps({"Return": "Record Inserted Successfully","ReturnCode": "RIS","Status": "Success","StatusCode": "200"},indent = 4)
def Select_Room_Type(request):
    d=request.json
    d1 = json.loads(gensql('select','room_type','*',d))
    return(json.dumps({"Message":"Record Selected Successfully","Message_Code":"RSS","Service_Status":"Success","output":d1},indent=4))

def Update_Roomtype(request):
    d = request.json
   
    b={k : v for k,v in d.items() if k in ('roomtype_image')}
    c={ k : v for k,v in d.items() if k in('business_id','roomtype_id')}
    sql=gensql('update','room_type',b,c)
    return json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUS","Status": "Success","StatusCode": "200"},indent = 4)
