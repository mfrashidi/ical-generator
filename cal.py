from icalendar import Calendar, Event
import pytz,jdatetime,calendar,os
from datetime import datetime
from PyInquirer import prompt, print_json
from termcolor import colored
from examples import custom_style_2
from pprint import pprint


def convert(date):
    a = jdatetime.datetime(date.year,date.month,date.day,date.hour,date.minute)
    return datetime.utcfromtimestamp(calendar.timegm(a.utctimetuple()))

print(colored('iCal Generator','cyan') + colored('\n@mfrashidi','green'))
classes = []
dateV = lambda x: True if x.count('/')==2 and len(x.split('/')[0])==4 else 'Invalid Format'
timeV = lambda x: True if x.count(':')==2 and x.count('-')==1 else 'Invalid Format'
day = {'saturday':'SA','sunday':'SU','monday':'MO','tuesday':'TU','thursday':'TH','wednesday':'WE','friday':'FR'}

questions = [
    {
        'type': 'input',
        'name': 'class_name',
        'message': 'What is your class name?',
    },
    {
        'type': 'input',
        'name': 'first_class',
        'default':'1400/7/1',
        'message': 'When is your first class? (Ex. 1400/7/1)',
        'validate': dateV
    },
    {
        'type': 'input',
        'name': 'last_class',
        'message': 'When does the class end? (Ex. 1400/11/1)',
        'validate': dateV
    },
    {
        'type': 'input',
        'name': 'time',
        'message': 'What time of day do you have the class? (Ex. 10:00-12:00)',
        'validate': timeV
    },
    {
        'type': 'expand',
        'message': 'Which day do you have the class? (Press H to see your options)',
        'name': 'day',
        'choices': [
            {
                'key': 'a',
                'name': 'Saturday',
                'value': 'saturday'
            },
            {
                'key': 'b',
                'name': 'Sunday',
                'value': 'sunday'
            },
            {
                'key': 'c',
                'name': 'Monday',
                'value': 'monday'
            },
            {
                'key': 'd',
                'name': 'Tuesday',
                'value': 'tuesday'
            },
            {
                'key': 'e',
                'name': 'Wednesday',
                'value': 'wednesday'
            },
            {
                'key': 'f',
                'name': 'Thursday',
                'value': 'thursday'
            },
            {
                'key': 'g',
                'name': 'Friday',
                'value': 'friday'
            }
        ]
    }
]

answers = prompt(questions, style=custom_style_2)



formatTime = lambda x:convert(datetime(int(x.split('/')[0]), int(x.split('/')[1]), int(x.split('/')[2].split(' ')[0]), int(x.split(' ')[1].split(':')[0]), int(x.split(' ')[1].split(':')[1]), tzinfo=pytz.utc))
cal = Calendar()
event = Event()
event.add('summary', answers['class_name'])
event.add('dtstart', formatTime('%s %s'%(answers['first_class'],answers['time'].split('-')[0])))
event.add('dtend', formatTime('%s %s'%(answers['first_class'],answers['time'].split('-')[1])))
event.add('rrule', {'freq': 'weekly','byday':day[answers['day'].lower()],'until':formatTime('%s %s'%(answers['last_class'],'00:00'))})
cal.add_component(event)
desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop') + '/'
filename = desktop+answers['class_name']+'.ics'
if os.path.exists(filename):
    n = 1
    while 1:
        filename = desktop+answers['class_name']+' '+str(n)+'.ics'
        if not os.path.exists():
            f = open(filename,'wb')
            f.write(cal.to_ical())
            f.close()
            break
        n+=1
else:
    f = open(filename,'wb')
    f.write(cal.to_ical())
    f.close()
print(colored("File saved at ",'green') + colored(filename,'red'))
