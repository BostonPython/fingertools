import sys

import requests
import lxml.html

event_id = sys.argv[1]
url = f"https://www.meetup.com/mu_api/urlname/events/eventId/attendees?queries=(endpoint:bostonpython/events/{event_id}/attendance,meta:(method:get),params:(desc:!t,fields:'self,web_actions,answers,pay_status',order:time),ref:eventAttendance_bostonpython_{event_id},type:attendance)"
resp = requests.get(url).json()
attendees = resp["responses"][0]["value"]
print(f"{len(attendees)} attendees")
names = [att["member"]["name"] for att in attendees]
print(names)
