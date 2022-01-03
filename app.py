#!flask/bin/python
from flask import Flask
from datetime import datetime, timedelta
from dotenv import load_dotenv
import caldav, re, os


app = Flask(__name__)


def get_caldat(calender_name):
    dt_start = datetime.today()
    dt_start = dt_start.replace(hour=0, minute=0, second=0, microsecond=0)
    dt_end = dt_start + timedelta(days=look_ahead_days)

    print (dt_start)

    # Select the "right one"
    my_calendar = my_principal.calendar(name=calender_name)
    
    return my_calendar.date_search(
    start=dt_start,
    end=dt_end, expand=True)


def get_caldat_today(calender_name):
    dt_start = datetime.today()
    dt_start = dt_start.replace(hour=0, minute=0, second=0, microsecond=0)
    dt_end = dt_start # only today

    print (dt_start)

    # Select the "right one"
    my_calendar = my_principal.calendar(name=calender_name)
    
    return my_calendar.date_search(
    start=dt_start,
    end=dt_end, expand=True)

def is_match(search_string, string):
    
    search_string = search_string.replace('_',' ')

    if re.search(search_string,string, re.IGNORECASE) != None:
        return True
    return False
    

@app.route('/flaav/api/v1.0/<string:calender_name>/events', methods=['GET'])
def get_events(calender_name):
    rt = ''
    for event in get_caldat(calender_name):
        rt += event.data
    return rt


@app.route('/flaav/api/v1.0/<string:calender_name>/events/any/<string:summary>', methods=['GET'])
def get_event(calender_name, summary):
    rt = ''
    for event in get_caldat(calender_name):
        if is_match(summary,event.vobject_instance.vevent.summary.value):
            if rt != '':
                rt +=  '\r\n'
            rt += event.data
    if rt == '':
        return '404 Not Found'
    return rt


@app.route('/flaav/api/v1.0/<string:calender_name>/events/any/<string:summary>/<string:component>', methods=['GET'])
def get_component(calender_name, summary, component):
    rt = ''
    for event in get_caldat(calender_name):
        if is_match(summary,event.vobject_instance.vevent.summary.value):
            if rt != '':
                rt += '\r\n'
            rt += event.icalendar_instance.subcomponents[0][component].to_ical().decode('UTF-8')
    if rt == '':
        return '404 Not Found'
    return rt

@app.route('/flaav/api/v1.0/<string:calender_name>/events/next/<string:summary>/<string:component>', methods=['GET'])
def get_component_from_next_event(calender_name, summary, component):
    rt = ''
    dt_min = datetime.today().date() + timedelta(days=look_ahead_days)
    for event in get_caldat(calender_name):
        if is_match(summary,event.vobject_instance.vevent.summary.value):
            if event.icalendar_instance.subcomponents[0]['dtstart'].dt <= dt_min:
                dt_min = event.vobject_instance.vevent.dtstart
                rt = event.icalendar_instance.subcomponents[0][component].to_ical().decode('UTF-8')
    if rt == '':
        return '404 Not Found'
    return rt


@app.route('/flaav/api/v1.0/<string:calender_name>/events/any/<string:summary>/is_today', methods=['GET'])
def get_event_is_today(calender_name, summary):
    rt = '0'
    for event in get_caldat_today(calender_name):
        if is_match(summary,event.vobject_instance.vevent.summary.value):
            rt= '1'
    return rt

if __name__ == '__main__':
    load_dotenv()

    caldav_url = os.environ.get('caldav_url')
    caldav_username = os.environ.get('caldav_username')
    caldav_passwd = os.environ.get('caldav_passwd')
    udp_target_ip = os.environ.get('udp_target_ip')
    udp_port = int(os.environ.get('udp_port'))
    api_port = os.environ.get('port')
    look_ahead_days = int(os.environ.get('look_ahead_days'))


    # create caldav client
    client = caldav.DAVClient(url=caldav_url, username=caldav_username, password=caldav_passwd)
    my_principal = client.principal()
    # get all Calenders
    calendars = my_principal.calendars()

    app.run(debug=True,  host='0.0.0.0')