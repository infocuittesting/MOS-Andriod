from sqlwrapper import *
from collections import defaultdict
def room_no_report(request):
    print("success")
    d= request.json
#-----------------------Room based Report-------------------------------------------------#
    hkrequest = json.loads(dbget("select room_no, count(*) from hk_requests \
      where date(request_time) between '"+d['datefrom']+"' and '"+d['dateto']+"' and business_id ='"+d['business_id']+"' group by room_no"))
    
    
    fdrequest = json.loads(dbget("select room_no, count(*) from  fd_requests  \
	 where date(request_time) between '"+d['datefrom']+"' and '"+d['dateto']+"' and business_id ='"+d['business_id']+"' group by room_no"))

   
    fbrequest = json.loads(dbget("select room_no, count(*) from fb_requests \
	  where date(request_time) between '"+d['datefrom']+"' and '"+d['dateto']+"' and business_id ='"+d['business_id']+"' group by room_no"))

    laundry_request = json.loads(dbget("select room_no,count(*) from ldry_request where date(request_time)\
                                         between '"+d['datefrom']+"' and '"+d['dateto']+"' and business_id= '"+d['business_id']+"' group by room_no"))
    final_request=hkrequest+fdrequest+fbrequest+laundry_request
    c = defaultdict(int)
    for s in final_request:
                        c[s['room_no']] += s['count']
    finals = [{'room_no': k ,'Count': v} for k,v in c.items()]
    print("mohannnnnnnnnnnnnnnnnnnnnnnnnnnnn")
#-------------------------department_report---------------------------#
    fbrequest1 = json.loads(dbget("select hotel_department.dept_name as department ,count(*) from fb_requests \
                                  join fb_collection on fb_collection.fbcollection_id = fb_requests.fbcollection_id\
                                  join foodandbeverage_items on foodandbeverage_items.fbitem_id=fb_collection.fbitem_id\
                                  join food_category on food_category.foodcateg_id = foodandbeverage_items.foodcategory_id \
                                  join hotel_department on hotel_department.dept_id=foodandbeverage_items.dept_id where \
                                  date(request_time) between '"+d['datefrom']+"' and '"+d['dateto']+"' and \
                                  fb_requests.business_id ='"+d['business_id']+"' group by hotel_department.dept_name"))

    hk_request1=json.loads(dbget("select housekeeping_category.hkcateg_name as department,count(*) from hk_requests\
      join housekeeping_items on housekeeping_items.hkitem_id = hk_requests.hkitem_id\
      join housekeeping_category on housekeeping_category.hkcateg_id = housekeeping_items.hkitemcateg_id\
      where date(request_time) between '"+d['datefrom']+"' and '"+d['dateto']+"' and hk_requests.business_id ='"+d['business_id']+"'\
      group by housekeeping_category.hkcateg_name"))

    fd_request1=json.loads(dbget("select fdcategory.fdcategory_name as department,count(*) from fd_requests\
      join frontdesk_items on frontdesk_items.fditem_id = fd_requests.fditem_id\
      join fdcategory on fdcategory.fdcategory_id = frontdesk_items.fdcategory_id\
      where date(request_time) between '"+d['datefrom']+"' and '"+d['dateto']+"' and \
      fd_requests.business_id ='"+d['business_id']+"' group by fdcategory.fdcategory_name"))

    laundry_request1 = json.loads(dbget("select hotel_department.dept_name as department ,count(*) from ldry_request \
                                  join ldry_collection on ldry_collection.ldrycollection_id = ldry_request.ldrycollect_id\
                                  join laundry_items on laundry_items.ldryitem_id=ldry_collection.ldryitem_id\
                                  join laundry_category on laundry_category.ldrycateg_id = laundry_items.ldrycateg_id \
                                  join hotel_department on hotel_department.dept_id=laundry_items.dept_id where \
                                  date(request_time) between '"+d['datefrom']+"' and '"+d['dateto']+"' and \
                                  ldry_request.business_id ='"+d['business_id']+"' group by hotel_department.dept_name"))
      
    
    dept_final=hk_request1+fbrequest1+fd_request1+laundry_request1
    
