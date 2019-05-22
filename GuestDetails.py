from sqlwrapper import *
from Fetch_Current_Datetime import *
import json

def Add_Guest_Details(request):
    d = request.json
    print(d)
    r_count = json.loads(dbget("select count(*) from guest_details where room_no='"+str(d['room_no'])+"'\
                                and checkout is null"))
    if r_count[0]['count'] == 0:
       d.update({'checkin':str(application_datetime())})
       gensql('insert','guest_details',d)
       dbput("update hotel_rooms set roomstatus_id='1' where room_no='"+str(d['room_no'])+"' \
              and business_id='"+str(d['business_id'])+"' ")
       
       return json.dumps({"Return": "Record Inserted Successfully","ReturnCode": "RIS",
                          "Status": "Success","StatusCode": "200"},indent = 4)    
       
    else:
        return json.dumps({"Return": "Room '"+str(d['room_no'])+"' Occupied","ReturnCode": "RO","Status": "Success",
                           "StatusCode": "200"},indent = 4)
        
    
def Edit_Guest_Details(request):
    d = request.json
    print(d)
    y = {k:v for k,v in d.items() if v != '' if k in ('guest_id','business_id')}
    x = {k:v for k,v in d.items() if v != '' if k not in ('guest_id','business_id')}
    gensql('update','guest_details',x,y)
    return json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUS",
                          "Status": "Success","StatusCode": "200"},indent = 4)    
       


def Checkout_Guest(request):
    y = request.json
    print(y)

    dbput("update guest_details  set  checkout='"+str(application_datetime())+"'  where  \
           guest_id='"+str(y['guest_id'])+"' and room_no='"+str(y['room_no'])+"' and \
           business_id='"+str(y['business_id'])+"'; \
           update hotel_rooms set roomstatus_id='2' where room_no='"+str(y['room_no'])+"' \
           and business_id='"+str(y['business_id'])+"';")

    return json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUS",
                          "Status": "Success","StatusCode": "200"},indent = 4)    
           

def Query_Guest_Details(request):
    d = request.json
    print(d)
    gus_details = json.loads(dbget("select * from guest_details where business_id='"+str(d['business_id'])+"'\
                                    order by checkin_date "))
    
    return json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS",
                       "Returnvalue":gus_details},indent=2)
def Query_Billing_Details(request):
    d=request.json
    guest = json.loads(dbget("select hotel_rooms.price,* from guest_details\
	join hotel_rooms on hotel_rooms.room_no = guest_details.room_no\
	 where guest_details.room_no='"+str(d['room_no'])+"' and checkout IS Null;"))
    food= json.loads(dbget("select * from fb_requests where date(request_time) between '"+str(guest[0]['checkin_date'])+"' and '"+str(guest[0]['checkout_date'])+"' and room_no='"+str(d['room_no'])+"';"))
    ldry = json.loads(dbget("	select * from ldry_request where date(request_time) between '"+str(guest[0]['checkin_date'])+"' and '"+str(guest[0]['checkout_date'])+"' and room_no='"+str(d['room_no'])+"';"))
    total_amount_laundry = sum( dry['total_amount'] for dry in ldry)
    print(total_amount_laundry)
    total_amt_food = sum( fd['total_amount'] for fd in food)
    print(total_amt_food)
    d1 = datetime.strptime(guest[0]['checkin_date'], "%Y-%m-%d")
    d2 = datetime.strptime(guest[0]['checkout_date'], "%Y-%m-%d")
    total_days = abs((d2 - d1).days)
    print(total_days)
    total_price= total_days * guest[0]['price']
    return json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS",
                       "Food_beverage":food,"laundry":ldry,"room_price":guest,
                       "total_amount":total_price+total_amount_laundry  +total_amt_food},indent=2)

