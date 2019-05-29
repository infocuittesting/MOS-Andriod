from sqlwrapper import *
import random
import requests
import collections

def Insert_Housekeeping_Item(request):
    d = request.json
    check_item = json.loads(dbget("select count(*) from housekeeping_items \
                                     where business_id='"+str(d['business_id'])+"' and hkitem_name= '"+str(d['hkitem_name'].title())+"'"))
    if len(d['hkitem_image']) != 0:
                r = requests.post("https://k746kt3782.execute-api.us-east-1.amazonaws.com/mos-android_imageupload",json={"base64":d['hkitem_image'],"branch_name":d['branch_name']})
                data = r.json()
                d['hkitem_image'] = data['body']['url']
    else:
        pass
    if check_item[0]['count'] == 0:
        d.update({'hkitem_id': (str(d['hkitem_name'][:3]) +str(random.randint(100,300))).lower(),'hkitem_name':d['hkitem_name'].title()})
        a = {k:v for k,v in d.items() if v is not None if k not in ('branch_name')}
        gensql('insert','housekeeping_items',a)
        return json.dumps({"Return": "Record Inserted Successfully","ReturnCode": "RIS","Status": "Success","StatusCode": "200"},indent = 4)
    else:
        return json.dumps({"Return": "Record Already Inserted ","ReturnCode": "RAI","Status": "Success","StatusCode": "200"},indent = 4)

def Select_Housekeeping_Item(request):
    d= request.json
    finals = []
    output = json.loads(dbget("select housekeeping_items.*, housekeeping_category.hkcateg_name,\
                    housekeeping_category.hkcateg_image\
                    from housekeeping_items join  housekeeping_category on \
                    housekeeping_items.hkitemcateg_id=housekeeping_category.hkcateg_id where housekeeping_items.business_id='"+str(d['business_id'])+"' "))
    grouped = collections.defaultdict(list)
    for item in output:
        
        grouped[item['hkcateg_name']].append(item)

    print(grouped)
    for model, group in grouped.items():
    #print
    #print model
    #pprint(group, width=150)
       finals.append({"hkcateg_name":model,"housekeeping_items":group})
    return(json.dumps({"Message":"Record Selected Successfully","Message_Code":"RSS","Service_Status":"Success","output":finals},indent=4))

def Update_Housekeeping_Item(request):
    d= request.json
    if len(d['hkitem_image']) != 0:
                r = requests.post("https://k746kt3782.execute-api.us-east-1.amazonaws.com/mos-android_imageupload",json={"base64":d['hkitem_image'],"branch_name":d['branch_name']})
                data = r.json()
                d['hkitem_image'] = data['body']['url']
    else:
        pass
    b={k : v for k,v in d.items() if k in ('hkitem_image','hkitem_name','hkitemcateg_id')}
    c={ k : v for k,v in d.items() if k in('business_id','hkitem_id')}
    sql=gensql('update','housekeeping_items',b,c)
    return json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUS","Status": "Success","StatusCode": "200"},indent = 4)

def Select_Housekeeping_Item_for_angular(request):
    d= request.json
  
    output = json.loads(dbget("select housekeeping_items.*, housekeeping_category.hkcateg_name,\
                    housekeeping_category.hkcateg_image\
                    from housekeeping_items join  housekeeping_category on \
                    housekeeping_items.hkitemcateg_id=housekeeping_category.hkcateg_id where housekeeping_items.business_id='"+str(d['business_id'])+"' "))
    return(json.dumps({"Message":"Record Selected Successfully","Message_Code":"RSS","Service_Status":"Success","output":output},indent=4))


    