#----------------------------remainder_count_report---------------------------------------#  
    hkrequest2 = json.loads(dbget("select housekeeping_category.hkcateg_name as department,\
    (select count(reminder_count) as reminder_one from hk_requests where reminder_count=1),\
    (select count(reminder_count) as reminder_two from hk_requests where reminder_count=2)\
    from hk_requests\
    join housekeeping_items on housekeeping_items.hkitem_id = hk_requests.hkitem_id\
    join housekeeping_category on housekeeping_category.hkcateg_id = housekeeping_items.hkitemcateg_id\
    where date(request_time) between '"+d['datefrom']+"' and '"+d['dateto']+"' and\
    hk_requests.business_id ='"+d['business_id']+"'\
    group by housekeeping_category.hkcateg_name"))
    print(hkrequest2,'')

    fb_request2= json.loads(dbget("select hotel_department.dept_name as department,\
    (select count(reminder_count) as reminder_one from fb_requests where reminder_count=1),\
    (select count(reminder_count) as reminder_two from fb_requests where reminder_count=2)\
    from fb_requests\
     join fb_collection on fb_collection.fbcollection_id = fb_requests.fbcollection_id\
    join foodandbeverage_items on foodandbeverage_items.fbitem_id=fb_collection.fbitem_id\
    join hotel_department on hotel_department.dept_id=foodandbeverage_items.dept_id\
     where date(request_time) between '"+d['datefrom']+"' and '"+d['dateto']+"' and fb_requests.business_id ='"+d['business_id']+"'\
     group by hotel_department.dept_name"))\

    fd_request2=json.loads(dbget("select fdcategory.fdcategory_name as department,\
    (select count(reminder_count) as reminder_one from fd_requests where reminder_count=1),\
    (select count(reminder_count) as reminder_two from fd_requests where reminder_count=2) from fd_requests\
      join frontdesk_items on frontdesk_items.fditem_id = fd_requests.fditem_id\
      join fdcategory on fdcategory.fdcategory_id = frontdesk_items.fdcategory_id\
      where date(request_time) between '"+d['datefrom']+"' and '"+d['dateto']+"' \
      and fd_requests.business_id ='"+d['business_id']+"' group by fdcategory.fdcategory_name"))

    
    
    laundry_request2 = json.loads(dbget("select hotel_department.dept_name as department,\
    (select count(reminder_count) as reminder_one from ldry_request where reminder_count=1),\
    (select count(reminder_count) as reminder_two from ldry_request where reminder_count=2) from ldry_request\
    join ldry_collection on ldry_collection.ldrycollection_id = ldry_request.ldrycollect_id\
    join laundry_items on laundry_items.ldryitem_id=ldry_collection.ldryitem_id\
    join hotel_department on hotel_department.dept_id=laundry_items.dept_id\
      where date(request_time) between '"+d['datefrom']+"' and '"+d['dateto']+"' \
      and ldry_request.business_id ='"+d['business_id']+"' group by  hotel_department.dept_name"))

    remainder_report=hkrequest2+fb_request2+fd_request2+laundry_request2

