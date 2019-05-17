from sqlwrapper import *
import random

def insert_hotelrooms(request):
    d=  request.json
    gensql('insert','hotel_rooms',d)
    return json.dumps({"Return": "Record Inserted Successfully","ReturnCode": "RIS","Status": "Success","StatusCode": "200"},indent = 4)

def select_hotelrooms(request):
    d = request.json
    rooms = json.loads(dbget("select h.room_no,h.roomtype_id,h.price,h.business_id,h.roomstatus_id,h.room_password,h.loginstatus_id,\
    r.roomtype_name,r.roomtype_image,\
    s.roomstatus,l.loginstatus\
    from hotel_rooms h \
    join room_type r on h.roomtype_id = r.roomtype_id \
    join room_status s on h.roomstatus_id = s.roomstatus_id\
    join login_status l on h.loginstatus_id = l.loginstatus_id\
    where h.business_id = '"+str(d['business_id'])+"'"))
    
    return json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS","ReturnValue":rooms,"Status": "Success","StatusCode": "200"},indent = 4)


def update_roomlogin(request):
    d = request.json
    b={k : v for k,v in d.items() if k in ('loginstatus_id')}
    c={ k : v for k,v in d.items() if k in('business_id','room_no')}
    sql=gensql('update','hotel_rooms',b,c)
    print("status",sql)
    return json.dumps({"Return": "Room Login Successfully","ReturnCode": "RLS","Status": "Success","StatusCode": "200"},indent = 4)
