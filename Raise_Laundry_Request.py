from sqlwrapper import *
import re
from Fetch_Current_Datetime import *

def Raise_lanudry_request(request):
    d=request.json
    list1 = []
    order_no = json.loads(dbget("SELECT array_to_string(ARRAY(SELECT chr((48 + round(random() * 9)) :: integer) \
                                FROM generate_series(1,10)), '');"))
    print(order_no)
    for item in d['lan_items']:
        list1.append(tuple((order_no[0]['array_to_string'],item['ldryitem_id'],item['quantity'])))
    values = ', '.join(map(str, list1))
    dbput("INSERT INTO  ldry_collection (ldrycollection_id, ldryitem_id, quantity)VALUES {}".format(values))
                
    local_tz = pytz.timezone('Asia/Tokyo')

    start_date = local_tz.localize(datetime(2012, 9, 27), is_dst=None)
    now_utc = datetime.utcnow().replace(tzinfo=pytz.utc)

    ticket_no = str(now_utc.strftime("%Y-%m-%d%H:%M:%S"))+str(d['room_no'])+'foo2106'+str(order_no[0]['array_to_string'])
    
    d.update({'reminder_count':0,'escalation_count':0,
              'ticketstatus_id':1,'request_time':str(now_utc.strftime("%Y-%m-%d %H:%M:%S")),
              'ticket_no':re.sub("-|:","",ticket_no),'ldrycollect_id':order_no[0]['array_to_string'],'ldryitem_count':d['ldryitem_count'],'total_amount':d['total_amount']})
    print(d)
    d={k:v for k,v in d.items() if k not in ('lan_items')}
    gensql('insert','ldry_request',d)
    return json.dumps({"Return": "Record Inserted Successfully","ReturnCode": "RIS","Status": "Success","StatusCode": "200"},indent = 4)

def Close_Laundry_Request(request):
    
    
    d=request.json
    dbput("update ldry_request set ticketstatus_id='2' where ticket_no='"+str(d['ticket_no'])+"'")
    return json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUS","Status": "Success","StatusCode": "200"},indent = 4)

def Query_laundry_Request(request):
    d=request.json
    list1,finals = [],[]
    details = json.loads(dbget("select r.*,c.quantity,l.ldryitem_name,l.ldryitem_image,\
                               l.ldryitem_description,l.price,l.dept_id,lc.* from ldry_request r \
                               join ldry_collection c on r.ldrycollect_id = c.ldrycollection_id\
                               join laundry_items l on c.ldryitem_id = l.ldryitem_id\
                               join laundry_category lc on l.ldrycateg_id = lc.ldrycateg_id\
                               where r.business_id='"+str(d['business_id'])+"'"))
    
    for detail in details:
        if detail['ticket_no'] not in list1:
            #print(list1)
            list1.append(detail['ticket_no'])
            finals.append({"ticket_no":detail['ticket_no'],"lan_items":[]})
    for final in finals:
        for detail in details:
            if detail['ticket_no'] == final['ticket_no']:
                final['lan_items'].append(detail)
    
    return json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS","Returnvalue":finals,"Status": "Success","StatusCode": "200"},indent = 4)





