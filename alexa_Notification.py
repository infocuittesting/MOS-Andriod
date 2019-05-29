import requests
import datetime
from datetime import timedelta
from Fetch_Iso_Current_Datetime import *
import json


def Alexa_Notification(request):
   d = request.json
   current_datetime=application_datetime()
   print(current_datetime[0])
   print(current_datetime[1])
   print(d['user_Id'],type(d['user_Id']))
   url='https://api.amazon.com/auth/O2/token'
   headers = {
   'Content-Type': 'application/x-www-form-urlencoded',
   }
   payload={'grant_type':'client_credentials','client_id':'amzn1.application-oa2-client.55fd9f1470dd422b91e5f451c4029457',
       'client_secret':'1f5688a0b474c57e6b7335e4913d200b3410dc0116e1338cbf225d361eca762e','scope':'alexa::proactive_events'
   }
   s = requests.post(url, headers=headers, data=payload)
   token_res = s.json()
   print(token_res['access_token'])
   request_header={'Authorization': 'Bearer {}'.format(token_res['access_token']),"Content-Type":"application/json"}
    
   api_url='https://api.amazonalexa.com/v1/proactiveEvents/stages/development'





   notify_json = {


       "timestamp": str(current_datetime[0]),
       "referenceId": "orangetango2221800f44-436a-4c47-8d9f-e14356bb010c",


       "expiryTime": str(current_datetime[0]),
       "event": {

           "name": "AMAZON.MessageAlert.Activated",

           "payload": {

               "state": {

                   "status": "UNREAD",

                   "freshness": "NEW"

               },

               "messageGroup": {

                   "creator": {

                       "name": str(d['Object'])+"request has been closed"

                   },

                   "count": 1,

                   "urgency": "URGENT"

               }

           }

       },

       "relevantAudience": {

           "type": "Unicast",

           "payload": {

               "user":"amzn1.ask.account.AGED2IIT4HCFBGQYEBXCDHVKQIXUARZN245R5J6OBQT7MLVNHORSPXTOVLJAQWRVSWG2RLPJ6MHYEUFD3DQ4JUYMJB44GGPVRSMJDTUD24S7ULYDCC7AILSNHSAN6QF42YG3SZ2OANYLKLXMPUFKBKK6AYPB6WEY3YKW3VHDJ5TB7FZA73FQ3PCCIBMSRP3UEA2JB4DVOR37QIA"

           }

       }

   }
   notifcation_send = requests.post(api_url,headers=request_header,json =notify_json )
   print("notification_send:",notifcation_send.json())
   return json.dumps({"Return": "Run Successfully"})