#-----------------------Escalation_based_report---------------------#
    
    hkrequest3 = json.loads(dbget("select housekeeping_category.hkcateg_name as department,\
    (select count(escalation_count) as escalation_one from hk_requests where escalation_count=1),\
    (select count(escalation_count) as escalation_two from hk_requests where escalation_count=2)\
    from hk_requests\
    join housekeeping_items on housekeeping_items.hkitem_id = hk_requests.hkitem_id\
    join housekeeping_category on housekeeping_category.hkcateg_id = housekeeping_items.hkitemcateg_id\
    where date(request_time) between '"+d['datefrom']+"' and '"+d['dateto']+"' and\
    hk_requests.business_id ='"+d['business_id']+"'\
    group by housekeeping_category.hkcateg_name"))
    print(hkrequest2,'')

    fb_request3= json.loads(dbget("select hotel_department.dept_name as department,\
    (select count(escalation_count) as escalation_one from fb_requests where escalation_count=1),\
    (select count(escalation_count) as escalation_two from fb_requests where escalation_count=2)\
    from fb_requests\
    join fb_collection on fb_collection.fbcollection_id = fb_requests.fbcollection_id\
    join foodandbeverage_items on foodandbeverage_items.fbitem_id=fb_collection.fbitem_id\
    join hotel_department on hotel_department.dept_id=foodandbeverage_items.dept_id\
     where date(request_time) between '"+d['datefrom']+"' and '"+d['dateto']+"' and fb_requests.business_id ='"+d['business_id']+"'\
     group by hotel_department.dept_name"))

    fd_request3=json.loads(dbget("select fdcategory.fdcategory_name as department,\
    (select count(reminder_count) as reminder_one from fd_requests where reminder_count=1),\
    (select count(reminder_count) as reminder_two from fd_requests where reminder_count=2) from fd_requests\
      join frontdesk_items on frontdesk_items.fditem_id = fd_requests.fditem_id\
      join fdcategory on fdcategory.fdcategory_id = frontdesk_items.fdcategory_id\
      where date(request_time) between '"+d['datefrom']+"' and '"+d['dateto']+"' \
      and fd_requests.business_id ='"+d['business_id']+"' group by fdcategory.fdcategory_name"))

    laundry_request3 = json.loads(dbget("select hotel_department.dept_name as department,\
    (select count(escalation_count) as escalation_one from ldry_request where escalation_count=1),\
    (select count(escalation_count) as escalation_two from ldry_request where escalation_count=2) from ldry_request\
    join ldry_collection on ldry_collection.ldrycollection_id = ldry_request.ldrycollect_id\
    join laundry_items on laundry_items.ldryitem_id=ldry_collection.ldryitem_id\
    join hotel_department on hotel_department.dept_id=laundry_items.dept_id\
      where date(request_time) between '"+d['datefrom']+"' and '"+d['dateto']+"' \
      and ldry_request.business_id ='"+d['business_id']+"' group by hotel_department.dept_name"))

    esclation=fd_request3+fb_request3+hkrequest3+laundry_request3
    


    return (json.dumps({"Return": "Record Retrived Successfully",
                        "ReturnCode": "RRS",
                        "Room_based_report":finals,
                        "Department_based_report":dept_final,
                        "Remainder_based_report":remainder_report,
                        "Escalation_based_report":esclation,
                        "Status": "Success","StatusCode": "200"},indent=4))
   
#---------------------------department based request count----------------------#

 #------------------------------device based report-----------------------------#

