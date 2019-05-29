from sqlwrapper import *
import random
from Fetch_Current_Datetime import *
import requests
def Foodandbeverage_Items(request):
    d = request.json
    d.update({'dept_id':'foo2106'})
    check_item = json.loads(dbget("select count(*) from foodandbeverage_items \
                                     where business_id='"+str(d['business_id'])+"' and item_name= '"+str(d['item_name'].title())+"'"))
    if check_item[0]['count'] == 0:
        get_category = json.loads(dbget("select count(*) from food_category \
                                     where business_id='"+str(d['business_id'])+"' and foodcateg_name = '"+str(d['foodcateg_name'].title())+"'"))
        #upload item image
        if len(d['item_image']) != 0:
                r = requests.post("https://k746kt3782.execute-api.us-east-1.amazonaws.com/mos-android_imageupload",json={"base64":d['item_image'],"branch_name":d['branch_name']})
                data = r.json()
                d['item_image'] = data['body']['url']
        else:
            pass
        #insert food category
    
        if get_category[0]['count'] == 0:
            #upload image for food category
            if len(d['foodcateg_image']) != 0:
                r = requests.post("https://k746kt3782.execute-api.us-east-1.amazonaws.com/mos-android_imageupload",json={"base64":d['foodcateg_image'],"branch_name":d['branch_name']})
                data = r.json()
                d['foodcateg_image'] = data['body']['url']
            else:
                pass
            #insert food category
            s={"foodcateg_id":(d['foodcateg_name'][:3]+str(random.randint(1000,3000))).lower(),
               "foodcateg_name":d['foodcateg_name'].title(),
               "foodcateg_image":d['foodcateg_image'],
               "business_id":d['business_id']}
            s = {k:v for k,v in s.items() if v!= ""}
            catogory = gensql('insert','food_category',s)
            print("if_catogory",catogory)

       
        
            d.update({'fbitem_id': (d['item_name'][:3]+str(random.randint(1000,3000))).lower(),"foodcategory_id":s['foodcateg_id'],"item_name":d['item_name'].title(),"item_createdon":str(application_datetime())})
            d = {k:v for k,v in d.items() if v!= "" if k not in ('foodcateg_name','foodcateg_image','branch_name')}
            insert_item = gensql('insert','foodandbeverage_items',d)
            print("if_insert item:",insert_item)
        else:
            print("ssssssssssssssssssssssssssssssss")
            d.update({'fbitem_id': (d['item_name'][:3]+str(random.randint(1000,3000))).lower(),"foodcategory_id":str(d['foodcateg_id']),"item_name":d['item_name'].title(),"item_createdon":str(application_datetime())})
            d = {k:v for k,v in d.items() if v!= "" if k not in ('foodcateg_name','foodcateg_image','foodcateg_id','branch_name')}
            insert_item = gensql('insert','foodandbeverage_items',d)
        print("else_insert item:",insert_item)
    #return json.dumps({"Retun":d},indent=4)

        return json.dumps({"Return": "Record Inserted Successfully","ReturnCode": "RIS","Status": "Success","StatusCode": "200"},indent = 4)
    else:
        return json.dumps({"Return": "Record Already Inserted ","ReturnCode": "RAI","Status": "Success","StatusCode": "200"},indent = 4)

def Select_Foodandbeverage_Items(request):
    d = request.json
    rooms = json.loads(dbget("select f.item_name,f.business_id,f.dept_id,f.item_description,f.price,f.foodtype_id,f.todayspecial_id,\
    f.fbitem_id,f.foodcategory_id,f.item_createdon,o.foodcateg_name,o.foodcateg_image,\
    h.dept_name,h.dept_image,t.foodtype_name,s.special from foodandbeverage_items f \
    join food_category o on f.foodcategory_id = o.foodcateg_id\
    join hotel_department h on f.dept_id = h.dept_id\
    join foodtype t on f.foodtype_id = t.foodtype_id\
    join todayspecial s on  f.todayspecial_id = s.todayspecial_id\
    where f.business_id = '"+str(d['business_id'])+"'"))
    
    return json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS","ReturnValue":rooms,"Status": "Success","StatusCode": "200"},indent = 4)


def Update_Foodandbeverage_Items(request):
    d = request.json
    d.update({'foodcateg_name':d['foodcateg_name'].title(),"item_name":d['item_name'].title()})
    print(d)
    if len(d['foodcateg_image']) != 0:
                r = requests.post("https://k746kt3782.execute-api.us-east-1.amazonaws.com/mos-android_imageupload",json={"base64":d['foodcateg_image'],"branch_name":d['branch_name']})
                data = r.json()
                d['foodcateg_image'] = data['body']['url']
                print("length ",len(d['foodcateg_image']))
    else:
        pass

    b={k : v for k,v in d.items() if k in ('foodcateg_name','foodcateg_image')}
    c={ k : v for k,v in d.items() if k in('foodcateg_id','business_id')}
    sql=gensql('update','food_category',b,c)

    if len(d['item_image']) != 0:
                r = requests.post("https://k746kt3782.execute-api.us-east-1.amazonaws.com/mos-android_imageupload",json={"base64":d['item_image'],"branch_name":d['branch_name']})
                data = r.json()
                d['item_image'] = data['body']['url']
                print("length ",len(d['item_image']))
    else:
        pass
    
    b={k : v for k,v in d.items() if k in ('item_name','foodcategory_id','item_description','price','foodtype_id','todayspecial_id','item_image')}
    c={ k : v for k,v in d.items() if k in('fbitem_id','business_id')}
    sql=gensql('update','foodandbeverage_items',b,c)
    return json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUS","Status": "Success","StatusCode": "200"},indent = 4)       



