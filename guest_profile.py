from sqlwrapper import *

def Insert_Guest_Profile(request):
    d= request.json
    d.update({'guest_name':d['guest_name'].title(),'address':d['address'].title()})
    r_count = json.loads(dbget("select count(*) from guest_profile where mobile='"+str(d['mobile'])+"' and business_id ='"+str(d['business_id'])+"' "))
    if r_count[0]['count'] == 0:
        gensql('insert','guest_profile',d)
        return json.dumps({"Return": "Record Inserted Successfully","ReturnCode": "RIS","Status": "Success","StatusCode": "200"},indent = 4)
    else:
        return json.dumps({"Return": "Record Already Inserted","ReturnCode": "RAI","Status": "Success","StatusCode": "200"},indent = 4)


def Select_Guest_Profile(request):
    d = request.json
    gus_profile = json.loads(dbget("select * from guest_profile where business_id='"+str(d['business_id'])+"'"))
    
    return json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS","Returnvalue":gus_profile,"Status": "Success","StatusCode": "200"},indent=2)


def Update_Guest_profile(request):
    d = request.json
    d.update({'guest_name':d['guest_name'].title(),'address':d['address'].title()})
    b={k : v for k,v in d.items() if k in ('email','guest_name','address')}
    c={ k : v for k,v in d.items() if k in('business_id','mobile')}
    sql=gensql('update','guest_profile',b,c)
    print("status",sql)
    return json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUP","Status": "Success","StatusCode": "200"},indent = 4)
        
