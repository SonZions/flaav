#!/usr/bin/env python
# coding: utf-8

# In[1]:


from datetime import datetime, date, timedelta
from dotenv import load_dotenv
import time, caldav, socket, re, os


# In[2]:
# load .env to os.env if local
load_dotenv()

caldav_url = os.environ.get('caldav_url')
caldav_username = os.environ.get('caldav_username')
caldav_passwd = os.environ.get('caldav_passwd')
udp_target_ip = os.environ.get('udp_target_ip')
udp_port = int(os.environ.get('udp_port'))
calender_name = os.environ.get('calender_name')
summary_search_string = os.environ.get('summary_search_string')



# In[3]:

# create caldav client
client = caldav.DAVClient(url=caldav_url, username=caldav_username, password=caldav_passwd)
my_principal = client.principal()
# get all Calenders
calendars = my_principal.calendars()
# Select the "right one"
my_calendar = my_principal.calendar(name=calender_name)


# In[ ]:

#Create UDP Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# In[ ]:

while 1==1:

    dt = datetime.today()
    dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    print (dt)
    
    udp_message = 'Urlaub=0'
    
    events_fetched = my_calendar.date_search(
    start=datetime(2021, 12, 26),
    end=datetime(2021, 12, 26), expand=True)
   
    for x in range(len(events_fetched)):
        summary_value = events_fetched[x].vobject_instance.vevent.summary.value
        print (summary_value)
        if re.search(summary_search_string,summary_value) != None:
            print ("Match")
            udp_message = 'Urlaub='+'1'

    # Send UDP Message to Miniserver
    sock.sendto(bytes(udp_message, "utf-8"), (udp_target_ip, udp_port))
    
    # sleep until 2AM
    t = datetime.today()
    future = datetime(t.year,t.month,t.day,2,0)
    if t.hour >= 2:
        future += timedelta(days=1)
    time.sleep((future-t).total_seconds())


# %%
