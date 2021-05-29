from hyper import HTTP20Connection
import winrt.windows.ui.notifications as notifications
import winrt.windows.data.xml.dom as dom
import sys
import json
import time
import os


def send_notif(date,msg):
   app = '{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\\WindowsPowerShell\\v1.0\\powershell.exe'

   #create notifier
   nManager = notifications.ToastNotificationManager
   notifier = nManager.create_toast_notifier(app)
   
   #define your notification as string
   tString = """
     <toast>
       <visual>
         <binding template='ToastGeneric'>
           <text>Vaccine slot is open for """+date+"""</text>
           <text>"""+msg+"""</text>
         </binding>
       </visual>
       <actions>
         <action
           content="Dismiss"
           arguments="action=dismiss"/>
       </actions>        
     </toast>
   """

   #convert notification to an XmlDocument 
   xDoc = dom.XmlDocument()
   xDoc.load_xml(tString)
   notifier.show(notifications.ToastNotification(xDoc))

def check_vaccine_slot(date,pincode,frequency,min18,min45,pref_slot,pref_vax):
   conn = HTTP20Connection("cdn-api.co-vin.in",proxy_host="",proxy_port="",secure=True)
#   url="/api/v2/appointment/sessions/public/findByPin?pincode="+pincode+"&date="+date
   url="/api/v2/appointment/sessions/public/findByDistrict?district_id="+pincode+"&date="+date
   os.environ['NO_PROXY']="cdn-api.co-vin.in"
   os.environ['no_proxy']="cdn-api.co-vin.in"
   conn.request("GET",url)
   response = conn.get_response().read()
   msg=""
   response = json.loads(response.decode('utf-8'))
   for i in response['sessions']:
       if i['min_age_limit'] == 18:
         if int(pref_slot) == 1 or int(pref_slot) == 0:
          if (int(min18) != -1 and i['available_capacity_dose1'] >=int(min18) and (i['vaccine'].lower() == pref_vax.lower() or pref_vax.lower() == "both")):
             msg+=str(i['available_capacity_dose1'])+" 1st Dose(s) of "+i['vaccine']+" is available at "+i['name']+","+i['address']+" for people above age of "+str(i['min_age_limit'])+" for Rs. "+str(i['fee'])+"\n"
         if int(pref_slot) == 2 or int(pref_slot) == 0:
          if (int(min18) != -1 and i['available_capacity_dose2'] >=int(min18) and (i['vaccine'].lower() == pref_vax.lower() or pref_vax.lower() == "both")):
             msg+=str(i['available_capacity_dose2'])+" 2nd Dose(s) of "+i['vaccine']+" is available at "+i['name']+","+i['address']+" for people above age of "+str(i['min_age_limit'])+" for Rs. "+str(i['fee'])+"\n"
       elif i['min_age_limit'] == 45:
         if int(pref_slot) == 1 or int(pref_slot) == 0:
          if (int(min45) != -1 and i['available_capacity_dose1'] >=int(min45) and (i['vaccine'].lower() == pref_vax.lower() or pref_vax.lower() == "both")):
             msg+=str(i['available_capacity_dose1'])+" 1st Dose(s) of "+i['vaccine']+" is available at "+i['name']+","+i['address']+" for people above age of "+str(i['min_age_limit'])+" for Rs. "+str(i['fee'])+"\n"
         if int(pref_slot) == 2 or int(pref_slot) == 0:
          if (int(min45) != -1 and i['available_capacity_dose2'] >=int(min45) and (i['vaccine'].lower() == pref_vax.lower() or pref_vax.lower() == "both")):
             msg+=str(i['available_capacity_dose2'])+" 2nd Dose(s) of "+i['vaccine']+" is available at "+i['name']+","+i['address']+" for people above age of "+str(i['min_age_limit'])+" for Rs. "+str(i['fee'])+"\n"
   if msg != "":
      print(msg)
      send_notif(date,msg)
   else:
      print("No Slot Found. Retrying in "+str(int(60/int(frequency)))+"seconds")
      time.sleep(int(60/int(frequency)))
      check_vaccine_slot(date,pincode,frequency,min18,min45,pref_slot,pref_vax)

date=sys.argv[1]
pincode = sys.argv[2]
frequency= sys.argv[3]
min18 = sys.argv[4]
min45 = sys.argv[5]
pref_slot = sys.argv[6]
pref_vax = sys.argv[7]
if int(pref_slot) != 0 and int(pref_slot) != 1 and int(pref_slot) != 2:
   print("Incorrect slot chosen. Choose 1 or 2, 0 if both slots need to be checked")
   raise Exception

if pref_vax.lower() != "covishield" and pref_vax.lower() != "covaxin" and pref_vax.lower() != "both":
   print("Incorrect preferred vaccine chosen. Choose Covishield or Covaxin, or Both if no preferrence is required")
   raise Exception

check_vaccine_slot(date,pincode,frequency,min18,min45,pref_slot,pref_vax)
