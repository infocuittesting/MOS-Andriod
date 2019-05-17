from flask import Flask,request
from flask_cors import CORS


app = Flask(__name__) #here i set environment varible for flask framework web application
CORS(app)
#-----------------------Configuration-------------------
from Signup_Details import *
from Frontdesk_Request import *
from Raise_Front_Desk_Request import *
from GuestDetails import *
from HouseKeeping_Request import *
from room_configuration import *
from hotel_contact import *
from housekeeping_configuration import *

from configure_hotelrooms import *
from configure_hotelDepartment import *
from configure_foodandbeverage import *
from Raise_Foodandbeverage_Request import * 
#below i set path for web application

@app.route("/",methods=['GET','POST'])
def mos_index():
    return "Hello mos Manager"

#@TOS.route("/<string:name>",methods=['GET','POST'])
#def pass_param(name):
   # return (name)
#-----------hotel signup details--------------

@app.route("/Hotel_Signup_Details",methods=['POST'])
def sigupdetail():
    return Hotel_Signup_Details(request)


@app.route("/Query_Hotel_Signup_Details",methods=['GET'])
def querysigupdetail():
    return Query_Hotel_Signup_Details(request)


@app.route("/Configure_Front_Desk_Items",methods=['POST'])
def frontdeskservice():
    return Configure_Front_Desk_Items(request)

@app.route("/Update_Front_Desk_Items",methods=['POST'])
def updatefrontdeskitems():
    return Update_Front_Desk_Items(request)

#----------------configuration----------#

@app.route("/Update_Roomtype",methods=['POST'])
def updateroomtype():
    return update_room_type(request)

@app.route("/Insert_Roomtype",methods=['POST'])
def insertroomtype():
    return insert_room(request)

@app.route("/Select_Room_Type",methods=['POST'])
def selectroomtype():
   return select_room(request)

@app.route("/Insert_Contact_Number",methods=['POST'])
def insertcontactnumber():
    return insert_number(request)

@app.route("/Select_Contact_Number",methods=['POST'])
def selectcontactnumber():
    return select_number(request)

@app.route("/Delete_Contact_Number",methods=['POST'])
def deletecontactnumber():
    return delete_number(request)
@app.route("/Insert_Housekeeping_Item",methods=['POST'])
def housekeepingitem():
   return insert_housekeeping_items(request)

@app.route("/Select_Housekeeping_Item",methods=['POST'])
def selecthousekeepingitem():
   return select_housekeeping_items(request)

@app.route("/Update_Housekeeping_Item",methods=['POST'])
def updatehousekeepingitem():
   return update_housekeeping_items(request)
#configure hotel rooms*******************************

@app.route("/Insert_Hotel_room",methods=['POST'])
def hotelroom():
    return insert_hotelrooms(request)

@app.route("/Select_Hotel_Room",methods=['POST'])
def hotel_room():
    return select_hotelrooms(request)

@app.route("/Update_Room_Status",methods=['POST'])
def hotel_rooms():
    return update_roomlogin(request)

#****************department***************

@app.route("/Insert_Hotel_Department",methods=['POST'])
def hotel_department():
    return insert_hoteldepartment(request)

@app.route("/Update_Department_Status",methods=['POST'])
def update_department():
    return update_departmentlogin(request)

@app.route("/Update_Hotel_Department",methods=['POST'])
def update_departments():
    return update_hoteldepartment(request)

@app.route("/Select_Hotel_Department",methods=['POST'])
def select_department():
    return select_hoteldepartment(request)
#configure food and beverage******************************
@app.route("/Foodandbeverage_Items",methods=['POST'])
def foodandbeverage():
    return Configure_Foodandbeverage_Items(request)

@app.route("/Select_Foodandbeverage_Items",methods=['POST'])
def select_foodandbeverage():
    return select_Foodandbeverage_Items(request)

@app.route("/Update_Foodandbeverage_Items",methods=['POST'])
def update_foodandbeverage():
    return update_Foodandbeverage_Items(request)

#----------------------------------------------Raise Request

@app.route("/Raise_Front_Desk_Request",methods=['POST'])
def raisefrontoffice():
    return Raise_Front_Desk_Request(request)
@app.route("/Close_Front_Desk_Request",methods=['POST'])
def closefrontoffce():
    return Close_Front_Desk_Request(request)
@app.route("/Query_Front_Desk_Request",methods=['POST'])
def selectfrontoffice():
    return Query_Front_Desk_Request(request)

@app.route("/Raise_Foodandbeverage_Request",methods=['POST'])
def raisefooditem():
    return Raise_Foodandbeverage_Request(request)
@app.route("/Close_Foodandbeverage_Request",methods=['POST'])
def closefooditem():
    return Close_Foodandbeverage_Request(request)
@app.route("/Query_Foodandbeverage_Request",methods=['POST'])
def selectfooditem():
    return Query_Foodandbeverage_Request(request)


#----------GuestDetails-----------------------

@app.route("/Add_Guest_Details",methods=['POST'])
def addguest():
   return Add_Guest_Details(request)
@app.route("/Edit_Guest_Details",methods=['POST'])
def editguest():
   return Edit_Guest_Details(request)
@app.route("/Checkout_Guest",methods=['POST'])
def checkoutguest():
   return Checkout_Guest(request)

@app.route("/Query_Guest_Details",methods=['POST'])
def QueryGuestDetails():
    return Query_Guest_Details(request)

#----------HouseKeeping Reqeust-----------------
@app.route("/Raise_HK_Request",methods=['POST'])
def RaiseHKRequest():
   return Raise_HK_Request(request)

@app.route("/Close_HK_Request",methods=['POST'])
def CloseHKRequest():
   return Close_HK_Request(request)

@app.route("/Query_Hk_Request",methods=['POST'])
def QueryHkRequest():
   return Query_Hk_Request(request)

@app.errorhandler(404)
def unhandled_exception(e):
   return(json.dumps({"Return":"page Not Found","Returncode":"404"}))
@app.errorhandler(405)
def unhandled_exception(e):
 return(json.dumps({"Return":"Method Not Allowed","Returncode":"405"}))
	
if __name__ == "__main__":
    #TOS.run(debug=True)
    app.run(host ='192.168.99.1',port =5000)#run web application
