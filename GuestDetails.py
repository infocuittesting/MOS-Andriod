from sqlwrapper import *

from Fetch_Current_Datetime import *
import json
import datetime
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
    r_count = json.loads(dbget("select count(*) from guest_details where room_no='"+str(d['room_no'])+"'\
                                and checkout is null"))
    if r_count[0]['count'] == 0:
        y = {k:v for k,v in d.items() if v != '' if k in ('guest_id','business_id')}
        x = {k:v for k,v in d.items() if v != '' if k not in ('guest_id','business_id')}
        gensql('update','guest_details',x,y)
        return json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUS",
                              "Status": "Success","StatusCode": "200"},indent = 4)
    else:
        return json.dumps({"Return": "Room '"+str(d['room_no'])+"' Occupied","ReturnCode": "RO","Status": "Success",
                           "StatusCode": "200"},indent = 4)
       


def Checkout_Guest(request):
    y = request.json
    
    current_date=datetime.date.today()
    get_checkoutdate=json.loads(dbget("select checkout_date  from guest_details where business_id='"+str(y['business_id'])+"'\
                                   and guest_id='"+str(y['guest_id'])+"' and room_no='"+str(y['room_no'])+"'"))
    print(get_checkoutdate)
    #y1 = {k:v for k,v in get_checkoutdate('checkout_date')}
    v1=get_checkoutdate[0]['checkout_date']
    if v1 == str(current_date):
        
        dbput("update guest_details  set  checkout='"+str(application_datetime())+"'  where  \
               guest_id='"+str(y['guest_id'])+"' and room_no='"+str(y['room_no'])+"' and \
               business_id='"+str(y['business_id'])+"'; \
               update hotel_rooms set roomstatus_id='2' where room_no='"+str(y['room_no'])+"' \
               and business_id='"+str(y['business_id'])+"';")

        return json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUS",
                              "Status": "Success","StatusCode": "200"},indent = 4)
    else:
        return json.dumps({"Return": "This Is Not Your Checkoutdate","ReturnCode": "TINYC",
                              "Status": "Success","StatusCode": "200"},indent = 4)
        
           

def Query_Guest_Details(request):
    d = request.json
    print(d)
    gus_details = json.loads(dbget("select guest_profile.guest_name,Guest_details.* from guest_details\
                                    join guest_profile on guest_profile.mobile = guest_details.mobile_no where guest_details.business_id='"+str(d['business_id'])+"'\
                                    order by checkin_date "))
    
    return json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS",
                       "Returnvalue":gus_details},indent=2)
def query_collection(coll_id):
    print("query collection")
    a = json.loads(dbget("select * from fb_collection where fbcollection_id='"+str(coll_id)+"' "))
    return(a)
def query_collection2(coll_id):    
    b= json.loads(dbget("select * from ldry_collection where ldrycollection_id='"+str(coll_id)+"' "))
    return(b)
    
def Query_Billing_Details(request):
    d=request.json
    guest = json.loads(dbget("select hotel_rooms.price,* from guest_details\
	join hotel_rooms on hotel_rooms.room_no = guest_details.room_no\
	 where guest_details.room_no='"+str(d['room_no'])+"' and checkout IS Null;"))
    food= json.loads(dbget("select * from fb_requests where date(request_time) between '"+str(guest[0]['checkin_date'])+"' and '"+str(guest[0]['checkout_date'])+"' and room_no='"+str(d['room_no'])+"';"))
    print("food",  food)
    ldry = json.loads(dbget("	select * from ldry_request where date(request_time) between '"+str(guest[0]['checkin_date'])+"' and '"+str(guest[0]['checkout_date'])+"' and room_no='"+str(d['room_no'])+"';"))
    total_amount_laundry = sum( dry['total_amount'] for dry in ldry)
    print(total_amount_laundry)
    total_amt_food = sum( fd['total_amount'] for fd in food)
    print(total_amt_food)
    d1 = datetime.datetime.strptime(guest[0]['checkin_date'], "%Y-%m-%d")
    d2 = datetime.datetime.strptime(guest[0]['checkout_date'], "%Y-%m-%d")
    total_days = abs((d2 - d1).days)
    print(total_days)
    total_price= total_days * guest[0]['price']
    return json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS",
                       "Food_beverage":{
                           'fb_order':[dict(f,item=query_collection(f['fbcollection_id'])) for f in food]
                           },
                       "laundry":{
                           'ldry_order':[dict(f,item=query_collection2(f['ldrycollect_id'])) for f in ldry]
                           },
                       "room_price":guest,
                       "total_amount":total_price+total_amount_laundry+total_amt_food},indent=2)
