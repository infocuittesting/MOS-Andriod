from sqlwrapper import *
import re
from Fetch_Current_Datetime import *
def Raise_Foodandbeverage_Request(request):
    d=request.json
    current_datetime=application_datetime()
    ticket_no = str(current_datetime.strftime("%Y-%m-%d%H:%M:%S"))+str(d['room_no'])+'foo2106'+str(d['fbitem_id'])
    
    d.update({'reminder_count':0,'escalation_count':0,
              'ticketstatus_id':1,'request_time':str(current_datetime.strftime("%Y-%m-%d %H:%M:%S")),
              'ticket_no':re.sub("-|:","",ticket_no)})
    gensql('insert','fb_requests',d)
    return json.dumps({"Return": "Record Inserted Successfully","ReturnCode": "RIS","Status": "Success","StatusCode": "200"},indent = 4)

    
    
def Close_Foodandbeverage_Request(request):
    
    
    d=request.json
    dbput("update fb_requests set ticketstatus_id='2' where ticket_no='"+str(d['ticket_no'])+"'")
    return json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUS","Status": "Success","StatusCode": "200"},indent = 4)

def Query_Foodandbeverage_Request(request):
    
    d=request.json
    details = json.loads(dbget("select f.item_name,f.item_description,f.price,f.item_image,f.item_createdon,f.dept_id,c.*,t.*,s.*,r.* from fb_requests r\
    join foodandbeverage_items f  on r.fbitem_id = f.fbitem_id\
    join food_category c on f.foodcategory_id = c.foodcateg_id\
    join foodtype t on f.foodtype_id = t.foodtype_id\
    join todayspecial s on f.todayspecial_id = s.todayspecial_id\
    where r.business_id='"+str(d['business_id'])+"' "))
    return json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS","Returnvalue":details,"Status": "Success","StatusCode": "200"},indent = 4)



