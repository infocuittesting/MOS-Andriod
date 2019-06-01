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
def Display_Food_Menu_For_Android(request):
    d = request.json
    food_details,food_menu_details = [],[]
    GET_FOOD_MENUS = json.loads(dbget("select foodtype.*,food_category.*,foodandbeverage_items.* from foodandbeverage_items\
                                          join food_category on food_category.foodcateg_id = foodandbeverage_items.foodcategory_id \
                                          join foodtype on foodtype.foodtype_id = foodandbeverage_items.foodtype_id\
                                          where foodandbeverage_items.business_id = '"+str(d['business_id'])+"' "))
       #get_best_sellers = json.loads(dbget(""))
    for food_menu in GET_FOOD_MENUS:
          if food_menu['foodcateg_name'] not in food_details:
             food_details.append(food_menu['foodcateg_name'])
             food_menu_details.append({"categry_name":food_menu['foodcateg_name'],"category_img":food_menu['foodcateg_image'],"items":[]})
    for food_menu in GET_FOOD_MENUS:
          for food_menu_detail in food_menu_details:
            
             if food_menu['foodcateg_name'] ==food_menu_detail['categry_name']:
                food_menu['item_images'] = [{"item_image":food_menu['item_image']}]
                food_menu_detail["items"].append(food_menu)
    get_best_sellers= json.loads(dbget("select count(*),\
                                       foodandbeverage_items.fbitem_id,foodandbeverage_items.item_name,\
                                       foodandbeverage_items.item_image,foodandbeverage_items.price,foodandbeverage_items.foodtype_id,\
                                       foodandbeverage_items.todayspecial_id,foodandbeverage_items.business_id,\
                                       food_category.foodcateg_name,food_category.foodcateg_id,\
                                       food_category.foodcateg_image,foodtype.foodtype_name,todayspecial.special from fb_collection\
                                       join foodandbeverage_items on foodandbeverage_items.fbitem_id=fb_collection.fbitem_id\
                                       join food_category on foodandbeverage_items.foodcategory_id=food_category.foodcateg_id\
                                       join foodtype on foodandbeverage_items.foodtype_id=foodtype.foodtype_id\
                                       join todayspecial on foodandbeverage_items.todayspecial_id=todayspecial.todayspecial_id\
                                       where foodandbeverage_items.business_id='"+str(d['business_id'])+"'\
                                       group by food_category.foodcateg_name,food_category.foodcateg_image,foodtype.foodtype_name,todayspecial.special,\
                                       foodandbeverage_items.fbitem_id,foodandbeverage_items.item_name,food_category.foodcateg_id,\
                                       foodandbeverage_items.item_image,foodandbeverage_items.price,foodandbeverage_items.foodtype_id,\
                                       foodandbeverage_items.todayspecial_id,foodandbeverage_items.business_id\
                                       order by count desc"))
    k = [x['foodcateg_name'] for x in get_best_sellers]

    new_vals=[]

    for i in Counter(k):
           all_values = [x for x in get_best_sellers if x['foodcateg_name']==i]
           #all_values['']
           #print("all",all_values)
           new_vals.append(max(all_values, key=lambda x: x['count']))    
    specials = json.loads(dbget("select food_category.foodcateg_id,food_category.foodcateg_name,food_category.foodcateg_image,foodandbeverage_items.*,\
                                    todayspecial.special,\
                                    foodtype.foodtype_id,foodtype.foodtype_name\
                                    from foodandbeverage_items\
                                    join todayspecial on foodandbeverage_items.todayspecial_id = todayspecial.todayspecial_id \
                                    join food_category on food_category.foodcateg_id= foodandbeverage_items.foodcategory_id\
                                    join foodtype on foodtype.foodtype_id = foodandbeverage_items.foodtype_id\
                                    where foodandbeverage_items.todayspecial_id=1"))
    
    final_get_best_sellers_menu = [dict(item, item_images=[dict(item_image=item['item_image'])]) for item in new_vals]
    today_specials = [dict(special, item_image=[dict(image_url=special['item_image'])]) for special in specials]
    final_food_menu = [{"Food_Category":food_menu_details,
                          "Best_Sellers":final_get_best_sellers_menu,
                          "Today_Special":{"categry_name":"Today_Specials",
                                           "category_img":"https://s3.amazonaws.com/image-upload-rekognition/tosfoodimages/new_work_cadillacmagazine-624x406.png",
                                           "items":today_specials}}]

    return json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS","Returnvalue":final_food_menu,"Status": "Success","StatusCode": "200"},indent = 4)







