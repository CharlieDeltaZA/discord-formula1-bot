#!/usr/bin/python3
import datetime
import os
from DiscordWebhook import DiscordWebhook
from F1Calendar import F1Calendar
from discord_webhook import DiscordWebhook, DiscordEmbed

DO_REQUEST = True
root_dir = os.path.dirname(os.path.realpath(__file__))
# Source the 2019 calendar from here when avail -- https://www.f1calendar.com/
# Else, find a way to get one from formula1.com / FOM / FIA
CALENDAR_FILE = root_dir + "/formula.1.2020.ics"
WEBHOOK_URL = open(root_dir + '/webhook_url.conf', 'r').readlines()[0].strip()

webhook = DiscordWebhook(WEBHOOK_URL)
cal = F1Calendar(CALENDAR_FILE)
dow = datetime.datetime.today().weekday()
output_str = None

# Monday
if dow == 0:
    # Custom discord emotes in use here...
    prefix_str = u"<:f1:511528935180468225> Happy Monday! Here is the schedule for the next race weekend: \n\n"
    suffix_str = u"<:ferrari:455426708674445312>"
    # events = cal.get_next_race_events()
    events = cal.getNextRaceEvents()
    # print(events)
    # output_str = prefix_str + "\n".join(events) + "\n" + suffix_str
    
# """
# Suppose this isn't entirely needed. It can fail silently without pushing a message to DC.
# Tues, Wed, Or None avail
# USE ME TO DEBUG IF TRYING TO RUN ON A TUES OR WED!
# elif dow in (1, 2):
#    events = "None found"
#    output_str = "No Events Found!"
# """

# Thurs, Fri, Sat, Sun
elif dow in (3, 4, 5, 6):
    # Custom discord emotes in use here...
    prefix_str = u"<:f1:511528935180468225> Race Weekend! In the next 24 hours: \n"
    suffix_str = u"<:ferrari:455426708674445312>"
    events = cal.get_events_next_24h()
    output_str = prefix_str + "\n".join(events) + "\n" + suffix_str


if events:
    # print("Sending: " + output_str)  # .encode('utf-8'))
    for e in events:
        webhook.add_embed(e)
    # webhook = DiscordWebhook(url=WEBHOOK_URL, content=output_str)

    if DO_REQUEST:
        response = webhook.execute()
        # print(WEBHOOK_URL)
        print(response)
        # webhook.send_message(output_str)
