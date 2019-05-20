from sqlwrapper import *
import random

def Configure_Laundry_Items(request):
    d = request.json
    print(d) 
    get_category = json.loads(dbget("select count(*) from laundry_category \
                                     where business_id='"+str(d['business_id'])+"' and ldrycateg_name = '"+str(d['ldrycateg_name'].title())+"'"))
    
    if get_category[0]['count'] == 0:
        s={"ldrycateg_id":(d['ldrycateg_name'][:3]+str(random.randint(1000,3000))).lower(),
           "ldrycateg_name":d['ldrycateg_name'].title(),
           "ldrycateg_image":d['ldrycateg_image'],
           "business_id":d['business_id']}
        s = {k:v for k,v in s.items() if v!= ""}
        catogory = gensql('insert','laundry_category',s)
        print("if_catogory",catogory)
        
        d.update({'ldryitem_id':(d['ldryitem_name'][:3]+str(random.randint(1000,3000))).lower(),"ldrycateg_id":str(s['ldrycateg_id']),"ldryitem_name":d['ldryitem_name'].title()})
        d = {k:v for k,v in d.items() if v!= "" if k not in ('ldrycateg_name','ldrycateg_image')}
        insert_item = gensql('insert','laundry_items',d)
        print("if_insert item:",insert_item)
    else:
        print("ssssssssssssssssssssssssssssssss")
        d.update({'ldryitem_id': (d['ldryitem_name'][:3]+str(random.randint(1000,3000))).lower(),"ldrycateg_id":str(d['ldrycateg_id']),"ldryitem_name":d['ldryitem_name'].title()})
        d = {k:v for k,v in d.items() if v!= "" if k not in ('ldrycateg_name','ldrycateg_image','ldrycateg_id')}
        insert_item = gensql('insert','laundry_items',d)
        print("else_insert item:",insert_item)
    #return json.dumps({"Retun":d},indent=4)

    return json.dumps({"Return": "Record Inserted Successfully","ReturnCode": "RIS","Status": "Success","StatusCode": "200"},indent = 4)


def Select_Laundry_Items(request):
    d = request.json
    rooms = json.loads(dbget("select li.*,lc.ldrycateg_name,lc.ldrycateg_image from laundry_items li \
    join laundry_category lc on li.ldrycateg_id = lc.ldrycateg_id \
    where li.business_id = '"+str(d['business_id'])+"'"))
    
    return json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS","ReturnValue":rooms,"Status": "Success","StatusCode": "200"},indent = 4)


def Update_Laundry_Items(request):
    d = request.json
    d.update({'ldrycateg_name':d['ldrycateg_name'].title(),"ldryitem_name":d['ldryitem_name'].title()})
    print(d) 

    b={k : v for k,v in d.items() if k in ('ldrycateg_name','ldrycateg_image')}
    c={ k : v for k,v in d.items() if k in('ldrycateg_id','business_id')}
    sql=gensql('update','laundry_category',b,c)
    
    b={k : v for k,v in d.items() if k in ('ldryitem_name','ldrycateg_id','ldryitem_description','price')}
    c={ k : v for k,v in d.items() if k in('ldryitem_id','business_id')}
    sql=gensql('update','laundry_items',b,c)
    return json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUS","Status": "Success","StatusCode": "200"},indent = 4)       
