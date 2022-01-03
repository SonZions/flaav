#!flask/bin/python
from flask import Flask
from datetime import datetime, timedelta
from dotenv import load_dotenv
import caldav, re, os

app = Flask(__name__)


def get_caldat(calender_name):
    # get a specific calendar and male a date search
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
    # regex to detect a matching entrance
    if re.search(search_string,string, re.IGNORECASE) != None:
        return True
    return False
    
@app.route('/flaav/api/v0.1', methods=['GET'])
def get_calenders():
    # List all Calendernames that are available
    rt = ''
    for c in my_principal.calendars():
        rt += c.name + '\r\n'
    if rt == '':
        return '404 Not Found'
    return rt

@app.route('/flaav/api/v0.1/<string:calender_name>/events', methods=['GET'])
def get_events(calender_name):
    # list all events from choosen calendar
    rt = ''
    for event in get_caldat(calender_name):
        rt += event.data
    return rt


@app.route('/flaav/api/v0.1/<string:calender_name>/events/any/<string:summary>', methods=['GET'])
def get_event(calender_name, summary):
    # list every occourance of the event with the given name/summary
    rt = ''
    for event in get_caldat(calender_name):
        if is_match(summary,event.vobject_instance.vevent.summary.value):
            if rt != '':
                rt +=  '\r\n'
            rt += event.data
    if rt == '':
        return '404 Not Found'
    return rt


@app.route('/flaav/api/v0.1/<string:calender_name>/events/today/<string:summary>', methods=['GET'])
def get_event_from_today(calender_name, summary):
    # list every occourance of the event with the given name/summary
    rt = ''
    for event in get_caldat_today(calender_name):
        if is_match(summary,event.vobject_instance.vevent.summary.value):
            if rt != '':
                rt +=  '\r\n'
            rt += event.data
    if rt == '':
        return '404 Not Found'
    return rt

@app.route('/flaav/api/v0.1/<string:calender_name>/events/next/<string:summary>', methods=['GET'])
def get_next_event(calender_name, summary):
    # get component-value from given comonent of the next upcomming event with given name/summary
    rt = ''
    dt_min = datetime.today().date() + timedelta(days=look_ahead_days)
    for event in get_caldat(calender_name):
        if is_match(summary,event.vobject_instance.vevent.summary.value):
            try:
                if event.icalendar_instance.subcomponents[0]['dtstart'].dt <= dt_min:
                    dt_min = event.vobject_instance.vevent.dtstart
                    rt = event.data
            except:
                pass
    if rt == '':
        return '404 Not Found'
    return rt


@app.route('/flaav/api/v0.1/<string:calender_name>/events/any/<string:summary>/<string:component>', methods=['GET'])
def get_component(calender_name, summary, component):
    # List component value from given component of every occurance of given event
    rt = ''
    for event in get_caldat(calender_name):
        if is_match(summary,event.vobject_instance.vevent.summary.value):
            if rt != '':
                rt += '\r\n'
            rt += event.icalendar_instance.subcomponents[0][component].to_ical().decode('UTF-8')
    if rt == '':
        return '404 Not Found'
    return rt

@app.route('/flaav/api/v0.1/<string:calender_name>/events/next/<string:summary>/<string:component>', methods=['GET'])
def get_component_from_next_event(calender_name, summary, component):
    # get component-value from given comonent of the next upcomming event with given name/summary
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

@app.route('/flaav/api/v0.1/<string:calender_name>/events/today/<string:summary>/<string:component>', methods=['GET'])
def get_component_from_today(calender_name, summary, component):
    # List component value from given component of todays occurance of given event
    rt = ''
    for event in get_caldat_today(calender_name):
        if is_match(summary,event.vobject_instance.vevent.summary.value):
            if rt != '':
                rt += '\r\n'
            rt += event.icalendar_instance.subcomponents[0][component].to_ical().decode('UTF-8')
    if rt == '':
        return '404 Not Found'
    return rt


@app.route('/flaav/api/v0.1/<string:calender_name>/events/any/<string:summary>/is_today', methods=['GET'])
def get_event_is_today(calender_name, summary):
    # return 0 or 1 depending if the event with given name appears today
    rt = '0'
    for event in get_caldat_today(calender_name):
        if is_match(summary,event.vobject_instance.vevent.summary.value):
            rt= '1'
    return rt

if __name__ == '__main__':
    # for local testing load .env-file
    load_dotenv()

    # get env variables
    caldav_url = os.environ.get('caldav_url')
    caldav_username = os.environ.get('caldav_username')
    caldav_passwd = os.environ.get('caldav_passwd')
    look_ahead_days = int(os.environ.get('look_ahead_days'))

    # create caldav client
    client = caldav.DAVClient(url=caldav_url, username=caldav_username, password=caldav_passwd)
    my_principal = client.principal()

    app.run(debug=True,  host='0.0.0.0')