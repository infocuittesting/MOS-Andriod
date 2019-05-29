from sqlwrapper import *
import random

def Insert_Hotel_room(request):
    d=  request.json
    d.update( {'roomstatus_id' : 2,'loginstatus_id':2} )
    check_item = json.loads(dbget("select count(*) from hotel_rooms \
                                     where business_id='"+str(d['business_id'])+"' and room_no= '"+str(d['room_no'])+"'"))
    if check_item[0]['count'] == 0:
        gensql('insert','hotel_rooms',d)
        return json.dumps({"Return": "Record Inserted Successfully","ReturnCode": "RIS","Status": "Success","StatusCode": "200"},indent = 4)
    else:
        return json.dumps({"Return": "Record Already Inserted","ReturnCode": "RIS","Status": "Success","StatusCode": "200"},indent = 4)

def Select_Hotel_Room(request):
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


def Update_Room_Login(request):
    d = request.json
    psql = json.loads(dbget("select count(loginstatus_id) from hotel_rooms where business_id ='"+str(d['business_id'])+"'\
                    and loginstatus_id = '"+str(d['loginstatus_id'])+"' and room_no = '"+str(d['room_no'])+"'"))
    if psql[0]['count'] == 0:
        if d['loginstatus_id'] == 1 :
            b={k : v for k,v in d.items() if k in ('loginstatus_id')}
            c={ k : v for k,v in d.items() if k in('business_id','room_no')}
            sql=gensql('update','hotel_rooms',b,c)
            print("status",sql)
            return json.dumps({"Return": "Log In Successfully","ReturnCode": "LIS","Status": "Success","StatusCode": "200"},indent = 4)
        
        else:
            b={k : v for k,v in d.items() if k in ('loginstatus_id')}
            c={ k : v for k,v in d.items() if k in('room_no','business_id')}
            sql=gensql('update','hotel_rooms',b,c)
            return json.dumps({"Return": "Log Out Successfully","ReturnCode": "LOS","Status": "Success","StatusCode": "200"},indent = 4)
    else:
        return json.dumps({"Return": "Already Login/LogOut Successfully","ReturnCode": "ALS","Status": "Success","StatusCode": "200"},indent = 4)
