from sqlwrapper import *
import re
from Fetch_Current_Datetime import *
import collections
def Raise_Front_Desk_Request(request):
    d=request.json
    current_datetime=application_datetime()
    ticket_no = str(current_datetime.strftime("%Y-%m-%d%H:%M:%S"))+str(d['room_no'])+'fro1494'+str(d['fditem_id'])
    
    d.update({'reminder_count':0,'escalation_count':0,
              'ticketstatus_id':1,'request_time':str(current_datetime.strftime("%Y-%m-%d %H:%M:%S")),
              'ticket_no':re.sub("-|:","",ticket_no)})
    gensql('insert','fd_requests',d)
    return json.dumps({"Return": "Record Inserted Successfully","ReturnCode": "RIS","Status": "Success","StatusCode": "200"},indent = 4)

    
    
def Close_Front_Desk_Request(request):
    
    
    d=request.json
    dbput("update fd_requests set ticketstatus_id='2' where ticket_no='"+str(d['ticket_no'])+"'")
    return json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUS","Status": "Success","StatusCode": "200"},indent = 4)

def Query_Front_Desk_Request(request):
    
    d=request.json
    current_datetime=application_datetime().date()
    details = json.loads(dbget("select guest_profile.guest_name, ticketstatus,fdcategory_name,fdcategory_image,fditem_names,fditem_image,fd_requests.* from fd_requests\
				join frontdesk_items on frontdesk_items.fditem_id=fd_requests.fditem_id\
				join fdcategory on fdcategory.fdcategory_id = frontdesk_items.fdcategory_id\
				join ticket_status on ticket_status.ticketstatus_id = fd_requests.ticketstatus_id\
				join guest_details  on guest_details.room_no = fd_requests.room_no\
                                join guest_profile on guest_profile.mobile = guest_details.mobile_no\
			where fd_requests.business_id='"+d['business_id']+"' and frontdesk_items.business_id='"+d['business_id']+"' \
                        and fdcategory.business_id='"+d['business_id']+"' and date(request_time) = '"+str(current_datetime)+"'"))
    return json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS","Returnvalue":details,"Status": "Success","StatusCode": "200"},indent = 4)
def  Query_Categorywise_Front_Desk_Request(request):
    d=request.json
    finals = []
    current_datetime=application_datetime().date()
    details = json.loads(dbget("select guest_profile.guest_name,ticketstatus,fdcategory_name,fdcategory_image,fditem_names,fditem_image,fd_requests.* from fd_requests\
				join frontdesk_items on frontdesk_items.fditem_id=fd_requests.fditem_id\
				join fdcategory on fdcategory.fdcategory_id = frontdesk_items.fdcategory_id\
				join ticket_status on ticket_status.ticketstatus_id = fd_requests.ticketstatus_id\
				join guest_details  on guest_details.room_no = fd_requests.room_no\
                                join guest_profile on guest_profile.mobile = guest_details.mobile_no\
			where fd_requests.business_id='"+d['business_id']+"' and frontdesk_items.business_id='"+d['business_id']+"' \
                        and fdcategory.business_id='"+d['business_id']+"' and date(request_time) = '"+str(current_datetime)+"'"))
    grouped = collections.defaultdict(list)
    for item in details:
        
        grouped[item['fdcategory_name']].append(item)

    #print(grouped)
    #for model, group in grouped.items():
    #print
    #print model
    #pprint(group, width=150)
      # finals.append({"fdcategory_name":model,"frontdesk_items":group})
    return json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS","Returnvalue":grouped,"Status": "Success","StatusCode": "200"},indent = 4)