def Week_Day_Report(request):

    today_date = datetime.datetime.today()
    #today_date = datetime.datetime(2019, 5, 27)
    day = today_date.weekday()
    print("today", today_date.weekday())
    if day == 0:
        start_date = today_date.date()
        end_date = (today_date + datetime.timedelta(days=6)).date()
    else:
        start_date = (today_date - datetime.timedelta(days=day)).date()
        end_date = (today_date + datetime.timedelta(days=6-day)).date()
    #print("st:",start_date,"ed:",end_date)
    #Days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    fb = json.loads(dbget("select to_char(date(request_time), 'Dy') as day,count(*) from fb_requests where date(request_time) \
                           between '"+str(start_date)+"' and '"+str(end_date)+"' group by date(request_time)"))

    hk = json.loads(dbget("select to_char(date(request_time), 'Dy') as day,count(*) from hk_requests where date(request_time) \
                               between '" +str(start_date)+ "' and '" +str(end_date)+ "' group by date(request_time)"))

    ldry = json.loads(dbget("select to_char(date(request_time), 'Dy') as day,count(*) from ldry_request where date(request_time) \
                                   between '" +str(start_date)+ "' and '" +str(end_date)+ "' group by date(request_time)"))

    fd = json.loads(dbget("select to_char(date(request_time), 'Dy') as day,count(*) from fd_requests where date(request_time) \
                                       between '" +str(start_date)+ "' and '" +str(end_date)+ "' group by date(request_time)"))
    day_count = [{'day':'Mon','count':0},{'day':'Tue','count':0},{'day':'Wed','count':0},{'day':'Thu','count':0},
                 {'day': 'Fri', 'count': 0},{'day':'Sat','count':0},{'day':'Sun','count':0}]
    for d in day_count:
        val = 0
        try:
          val = [f['count'] for f in fb if f['day'] == d['day'] if f['count']>val][0]
          d['department'] = "Food And Beverage"
        except:
            pass
        try:
          val = [f['count'] for f in hk if f['day'] == d['day'] if f['count']>val][0]
          d['department'] = "HouseKeeping"
        except:
            pass
        try:
          val = [f['count'] for f in ldry if f['day'] == d['day'] if f['count']>val][0]
          d['department'] = "Laundry"
        except:
            pass
        try:
          val = [f['count'] for f in fd if f['day'] == d['day'] if f['count']>val][0]
          d['department'] = "Front Desk"
        except:
            pass
        d['count'] = val


    #print('fd',day_count)
    return (json.dumps({"Return": "Record Retrived Successfully",
                        "ReturnCode": "RRS",
                        "ReturnValue":day_count,
                        "Status": "Success", "StatusCode": "200"}, indent=4))
#-------------------------------roombased report------------------------------#
def roombasedreport(request):
    d= request.json

    hkrequest = json.loads(dbget("select CAST(room_no AS varchar(10)) , count(*) from hk_requests \
      where date(request_time) between '"+d['datefrom']+"' and '"+d['dateto']+"' and business_id ='"+d['business_id']+"' group by room_no"))
    
    
    fdrequest = json.loads(dbget("select CAST(room_no AS varchar(10)), count(*) from  fd_requests  \
	 where date(request_time) between '"+d['datefrom']+"' and '"+d['dateto']+"' and business_id ='"+d['business_id']+"' group by room_no"))

   
    fbrequest = json.loads(dbget("select CAST(room_no AS varchar(10)), count(*) from fb_requests \
	  where date(request_time) between '"+d['datefrom']+"' and '"+d['dateto']+"' and business_id ='"+d['business_id']+"' group by room_no"))

    laundry_request = json.loads(dbget("select CAST(room_no AS varchar(10)),count(*) from ldry_request where date(request_time)\
                                         between '"+d['datefrom']+"' and '"+d['dateto']+"' and business_id= '"+d['business_id']+"' group by room_no"))
    
    final_request=hkrequest+fdrequest+fbrequest+laundry_request
    c = defaultdict(int)
    for s in final_request:
                        c[s['room_no']] += s['count']
    finals = [{'room_no': k ,'Count': v} for k,v in c.items()]
    print("mohannnnnnnnnnnnnnnnnnnnnnnnnnnnn")


    hkrequest1 = json.loads(dbget("select hk_requests.*,housekeeping_items.hkitem_name from hk_requests\
                                 join housekeeping_items on housekeeping_items.hkitem_id=hk_requests.hkitem_id \
      where date(request_time) between '"+d['datefrom']+"' and '"+d['dateto']+"' and hk_requests.business_id ='"+d['business_id']+"' "))
    
    hkrequest2 = [hk.update({'Department':'House Keeping','room_no':str(hk['room_no'])}) for hk in hkrequest1]
    print(hkrequest1)
    fdrequest1 = json.loads(dbget("select fd_requests.*,frontdesk_items.fditem_names from fd_requests  \
                                    join frontdesk_items on frontdesk_items.fditem_id=fd_requests.fditem_id\
                                    where date(request_time) between '"+d['datefrom']+"' and '"+d['dateto']+"' and fd_requests.business_id ='"+d['business_id']+"' "))
    fdrequest2 = [hk.update({'Department':'Front Desk','room_no':str(hk['room_no'])})  for hk in fdrequest1]
   
    fbrequest1 = json.loads(dbget("select * from fb_requests \
	  where date(request_time) between '"+d['datefrom']+"' and '"+d['dateto']+"' and business_id ='"+d['business_id']+"' "))
    fbrequest2 = [hk.update({'Department':'Food And Beverage','room_no':str(hk['room_no'])})for hk in fbrequest1]

    laundry_request1= json.loads(dbget("select * from ldry_request where date(request_time)\
                                         between '"+d['datefrom']+"' and '"+d['dateto']+"' and business_id= '"+d['business_id']+"' "))
    
    laundry_request2 = [hk.update({'Department':'Laundry','room_no':str(hk['room_no'])})for hk in laundry_request1]
    
    final_request1=hkrequest1+fdrequest1+fbrequest1+laundry_request1
    return (json.dumps({"Return": "Record Retrived Successfully",
                        "ReturnCode": "RRS",
                        "Room_based_report":finals,
                        "Room_details":final_request1,
                        "Status": "Success","StatusCode": "200"},indent=4))
