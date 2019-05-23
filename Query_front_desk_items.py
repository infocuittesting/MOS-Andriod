from sqlwrapper import *
import random
import requests



def Select_Travel_Desk_Items(request):
    d = request.json
    output = json.loads(dbget("select fdcategory.fdcategory_id,fdcategory.fdcategory_name,fdcategory.fdcategory_image,frontdesk_items.fditem_id,\
                               frontdesk_items.fditem_names,frontdesk_items.fditem_image,\
                               frontdesk_items.dept_id fdcategory,hotel_department.dept_name,hotel_department.dept_image from frontdesk_items \
                               join  fdcategory on frontdesk_items.fdcategory_id=fdcategory.fdcategory_id \
                               join  hotel_department on frontdesk_items.dept_id=hotel_department.dept_id\
                               where frontdesk_items.business_id='"+str(d['business_id'])+"' and frontdesk_items.fdcategory_id= 'tra2095'"))
    return(json.dumps({"Message":"Record Selected Successfully","Message_Code":"RSS","Service_Status":"Success","output":output},indent=4))


def Select_FrontDesk_Items(request):
    d = request.json
    output = json.loads(dbget("select fdcategory.fdcategory_id,fdcategory.fdcategory_name,fdcategory.fdcategory_image,frontdesk_items.fditem_id,\
                               frontdesk_items.fditem_names,frontdesk_items.fditem_image,\
                               frontdesk_items.dept_id fdcategory,hotel_department.dept_name,hotel_department.dept_image from frontdesk_items \
                               join  fdcategory on frontdesk_items.fdcategory_id=fdcategory.fdcategory_id \
                               join  hotel_department on frontdesk_items.dept_id=hotel_department.dept_id\
                               where frontdesk_items.business_id='"+str(d['business_id'])+"' and frontdesk_items.fdcategory_id= 'fro2219'"))
    return(json.dumps({"Message":"Record Selected Successfully","Message_Code":"RSS","Service_Status":"Success","output":output},indent=4))

def Select_Extra_Items(request):
    d = request.json
    output = json.loads(dbget("select fdcategory.fdcategory_id,fdcategory.fdcategory_name,fdcategory.fdcategory_image,frontdesk_items.fditem_id,\
                               frontdesk_items.fditem_names,frontdesk_items.fditem_image,\
                               frontdesk_items.dept_id fdcategory,hotel_department.dept_name,hotel_department.dept_image from frontdesk_items \
                               join  fdcategory on frontdesk_items.fdcategory_id=fdcategory.fdcategory_id \
                               join  hotel_department on frontdesk_items.dept_id=hotel_department.dept_id\
                               where frontdesk_items.business_id='"+str(d['business_id'])+"' and frontdesk_items.fdcategory_id= 'ext1478'"))
    return(json.dumps({"Message":"Record Selected Successfully","Message_Code":"RSS","Service_Status":"Success","output":output},indent=4))

