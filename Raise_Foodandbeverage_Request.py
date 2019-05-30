from sqlwrapper import *
import re
from Fetch_Current_Datetime import *
def Raise_Foodandbeverage_Request(request):
    d=request.json
    list1 = []
    order_no = json.loads(dbget("SELECT array_to_string(ARRAY(SELECT chr((48 + round(random() * 9)) :: integer) \
                                FROM generate_series(1,10)), '');"))
    print(order_no)
    for item in d['food_items']:
        list1.append(tuple((order_no[0]['array_to_string'],item['fbitem_id'],item['quantity'])))
    values = ', '.join(map(str, list1))
    dbput("INSERT INTO  fb_collection (fbcollection_id, fbitem_id, quantity)VALUES {}".format(values))
                
    current_datetime=application_datetime()
    ticket_no = str(current_datetime.strftime("%Y-%m-%d%H:%M:%S"))+str(d['room_no'])+'foo2106'+str(order_no[0]['array_to_string'])
    
    d.update({'reminder_count':0,'escalation_count':0,
              'ticketstatus_id':1,'request_time':str(current_datetime.strftime("%Y-%m-%d %H:%M:%S")),
              'ticket_no':re.sub("-|:","",ticket_no),'fbcollection_id':order_no[0]['array_to_string'],'fbitem_count':d['fbitem_count'],'total_amount':d['total_amount']})
    print(d)
    d={k:v for k,v in d.items() if k not in ('food_items')}
    gensql('insert','fb_requests',d)
    return json.dumps({"Return": "Record Inserted Successfully","ReturnCode": "RIS","Status": "Success","StatusCode": "200"},indent = 4)

    
    
def Close_Foodandbeverage_Request(request):
    
    
    d=request.json
    dbput("update fb_requests set ticketstatus_id='2' where ticket_no='"+str(d['ticket_no'])+"'")
    return json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUS","Status": "Success","StatusCode": "200"},indent = 4)

def Query_Foodandbeverage_Request(request):
    
    d=request.json
    list1,finals = [],[]
    current_datetime=application_datetime().date()
    details = json.loads(dbget("select guest_profile.guest_name,foodandbeverage_items.item_name,fb_collection.quantity,foodandbeverage_items.item_description,\
                foodandbeverage_items.price,foodandbeverage_items.item_image,\
                foodandbeverage_items.item_createdon,foodandbeverage_items.dept_id,food_category.*,foodtype.*,todayspecial.*,fb_requests.* from fb_requests \
                join fb_collection on fb_collection.fbcollection_id = fb_requests.fbcollection_id\
                join foodandbeverage_items  on fb_collection.fbitem_id = foodandbeverage_items.fbitem_id\
                join food_category  on foodandbeverage_items.foodcategory_id = food_category.foodcateg_id\
                join foodtype on foodandbeverage_items.foodtype_id = foodtype.foodtype_id\
                join todayspecial on foodandbeverage_items.todayspecial_id =todayspecial.todayspecial_id\
                join guest_details  on guest_details.room_no = fb_requests.room_no\
                join guest_profile on guest_profile.mobile = guest_details.mobile_no\
                where fb_requests.business_id='"+str(d['business_id'])+"'\
                and date(request_time) = '"+str(current_datetime)+"' "))
    print(details)
    for detail in details:
        if detail['ticket_no'] not in list1:
            #print(list1)
            list1.append(detail['ticket_no'])
            finals.append({"ticket_no":detail['ticket_no'],"room_no":detail['room_no'],"total_amount":detail['total_amount'],"guest_name":detail['guest_name'],"food_items":[]})
    for final in finals:
        for detail in details:
            if detail['ticket_no'] == final['ticket_no']:
                final['food_items'].append(detail)
    
    return json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS","Returnvalue":finals,"Status": "Success","StatusCode": "200"},indent = 4)