#--------------------------------------------departmentbased_report------------------------------#
import datetime

def complete_count(hkre,st,n):
    y = 0
    #for x in hkre:
    #    print(x,st,n)
    #    if x['date'] == str(st) and x['ticketstatus_id'] == n:
    #        y = x['count']
    #        break
    y = list(filter(lambda x: x['date'] == str(st) and  x['ticketstatus_id'] == n, hkre))
    if len(y) == 0:
        return 0
    else:
        return (y[0]['count']) 

    
def departmentbasedreport(request):
    d=request.json
    hkrequest3=json.loads(dbget("select date(request_time),ticketstatus_id ,count(*) from "+d['department']+" where\
                             request_time between '"+d['datefrom']+"' and '"+d['dateto']+"' and business_id= '"+d['business_id']+"'\
                                 group by ticketstatus_id, date(request_time) order by date"))
    print(hkrequest3)
    st_date = datetime.datetime.strptime(d['datefrom'], '%Y-%m-%d').date()
    ed_date = datetime.datetime.strptime(d['dateto'], '%Y-%m-%d').date()
    dep_count_report = []
    #complete_count = filter(lambda x: x.ticketstatus_id == 2,  hkrequest3)
    #pending_count = filter(lambda x: x.ticketstatus_id == 1,  hkrequest3)
    while st_date <= ed_date:
        print(st_date)
        dep_count_report.append({'date':str(st_date.strftime('%b %d')),
                                'Completed': complete_count(hkrequest3,st_date,n=2),
                                'Pending': complete_count(hkrequest3,st_date,n=1)
                                })
        
        st_date+=datetime.timedelta(days=1)
    #print(dep_count_report)
    remainder_count=json.loads(dbget("select reminder_count, escalation_count from "+d['department']+" where \
                                     date(request_time) between '"+d['datefrom']+"' and '"+d['dateto']+"' "))

    r1, r2, e1, e2 = 0,0,0,0
    for x in remainder_count:
        if x['reminder_count'] == 1:
            r1+=1
        elif x['reminder_count'] == 2:
            r2+=1
        if x['escalation_count'] == 1:
            e1+=1
        elif x['escalation_count'] == 2:
            e2+=1
            
    return(json.dumps({"Return": "Record Retrived Successfully",
                        "ReturnCode": "RRS",
                        "Department": d['department'],
                                'status_report':dep_count_report,
                                'Reminder':[{
                                    'reminder1':'reminder1',
                                    'count':r1 
                                    },
                                    {
                                    'reminder1':'reminder2',
                                    'count':r2    
                                        }],        
                                'escalation':[
                                    {
                                     "Escalation1": "Escalation1",
                                     "count": e1
                                     },{
                                     "Escalation1": "Escalation2",
                                     "count": e2
                                    }
                                    ],
                                
                                
                        "Status": "Success","StatusCode": "200"},indent=4))
    

